#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QDialog
from ui_song_screen import Ui_SongScreenDlg
from settings import ClassSettings

class SongScreenDlg(Ui_SongScreenDlg, QDialog):
    midisong = None

    def __init__(self, midisong, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Song")
        self.Update(midisong)
        # Drop file
        self.textBrowser.installEventFilter(self)

    def Update(self,midisong):
        self.midisong = midisong
        self.textBrowser.clear()
        header_style = " style='color:#FFFFFF;background-color:#333333;font-size: 32px;text-transform: uppercase;' "
        text_style = " style='color:#FFFFFF;font-size: 18px;' "
        name = self.midisong.GetName()
        name = name.replace('_',' ')
        name = name.replace('-',' ')
        duration = self.midisong.GetDuration()
        minutes = int(duration)
        seconds = int((duration-minutes)*60)
        text = ""
        text += f"<p{header_style}>{name}</p>"
        text += f"<span{text_style}>Duration : {minutes} minutes {seconds} seconds</span>"
        if self.midisong.GetTracks():
            for i in range(len(self.midisong.GetTracks())):
                text += f"<br><span{text_style}>track {i} : {self.midisong.tracks[i]}</span>"
        if not self.midisong.Active():
            text += "<br>(STOPPED)"
        else:
            text += "<br>(ACTIVE)"
        self.textBrowser.insertHtml(text)

    def eventFilter(self, o, e):
        if e.type() == QEvent.DragEnter: #remember to accept the enter event
            e.acceptProposedAction()
            return True
        if e.type() == QEvent.Drop:
            data = e.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                #   Futur use
                print("-->SongScreenDlg:Dropped =", urls[0].path())
                '''
                self.midisong.Setfilepath(urls[0].path())
                self.midi.SetMidiSong(self.midisong)
                # not possible yet ->  self.ui.FileCombo.setLineEdit(urls[0].fileName()) #
                self.setWindowTitle(f"I Like Chopin : {self.midisong.GetName()}")
                UpdateSongScreen(self,self.midisong)
                '''
                return True
        return False #remember to return false for other event types

    def closeEvent(self, event): # overwritten
        # print("SongScreenDlg:closeEvent")
        pass

    def quit(self):
        self.close()

SongScreen = None
settings = ClassSettings()

def UpdateSongScreen(pParent,midisong):
    global SongScreen
    if not SongScreen:
        SongScreen = SongScreenDlg(midisong,pParent)
        if settings.GetShowSongInfo():
            SongScreen.show()
    else:
        SongScreen.Update(midisong)
        if not SongScreen.isVisible() and settings.GetShowSongInfo():
            SongScreen.show()
