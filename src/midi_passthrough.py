#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

from threading import Thread
from mido import open_input, open_output
from  midi_numbers import number_to_note

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
            self.inport = open_input(self.in_device, callback=self.callback)
        except:
            self.pParent.PrintBrowser(f"Passthrough:Error open input [{self.in_device}]")
            self.Stop()
            return

        try:
            self.outport = open_output(self.out_device)
        except:
            self.pParent.PrintBrowser(f"Passthrough:Error open ouput [{self.out_device}]")
            self.Stop()
            return

        self.pParent.PrintBrowser("Passthrough started")

    def callback(self, message):
        if not self.keys['run']:
            return
        try:
            self.outport.send(message)
            if message.type == 'note_on' : # or message.type == 'note_off':
                note, octave = number_to_note(message.note)
                print=f" {note}{octave} ({message.note}) {message.type}"
            else:
                print=f" {message.type}"

            self.pParent.PrintKeys(str(self.keys['key_on'])+print)
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
