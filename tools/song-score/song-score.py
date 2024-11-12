#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 19:55:26 2024
@author: obooklage

WARNING : require musescore3

$ pip install music21
$ sudo apt install musescore3
"""
import os
import shutil
from music21 import converter

current_dir = os.path.dirname(os.path.abspath(__file__))

parsed = converter.parse('midi.mid')  # stream.Score object

# midi out, writed in current path
parsed.write('midi', fp='fileout.mid')

# xml
tempfilename = parsed.write('musicxml.xml')  # generally in /tmp/music21
shutil.copyfile(tempfilename, os.path.join(current_dir, 'fileout.xml'))

# png
tempfilename = parsed.write('musicxml.png')  # generally in /tmp/music21
shutil.copyfile(tempfilename, os.path.join(current_dir, 'fileout.png'))
