#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import uuid
import time

from mido import open_output, Message
from PySide6.QtCore import QThread, Signal


class ClassThreadOutput(QThread):
    """Class for output midi to device"""

    uuid = uuid.uuid4()
    pParent = None
    out_device = None
    outport = None
    Settings = None
    please_wait = False
    ready = False

    led_activity = Signal(int)

    def __init__(self, out_device, pParent):
        QThread.__init__(self)
        self.pParent = pParent
        self.Settings = pParent.Settings
        self.out_device = out_device
        self.led_activity.connect(self.pParent.SetLedOutput)
        print(f"MidiOutput {self.uuid} created [{self.out_device}]")

    def __del__(self):
        print(f"MidiOutput {self.uuid} destroyed [{self.out_device}]")

    def run(self):
        self.please_wait = True
        try:
            self.outport = open_output(self.out_device, autoreset=True)
        except:
            self.outport = None
            print(
                f"|!| MidiOutput {self.uuid} midi_output open [{self.out_device}] ERROR"
            )

        # Set all channels to Piano ('Acoustic Grand Piano') if set
        self.forcePiano()
        self.please_wait = False
        self.ready = True
        while self.ready:
            self.sleep(1)  # or self

        if self.outport:
            if not self.outport.closed:
                self.outport.close()

    def IsReady(self):
        return self.ready

    def forcePiano(self):
        if self.outport:
            if self.Settings.GetForceIntrument():
                print(f"MidiOutput {self.uuid} forcePiano")
                init_message = Message("program_change")
                # TODO : select bank 0 by control_change
                # See https://music.stackexchange.com/questions/95786/how-do-you-implement-control-change-messages-using-the-mido-library
                init_message.program = (
                    self.Settings.GetPianoProgram()
                )  # Bank 0 Intrument 0
                for i in range(16):
                    init_message.channel = i
                    if i != 9:  # not for drums
                        try:
                            self.outport.send(init_message)
                        except:
                            print(f"MidiOutput {self.uuid} self.outport.send ERROR")

    def send(self, message):
        if self.ready:
            if message.type == "note_on":
                self.led_activity.emit(1)
            else:
                self.led_activity.emit(0)
            if self.outport:
                try:
                    self.outport.send(message)
                except:
                    pass

    def getport(self):
        while self.please_wait == True:
            time.sleep(0.01)
        return self.outport

    def panic(self):
        if self.outport:
            self.outport.panic()
            self.forcePiano()

    def reset(self):
        if self.outport:
            self.outport.reset()
            self.outport.panic()

    def stop(self):
        self.ready = False
