#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage

TODO : mutiples calls for nothing..

"""

import json
import os
import shutil
import uuid
from midi_song import modes


class ClassSettings:
    """Class for recall and store preferences and settings"""

    uuid = None
    applicationpath = os.path.dirname(os.path.realpath(__file__))
    settingspath = os.path.join(os.path.expanduser("~"), ".config")
    settingsfile = os.path.join(settingspath, "i-like-chopin.json")
    defaultmidipath = os.path.join(
        os.path.expanduser("~"), ".local", "share", "i-like-chopin", "midi"
    )
    serverindextemplate = os.path.join(
        applicationpath, "template", "index-template.html"
    )
    config = {
        "InputDevice": "(None)",
        "OutputDevice": "(None)",
        "MidiPath": defaultmidipath,
        "ForceInstrument": False,
        "PianoProgram": 0,
        "Mode": modes["playback"],
        "SustainChannel":64 # Sustain/Forte
    }

    def __init__(self):
        self.uuid = uuid.uuid4()
        print(f"Settings {self.uuid} read [{self.settingsfile}]")
        if not os.path.isdir(self.settingspath):
            os.makedirs(self.settingspath, exist_ok=True)
        if not os.path.isdir(self.defaultmidipath):
            midifiles_path_src = os.path.join(self.application_path, "midi")
            try:
                shutil.copytree(midifiles_path_src, self.defaultmidipath)
            except:
                print(
                    f"Settings {self.uuid} unable de copy midifiles [{self.defaultmidipath}]"
                )
        self.LoadConfig()

    def __del__(self):
        print(f"Settings {self.uuid} destroyed [{self.settingsfile}]")

    def LoadConfig(self):
        try:
            with open(self.settingsfile, "r") as f:
                self.config = json.load(f)
                f.close
        except:
            pass

        return True

    def SaveConfig(self):
        try:
            with open(self.settingsfile, "w", newline='\r\n') as f:
                json.dump(self.config, f, indent=4, sort_keys=True, ensure_ascii=False)
                f.close
        except:
            return False
        return True

    def GetConfigPath(self):
        return self.settingsfile

    """
    Tools functions
    """

    def GetApplicationPath(self):
        return self.applicationpath

    def GetIndexTemplate(self):
        return self.serverindextemplate

    """
    Globals settings functions
    """

    def GetSetting(self, key, default=None):
        self.LoadConfig()
        if not key in self.config:
            self.config[key] = default
            self.SaveConfig()
        return self.config[key]

    def SetSetting(self, key, value):
        self.config[key] = value
        return self.SaveConfig()

    """
    Individuals functions
    """

    def GetInputDevice(self):
        return self.GetSetting("InputDevice", "(None)")

    def SaveInputDevice(self, value):
        return self.SetSetting("InputDevice", value)

    def GetOutputDevice(self):
        return self.GetSetting("OutputDevice", "(None)")

    def SaveOutputDevice(self, value):
        return self.SetSetting("OutputDevice", value)

    def GetMidifile(self):
        return self.GetSetting("MidiSong", "(None)")

    def SaveMidifile(self, value):
        return self.SetSetting("MidiSong", value)

    def GetMidiPath(self):
        return self.GetSetting("MidiPath", self.defaultmidipath)

    def GetForceIntrument(self):
        return self.GetSetting("ForceInstrument", False)

    def SaveForceIntrument(self, value):
        return self.SetSetting("ForceInstrument", value)

    def GetPianoProgram(self):
        return self.GetSetting("PianoProgram", 0)

    def SavePianoProgram(self, value):  # not used
        return self.SetSetting("PianoProgram", value)

    def GetMode(self):
        return self.GetSetting("Mode", modes["playback"])

    def IsMode(self, mode):  # EG IsMode(modes['playback'])
        if self.GetMode() == mode:
            return True
        return False

    def SaveMode(self, value):
        return self.SetSetting("Mode", value)

    def GetServerPort(self):
        return self.GetSetting("ServerPort", 8888)

    def GetSustainChannel(self):
        return self.GetSetting("SustainChannel", 61)


