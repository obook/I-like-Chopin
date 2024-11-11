#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:17:57 2024
@author: obooklage
Tool for search nice midifiles regarding tracks and sustain pedal
"""

import os
import glob
import os
from mido import MidiFile


def SystainPedalCheck(file):
    sustain = 0
    tracks = 0
    duration = 0

    try:
        # Tracks
        midi = MidiFile(file)
        duration = midi.length / 60
        for i, track in enumerate(midi.tracks):
            tracks += 1

        for msg in MidiFile(file):
            if msg.type == "control_change":
                # The sustain pedal sends CC 64 127
                # and CC 64 0 messages on channel 1
                if msg.control == 64:
                    sustain += 1
    except Exception as error:
        print(f"|!| CAN NOT READ {file} {error}")
        sustain = 0
        tracks = 0
        pass

    return duration, tracks, sustain


print("** START")

root_dir = os.path.expanduser("~/MIDI")
logfile = os.path.join(root_dir, "MIDILIST.csv")
f = open(logfile, "w")

files = glob.glob(root_dir + '/**/*.mid', recursive=True)
print(f"Scan for {len(files)} files in {root_dir}")

index = 1
for filename in files:
    duration, tracks, sustain = SystainPedalCheck(filename)
    if tracks <= 4 and sustain > 10:
        print(f"tracks={tracks} sustain={sustain} {filename}")
        f.write(f"{index};{filename};{round(duration)};{tracks};{sustain}"+"\n")
        index += 1
        f.flush()

f.close()

print("** END")
