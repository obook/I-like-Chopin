#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
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
    configpath = os.path.join(os.path.expanduser("~"), ".config", "i-like-chopin")
    localpath = os.path.join(
        os.path.expanduser("~"), ".local", "share", "i-like-chopin"
    )

    settingsfile = os.path.join(configpath, "i-like-chopin.json")
    defaultmidipath = os.path.join(localpath, "midi")
    serverindextemplate = os.path.join(applicationpath, "template", "index-template.html")

    uipath = os.path.join(applicationpath, "ui")

    config = {
        "InputDevice": "(None)",
        "OutputDevice": "(None)",
        "MidiPath": defaultmidipath,
        "ForceInstrument": False,
        "PianoProgram": 0,
        "Mode": modes["playback"],
        "SustainChannel": 64,  # Sustain/Forte
        "HumanizeChannel": 71,
        "SpeedControlChannel": 76,
        "FilesControlChannel": 77,
        "RtMidiBackend": "",  # Empty, LINUX_ALSA or UNIX_JACK
    }

    def __init__(self):
        self.uuid = uuid.uuid4()
        print(f"Settings {self.uuid} read [{self.settingsfile}]")

        if not os.path.isdir(self.configpath):
            os.makedirs(self.configpath, exist_ok=True)
        if not os.path.isdir(self.defaultmidipath):
            midifiles_path_src = os.path.join(self.applicationpath, "midi")
            try:
                shutil.copytree(midifiles_path_src, self.defaultmidipath)
            except Exception as error:
                print(
                    f"Settings {self.uuid} unable de copy midifiles [{self.defaultmidipath}] {error}"
                )

        self.LoadConfig()

    def __del__(self):
        print(f"Settings {self.uuid} destroyed [{self.settingsfile}]")

    """
    Load/Save settings File
    """

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
            with open(self.settingsfile, "w", newline="\r\n") as f:
                json.dump(self.config, f, indent=4, sort_keys=True, ensure_ascii=False)
                f.close
        except Exception as error:
            print(
                f"Settings {self.uuid} SaveConfig [{self.settingsfile}] ERROR {error}"
            )
            return False
        return True

    """
    Tools functions
    """

    def GetApplicationPath(self):
        return self.applicationpath

    def GetIndexTemplate(self):
        return self.serverindextemplate

    def GetLocalPath(self):
        return self.localpath

    def GetConfigPath(self):
        return self.settingsfile

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

    """
    Only manual editing
    """

    def GetPianoProgram(self):
        return self.GetSetting("PianoProgram", 0)

    def GetServerPort(self):
        return self.GetSetting("ServerPort", 8888)

    def GetSustainChannel(self):
        return self.GetSetting(
            "SustainChannel", 64
        )  # The sustain pedal sends CC 64 127 and CC 64 0 messages on channel 1

    """
    Not ditable
    """
    def GetUIPath(self):
        return self.uipath
