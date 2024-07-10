#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import json

config = {"InputDeviceId": 0, "OutputDeviceId": 0, "Midifile":"", "MidiPath":"./midi"}

settingsfile = 'i-like-chopin.json'

def LoadConfig():
    global config
    
    try:
        with open(settingsfile, 'r') as f:
            config = json.load(f)
    except:
        SaveConfig()
        
    return True

def SaveConfig():
    with open(settingsfile, 'w') as f:
        json.dump(config, f)
    return True

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
        config['MidiPath'] = "./midi"
        SaveConfig()
    return config['MidiPath']

