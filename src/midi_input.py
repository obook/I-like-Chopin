#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from mido import open_input
from threading import Thread
from settings import ClassSettings
from midi_numbers import number_to_note
import uuid

class ClassThreadInput(Thread):
    in_device = None
    in_port = None
    out_port = None
    running = False
    uuid = None

    def __init__(self, in_device, keys, pParent):
        Thread.__init__( self )
        self.settings = ClassSettings()
        self.in_device = in_device
        self.keys = keys
        self.pParent = pParent
        self.running = True
        self.uuid = uuid.uuid4()
        print(f"MidiInput {self.uuid} created [{self.in_device}]")

    def __del__(self):
        print(f"MidiInput {self.uuid} destroyed [{self.in_device}]")

    def SetOutPort(self,out_port):
        self.out_port = out_port

    def run(self):
        self.stop()
        try:
            self.in_port = open_input(self.in_device, callback=self.callback)
            self.running = True
        except:
            print(f"MidiInput {self.uuid} midi_input:Error connect from {self.in_device}")
            return
        self.pParent.PrintStatusBar(f"Waiting:{self.in_device} ...")

    def callback(self, message):

        if self.settings.GetPrintTerm():
            filter =['clock','stop','note_off']
            if message.type not in filter:
                print(f"MidiInput {self.uuid}:{message}")

        # Control change - Midi commands
        if message.type =='control_change':
            if message.control == 71:
                self.keys['humanize'] = message.value #0 to 127
                self.pParent.PrintHumanize(message.value)
            elif message.control == 76:
                self.keys['speed'] = message.value #0 to 127
                self.pParent.PrintSpeed(message.value)
            elif message.control == 77:
                self.pParent.ChangeMidiFile(message.value)
            elif message.control == 51 and message.value == 127:
                self.pParent.Mode()

        # Playback/Passthrough mode
        if not self.keys['playback']:
            self.keys['key_on'] = 0
            # Play
            try: # meta messages can't be send to ports
                if self.out_port:
                    self.out_port.send(message)
            except:
                pass
            return

        # Keys pressed counter
        if message.type == 'note_on':
            self.keys['key_on'] +=1
        elif message.type == 'note_off':
            self.keys['key_on'] -=1

        # Rares cases
        if self.keys['key_on'] < 0:
            self.keys['key_on'] = 0

        text = f"Keys\t{self.keys['key_on']}"
        if message.type == 'note_on': # or message.type == 'note_off':
            note, octave = number_to_note(message.note)
            text = text + f"\t\t {note}{octave} \t\t [{message.note}]"
        self.pParent.PrintStatusBar(text)

    def active(self):
        if self.in_port :
            return True
        return False

    def stop(self):
        # print(f"MidiInput {self.uuid} stop")
        self.running = False
        if self.in_port :
            self.in_port.close()
            self.in_port = None

