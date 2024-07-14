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
    running = False

    def __init__(self,keys):
        Thread.__init__( self )
        self.keys = keys
        self.running = True
        self.tracks = None

    def __del__(self):
            print("ClassThreadMidiFile destroyed")

    def SetMidiFile(self, filename, tracks):
        self.midifile = filename
        self.tracks = tracks
        try:
            midi = MidiFile(self.midifile)
            print(f"{self.midifile} = {round(midi.length/60,2)} minutes ")
            for i, track in enumerate(midi.tracks):
                print('Track {}: {}'.format(i, track.name))
        except:
            print(f"ClassThreadMidiFile:Cannot read {self.midifile}")

    def SetMidiPort(self,port_out):
        self.port_out = port_out

    def run(self):

        print(f"ClassThreadMidiFile:run : [{self.midifile}]")

        for msg in MidiFile(self.midifile):
            print("ClassThreadMidiFile:msg =",msg, "keys=",self.keys['key_on'] )

            time.sleep(msg.time)

            # Pause ?
            if msg.type == 'note_on':
                while not self.keys['key_on']: # Loop waiting keyboard
                    if not self.running:
                        break
                    time.sleep(msg.time)

            # Play
            try: # meta messages can't be send to ports
                if self.port_out and self.tracks[msg.channel]:
                    self.port_out.send(msg)
            except:
                # print("ClassThreadMidiFile:ERROR port_out.send type=", type(self.port_out), "msg=", msg)
                pass

            # Stop while running ?
            if not self.running:
                break

        # End of song
        self.quit()

    def quit(self):
        print("midi_file:return")
        self.running = False
        return

