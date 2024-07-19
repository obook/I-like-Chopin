#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import json
import os
import shutil

class ClassSettings:

    settingspath = os.path.join(os.path.expanduser("~"), ".config")
    settingsfile =  os.path.join(settingspath, "i-like-chopin.json")
    defaultmidipath = os.path.join(os.path.expanduser("~"), ".local","share","i-like-chopin","midi")
    config = {"InputDevice": '(None)', "OutputDevice": '(None)', "Midifile":"(None)", "MidiPath":defaultmidipath,"PrintTerm":False}

    def __init__(self):

        self.application_path = os.path.dirname(os.path.realpath(__file__))

        if not os.path.isdir(self.settingspath):
            os.makedirs(self.settingspath, exist_ok=True)
        if not os.path.isdir(self.defaultmidipath):
            midifiles_path_src = os.path.join(self.application_path, "midi")
            try:
                shutil.copytree( midifiles_path_src, self.defaultmidipath )
            except:
                pass

    def LoadConfig(self):
        try:
            with open(self.settingsfile, 'r') as f:
                self.config = json.load(f)
        except:
            self.SaveConfig()

        #if old version
        if not 'InputDevice' in self.config:
            print('ClassSettings->conversion')
            self.config['InputDevice'] = '(None)'
            self.config['OutputDevice'] = '(None)'
            self.config['Midifile'] = '(None)'
            self.config['MidiPath'] = self.defaultmidipath
        return True

    def SaveConfig(self):
        with open(self.settingsfile, 'w') as f:
            json.dump(self.config, f)
        return True

    def GetInputDevice(self):
        self.LoadConfig()
        if not self.config.get('InputDevice'):
            self.config['InputDevice'] = '(None)'
        return self.config['InputDevice']

    def SaveInputDevice(self,name):
        self.config['InputDevice'] = name
        return self.SaveConfig()

    def GetOutputDevice(self):
        self.LoadConfig()
        if not self.config.get('OutputDevice'):
            self.config['OutputDevice'] = '(None)'
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
        if not self.config.get('Midifile'):
            self.config['Midifile'] = '(None)'
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

    def GetConfigPath(self):
        return self.settingsfile

    def GetPrintTerm(self):
        self.LoadConfig()
        if not self.config.get('PrintTerm'):
            self.config['PrintTerm'] = False
        return self.config['PrintTerm']

    def SetPrintTerm(self,status):
        self.config['PrintTerm'] = status
        return self.SaveConfig()

    def GetForceIntrument(self):
        self.LoadConfig()
        if not self.config.get('ForceInstrument'):
            self.config['ForceInstrument'] = False
        return self.config['ForceInstrument']

    def SetForceIntrument(self,status):
        self.config['ForceInstrument'] = status
        return self.SaveConfig()

    def WarningNoMidifile(self):
        print(f"WARNING : Copy midifiles to {self.config['MidiPath']}")


