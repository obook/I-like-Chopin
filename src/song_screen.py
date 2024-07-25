#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from PySide6.QtCore import QEvent, QTimer
from PySide6.QtWidgets import QDialog
from ui_song_screen import Ui_SongScreenDlg

class SongScreenDlg(Ui_SongScreenDlg, QDialog):
    midisong = None
    pParent = None
    settings = None
    def __init__(self, midisong, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pParent = parent
        self.settings = self.pParent.settings
        self.setWindowTitle("Song - drop files here")
        self.Update(midisong)
        # Drop file
        self.textBrowser.installEventFilter(self)
        # ProgressBar
        #self.ui.progressBar.setStyleSheet("QProgressBar::chunk {background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,stop: 0 #78d,stop: 0.4999 #46a,stop: 0.5 #45a,stop: 1 #238 );border: 1px solid black;}")
        self.progressBar.setRange(0,100)
        self.progressBar.setTextVisible(False)
        self.progressBar.setValue(0)
        # Timer
        timer = QTimer(self)
        timer.timeout.connect(self.timer)
        timer.start(2000)

    def Update(self,midisong):
        self.midisong = midisong
        self.textBrowser.clear()

        if self.midisong.IsState('cueing'):
            color = '#999900'
        elif self.midisong.IsState('playing'):
            color = '#339933'
        else:
            color = '#993333'

        header_style = f" style='color:{color};background-color:#333333;font-size: 32px;text-transform: uppercase;' "

        text_style = " style='font-size: 18px;' "
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
                text += f"<br><span{text_style}>track {i} : {self.midisong.GetTracks(i)}</span>"

        self.textBrowser.insertHtml(text)
        cursor = self.textBrowser.textCursor()
        cursor.setPosition(0);
        self.textBrowser.setTextCursor(cursor);

    def eventFilter(self, o, e):
        if e.type() == QEvent.DragEnter: #remember to accept the enter event
            e.acceptProposedAction()
            return True
        if e.type() == QEvent.Drop:
            data = e.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                if self.pParent:
                    self.pParent.MidifileChange(urls[0].path())
                return True
        return False #remember to return false for other event types

    def timer(self):
        self.Update(self.midisong)
        if self.midisong:
            self.progressBar.setValue(self.midisong.GetPlayed())

    def closeEvent(self, event): # overwritten
        #self.settings.SaveShowSongInfo(False)
        pass

    def quit(self):
        self.close()

SongScreen = None

def UpdateSongScreen(pParent,midisong):
    global SongScreen
    if not SongScreen:
        SongScreen = SongScreenDlg(midisong,pParent)
        if pParent.settings.GetShowSongInfo():
            SongScreen.show()
    else:
        SongScreen.Update(midisong)
        if not SongScreen.isVisible() and pParent.settings.GetShowSongInfo():
            SongScreen.show()
