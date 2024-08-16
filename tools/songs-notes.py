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
from rich.console import Console # Console colorisée
from rich.table import Column, Table # Construire une table
from mido import MidiFile
from midi_numbers import number_to_note

applicationpath = os.path.dirname(os.path.realpath(__file__))
logfile = os.path.join(applicationpath,"log.txt")
if os.path.isfile(logfile):
    os.remove(logfile)

def printlog(string):
    f = open(logfile,"a")
    f.write(string)
    f.writelines("\n")
    f.close
    print(string)
    
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
        midi = MidiFile(file, clip=False)  # , debug=True  # PUT IN MIDI_SONG
        #print(type(midi))
    except Exception as error:
        print(f"|!|[{file}] {error}")
        return False  # Bad Midifile (value > 127 ?)
    
    table = Table(title="MIDI")

    for i, track in enumerate(midi.tracks):
        tracks.append(track.name)
        table.add_column(track.name)
                
    #print(f"tracks={tracks}")

    # Notes in selected channels (0-15)
    #for msg in MidiFile(file, clip=False):
    for track in range(len(midi.tracks)):
        printlog(f"----- [{track}] {tracks[track]} -----")
        for msg in midi.tracks[track]:
            
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
                    # printlog(f"{note} {octave+1} {msg.time}")
                    #print(f"--> [{midi.tracks[i]} {note} {octave+1} {msg.time}] ", end="")
                    #time.sleep(msg.time)
                    table.add_row(str(note), str(octave+1), str(msg.time))
                    
    console = Console()
    console.print(table)

midifile = os.path.join(
    os.path.expanduser("~"),
    ".local",
    "share",
    "i-like-chopin",
    "midi",
    "CHOPIN FREDERIC",
    "Fantaisie-Impromptu Opus 66.mid"
)

midifile="/home/obooklage/.local/share/i-like-chopin/midiperso/DVORAK ANTONIN/Slavonic Dance No.10 COURT.mid"

print("** START")
ReadMidiSong(midifile)
print("** END")
