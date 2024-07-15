#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import json
import os

class ClassSettings:

    config = {"InputDevice": '(None)', "OutputDevice": '(None)', "Midifile":"(None)", "MidiPath":None}
    settingsfile = os.path.expanduser("~") + "/.config/chopin-lab.json"
    defaultmidipath = os.path.expanduser("~") + "/.local/share/chopin-lab/midi"

    def __init__(self):
        print(f"Settings file = [{self.settingsfile}]")

    def LoadConfig(self):
        try:
            with open(self.settingsfile, 'r') as f:
                self.config = json.load(f)
        except:
            self.SaveConfig()
        return True

    def SaveConfig(self):
        with open(self.settingsfile, 'w') as f:
            json.dump(self.config, f)
        return True

    def GetInputDevice(self):
        self.LoadConfig()
        return self.config['InputDevice']

    def SaveInputDevice(self,name):
        self.config['InputDevice'] = name
        return self.SaveConfig()

    def GetOutputDevice(self):
        self.LoadConfig()
        return self.config['OutputDevice']

    def SaveOutputDevice(self,name):
        self.config['OutputDevice'] = name
        return self.SaveConfig()
    '''
    def GetMidifileId(self):
        self.LoadConfig()
        return self.config['MidifileId']

    def SaveMidifileId(self,id):
        self.config['MidifileId'] = id
        return self.SaveConfig()
    '''
    def GetMidifile(self):
        self.LoadConfig()
        return self.config['Midifile']

    def SaveMidifile(self,name):
        self.config['Midifile'] = name
        return self.SaveConfig()

    def GetMidiPath(self):
        self.LoadConfig()
        if not self.config.get('MidiPath'):
            os.makedirs(self.defaultmidipath, exist_ok=True)
            self.WarningNoMidifile()
            self.config['MidiPath'] = self.defaultmidipath
            self.SaveConfig()
        return self.config['MidiPath']

    def WarningNoMidifile(self):
        print(f"WARNING : Copy midifiles to {self.config['MidiPath']}")


