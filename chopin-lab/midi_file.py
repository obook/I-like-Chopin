#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from mido import MidiFile
from threading import Thread
import time
import os

class ClassThreadMidiFile(Thread):
    midifile = None
    keys = None
    port_out = None
    running = False

    def __init__(self,keys,tracks):
        Thread.__init__( self )
        self.keys = keys
        self.running = False
        self.tracks = tracks
        print("ClassThreadMidiFile created")

    def __del__(self):
            print("ClassThreadMidiFile destroyed")

    def SetMidiFile(self, filename):
        self.midifile = filename
        try:
            midi = MidiFile(self.midifile)
            print(f"{self.midifile} = {round(midi.length/60,2)} minutes")
            for i, track in enumerate(midi.tracks):
                print('Track {}: {}'.format(i, track.name))
        except:
            print(f"ClassThreadMidiFile:Cannot read {self.midifile}")

    def SetMidiPort(self,port_out):
        print("ClassThreadMidiFile:SetMidiPort")
        self.port_out = port_out

    def run(self):

        print(f"ClassThreadMidiFile:run : [{self.midifile}]")
        if self.midifile:
            if not os.path.isfile(self.midifile):
                print("ClassThreadMidiFile:midifile not found")
                return

        self.running = True

        for msg in MidiFile(self.midifile):
            # ("ClassThreadMidiFile:msg =",msg, "keys=",self.keys['key_on'] )

            # Stop while running ?
            if not self.running:
                break

            # Speed controlled by knob, see midi_input
            if msg.type == 'note_on':
                msg.time = msg.time + self.keys['tempo']/5000

            time.sleep(msg.time)

            # Pause ?
            if msg.type == 'note_on':
                while not self.keys['key_on']: # Loop waiting keyboard
                    if not self.running:
                        self.stop()
                        return
                    time.sleep(msg.time)

            # Play
            try: # meta messages can't be send to ports
                if self.port_out and self.tracks[msg.channel]:
                    self.port_out.send(msg)
            except:
                # print("ERROR->ClassThreadMidiFile:port_out.send type=", type(self.port_out), "msg=", msg)
                pass

        # End of song
        self.stop()

    def active(self):
        return self.running

    def stop(self):
        print("midi_file:stop")
        self.running = False


