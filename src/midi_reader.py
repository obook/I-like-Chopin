#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import time
import random
import uuid
from threading import Thread

from mido import MidiFile
from midi_song import ClassMidiSong, states, modes
from midi_numbers import number_to_note


class ClassThreadMidiReader(Thread):
    """Read midifile and send to output device"""

    uuid = uuid.uuid4()
    parent = None
    midisong = None
    keys = None
    port_out = None
    settings = None
    ready = False
    total_notes_on = 0
    notes_on_channels = 0
    current_notes_on = 0
    channels = None
    channels_notes = {}
    wait_time = 0

    def __init__(self, midifile, keys, channels, pParent):
        Thread.__init__(self)
        self.parent = pParent
        self.settings = self.parent.settings
        self.midisong = ClassMidiSong(midifile)
        self.midisong.SetState(states["unknown"])
        self.keys = keys
        self.channels = channels
        print(f"MidiReader {self.uuid} created [{self.midisong.Getfilepath()}]")

    def __del__(self):
        print(f"MidiReader {self.uuid} destroyed [{self.midisong.Getfilepath()}]")

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

            for msg in MidiFile(self.midisong.Getfilepath()):  # PUT IN MIDI_SONG
                if msg.type == "note_on":
                    self.total_notes_on += 1
                    if self.channels[msg.channel]:
                        self.notes_on_channels += 1
                    key = str(msg.channel)
                    if not key in self.channels_notes.keys():
                        self.channels_notes[key] = 0
                    self.channels_notes[key] += 1

            self.midisong.SetChannels(self.channels_notes)
            # self.parent.ChannelsColorize()

            if self.notes_on_channels:
                self.midisong.SetState(states["cueing"])
            else:
                print(f"MidiReader {self.uuid} NO NOTE ON MIDI CHANNELS")
        except:
            self.midisong.SetState(states["bad"])
            print(f"MidiReader {self.uuid} ERROR READING {self.midisong.Getfilepath()}")

        return self.midisong

    def SetMidiPort(self, port_out):
        self.port_out = port_out

    def run(self):

        if not self.midisong:
            return

        if not self.midisong.IsState(states["cueing"]):
            return

        if self.midisong.IsMode(modes["player"]):
            time.sleep(3)  # more elegant

        elif self.midisong.IsMode(modes["passthrough"]):  # Here ?
            return

        for msg in MidiFile(self.midisong.Getfilepath()):

            # Stop while running ?
            if not self.midisong:
                return

            if self.midisong.GetState() < states["cueing"]:
                self.stop()
                return

            # Just a Midi player
            if self.midisong.IsMode(modes["player"]):

                if self.midisong.IsState(states["cueing"]):
                    msg.time = 0

                time.sleep(msg.time)

                if msg.type == "note_on":
                    if self.channels[msg.channel] and not self.midisong.IsState(
                        states["playing"]
                    ):  # First note on channels selected
                        print(f"MidiReader {self.uuid} ready !")
                        self.midisong.SetState(states["playing"])
                    # Stats
                    if msg.type == "note_on":
                        self.midisong.SetPlayed(
                            int(100 * self.current_notes_on / self.total_notes_on)
                        )
                        self.current_notes_on += 1

                    # Delay
                    if self.keys[
                        "humanize"
                    ]:  # Humanize controlled by knob, see midi_input
                        human = random.randrange(0, self.keys["humanize"], 1) / 2000
                    else:
                        human = 0

                    time.sleep(
                        self.keys["speed"] / 2000 + human
                    )  # Speed controlled by knob, see midi_input

                # Program change : force Prog 0 on all channels (Acoustic Grand Piano) except for drums
                if msg.type == "program_change" and self.settings.GetForceIntrument():
                    if msg.channel != 9:  # not for drums
                        msg.program = self.settings.GetPianoProgram()

                try:  # meta messages can't be send to ports
                    if (
                        self.channels[msg.channel]
                        or msg.type == "program_change"
                        and self.port_out
                    ):
                        self.port_out.send(msg)
                except:
                    pass
                    # if not self.port_out:
                    #    print(f"|!| MidiReader : can not send type=[{msg.type}] msg=[{msg}] to [{self.port_out}]")

                if msg.type == "note_on" and self.channels[msg.channel]:
                    text = f"Keys\t{self.keys['key_on']}"
                    note, octave = number_to_note(msg.note)
                    text = text + f"\t\t {note}{octave}\t\t [{msg.note}]"
                    self.parent.PrintStatusBar(text)

            # Playback : wait keyboard
            elif self.midisong.IsMode(modes["chopin"]):

                # Wait note time
                if (
                    self.midisong.IsState(states["playing"])
                    and msg.time > self.wait_time
                ):
                    time.sleep(msg.time)

                if msg.type == "note_on":
                    if self.channels[msg.channel] and not self.midisong.IsState(
                        states["playing"]
                    ):  # First note on channels selected
                        print(f"MidiReader {self.uuid} ready !")
                        self.midisong.SetState(states["playing"])

                    # Stats
                    self.midisong.SetPlayed(
                        int(100 * self.current_notes_on / self.total_notes_on)
                    )
                    self.current_notes_on += 1

                    # Delay
                    if self.keys[
                        "humanize"
                    ]:  # Humanize controlled by knob, see midi_input
                        human = random.randrange(0, self.keys["humanize"], 1) / 2000
                    else:
                        human = 0

                    time.sleep(
                        self.keys["speed"] / 2000 + human
                    )  # Speed controlled by knob, see midi_input

                if self.midisong.IsState(states["cueing"]):
                    msg.time = 0

                # Pause ?
                if msg.type == "note_on" and self.midisong.IsState(states["playing"]):
                    start_time = time.time()
                    while not self.keys["key_on"]:  # Loop waiting keyboard

                        if not self.channels[msg.channel]:
                            break

                        if not self.midisong:
                            self.stop()
                            return

                        if not self.midisong.IsState(states["playing"]):
                            self.stop()
                            return

                        time.sleep(0.001)  # for loop

                    # Wait a key how much time ?
                    self.wait_time = time.time() - start_time

                # Program change : force Prog 0 on all channels (Acoustic Grand Piano) except for drums
                if msg.type == "program_change" and self.settings.GetForceIntrument():
                    if msg.channel != 9:  # not for drums
                        msg.program = self.settings.GetPianoProgram()

                # Play
                try:  # meta messages can't be send to ports
                    if (
                        self.channels[msg.channel]
                        or msg.type == "program_change"
                        and self.port_out
                    ):
                        self.port_out.send(msg)
                except:
                    if not self.port_out:
                        print(
                            f"|!| MidiReader : can not send type=[{msg.type}] msg=[{msg}] to [{self.port_out}]"
                        )
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
                    time.sleep(0.5)

        # End of song
        self.midisong.SetPlayed(100)
        self.stop()

    def stop(self):
        # print(f"MidiReader {self.uuid} stop")
        if self.midisong:
            self.midisong.SetState(states["ended"])
        self.port_out = None
