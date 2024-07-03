#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This Python file uses the following encoding: utf-8

from threading import Thread
from mido import open_input, open_output

class MidiPassthrough(Thread):
    def __init__(self, in_device, out_device, keys, pParent):
        Thread.__init__( self )
        self.in_device = in_device
        self.out_device = out_device
        self.keys = keys
        self.pParent = pParent

    def run( self ):
        self.inport = open_input(self.in_device)
        self.outport = open_output(self.out_device)

        self.pParent.PrintBrowser("Passthrough Ready.")

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
        self.inport.close()
        self.outport.close()



