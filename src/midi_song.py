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

states = {
    "notracktoplay": -4,
    "bad": -3,
    "notfound": -2,
    "ended": -1,
    "unknown": 0,
    "cueing": 1,
    "ready": 2,  # wait a first keyboard key
    "playing": 3,
}

modes = {
    "error": -1,
    "unknown": 0,
    "playback": 1,
    "passthrough": 2,
    "player": 3,
    "random": 4,
}


class ClassMidiSong:
    """Class about midifile informations"""

    __filepath = None
    __duration = 0
    __played = 0  # percent
    __tracks = []
    __channels = {}
    __state = states["unknown"]
    __mode = modes["playback"]
    __uuid = uuid.uuid4()

    def __init__(self, filepath):
        self.__state = states["unknown"]
        text = ""
        if not os.path.isfile(filepath):
            self.SetState(states["notfound"])
            text = "NOT FOUND"
        self.__filepath = filepath
        print(f"MidiSong {self.__uuid} load [{self.Getfilepath()}] {text}")

    def __del__(self):
        print(f"MidiSong {self.__uuid} destroyed [{self.GetFilename()}]")

    def Getfilepath(self):  # complete path and filename
        return self.__filepath

    def GetParent(self):  # A/B/C/D.mid return C
        return PurePath(self.__filepath).parent.name

    def GetParentShort(self):  # A/B/C/D.mid return C
        parent = PurePath(self.__filepath).parent.name
        if parent:
            return parent.split(" ")[0]
        return "None"

    def GetFilename(self):  # with extension, eg : toto.mid
        return os.path.basename(self.__filepath)

    def GetName(self):  # without extension, eg : toto
        return Path(self.__filepath).stem

    def GetCleanName(self):  # without extension, eg : toto
        name = self.GetName()
        name = name.replace("_", " ")
        name = name.replace("-", " ")
        return name.upper()

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
        self, duration, key
    ):  # key=0-127 duration=original note duration
        delay = random.random() * key / 1024
        if random.random() < 0.6:  # 60% fastest
            delay = -1 * delay
        if duration + delay < 0:
            delay = -1 * delay
            # A revoir ..
        if duration + delay < 0:
            return 0
        return 0  # buggy delay # for calculate new_time = msg.time+delay
