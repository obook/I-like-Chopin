#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from mido import MidiFile
from threading import Thread
import time

class ClassThreadMidiFile(Thread):
    midifile = None
    keys = None
    port_out = None

    def __init__(self,keys):
        Thread.__init__( self )
        self.keys = keys

    def SetMidiFile(self, filename):
        self.midifile = filename
        try:
            midi = MidiFile(self.midifile)
            print(f"{self.midifile} = {round(midi.length/60,2)} minutes ")
            for i, track in enumerate(midi.tracks):
                print('Track {}: {}'.format(i, track.name))
        except:
            print(f"midi_file:Cannot read {self.midifile}")

    def run(self):
        pass

    def play(self, port_out):
        self.port_out = port_out
        print(f"midi_file:run : [{self.midifile}]")
        # self.keys['play'] = True
        for msg in MidiFile(self.midifile):
            print("midi_file:msg =",msg, "self.keys['play']=", self.keys['play'], "keys=",self.keys['key_on'] )

            time.sleep(msg.time)

            # Pause ?
            if msg.type == 'note_on':
                while not self.keys['key_on']: # Loop waiting keyboard
                    if not self.keys['play']:
                        print("BREAK:play1")
                        break
                    time.sleep(msg.time)

            # Play
            try: # meta messages can't be send to ports
                #if self.pParent.ChannelIsActive(msg.channel):
                self.port_out.send(msg)
            except:
                print("ClassThreadMidiFile:ERROR port_out.send")

            # Stop while running ?
            if not self.keys['play']:
                print("BREAK:play2")
                break

        # End of song
        self.stop()

    def stop(self):
        print("midi_file:stop")

