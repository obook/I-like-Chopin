#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from mido import MidiFile
from threading import Thread
from midi_numbers import number_to_note
import time
import os
import random
import uuid

class ClassThreadMidiReader(Thread):
    midisong = None
    keys = None
    port_out = None
    settings = None
    ready = False
    uuid = None
    total_notes_on = 0
    current_notes_on = 0
    channels = None

    def __init__(self,midisong,keys,channels,pParent):
        Thread.__init__( self )
        self.parent = pParent
        self.settings = self.parent.settings
        self.midisong = midisong
        self.keys = keys
        self.channels = channels
        self.uuid = uuid.uuid4()
        print(f"MidiReader {self.uuid} created [{self.midisong.GetFilename()}]")

    def __del__(self):
        print(f"MidiReader {self.uuid} destroyed [{self.midisong.GetFilename()}]")
        self.midisong = None

    def SetMidiSong(self, midisong): # returns array of tracks names

        self.midisong = midisong
        tracks = []
        try:
            midi = MidiFile(self.midisong.Getfilepath())
            #self.midisong.SetDuration(round(midi.length/60,2))
            self.midisong.SetDuration(midi.length/60)
            for i, track in enumerate(midi.tracks):
                tracks.append(track.name)

            self.total_notes_on = 0
            for msg in MidiFile(self.midisong.Getfilepath()):
                if msg.type == 'note_on':
                    self.total_notes_on +=1

            self.midisong.SetTracks(tracks)
            self.midisong.SetActive(True)
        except:
            print(f"MidiReader {self.uuid} ERROR READING {self.midisong.Getfilepath()}")
            return None

    def SetMidiPort(self,port_out):
        #print(f"MidiReader {self.uuid} SetMidiPort [{port_out}]")
        self.port_out = port_out

    def run(self):

        self.midisong.ready = False

        if not self.midisong.Active(): # SetMidiFile failed to get tracks, malformed midifile ?
            return

        if self.midisong:
            if not os.path.isfile(self.midisong.Getfilepath()):
                print("MidiReader {self.uuid} midisong [{self.midisong.Getfilepath()}] not found")
                return

        self.midisong.SetActive(True)

        for msg in MidiFile(self.midisong.Getfilepath()):

            # Stop while running ?
            if self.midisong:
                if not self.midisong.Active():
                    self.stop()
                    return

            # Note Time
            if self.midisong.ready:
                time.sleep(msg.time)

            if msg.type == 'note_on':
                #print(f"MidiReader {self.uuid} note_on msg.channel {msg.channel} self.midisong.ready {self.midisong.ready}")
                # First note on channels selected
                if self.channels[msg.channel] and not self.midisong.ready:
                    print(f"MidiReader {self.uuid} ready")
                    self.midisong.ready = True

                # Stats
                self.midisong.played = int(100*self.current_notes_on/self.total_notes_on)
                self.current_notes_on += 1

                # Humanize controlled by knob, see midi_input
                if self.keys['humanize']:
                    human = random.randrange(0,self.keys['humanize'],1)/2000
                else:
                    human = 0

                # Speed controlled by knob, see midi_input
                msg.time = msg.time + self.keys['speed']/2000 + human

            if not self.midisong.ready:
                msg.time = 0

            # Pause ?
            if msg.type == 'note_on' and self.midisong.ready:
                while not self.keys['key_on']: # Loop waiting keyboard

                    if not self.channels[msg.channel]:
                        break

                    if not self.midisong:
                            self.stop()
                            return

                    if not self.midisong.Active():
                        self.stop()
                        return

                    time.sleep(0.001) # for loop

            # Program change : force Prog 0 on all channels (Acoustic Grand Piano) except for drums
            if msg.type == 'program_change' and self.settings.GetForceIntrument():
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
        self.midisong.played = 100
        self.stop()

    def stop(self):
        # print(f"MidiReader {self.uuid} stop")
        if self.midisong:
            self.midisong.SetActive(False)
            self.midisong.ready = False
        self.port_out = None

