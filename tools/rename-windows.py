#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 16:53:29 2025
@author: obooklage
Scan files, check Windows filename compatibility, change if required.
"""
import os
import glob

path = os.path.expanduser("~/MIDI")
windows_forbiden = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*", "“", "”"]

for file in sorted(
    glob.glob(
        os.path.join(path, "**", "*.*"), recursive=True,
    )
):
    filename = os.path.basename(file)
    filepath = os.path.dirname(file)
    forbiden = [e for e in windows_forbiden if e in filename]
    if len(forbiden):
        newfilename = filename.translate({ord(x): '' for x in windows_forbiden})
        newfile = os.path.join(filepath, newfilename)
        print(f"RENAME : from {file} to {newfile}")
        os.rename(file, newfile)
