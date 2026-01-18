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
    midifiles_raw_random = [] # All files list
    midifiles_count = 0
    windows_forbiden = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*", "“", "”"]  # removed : , "'"

    def __init__(self):
        self.uuid = uuid.uuid4()
        print(f"MidiFiles {self.uuid} created")

    def __del__(self):
        print(f"MidiFiles {self.uuid} destroyed")

    def ScanFiles(self, defaultmidipath):

        self.defaultmidipath = defaultmidipath
        for file in sorted(
            glob.glob(
                os.path.join(self.defaultmidipath, "**", "*.mid"),
                recursive=True,
            )
        ):
            path = pathlib.PurePath(file)

            try: # Windows filenames do not accept " and some UTF8 chars

                # Check windows folder name compatibility
                if len([e for e in self.windows_forbiden if e in path.parent.name]):
                    print(f"MidiFiles {self.uuid} ==> WARNING path name not windows compatible : {path.parent.name}")

                if not any(
                    path.parent.name in keys for keys in self.midifiles_dict
                ):  # not in dictionnary
                    self.midifiles_dict[path.parent.name] = [file]
                else:  # in dictionnary
                    list = self.midifiles_dict[path.parent.name]

                    # Check windows folder name compatibility
                    filename = os.path.basename(file)
                    check_windows = [e for e in self.windows_forbiden if e in filename]
                    if len(check_windows):
                        print(f"MidiFiles {self.uuid} ==> WARNING file name not windows compatible in {path.parent.name} : {filename} {check_windows}")

                    list.append(file)
                self.midifiles_raw.append(file)
                self.midifiles_count += 1
            except Exception as error:
                 # print(f"|!| MidiFiles {self.uuid} BAD NAME or FILENAME : {error}")
                pass

            # Random
        self.MakeRandomPlaylist()

        print(
            f"MidiFiles {self.uuid} {self.midifiles_count} files in [{self.defaultmidipath}]"
        )
        return self.midifiles_dict

    def MakeRandomPlaylist(self):
        self.midifiles_raw_random = self.midifiles_raw.copy()
        random.shuffle(self.midifiles_raw_random)

    def GetRandomSong(self):
        next_random = ""

        if len(self.midifiles_raw_random):
            next_random = self.midifiles_raw_random.pop()
        else:
            self.MakeRandomPlaylist()

        return next_random

    def GetFiles(self):
        return self.midifiles_dict
