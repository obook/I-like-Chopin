#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

from PySide6.QtWidgets import QDialog
from ui_informations import Ui_DialogInformation
import platform
from settings import ClassSettings

class InformationsDlg(Ui_DialogInformation, QDialog):

    def __init__(self, midisong, parent=None):
        super().__init__(parent)
        self.midisong = midisong
        self.settings = ClassSettings()
        self.setupUi(self)
        self.setFixedSize(400,361)
        self.setWindowTitle("Informations")
        self.pushButton_Close.clicked.connect(self.quit)
        style = " style='color:#FFFFFF;background-color:#333333;'"
        text = ""
        text += f"<p{style}>SONG : {self.midisong.GetFilename()}</p>"
        text += f"Duration : {self.midisong.GetDuration()} minutes"
        if self.midisong.GetTracks():
            for i in range(len(self.midisong.GetTracks())):
                text += f"<br>track {i} : {self.midisong.tracks[i]}"
        text += f"<p{style}>SYSTEM</p>"
        text += f"{platform.system()}"
        text += f"<p{style}>CONFIG FILE</p>"
        text += f"{self.settings.GetConfigPath()}"
        text += f"<p{style}>MIDIFILES LIBRARY PATH</p>"
        text += f"{self.settings.GetMidiPath()}"
        text += f"<p{style}>HUMANIZE</p>"
        text += "control_change:control 71 (set your midi-device)"
        text += f"<p{style}>SPEED CONTROL</p>"
        text += "control_change:control 76 (set your midi-device)"
        text += f"<p{style}>MIDIFILE SELECT</p>"
        text += "control_change:control 77 (set your midi-device)"
        text += f"<p{style}>MODE TOGGLE PLAYBACK / PASSTHROUGH</p>"
        text += "control_change:control 51 (set your midi-device)"
        text += "<p style='color:#FF8888;'>PROJECT : <a href='https://github.com/obook/I-like-Chopin'>https://github.com/obook/I-like-Chopin</a></p>"
        self.textBrowser.setAcceptRichText(True)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.insertHtml(text)

        self.checkBox_PrintTerminalMsg.setChecked(self.settings.GetPrintTerm())
        self.checkBox_ForceIntrument0.setChecked(self.settings.GetForceIntrument())

        self.checkBox_ForceIntrument0.setText(f"Force piano (prog {self.settings.GetPianoProgram()})")

    def quit(self):
        self.settings.SavePrintTerm(self.checkBox_PrintTerminalMsg.isChecked())
        self.settings.SaveForceIntrument(self.checkBox_ForceIntrument0.isChecked())
        self.close()

def ShowInformation(pParent,midisong):
    dlg = InformationsDlg(midisong, pParent)
    dlg.show()
