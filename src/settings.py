#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import json
import os

'''
NOTICE
------
settings file 'i-like-chopin.json' is located to ~/.config
midifiles folder 'midi' is located to ~/.local/share/i-like-chopin
'''

settingsfile = os.path.join(os.path.expanduser("~"), ".config", "i-like-chopin.json")
defaultmidipath =os.path.join( os.path.expanduser("~"), ".local","share","i-like-chopin","midi")
config = {"InputDeviceId": 0, "OutputDeviceId": 0, "Midifile":"", "MidiPath":None}

def LoadConfig():
    global config

    print(f"Loading settings = [{settingsfile}]")
    
    try:
        with open(settingsfile, 'r') as f:
            config = json.load(f)
    except:
        path = os.path.join(os.path.expanduser("~"), ".config")
        os.makedirs(path, exist_ok=True)
        SaveConfig()
        
    return True

def SaveConfig():
    try:
        with open(settingsfile, 'w') as f:
            json.dump(config, f)
        return True
    except:
        print(f"ERROR write settings = [{settingsfile}]")
    return False

def GetInputDeviceId():
    LoadConfig()
    return config['InputDeviceId']

def SaveInputDeviceId(n):
    config['InputDeviceId'] = n
    return SaveConfig()

def GetOutputDeviceId():
    LoadConfig()
    return config['OutputDeviceId']

def SaveOutputDeviceId(n):
    config['OutputDeviceId'] = n
    return SaveConfig()

def GetMidifileId():
    LoadConfig()
    return config['Midifile']

def SaveMidifileId(n):
    config['Midifile'] = n
    return SaveConfig()

def GetMidiPath():
    LoadConfig()
    if not config.get('MidiPath'):
        os.makedirs(defaultmidipath, exist_ok=True)
        WarningNoMidifile()
        config['MidiPath'] = defaultmidipath
        SaveConfig()
    return config['MidiPath']

def GetConfigPath():
    return settingsfile

def WarningNoMidifile():
    print(f"WARNING : Copy midifiles to {config['MidiPath']}")

