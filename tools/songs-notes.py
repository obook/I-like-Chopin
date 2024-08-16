#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:17:57 2024
@author: obooklage
Try to print notes from midifile
! Channels are from 0 to 15
"""
import os
import time
from mido import MidiFile
from midi_numbers import number_to_note

def ReadMidiSong(file):
    tracks = []
    duration = 0
    total_notes_on = 0
    channels_notes_on = {}
    sustain = 0

    # Tracks Informations
    
    if not os.path.isfile(file):
        print(f"file {file} not found")
        return

    try:
        midi = MidiFile(file)  # , debug=True  # PUT IN MIDI_SONG
    except:
        return False  # Bad Midifile (value > 127 ?)

    for i, track in enumerate(midi.tracks):
        tracks.append(track.name)

    # Notes in selected channels (0-15)
    for msg in MidiFile(file):
        
        if not msg.is_meta:
            # print(f"msg={msg}")
            pass
        
        if msg.is_meta:
            #print(f"meta={msg} type={type(msg)}")
            pass
            #print(f"tempo2bpm()={tempo2bpm()})
        if msg.type == "note_on":
            if msg.velocity and msg.channel == 0:
                total_notes_on += 1
                note, octave = number_to_note(msg.note)
                print(f"{note} {octave+1} {msg.time}")
                time.sleep(msg.time)

midifile = os.path.join(
    os.path.expanduser("~"),
    ".local",
    "share",
    "i-like-chopin",
    "midi",
    "CHOPIN FREDERIC",
    "Fantaisie-Impromptu Opus 66.mid"
)

print("** START")
ReadMidiSong(midifile)
print("** END")
