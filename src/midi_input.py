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

class ClassThreadInput(QThread):

    uuid = None
    in_device = None
    in_port = None
    out_port = None
    pParent = None
    settings = None
    running = False

    led_activity = Signal(int)
    statusbar_activity = Signal(str)

    def __init__(self, in_device, keys, pParent):
        QThread.__init__(self)
        self.uuid = uuid.uuid4()
        self.pParent = pParent
        self.settings = self.pParent.settings
        self.in_device = in_device
        self.keys = keys
        self.running = True
        self.led_activity.connect(self.pParent.SetLedInput)
        self.statusbar_activity.connect(self.pParent.SetStatusBar)
        print(f"MidiInput {self.uuid} created [{self.in_device}]")

    def __del__(self):
        print(f"MidiInput {self.uuid} destroyed [{self.in_device}]")

    def SetOutPort(self, out_port):
        self.out_port = out_port

    def run(self):

        try:
            self.in_port = open_input(self.in_device, callback=self.callback)
            self.running = True
        except:
            print(
                f"MidiInput {self.uuid} midi_input:Error connect from {self.in_device}"
            )
            return
        if self.settings.GetMode() == modes["chopin"]:
            self.statusbar_activity.emit(f"Waiting : {self.in_device} ...")

        while self.running:
            time.sleep(1) # or self

        if self.in_port:
            self.in_port.callback = None
            if not self.in_port.closed:
                self.in_port.close()

    def callback(self, message):

        # Control change - Midi commands
        if message.type == "control_change":
            if message.control == 71:
                self.keys["humanize"] = message.value  # 0 to 127
                self.pParent.PrintHumanize(message.value)
            elif message.control == 76:
                self.keys["speed"] = message.value  # 0 to 127
                self.pParent.PrintSpeed(message.value)
            elif message.control == 77:
                self.pParent.ChangeMidiFile(message.value)
            elif message.control == 51 and message.value == 127:
                self.pParent.ChangePlayerMode()

        # Keys pressed counter
        if message.type == "note_on":
            self.led_activity.emit(1)
            self.keys["key_on"] += 1
        elif message.type == "note_off":
            self.led_activity.emit(0)
            self.keys["key_on"] -= 1

        # Rares cases
        if self.keys["key_on"] < 0:
            self.keys["key_on"] = 0

        if not self.settings.IsMode(modes["player"]):
            if message.type == "note_on":  # or message.type == 'note_off':
                note, octave = number_to_note(message.note)
                text = f"{note}{octave}\t\t [{message.note}]"
                self.statusbar_activity.emit(text)

        # Playback/Passthrough mode
        if self.settings.IsMode(modes["passthrough"]):
            self.keys["key_on"] = 0
            # Play
            try:  # meta messages can't be send to ports
                if self.out_port:
                    self.out_port.send(message)
                else:
                    print("---> NO PORT")
            except:
                pass
            return

    def getport(self):
        if self.in_port:
            return self.in_port
        return None

    def stop(self):
        self.running = False
