#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# if __name__ == "__main__":
#     pass

from mido import open_input
from threading import Thread

# Wait keys from keyboard
class MidiKeyboard( Thread ):

    inport = None

    def __init__( self, in_device, keys, pParent ):
        Thread.__init__( self )
        self.in_device = in_device
        self.keys = keys
        self.pParent = pParent

    def run( self ):

        try:
            self.inport = open_input(self.in_device, callback=self.callback)
            self.pParent.PrintBrowser(f'MidiKeyboard from [{self.in_device}]')
        except:
            self.pParent.PrintBrowser(f"MidiKeyboard:Error connect from {self.in_device}")
            return

        self.keys['MidiKeyboardRunning'] = True

    def callback(self,message):

        if message.type == 'note_on':
            self.keys['key_on'] +=1
            # Security ; press key C#4 (49) for pause
            if message.note == 49 :
                self.keys['key_on'] = 0
                self.pParent.PrintBrowser("MidiKeyboard:reset to zero key")

        elif message.type == 'note_off':
            self.keys['key_on'] -=1

        if self.keys['key_on'] <0 : # rare, in case of missing key on
            self.keys['key_on'] = 0


        # print(f"keys on:{self.keys['key_on']}\r", end="")
        self.pParent.PrintKeys(str(self.keys['key_on']))

        #if key.type == 'key_on' or key.type == 'note_off':
        #    note, octave = number_to_note(key.note)
        #    print(f"{key.type} {note}{octave} ({key.note}) [{keys['key_on']} keys on]")

    def Stop(self):
        # self.pParent.PrintBrowser('MidiKeyboard stop.')
        if self.inport :
            self.inport.close()
            self.inport = None

        self.keys['MidiKeyboardRunning'] = False
