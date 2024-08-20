#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:17:57 2024
@author: obooklage
Tool for checking midifiles : only channel 1, readeable
! Channels are from 0 to 15
"""

import glob
from mido import MidiFile

def SystainPedalCheck(file):
    sustain = 0
    tracks = 0

    try:
        # Tracks
        midi = MidiFile(file)
        for i, track in enumerate(midi.tracks):
            tracks+=1

        for msg in MidiFile(file):
            if msg.type == "control_change":
                if msg.value == 64: # The sustain pedal sends CC 64 127 and CC 64 0 messages on channel 1
                    sustain +=1
    except Exception as error:
        print(f"|!| CAN NOT READ {file} {error}")
        sustain=0
        tracks=0
        pass

    return tracks, sustain

print("** START")

root_dir = "/home/obooklage/obooklage@gmail.com/ownCloud.CAP/MUSIQUE/"

f = open("/home/obooklage/obooklage@gmail.com/ownCloud.CAP/DEV/Python/WEB-SERVER/LOG.txt","w")

for filename in glob.iglob(root_dir + '**/*.mid', recursive=True):
    tracks, sustain = SystainPedalCheck(filename)
    if tracks<4 and sustain>10:
        print(f"tracks={tracks} sustain={sustain} {filename}")
        f.writelines(filename+"\n")
        f.flush()

f.close()

print("** END")
