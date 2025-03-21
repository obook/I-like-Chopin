#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import os
from pathlib import Path, PurePath
import uuid
import random
from midi_modes import modes
from midi_states import states


class ClassMidiSong:
    """Class about midifile informations"""

    __filepath = None
    __duration = 0
    __played = 0  # percent
    __tracks = []
    __channels = {}
    __sustain = 0
    __state = states["unknown"]
    __mode = modes["playback"]
    __uuid = None

    def __init__(self, filepath):
        self.__uuid = uuid.uuid4()
        self.__state = states["unknown"]
        text = ""
        if not os.path.isfile(filepath):
            self.SetState(states["notfound"])
            text = "NOT FOUND"
        self.__filepath = filepath
        print(f"MidiSong {self.__uuid} load [{self.Getfilepath()}] {text}")

    def __del__(self):
        print(f"MidiSong {self.__uuid} destroyed [{self.GetFilename()}]")

    def Getuuid(self):
        return self.__uuid;

    def Getfilepath(self):  # complete path and filename
        return self.__filepath

    def GetParent(self):  # A/B/C/D.mid return C
        return PurePath(self.__filepath).parent.name

    def GetParentShort(self, lenght=None):  # A/B/C/D.mid return C but limit lenght
        parent = PurePath(self.__filepath).parent.name
        if lenght:
            parent = (parent[:lenght] + "..") if len(parent) > lenght else parent
        """
        if parent:
            return parent.split(" ")[0]
        return "None"
        """
        return parent

    def GetFilename(self):  # with extension, eg : toto.mid
        return os.path.basename(self.__filepath)

    def GetName(self):  # without extension, eg : toto
        return Path(self.__filepath).stem

    def GetCleanName(self):  # without extension, eg : toto
        name = self.GetName()
        name = name.replace("_", " ")
        name = name.replace("-", " ")
        return name.upper()

    def GetCleanNameShort(self, lenght=None):
        name = self.GetCleanName()
        if lenght:
            name = (name[:lenght] + "..") if len(name) > lenght else name
        return name

    def GetScore(self):  # parent/score.pdf
        folder = self.GetParent()
        file = self.GetName() + ".pdf"
        return os.path.join(folder, file)

    def SetDuration(self, duration):
        self.__duration = duration  # in minutes

    def GetDuration(self):
        return self.__duration

    def SetPlayed(self, played):
        self.__played = played  # in percent

    def GetPlayed(self):
        return self.__played

    def GetTracks(self, index=None):
        if not index == None and index < len(self.__tracks):
            return self.__tracks[index]
        return self.__tracks

    def SetTracks(self, tracks):
        self.__tracks = tracks

    def SetChannels(self, channels):  # Dictionnary
        self.__channels = channels

    def GetChannels(self):
        return self.__channels

    def SetSustain(self, value):
        self.__sustain = value

    def GetSustain(self):
        return self.__sustain

    def SetState(self, value):  # EG : SetState(states['cueing'])
        self.__state = value

    def GetState(self):
        return self.__state

    def IsState(self, value):  # EG : IsState(states['cueing'])
        if self.__state == value:
            return True
        return False

    # Modes : 'chopin' (wait keyboard) - 'passthrough' (keyboard to synth) - 'player' (autoplay midifile)

    def SetMode(self, value):  # EG : SetMode(modes['passthrough'])
        self.__mode = value

    def GetMode(self):
        return self.__mode

    def IsMode(self, value):  # EG : IsMode(modes['player'])
        if self.__mode == value:
            return True
        return False

    def HumanizeDuration(
        self, duration, value
    ):
        # 0.030 c'est trop ou c'est le max
        delay = random.uniform(-0.03*value/50, 0.03*value/50)  # random.standard_normal(-0.03*value/50, 0.03*value/50) n'existe pas
        if duration+delay < 0:
            delay = 0
        # print(f"HumanizeDuration delta={delay}")
        return delay
