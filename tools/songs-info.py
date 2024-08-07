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

indexes = {"tracks": 0, "duration": 1, "notes_on_channels": 2}
Song = namedtuple("Song", ["tracks", "duration", "notes_on_channels"])


def MidiSongInfo(file):
    tracks = []
    duration = 0
    total_notes_on = 0
    channels_notes_on = {}

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
            total_notes_on += 1
            key = int(msg.channel)
            if not key in channels_notes_on.keys():
                channels_notes_on[int(key)] = 0
            channels_notes_on[int(key)] += 1

    channels_notes_on = dict(
        sorted(channels_notes_on.items())
    )
    S = Song(tracks, duration, channels_notes_on)

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
        else:
            print(f"ERROR reading [{midifile}] bad file?")

print("** END")
