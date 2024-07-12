#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from mido import open_input
from threading import Thread

class ClassThreadInput(Thread):
    inport = None
    running = False

    def __init__(self, keys, pParent):
        Thread.__init__( self )
        self.keys = keys
        self.pParent = pParent

    def SetInput(self, in_device):
        self.in_device = in_device

    def run(self):
        self.stop()
        try:
            #self.inport = open_input(self.in_device, callback=self.CallbackInput)
            self.inport = open_input(self.in_device, callback=self.callback)
            self.running = True
        except:
            print(f"midi_input:Error connect from {self.in_device}")
            return

        print(f"midi_input:run open_output [{self.in_device}] READY")

    def stop(self):
        self.running = False
        if self.inport :
            self.inport.close()
            self.inport = None

    def callback(self, message):
        '''
        filter =['clock','stop','note_off']
        if message.type not in filter:
            print(f"ClassThreadInput:{message}")
        '''
        # Counter
        if message.type == 'note_on':
            self.keys['key_on'] +=1
        elif message.type == 'note_off':
            self.keys['key_on'] -=1

    def quit(self):
        print("midi_input:quit")
        self.stop()
        exit(0)
