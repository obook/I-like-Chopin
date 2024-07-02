#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# if __name__ == "__main__":
#     pass

from mido import open_input
from threading import Thread

# Wait keys from keyboard
class MidiKeyboard( Thread ):

    def __init__( self, in_device, keys, pParent ):
        Thread.__init__( self )
        self.in_device = in_device
        self.keys = keys
        self.pParent = pParent

    def run( self ):
        global inport

        self.keys['MidiKeyboardRunning'] = True

        # NON-BLOCKING
        inport = open_input(self.in_device)
        print(f'Wait keys from "{self.in_device}...')
        while True: # non-blocking
            if not self.keys['run']:
                print('MidiKeyboard closing port and stop.')
                inport.close()
                self.keys['MidiKeyboardRunning'] = False
                return

            for key in inport.iter_pending():

                if key.type == 'note_on':
                    self.keys['key_on'] +=1
                    # Security ; press key C#4 (49) for pause
                    if key.note == 49 :
                        self.keys['key_on'] = 0

                elif key.type == 'note_off':
                    self.keys['key_on'] -=1

                if self.keys['key_on'] <0 : # rare, in case of missing key on
                    self.keys['key_on'] = 0


                # print(f"keys on:{self.keys['key_on']}\r", end="")
                self.pParent.PrintKeys(str(self.keys['key_on']))

                #if key.type == 'key_on' or key.type == 'note_off':
                #    note, octave = number_to_note(key.note)
                #    print(f"{key.type} {note}{octave} ({key.note}) [{keys['key_on']} keys on]")

        '''
        # BLOCKING
        try:
            with open_input(self.in_device) as inport:
                print(f'Wait keys from "{self.in_device}...')
                for key in inport: # attente clavier

                    if not self.keys['run']:
                        print('MidiKeyboard closing port and stop.')
                        inport.close()
                        self.keys['MidiKeyboardRunning'] = False
                        return

                    elif key.type == 'note_on':
                        self.keys['key_on'] +=1
                        # note, octave = number_to_note(key.note)
                        # print(f"{key.note}={note}{octave}")
                        # Security ; press key C#4 (49) for pause
                        if key.note == 49 :
                            self.keys['key_on'] = 0

                    elif key.type == 'note_off':
                        self.keys['key_on'] -=1

                    if self.keys['key_on'] <0 : # rare, in case of missing key on
                        self.keys['key_on'] = 0

                    print(f"keys on:{self.keys['key_on']}\r", end="")
                    self.pParent.PrintKeys(str(self.keys['key_on']))
        except:
            print(f'Error connect to input "{self.in_device}"')
      '''
        self.keys['MidiKeyboardRunning'] = False

