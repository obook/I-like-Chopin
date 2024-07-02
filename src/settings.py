#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# if __name__ == "__main__":
#     pass

"""
Created on Wed Jun  5 18:19:14 2024

@author: obooklage
"""

# -*- coding: utf-8 -*-
"""
Created on Jun 2 2024
Projet NSI 2023-2024 Sainte-Marie Bastide/Bordeaux
@author: obook
"""

import json

config = {"InputDeviceId": 0, "OutputDeviceId": 0, "Midifile":""}

settingsfile = 'dummy_piano_player.json'

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

def GetmidifileId():
    LoadConfig()
    return config['Midifile']

def SavemidifileId(n):
    config['Midifile'] = n
    return SaveConfig()

    
