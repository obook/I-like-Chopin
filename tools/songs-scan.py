#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:17:57 2024
@author: obooklage
Tool for search nice midifiles regarding tracks and sustain pedal
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
            tracks += 1

        for msg in MidiFile(file):
            if msg.type == "control_change":
                # The sustain pedal sends CC 64 127
                # and CC 64 0 messages on channel 1
                if msg.value == 64:
                    sustain += 1
    except Exception as error:
        print(f"|!| CAN NOT READ {file} {error}")
        sustain = 0
        tracks = 0
        pass

    return tracks, sustain


print("** START")

root_dir = "~/MUSIQUE/"

f = open("~/MUSIQUE/LOG.txt", "w")

for filename in glob.iglob(root_dir + '**/*.mid', recursive=True):
    tracks, sustain = SystainPedalCheck(filename)
    if tracks < 4 and sustain > 10:
        print(f"tracks={tracks} sustain={sustain} {filename}")
        f.writelines(filename+"\n")
        f.flush()

f.close()

print("** END")
