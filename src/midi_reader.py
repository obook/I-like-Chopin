#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage

@Todo : si pas de note, se caler à la prochaine,
ici on a un soucis avec le release du sustain, et avec les notes off/note on avec vélocité nulle.

"""
import time
import uuid
import os
from mido import (MidiFile, Message)

from PySide6.QtCore import (QThread, Signal)

from midi_song import ClassMidiSong, states, modes
from midi_numbers import number_to_note
# from midi_controller import

class ClassThreadMidiReader(QThread):
    """Read midifile and send to output device"""

    uuid = None
    pParent = None
    midi = None
    midisong = None
    keys = None
    port_out = None
    Settings = None
    ready = False
    running = False

    total_notes_on = 0
    notes_on_channels = 0
    current_notes_on = 0
    channels = None
    channels_notes = {}
    total_sustain = 0
    wait_time = 0

    sustain_pedal = 0
    sustain_pedal_off = False

    statusbar_activity = Signal(str)
    led_file_activity = Signal(int)
    star_file_activity = Signal(int)

    SignalStop_activity = Signal()

    SignalLightPlay_activity = Signal()
    SignalLightStop_activity = Signal()

    def __init__(self, midifile, keys, channels, pParent):
        QThread.__init__(self)
        self.uuid = uuid.uuid4()
        if not midifile:
            print(f"MidiReader {self.uuid} midifile=None")
            return
        self.pParent = pParent
        self.midi = self.pParent.Midi
        self.Settings = self.pParent.Settings
        self.keys = keys
        self.channels = channels

        self.statusbar_activity.connect(self.pParent.SetStatusBar)
        self.led_file_activity.connect(self.pParent.SetLedFile)
        self.star_file_activity.connect(self.pParent.SetStarFile)

        self.SignalLightPlay_activity.connect(self.pParent.midi_controller.SignalLightPlay)
        self.SignalLightStop_activity.connect(self.pParent.midi_controller.SignalLightStop)

        print(f"MidiReader {self.uuid} created [{os.path.basename(midifile)}]")
        self.midisong = ClassMidiSong(midifile)

    def __del__(self):
        print(f"MidiReader {self.uuid} destroyed [{self.midisong.GetFilename()}]")

    def LoadMidiSong(self, mode):

        if not self.midisong:
            return

        self.midisong.SetMode(mode)

        tracks = []  # PUT IN MIDI_SONG

        try:

            # Informations
            midi = MidiFile(self.midisong.Getfilepath())  # PUT IN MIDI_SONG
            self.midisong.SetDuration(midi.length / 60)
            for i, track in enumerate(midi.tracks):
                tracks.append(track.name)

            self.midisong.SetTracks(tracks)

            self.total_notes_on = 0
            self.channels_notes = {}
            self.star_file_activity.emit(0)

            # counter : notes in channel
            for msg in MidiFile(self.midisong.Getfilepath()):  # PUT IN MIDI_SONG
                if msg.type == "note_on":  # with velocity or not
                    self.total_notes_on += 1
                    if self.channels[msg.channel]:
                        self.notes_on_channels += 1
                    key = str(msg.channel)
                    if not key in self.channels_notes.keys():
                        self.channels_notes[key] = 0
                    self.channels_notes[key] += 1

                # Quality : Sustain pedal detected
                if msg.type == "control_change":
                    if msg.control == self.Settings.GetSustainChannel():
                        self.total_sustain += 1

            if self.total_sustain:  # Quality icon
                self.star_file_activity.emit(2)
            else:
                self.star_file_activity.emit(-1)

            self.midisong.SetChannels(self.channels_notes)
            self.midisong.SetSustain(self.total_sustain)
            # self.pParent.ChannelsSetButtons()

            if self.notes_on_channels:
                self.midisong.SetState(states["cueing"])
                # self.led_file_activity.emit(0)
            else:
                print(f"|!| MidiReader {self.uuid} NO NOTE ON MIDI CHANNELS")
                self.midisong.SetState(states["notracktoplay"])
        except Exception as error:
            self.midisong.SetState(states["bad"])
            print(
                f"|!| MidiReader {self.uuid} ERROR [{self.midisong.GetFilename()}] {error}"
            )

        return self.midisong

    def SetMidiPort(self, port_out):
        self.port_out = port_out

    def run(self):

        self.led_file_activity.emit(0)  # OBOOK

        if not self.midisong:
            return

        if not self.midisong.IsState(states["cueing"]):
            return

        if self.midisong.IsMode(modes["player"]):
            time.sleep(3)  # more elegant

        elif self.midisong.IsMode(modes["passthrough"]):  # Here ?
            return

        self.running = True

        self.led_file_activity.emit(1)  # NEW

        # Before play, reset...
        self.pParent.Midi.ResetOutput()

        for msg in MidiFile(self.midisong.Getfilepath()):

            if self.Settings.GetDebugMsg():
                print(f"----> DEBUG MidiReader {self.uuid} msg =", msg)

            # Is passthrough mode ?
            while self.midisong.IsMode(modes["passthrough"]):
                if not self.running:
                    return
                self.sleep(1)

            # Stop while running ?
            if not self.running:
                return

            if self.midisong.GetState() < states["cueing"]:  # not used
                return

            # Sustain pedal memory
            if msg.type == "control_change":
                if msg.control == self.Settings.GetSustainChannel():
                    self.sustain_pedal = msg.value

            # For fun : not used
            '''
            if self.midisong.IsState(states["playing"]):
                if msg.type == "note_on":
                    if msg.velocity:
                        self.led_file_activity.emit(1)
                    else:
                        self.led_file_activity.emit(0)
                elif msg.type == "note_off":
                    self.led_file_activity.emit(0)
            '''
            # Just a Midi player ############################################################
            if self.midisong.IsMode(modes["player"]) or self.Settings.IsMode(modes["random"]):

                # Delay : Humanize controlled by knob, see midi_input
                human = 0
                if msg.type == "note_on" and self.keys["humanize"]:
                    human = self.midisong.HumanizeDuration(
                        msg.time, self.keys["humanize"]
                    )

                if self.midisong.IsState(states["cueing"]):
                    msg.time = 0

                # Time for the note
                time.sleep(msg.time + human + self.keys["speed"] / 2000)

                # Program change : force Prog 0 on all channels (Acoustic Grand Piano) except for drums
                if msg.type == "program_change" and self.Settings.GetForceIntrument():
                    if msg.channel != 9:  # not for drums
                        msg.program = self.Settings.GetPianoProgram()

                #  Send or not ?
                if msg.type == "note_on":

                    self.midisong.SetPlayed(int(100 * self.current_notes_on / self.total_notes_on))
                    self.current_notes_on += 1

                    if not self.midisong.IsState(states["playing"]): # First note on channels selected
                        print(f"MidiReader {self.uuid} player [{self.midisong.GetFilename()}] READY") # Utile ?
                        self.statusbar_activity.emit("READY")
                        self.midisong.SetState(states["playing"])
                        self.led_file_activity.emit(1)

                    if self.channels[msg.channel]:
                        self.pParent.Midi.SendOutput(msg)

                        if msg.velocity:
                            note, octave = number_to_note(msg.note)
                            text = f"[{msg.note}]\t\t{note} {octave-1}"
                            self.statusbar_activity.emit(text)

                else:
                    self.pParent.Midi.SendOutput(msg)

            # Playback : wait keyboard ############################################################
            elif self.midisong.IsMode(modes["playback"]):

                # restore sustain pedal value (after pause)
                if self.sustain_pedal_off and self.sustain_pedal:
                    msg = Message(
                        "control_change",
                        control=self.Settings.GetSustainChannel(),
                        value=self.sustain_pedal,
                    )
                    self.pParent.Midi.SendOutput(msg)
                    self.sustain_pedal_off = False

                # Wait note time
                if (
                    self.midisong.IsState(states["playing"])
                    and msg.time > self.wait_time
                ):

                    # self.led_file_activity.emit(0)  # NEW

                    # Delay : Humanize controlled by knob, see midi_input
                    human = 0
                    if msg.type == "note_on" and self.keys["humanize"]:
                        human = self.midisong.HumanizeDuration(
                            msg.time, self.keys["humanize"]
                        )

                    # Time for the note
                    time.sleep(msg.time + human + self.keys["speed"] / 2000)

                if msg.type == "note_on":  # with velocity or not
                    # First note on channels selected : cued and waiting keyboard pressed
                    if ( self.channels[msg.channel]
                        and not self.midisong.IsState(states["playing"])
                        and msg.velocity ):  # removed : and msg.time

                        print(
                            f"MidiReader {self.uuid} playback [{self.midisong.GetFilename()}] READY"
                        )
                        self.SignalLightPlay_activity.emit()
                        self.statusbar_activity.emit("READY")
                        self.midisong.SetState(states["playing"])

                    # Stats
                    self.midisong.SetPlayed(
                        int(100 * self.current_notes_on / self.total_notes_on)
                    )
                    self.current_notes_on += 1

                if self.midisong.IsState(states["cueing"]):
                    msg.time = 0 # skip time until note on channel
                ''' Show the next note... not used
                if msg.type == "note_on" and self.channels[msg.channel]:
                    if msg.velocity:
                        note, octave = number_to_note(msg.note)
                        text = f"[{msg.note}]\t\t{note} {octave-1}"
                        self.statusbar_activity.emit(text)
                '''
                # Pause ?
                if msg.type == "note_on" and self.midisong.IsState(states["playing"]):
                    start_time = time.time()
                    start_time_loop = time.time()
                    self.pedal_off = False
                    activity = False
                    while not self.keys["key_on"]:  # Loop waiting keyboard

                        # Finished ?
                        if not self.running or not self.midisong or not self.midisong.IsState(states["playing"]):
                            self.stop()
                            return
                        ''' Trop de problemes ?? ....                        '''
                        # no velocity (note off) 2025
                        # Il faudrait le faire au début du morceaux, pas dans la boucle d'attente
                        # Le problème se pose si en début de morceaux deux notes doivent être jouer en même temps ?
                        if msg.type == "note_on" or msg.type == "note_off":
                            if not msg.velocity:
                                 # or not msg.time => DANGER:
                                if self.Settings.GetDebugMsg():
                                    print("--> DEBUG NOTE OFF PLAYED")
                                break

                        # note present but must not be played; skip the pause
                        if not self.channels[msg.channel]:
                            break

                        # Note ready to play
                        elif msg.type == "note_on" and not activity :
                            activity = True
                            self.led_file_activity.emit(1)

                        # Wait long time : release systain pedal if active
                        if (
                            self.sustain_pedal
                            and time.time() - start_time_loop > 1.5
                            and not self.sustain_pedal_off
                        ):
                            msg = Message(
                                "control_change",
                                control=self.Settings.GetSustainChannel(),
                                value=0,
                            )
                            self.pParent.Midi.SendOutput(msg)
                            self.sustain_pedal_off = True

                        time.sleep(0.01)  # NOT SELF !!

                    # Wait a key how much time ?
                    self.wait_time = time.time() - start_time

                # Program change : force Prog 0 on all channels (Acoustic Grand Piano) except for drums
                if msg.type == "program_change" and self.Settings.GetForceIntrument():
                    if msg.channel != 9:  # not for drums
                        msg.program = self.Settings.GetPianoProgram()

                # Play
                if msg.type == "note_on":
                    if self.channels[msg.channel]:
                        self.pParent.Midi.SendOutput(msg)
                        if msg.velocity:
                            note, octave = number_to_note(msg.note)
                            text = f"[{msg.note}]\t\t{note} {octave-1}"
                            self.statusbar_activity.emit(text)
                else:
                    self.pParent.Midi.SendOutput(msg)
                """
                filter =[
                'program_change',
                'sysex',
                'text',
                'track_name',
                'set_tempo',
                'time_signature',
                'key_signature',
                'midi_port',
                'sequencer_specific',
                'copyright',
                'cue_marker',
                'marker',
                'smpte_offset',
                'lyrics',
                'end_of_track',
                'instrument_name'
                ]

                if not msg.type in filter:
                   print(f"|!| MidiReader : can not send type=[{msg.type}] msg=[{msg}] to [{self.port_out}]")
                """

                # Loop until passthrough mode active
                while self.midisong.IsMode(modes["passthrough"]):
                    self.sleep(0.5)

        # End of song
        # NO do not kill midisong
        # self.stop()
        self.midisong.SetState(states["ended"])
        self.midisong.SetPlayed(100)
        self.SignalLightStop_activity.emit()

    def stop(self):

        if self.running:
            if self.midisong:
                print(f"MidiReader {self.uuid} stop [{self.midisong.GetFilename()}] !")
                self.midisong.SetState(states["ended"])
                self.midisong.SetPlayed(100)
            else:
                print("MidiReader {self.uuid} stop")
            self.running = False
