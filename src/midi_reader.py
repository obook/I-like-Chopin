#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from mido import MidiFile
from threading import Thread, get_native_id
from settings import ClassSettings
import time
import os
import random

class ClassThreadMidiReader(Thread):
    midisong = None
    keys = None
    port_out = None
    ready = False

    def __init__(self,midisong,keys,channels):
        Thread.__init__( self )
        self.settings = ClassSettings()
        self.midisong = midisong
        self.keys = keys
        self.channels = channels
        print(f"ClassThreadMidiReader {get_native_id()} created")

    def __del__(self):
            print(f"ClassThreadMidiReader {get_native_id()} destroyed")

    def SetMidiSong(self, midisong): # returns array of tracks names

        self.midisong = midisong
        self.midisong.tracks = []
        try:
            midi = MidiFile(self.midisong.Getfilepath())
            self.midisong.SetDuration(round(midi.length/60,2))
            print(f"ClassThreadMidiReader:{self.midisong.Getfilepath()}={self.midisong.GetDuration()} minutes")
            for i, track in enumerate(midi.tracks):
                self.midisong.tracks.append(track.name)
                # print('ClassThreadMidiReader:Track {} [{}]'.format(i, track.name))
            self.ready = True
        except:
            print(f"ClassThreadMidiReader:ERROR READING {self.midisong.Getfilepath()}")
            return None

    def SetMidiPort(self,port_out):
        print(f"ClassThreadMidiReader:SetMidiPort [{port_out}]")
        self.port_out = port_out

    def run(self):

        if not self.ready: # SetMidiFile failed to get tracks, malformed midifile ?
            return

        print(f"ClassThreadMidiReader:run [{self.midisong.Getfilepath()}]")
        if self.midisong:
            if not os.path.isfile(self.midisong.Getfilepath()):
                print("ClassThreadMidiReader:midisong [{self.midisong.Getfilepath()}] not found")
                return

        for msg in MidiFile(self.midisong.Getfilepath()):

            # Stop while running ?
            if not self.ready:
                break

            # Speed controlled by knob, see midi_input
            if msg.type == 'note_on':
                if self.keys['humanize']:
                    human = random.randrange(0,self.keys['humanize'],1)/2000
                else:
                    human = 0
                msg.time = msg.time + self.keys['speed']/2000 + human

            time.sleep(msg.time)

            # Pause ?
            if msg.type == 'note_on':
                while not self.keys['key_on']: # Loop waiting keyboard
                    if not self.ready:
                        self.stop()
                        return
                    time.sleep(msg.time)

            # Program change : force Prog 0 on all channels (Acoustic Grand Piano) except for drums
            if msg.type == 'program_change' and self.settings.GetForceIntrument():
                # print(f"programme change channel {msg.channel}={program_to_instrument(msg.program+1)}")
                if msg.channel != 15: # not for drums
                    msg.program = self.settings.GetPianoProgram()

            # Play
            try: # meta messages can't be send to ports
                if self.port_out and self.channels[msg.channel]:
                    self.port_out.send(msg)
            except:
                # print("ERROR->ClassThreadMidiFile:port_out.send type=", type(self.port_out), "msg=", msg)
                pass

        # End of song
        self.stop()

    def active(self):
        return self.ready

    def stop(self):
        self.ready = False


