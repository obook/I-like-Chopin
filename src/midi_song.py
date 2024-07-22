# This Python file uses the following encoding: utf-8

import os
from pathlib import Path
import uuid

class ClassMidiSong:
    filepath = None
    duration = 0
    played = 0 #percent
    tracks = []
    active = False
    uuid = None
    ready = False # wait first key on keyboard

    def __init__(self, filepath):
        self.uuid = uuid.uuid4()
        self.filepath = filepath
        print(f"MidiSong {self.uuid} created [{self.GetFilename()}]")

    def __del__(self):
        print(f"MidiSong {self.uuid} destroyed [{self.GetFilename()}]")

    def Getfilepath(self): # complete path and filename
        return self.filepath

    def GetFilename(self): # with extension, eg : toto.mid
        return os.path.basename(self.filepath)

    def GetName(self): # without extension, eg : toto
        return Path(self.filepath).stem

    def SetDuration(self, duration):
        self.duration = duration # in minutes

    def GetDuration(self):
        return self.duration

    def SetTracks(self,tracks):
        self.tracks = tracks.copy()

    def GetTracks(self):
        return self.tracks

    def SetActive(self,value):
        self.active = value

    def Active(self):
        return self.active
