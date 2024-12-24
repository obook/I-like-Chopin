#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:09:41 2024

@author: obooklage
rename files extension *.MID to *.mid
"""

import glob
import os

folder = os.path.expanduser("~/MIDI")

for filename in glob.iglob(os.path.join(folder, '*.MID')):
    os.rename(filename, filename[:-4] + '.mid')
    print(filename)
