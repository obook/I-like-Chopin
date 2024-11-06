#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:17:57 2024
@author: obooklage
Tool for search nice midifiles regarding tracks and sustain pedal
"""

from pathlib import Path
from mido import MidiFile
import matplotlib.pyplot as plt


def scan_notes(file):
    ''' read all notes on channel 0 '''
    notes = []
    times = []
    time = 0
    for msg in MidiFile(file):
        if msg.type == "note_on" and msg.channel == 0:
            time += msg.time
            times.append(time)
            notes.append(msg.note)
    return [times, notes]


def graph_notes(file, composer):
    ''' plot notes '''
    name = Path(file).stem
    times, notes = scan_notes(file)
    plt.figure().set_figwidth(30)
    plt.plot(times, notes, 'k.', antialiased=False)
    plt.legend([composer+" " + name])
    plt.grid(visible=True)
    plt.show()
