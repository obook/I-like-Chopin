#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 19:55:26 2024
@author: obooklage
@Desc: convert midifiles from a folder to score (pdf)
WARNING: require musescore3
$ sudo apt install musescore3
@infos : Rosegarden and musescore3 do not save title in MetaMessage (see bellow)
"""

import os
import glob
from pathlib import Path
from subprocess import call
from datetime import datetime
from mido import MidiFile, MidiTrack


def MidiSongTitle(file):
    ''' Search MetaMessage text begin = @T , is tiles of song '''
    counter = 0
    for msg in MidiFile(file):
        ''' First is the main Tltle, second the composer, third as remarks '''
        if msg.is_meta:
            if msg.type == 'text':
                text = str(msg.text)
                if text.find("@T") == 0:
                    print(f"TEXT : {msg.text[2:]}")
                    counter += 1

    if not counter:
        print("NO TITLE !")
    return counter


def AppendTitle(file):
    # do not works yet
    pass
    '''
    print(f"Append tile to {file}")
    mid = MidiFile(file)
    # initialize with the right tempo
    new_mid = MidiFile(ticks_per_beat=mid.ticks_per_beat)
    new_track = MidiTrack()
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            new_track.append(msg)
    new_mid.tracks.append(new_track)
    new_mid.save('/home/obooklage/MIDI/ENFANTS CHILD/Alouette-new.mid')
    '''


def MakeScore(filename):

    # file infos
    filepath = os.path.dirname(filename)
    filename_without_ext = Path(filename).stem
    filename_pdf = os.path.join(filepath, filename_without_ext + '.pdf')
    # filename_png = os.path.join(filepath, filename_without_ext + '.png')
    call(['mscore3', filename, "-o", filename_pdf])


root_dir = os.path.expanduser("~/MIDI")
files = glob.glob(root_dir + '/**/*.mid', recursive=True)
print(f"Make score for {len(files)} files in {root_dir}")

maxi = len(files)
index = 1
for filename in files:
    now = datetime.now()
    clock = now.strftime("%H:%M:%S")
    print(f"{index}/{maxi} {clock}")
    MakeScore(filename)
    index += 1

'''
file = '/home/obooklage/MIDI/ENFANTS CHILD/Alouette.mid'
if not MidiSongTitle(file):
    AppendTitle(file)
MakeScore(file)
'''