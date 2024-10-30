#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:17:57 2024
@author: obooklage
Tool for search nice midifiles regarding tracks and sustain pedal
"""

import os
import sys
from mido import MidiFile
import matplotlib.pyplot as plt
from pathlib import Path


def ScanNotes(file):
    notes = []
    times = []
    time = 0
    for msg in MidiFile(file):
        if msg.type == "note_on" and msg.channel == 0:
            time += msg.time
            times.append(time)
            notes.append(msg.note)
    return [times, notes]


# if __name__ == "__main__":

composer = "none"
if len(sys.argv) < 2:  # pas de paramètres
    print("MODE DEMO - Passer le fichier en paramètre")
    midi_dir = os.path.expanduser("~/MIDI")
    composer = "BACH JOHANN SEBASTIAN"
    file = "Duet in E Minor, BWV 802.mid"
    midifile = os.path.join(midi_dir, composer, file)
else:
    midifile = sys.argv[1]

name = Path(midifile).stem

times, notes = ScanNotes(midifile)
plt.figure().set_figwidth(30)
plt.plot(times, notes, 'k.', antialiased=False)
plt.legend([composer+" " + name])
plt.grid(visible=True)
plt.show()
