#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import os
import uuid
from pathlib import Path, PurePath
import json

'''
Sample :

playlist = [
        {
        "artist": "ABBA",
        "title": "CHIQUITITA",
        "path": "/home/obooklage/obooklage@gmail.com/ownCloud.CAP/MUSIQUE/midiperso/ABBA/Chiquitita.mid"
        },
        {
        "artist": "BEETHOVEN LUDWIG VAN",
        "title": "32 VARIATIONS",
        "path": "/home/obooklage/obooklage@gmail.com/ownCloud.CAP/MUSIQUE/midiperso/BEETHOVEN LUDWIG VAN/32 Variations on a theme.mid"
        },
        {
        "artist": "CHAMINADE CÉCILE",
        "title": "CALIRRO OP.37",
        "path": "/home/obooklage/obooklage@gmail.com/ownCloud.CAP/MUSIQUE/midiperso/CHAMINADE CÉCILE/Calirro Op.37 No.4.mid"
        }
]
'''
class ClassPlaylist():

    uuid = None
    applicationpath = os.path.dirname(os.path.realpath(__file__))
    settingspath = os.path.join(os.path.expanduser("~"), ".config", "i-like-chopin")
    playlistfile = os.path.join(settingspath, "i-like-chopin-playlist.json")
    playlist = [] # All files list
    playlist_count = 0
    playlist_position = -1
    pParent = None

    def __init__(self, parent):
        self.uuid = uuid.uuid4()
        self.pParent = parent
        self.LoadPlaylist()
        print(f"ClassPlaylist {self.uuid} read [{self.playlistfile}]")

    def __del__(self):
        self.SavePlaylist()
        print(f"ClassPlaylist {self.uuid} destroyed [{self.playlistfile}]")

    def GetFilename(self):
        return self.playlistfile

    def LoadPlaylist(self):
        try:
            with open(self.playlistfile, "r") as f:
                self.playlist = json.load(f)
                f.close

            # Check is file exists
            for dic in self.playlist:
                artist = dic['artist']
                filepath = dic['path']
                if not os.path.isfile(filepath):
                    self.RemovePlaylist(filepath)

        except Exception as error:  # not yet exists
            print(f"ClassPlaylist {self.uuid} exception {error}")

    def SavePlaylist(self):
        try:
            with open(self.playlistfile, "w", encoding="utf-8", newline='\r\n') as outfile:
                json.dump(self.playlist, outfile, indent=4, sort_keys=True, ensure_ascii=False)
                outfile.close
        except:
            return False
        return True

    def GetPlayList(self):
        return self.playlist

    def GetNextFavorite(self):
        if len(self.playlist) and self.playlist_position < len(self.playlist)-1 :
            self.playlist_position += 1
            # print(f"--> DEBUG GetNextFavorite", self.playlist[self.playlist_position]['path'])
            self.pParent.MidifileChange(self.playlist[self.playlist_position]['path'])

    def GetPreviousFavorite(self):
        if len(self.playlist) and self.playlist_position > 0 :
            self.playlist_position -= 1
            # print(f"--> DEBUG GetPreviousFavorite", self.playlist[self.playlist_position]['path'])
            self.pParent.MidifileChange(self.playlist[self.playlist_position]['path'])

    # Midi files
    def AddPlaylist(self, midifile): # no quality for instance
        artist = PurePath(midifile).parent.name  # parent folder
        name = Path(midifile).stem
        name = name.replace("_", " ")
        name = name.replace("-", " ").upper() # name
        dic = {'artist':artist, 'title': name, 'path':midifile}

        self.playlist.append(dic)
        if len(self.playlist) > 20:  # limit to 20 titles
            self.playlist.pop(0)
        self.SavePlaylist()

    def RemovePlaylist(self, filepath):
        for i in range(len(self.playlist)):
            if self.playlist[i]['path'] == filepath:
                print(f"ClassPlaylist {self.uuid} file [filepath] not found removed")
                del self.playlist[i]
                self.SavePlaylist()
                break
