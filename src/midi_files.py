#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import uuid
import os
import glob
import pathlib
import random


class ClassMidiFiles:

    uuid = None
    defaultmidipath = None
    midifiles_dict = {} # files by artist key
    midifiles_raw = [] # All files list
    midifiles_count = 0

    def __init__(self):
        self.uuid = uuid.uuid4()
        print(f"MidiFiles {self.uuid} created")

    def __del__(self):
        print(f"MidiFiles {self.uuid} destroyed")

    def ScanFiles(self, defaultmidipath):
        self.defaultmidipath = defaultmidipath
        '''
        for file in sorted(
            glob.glob(
                os.path.join(self.defaultmidipath, "**", "*.mid"),
                recursive=True,
            )
        ):
            path = pathlib.PurePath(file)
            if not any(
                path.parent.name in keys for keys in self.midifiles_dict
            ):  # not in dictionnary
                self.midifiles_dict[path.parent.name] = [file]
            else:  # in dictionnary
                list = self.midifiles_dict[path.parent.name]
                list.append(file)
            self.midifiles_raw.append(file)
            self.midifiles_count += 1
            '''

        print(
            f"MidiFiles {self.uuid} {self.midifiles_count} files in [{self.defaultmidipath}]"
        )
        return self.midifiles_dict

    def GetRandomSong(self):
        return self.midifiles_raw[random.randrange(len(self.midifiles_raw))]

    def GetFiles(self):
        return self.midifiles_dict
