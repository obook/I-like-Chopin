#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import uuid

from threading import Thread
from mido import open_output, Message

class ClassThreadOutput(Thread):
    """Class for output midi to device"""
    out_device = None
    outport = None
    uuid = None
    settings = None

    def __init__(self, out_device, keys, pParent):
        Thread.__init__( self )
        self.pParent = pParent
        self.settings = self.pParent.settings
        self.out_device = out_device
        self.keys = keys
        self.uuid = uuid.uuid4()
        print(f"MidiOutput {self.uuid} created [{self.out_device}]")

    def __del__(self):
        print(f"MidiOutput {self.uuid} destroyed [{self.out_device}]")

    def run(self):
        self.stop()
        try:
            self.outport = open_output(self.out_device,autoreset=True)
        except:
            self.outport = None
            print(f"MidiOutput {self.uuid} midi_output open [{self.out_device}] ERROR")
            return

        # Set all channels to Piano ('Acoustic Grand Piano') if set
        self.forcePiano()

        return self.outport

    def forcePiano(self):
        if self.settings.GetForceIntrument():
            init_message = Message('program_change')
            # TODO : select bank 0 by control_change
            # See https://music.stackexchange.com/questions/95786/how-do-you-implement-control-change-messages-using-the-mido-library
            init_message.program = self.settings.GetPianoProgram() # Bank 0 Intrument 0
            for i in range(16):
                init_message.channel = i
                if i != 10 : # not for drums
                    try:
                        self.outport.send(init_message)
                    except:
                        pass

    def send(self, message):
        if self.outport :
            self.outport.send(message)

    def getport(self):
        return self.outport

    def panic(self):
        if self.outport :
            self.outport.panic()
            self.forcePiano()

    def active(self):
        if self.outport :
            return True
        return False

    def stop(self):
        #print(f"MidiOutput {self.uuid} stop")
        if self.outport :
            self.outport.close()
            self.outport = None

