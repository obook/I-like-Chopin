#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
#from PySide6 import QtCore
from PySide6.QtWidgets import QDialog
from ui_song_screen import Ui_SongScreenDlg

class SongScreenDlg(Ui_SongScreenDlg, QDialog):
    midisong = None

    def __init__(self, midisong, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Song")
        self.Update(midisong)

    def Update(self,midisong):
        self.midisong = midisong
        self.textBrowser.clear()
        header_style = " style='color:#FFFFFF;background-color:#333333;font-size: 32px;text-transform: uppercase;' "
        text_style = " style='color:#FFFFFF;font-size: 18px;' "
        text = ""
        text += f"<p{header_style}>{self.midisong.GetName()}</p>"
        text += f"<span{text_style}>Duration : {self.midisong.GetDuration()} minutes</span>"
        if self.midisong.GetTracks():
            for i in range(len(self.midisong.GetTracks())):
                text += f"<br><span{text_style}>track {i} : {self.midisong.tracks[i]}</span>"
        self.textBrowser.insertHtml(text)

    def closeEvent(self, event): # overwritten
        print("SongScreenDlg:closeEvent")

    def quit(self):
        self.close()

SongScreen = None

def ShowSongScreen(pParent,midisong):
    global SongScreen
    if not SongScreen:
        SongScreen = SongScreenDlg(midisong,pParent)
        SongScreen.show()
    else:
        SongScreen.Update(midisong)

