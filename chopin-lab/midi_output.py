#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from threading import Thread
from mido import open_output

class ClassThreadOutput(Thread):
    outport = None
    def __init__(self, keys, pParent):
        Thread.__init__( self )
        self.keys = keys
        self.pParent = pParent

    def __del__(self):
        print("ClassThreadOutput destroyed")

    def SetOutput(self, out_device):
        self.out_device = out_device

    def run(self):
        self.stop()
        try:
            self.outport = open_output(self.out_device)
        except:
            self.outport = None
            print(f"midi_output open [{self.out_device}] ERROR")
            return

        print(f"midi_output:run open_output [{self.out_device}] READY")

    def send(self, message):
        if self.outport :
            self.outport.send(message)

    def getport(self):
        return self.outport

    def panic(self):
        if self.outport :
            self.outport.panic()

    def stop(self):
        if self.outport :
            self.outport.close()
            self.outport = None

    def quit(self):
        print("midi_output:quit")
        self.stop()

