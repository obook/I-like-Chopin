# This Python file uses the following encoding: utf-8

import os
from pathlib import Path

# os.path.join(self.settings.GetMidiPath(),self.Midifile)

class ClassMidiSong:
    filepath = None
    duration = 0
    tracks = []
    active = False

    def __init__(self):
        pass

    def Setfilepath(self, filepath):
        self.filepath = filepath

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
