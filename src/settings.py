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
    config = {
    "InputDevice": '(None)',
    "OutputDevice": '(None)',
    "Midifile":"(None)",
    "MidiPath":defaultmidipath,
    "PrintTerm":False,
    "ForceInstrument":False,
    "PianoProgram":0}

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
                f.close
        except:
            pass

        return True

    def SaveConfig(self):
        try:
            with open(self.settingsfile, 'w') as f:
                json.dump(self.config, f)
                f.close
        except:
            return False
        return True

    def GetConfigPath(self):
        return self.settingsfile

    '''
    Globals functions
    '''

    def GetSetting(self,key,default=None):
        self.LoadConfig()
        if not key in self.config:
            self.config[key] = default
            self.SaveConfig()
        return self.config[key]

    def SetSetting(self,key,value):
        self.config[key] = value
        return self.SaveConfig()

    '''
    Individuals functions
    '''

    def GetInputDevice(self):
        return self.GetSetting('InputDevice','(None)')

    def SaveInputDevice(self,value):
        return self.SetSetting('InputDevice', value)

    def GetOutputDevice(self):
        return self.GetSetting('OutputDevice','(None)')

    def SaveOutputDevice(self,value):
        return self.SetSetting('OutputDevice', value)

    def GetMidifile(self):
        return self.GetSetting('Midifile','(None)')

    def SaveMidifile(self,value):
        return self.SetSetting('Midifile', value)

    def GetMidiPath(self):
         return self.GetSetting('MidiPath',self.defaultmidipath)

    def GetPrintTerm(self):
        return self.GetSetting('PrintTerm',False)

    def SavePrintTerm(self,value):
        return self.SetSetting('PrintTerm', value)

    def GetForceIntrument(self):
        return self.GetSetting('ForceInstrument',False)

    def SaveForceIntrument(self,value):
        return self.SetSetting('ForceInstrument', value)

    def GetPianoProgram(self):
        return self.GetSetting('PianoProgram',0)

    def SavePianoProgram(self,value): # not used
        return self.SetSetting('PianoProgram', value)
