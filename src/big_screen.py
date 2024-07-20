#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from PySide6.QtWidgets import QDialog
from ui_big_screen import Ui_BigScreenDlg

class BigScreenDlg(Ui_BigScreenDlg, QDialog):
    midisong = None

    def __init__(self, midisong, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("MidiSong")
        self.pushButtonClose.clicked.connect(self.quit)
        self.Update(midisong)

    def Update(self,midisong):
        self.midisong = midisong
        style = " style='color:#FFFFFF;background-color:#333333;'"
        text = ""
        text += f"<p{style}>SONG : {self.midisong.GetFilename()}</p>"
        text += f"Duration : {self.midisong.GetDuration()} minutes"
        if self.midisong.GetTracks():
            for i in range(len(self.midisong.GetTracks())):
                text += f"<br>track {i} : {self.midisong.tracks[i]}"
        self.textBrowser.insertHtml(text)

    def quit(self):
        self.close()

def ShowBigScreen(pParent,midisong):
    dlg = BigScreenDlg(midisong,pParent)
    dlg.show()
