#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from mido import open_input
from threading import Thread
from  midi_numbers import number_to_note

class ClassThreadInput(Thread):
    in_device = None
    inport = None
    running = False

    def __init__(self, in_device, keys, pParent):
        Thread.__init__( self )
        self.in_device = in_device
        self.keys = keys
        self.pParent = pParent
        self.running = True
        print("ClassThreadInput created")

    def __del__(self):
            print("ClassThreadInput destroyed")

    def run(self):
        self.stop()
        try:
            self.inport = open_input(self.in_device, callback=self.callback)
            self.running = True
        except:
            print(f"midi_input:Error connect from {self.in_device}")
            return

        print(f"midi_input:run open_output [{self.in_device}] READY")

    def callback(self, message):

        filter =['clock','stop','note_off']
        if message.type not in filter:
            print(f"ClassThreadInput:{message}")

        # Midi commands
        # control_change channel=1 control=77 -> Speed controlled by knob
        if message.type =='control_change':
            if message.control == 71:
                self.keys['humanize'] = message.value #0 to 127
                self.pParent.PrintHumanize(message.value)
            elif message.control == 76:
                self.keys['tempo'] = message.value #0 to 127
                self.pParent.PrintSlow(message.value)
            elif message.control == 77:
                self.pParent.ChangeMidiFile(message.value)

        # Counter
        if message.type == 'note_on':
            self.keys['key_on'] +=1
        elif message.type == 'note_off':
            self.keys['key_on'] -=1

        text = str(self.keys['key_on'])
        if message.type == 'note_on': # or message.type == 'note_off':
            note, octave = number_to_note(message.note)
            text = text + f"\t\t {note}{octave} \t\t [{message.note}]"
        self.pParent.PrintKeys(text)

    def active(self):
        if self.inport :
            return True
        return False

    def stop(self):
        print("midi_input:stop")
        self.running = False
        if self.inport :
            self.inport.close()
            self.inport = None

