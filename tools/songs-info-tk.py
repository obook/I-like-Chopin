#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:17:57 2024
@author: obooklage
Tool for checking midifiles : only channel 1, readeable
! Channels are from 0 to 15
"""
import os
import glob
import pathlib
from mido import MidiFile
from collections import namedtuple


import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


def open_midifile():
    """Open a file for informations."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.mid"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    '''
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    '''
    window.title(f"Mdifile Informations - {filepath}")


def save_file():
    """Save the current text as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")


window = tk.Tk()
window.title("Mdifile Informations")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(frm_buttons, text="Open", command=open_midifile)
btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()


'''
indexes = {"tracks": 0, "duration": 1, "notes_on_channels": 2, "sustain":3}
Song = namedtuple("Song", ["tracks", "duration", "notes_on_channels","sustain"])


def MidiSongInfo(file):
    tracks = []
    duration = 0
    total_notes_on = 0
    channels_notes_on = {}
    sustain = 0

    # Tracks Informations

    try:
        midi = MidiFile(file)  # , debug=True  # PUT IN MIDI_SONG
    except:
        return False  # Bad Midifile (value > 127 ?)

    duration = midi.length / 60
    for i, track in enumerate(midi.tracks):
        tracks.append(track.name)

    # Notes in selected channels (0-15)
    for msg in MidiFile(file):
        if msg.type == "note_on":
            if msg.velocity:
                total_notes_on += 1
                key = int(msg.channel)
                if not key in channels_notes_on.keys():
                    channels_notes_on[int(key)] = 0
                channels_notes_on[int(key)] += 1
        if msg.type == "control_change":
            if msg.value == 64: # The sustain pedal sends CC 64 127 and CC 64 0 messages on channel 1
                sustain +=1

    channels_notes_on = dict(
        sorted(channels_notes_on.items())
    )
    S = Song(tracks, duration, channels_notes_on, sustain)

    return S


def ScanFiles(midipath):
    midifiles_dict = {}
    midifiles_raw = []
    midifiles_count = 0

    for file in sorted(
        glob.glob(
            os.path.join(midipath, "**", "*.mid"),
            recursive=True,
        )
    ):
        path = pathlib.PurePath(file)

        if not any(
            path.parent.name in keys for keys in midifiles_dict
        ):  # not in dictionnary
            midifiles_dict[path.parent.name] = [file]
        else:  # in dictionnary
            list = midifiles_dict[path.parent.name]
            list.append(file)
        midifiles_raw.append(file)
        midifiles_count += 1

    return midifiles_dict  # , midifiles_raw, midifiles_count


folder = os.path.join(
    os.path.expanduser("~"), ".local", "share", "i-like-chopin", "midiperso"
)

songs = ScanFiles(folder)

print("** START")

for artist in songs.keys():
    print(f"Process {artist}\n-------------")
    midifiles = songs[artist]
    for midifile in sorted(midifiles, key=lambda s: s.lower()):
        midiname = pathlib.Path(midifile).stem
        Info = MidiSongInfo(midifile)
        if Info:
            channels = Info[indexes["notes_on_channels"]]  # dictionnary
            if int(0) in channels.keys():
                # remove key '0'
                save = channels.copy()
                del channels[0]
                if channels:  # other channels actives
                    print(f"MULTICHANNELS [{midiname}] {save}")

            else:
                print(f"WARNING no note channel 0 [{midifile}]")

            if not Info[indexes["sustain"]]:
                print(f"NO SUSTAIN [{midiname}] {save}")
        else:
            print(f"ERROR reading [{midifile}] bad file?")

print("** END")
'''