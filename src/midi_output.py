#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from threading import Thread, get_native_id
from mido import open_output, Message
from settings import ClassSettings

class ClassThreadOutput(Thread):
    out_device = None
    outport = None
    def __init__(self, out_device, keys, pParent):
        Thread.__init__( self )
        self.settings = ClassSettings()
        self.out_device = out_device
        self.keys = keys
        self.pParent = pParent
        print(f"ClassThreadOutput {get_native_id()} created")

    def __del__(self):
        print(f"ClassThreadOutput {get_native_id()} destroyed")

    def run(self):
        self.stop()
        try:
            self.outport = open_output(self.out_device,autoreset=True)
        except:
            self.outport = None
            print(f"midi_output open [{self.out_device}] ERROR")
            return

        print(f"midi_output:run open_output [{self.out_device}] READY")

        # Set all channels to Piano ('Acoustic Grand Piano') if set
        self.forcePiano()

        return self.outport

    def forcePiano(self):
        if self.outport and self.settings.GetForceIntrument():
            init_message = Message('program_change')
            init_message.program = 0 # Bank 0 Intrument 0
            for i in range(16):
                init_message.channel = i
                if i != 15 : # not for drums
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
        print("midi_output:stop")
        if self.outport :
            self.outport.close()
            self.outport = None

