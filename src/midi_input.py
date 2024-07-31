#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import uuid

from mido import open_input
from midi_numbers import number_to_note
from midi_song import modes
from PySide6.QtCore import QThread, Signal

class ClassThreadInput(QThread):

    uuid = uuid.uuid4()
    in_device = None
    in_port = None
    out_port = None
    pParent = None
    settings = None
    running = False

    led_activity = Signal(int)

    def __init__(self, in_device, keys, pParent):
        QThread.__init__(self)

        self.pParent = pParent
        self.settings = self.pParent.settings
        self.in_device = in_device
        self.keys = keys
        self.running = True
        self.led_activity.connect(self.pParent.SetLedInput)
        print(f"MidiInput {self.uuid} created [{self.in_device}]")

    def __del__(self):
        print(f"MidiInput {self.uuid} destroyed [{self.in_device}]")

    def SetOutPort(self, out_port):
        self.out_port = out_port

    def run(self):
        self.stop()
        try:
            self.in_port = open_input(self.in_device, callback=self.callback)
            self.running = True
        except:
            print(
                f"MidiInput {self.uuid} midi_input:Error connect from {self.in_device}"
            )
            return
        if self.settings.GetMode() == modes["chopin"]:
            self.pParent.PrintStatusBar(f"Waiting : {self.in_device} ...")

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
            text = f"Keys\t{self.keys['key_on']}"
            if message.type == "note_on":  # or message.type == 'note_off':
                note, octave = number_to_note(message.note)
                text = text + f"\t\t {note}{octave}\t\t [{message.note}]"
            self.pParent.PrintStatusBar(text)

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

    def active(self):
        if self.in_port:
            return True
        return False

    def stop(self):
        # print(f"MidiInput {self.uuid} stop")
        self.running = False
        if self.in_port:
            self.in_port.close()
            self.in_port = None
