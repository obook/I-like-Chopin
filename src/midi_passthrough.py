#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

from threading import Thread
from mido import open_input, open_output

class MidiPassthrough(Thread):
    inport = None
    outport = None

    def __init__(self, in_device, out_device, keys, pParent):
        Thread.__init__( self )
        self.in_device = in_device
        self.out_device = out_device
        self.keys = keys
        self.pParent = pParent

    def run( self ):
        try:
            self.inport = open_input(self.in_device)
            self.outport = open_output(self.out_device)
        except:
            self.pParent.PrintBrowser("Passthrough:Error open ports.")
            self.Stop()
            return

        self.pParent.PrintBrowser("Passthrough Started")

        while True: # non-blocking

            if not self.keys['run']:
                break

            for key in self.inport.iter_pending():
                # Play
                try:
                    self.outport.send(key)
                    self.pParent.PrintKeys(str(self.keys['key_on']))
                except:
                    pass

    def Stop(self):
        if self.inport :
            self.inport.close()
            self.inport = None
        if self.outport:
            self.outport.close()
            self.outport = None
        self.pParent.PrintBrowser("Passthrough ended")
