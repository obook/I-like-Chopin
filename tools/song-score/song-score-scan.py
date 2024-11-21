#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 19:55:26 2024
@author: obooklage
@Desc: convert midifiles from a folder to score (pdf)
WARNING: require musescore3
$ sudo apt install musescore3
"""

import os
import glob
from pathlib import Path
from subprocess import call


def MakeScore(filename):

    # file infos
    filepath = os.path.dirname(filename)
    filename_without_ext = Path(filename).stem
    filename_pdf = os.path.join(filepath, filename_without_ext + '.pdf')
    # filename_png = os.path.join(filepath, filename_without_ext + '.png')
    call(['mscore3', filename, "-o", filename_pdf])


root_dir = os.path.expanduser("~/MIDI/ABBA")
files = glob.glob(root_dir + '/**/*.mid', recursive=True)
print(f"Make score for {len(files)} files in {root_dir}")

maxi = len(files)
index = 1
for filename in files:
    print(f"{index}/{maxi}")
    MakeScore(filename)
    index += 1
