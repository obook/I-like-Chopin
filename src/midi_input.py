#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import uuid
import time

from mido import open_input
from midi_numbers import number_to_note
from midi_song import modes
from PySide6.QtCore import QThread, Signal

from settings_dialog import CleanDeviceName


class ClassThreadInput(QThread):

    uuid = None
    in_device = None
    in_port = None
    out_port = None
    pParent = None
    Settings = None
    running = False
    modulation_start_time = 0

    led_input_activity = Signal(int)
    statusbar_activity = Signal(str)
    shuffle_activity = Signal()
    replay_activity = Signal()
    toogle_activity = Signal()




    def __init__(self, in_device, keys, pParent):
        QThread.__init__(self)
        self.uuid = uuid.uuid4()
        self.pParent = pParent
        self.Settings = self.pParent.Settings
        self.in_device = in_device
        self.keys = keys
        self.running = True
        self.led_input_activity.connect(self.pParent.SetLedInput)
        self.statusbar_activity.connect(self.pParent.SetStatusBar)

        self.shuffle_activity.connect(self.pParent.SignalShuffleMidifile)
        self.replay_activity.connect(self.pParent.SignalReplayMidifile)
        self.toogle_activity.connect(self.pParent.SignalTooglePlayerMode)

        # self.nextsong_activity.connect(self.pParent.NextMidifile)
        # self.previousong_activity.connect(self.pParent.PreviousMidifile)
        print(f"MidiInput {self.uuid} created [{self.in_device}]")

    def __del__(self):
        print(f"MidiInput {self.uuid} destroyed [{self.in_device}]")

    def SetOutPort(self, out_port):
        self.out_port = out_port

    def run(self):

        try:
            self.in_port = open_input(self.in_device, callback=self.callback)  # , client_name='INPUT CHOPIN' = no connexion
            self.running = True
        except Exception as error:
            print(f"|!| MidiInput {self.uuid} {error}")
            return
        if self.Settings.GetMode() == modes["playback"]:
            self.statusbar_activity.emit(
                f"Waiting : {CleanDeviceName(self.in_device)} ..."
            )
            self.led_input_activity.emit(0)

        while self.running:
            self.sleep(1)

        if self.in_port:
            self.in_port.callback = None
            if not self.in_port.closed:
                self.in_port.close()

    def callback(self, msg):

        # Control change - Midi commands
        if msg.type == "control_change":
            if msg.control == 71:
                self.keys["humanize"] = msg.value  # 0 to 127
                self.pParent.PrintHumanize(msg.value)  # PLEASE USE SIGNAL
            elif msg.control == 76:
                self.keys["speed"] = msg.value  # 0 to 127
                self.pParent.PrintSpeed(msg.value)  # PLEASE USE SIGNAL

            ''' Arturia KeyStep 37
            elif msg.control == 51 and msg.value == 127:
                self.toogle_activity.emit()
            '''

            """
            elif msg.control == 1:  # modulation
                diff = time.time() - self.modulation_start_time
                if diff > 3:
                    if msg.value > 64:
                        self.nextsong_activity.emit()
                    else:
                        self.previousong_activity.emit()
                    self.modulation_start_time = time.time()
                self.sleep(0.01)  #  for QT
            """

        # Special Arturia keylab 61 essential, not used if controller present
        elif msg.type == "sysex":
            if msg.data == (0,32,107,127,66,2,0,0,25,0):  # shuffle with the key '->' released
                self.shuffle_activity.emit()
            elif msg.data == (0, 32, 107, 127, 66, 2, 0, 0, 24, 0):  # replay with the key '<-' released
                self.replay_activity.emit()
            elif msg.data == (0, 32, 107, 127, 66, 2, 0, 0, 23, 0):  # switch mode playnack/passthrough with the key 'Preset' released
                self.toogle_activity.emit()

        # Keys pressed counter
        elif msg.type == "note_on":
            if msg.velocity:
                self.keys["key_on"] += 1
                self.led_input_activity.emit(1)
            else:
                # A MIDI Note On with a velocity of 0 is regarded as a Note Off.
                # That is part of the MIDI Standard
                self.keys["key_on"] -= 1
                self.led_input_activity.emit(0)

        elif msg.type == "note_off":
            self.keys["key_on"] -= 1
            self.led_input_activity.emit(0)

        # Rares cases
        if self.keys["key_on"] < 0:
            self.keys["key_on"] = 0

        # Passthrough mode
        if self.Settings.IsMode(modes["passthrough"]):

            self.keys["key_on"] = 0

            if msg.type == "note_on":  # or message.type == 'note_off':
                if msg.velocity:
                    note, octave = number_to_note(msg.note)
                    text = f"[{msg.note}]\t\t{note} {octave-1}"
                    self.statusbar_activity.emit(text)

            # Play
            self.pParent.Midi.SendOutput(msg)

    def getport(self):
        if self.in_port:
            return self.in_port
        return None

    def stop(self):
        self.running = False
