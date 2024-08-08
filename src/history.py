#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import os
import json
import uuid
from pathlib import Path


class ClassHistory:
    uuid = None
    applicationpath = os.path.dirname(os.path.realpath(__file__))
    settingspath = os.path.join(os.path.expanduser("~"), ".config", "i-like-chopin")
    historyfile = os.path.join(settingspath, "i-like-chopin-history.json")
    history = []

    def __init__(self):
        self.uuid = uuid.uuid4()
        self.LoadHistory()
        print(f"History {self.uuid} read [{self.historyfile}]")

    def __del__(self):
        print(f"History {self.uuid} destroyed [{self.historyfile}]")

    # Globals

    def LoadHistory(self):
        try:
            with open(self.historyfile, "r") as f:
                self.history = json.load(f)
                f.close
        except:  # not yet exists
            pass

        # cleanup
        new_history = []
        for i in range(len(self.history)):
            # json do not load null
            try:
                if os.path.isfile(self.history[i]):
                    new_history.append(self.history[i])
            except:
                pass
        self.history = new_history

    def SaveHistory(self):
        try:
            with open(self.historyfile, "w") as f:
                json.dump(self.history, f)
                f.close
        except:
            return False
        return True

    # Midi files
    def AddHistory(self, midifile):
        if not midifile in self.history:
            if len(self.history) > 127:
                self.history.pop(0)  # remove fist
            self.history.append(midifile)
            self.SaveHistory()

    def GetHistory(self):
        """
        Can not : because song 0 is alway last song
        reversed = self.history.copy().reverse() # reverse or not ?
        return reversed
        """
        return self.history

    def GetName(self, index):  # without extension, eg : toto
        if index > len(self.history):
            return ""
        return Path(self.history[index]).stem

    def GetCleanName(self, index):  # without extension, eg : toto
        name = self.GetName(index)
        name = name.replace("_", " ")
        name = name.replace("-", " ")
        return name.upper()
