#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from mido import MidiFile
from threading import Thread
import time

class midi_file(Thread):
    midifile = None

    def __init__(self):
        Thread.__init__( self )
        pass

    def SetMidiFile(self, filename):
        self.midifile = filename
        try:
            midi = MidiFile(self.midifile)
            for i, track in enumerate(midi.tracks):
                print('Track {}: {}'.format(i, track.name))
        except:
            print(f"midi_file:Cannot read {self.midifile}")

    def run(self):
        for msg in MidiFile(self.midifile):
            time.sleep(msg.time)

            # Pause ?
            if msg.type == 'note_on':
                while not self.keys['key_on']: # Loop waiting keyboard
                    if not self.keys['run']:
                        break
                    time.sleep(msg.time)

            # Play
            try: # meta messages can't be send to ports
                if self.pParent.ChannelIsActive(msg.channel):
                    self.outport.send(msg)
            except:
                pass

            # Stop while running ?
            if not self.keys['run']:
                break

        # End of song
        self.Stop()

    def stop(self):
        pass

