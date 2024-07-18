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

info_midifile = []
info_tracks = []

class InformationsDlg(Ui_DialogInformation, QDialog):

    global info_midifile,info_tracks

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = ClassSettings()
        self.setupUi(self)
        self.setFixedSize(400,361)
        self.setWindowTitle("Informations")
        self.pushButton_Close.clicked.connect(self.quit)
        style = " style='color:#FFFFFF;background-color:#333333;'"
        text = ""
        text += f"<p{style}>SONG</p>"
        text += f"{info_midifile}"
        if info_tracks:
            for i in range(len(info_tracks)):
                text += f"<br>track {i} : {info_tracks[i]}"
        text += f"<p{style}>SYSTEM</p>"
        text += f"{platform.system()}"
        text += f"<p{style}>CONFIG FILE</p>"
        text += f"{self.settings.GetConfigPath()}"
        text += f"<p{style}>MIDIFILES PATH</p>"
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

    def quit(self):
        self.settings.SetPrintTerm(self.checkBox_PrintTerminalMsg.isChecked())
        self.settings.SetForceIntrument(self.checkBox_ForceIntrument0.isChecked())
        self.close()

def ShowInformation(pParent,midifile,tracks):
    global info_midifile,info_tracks
    info_midifile = midifile
    info_tracks = tracks
    dlg = InformationsDlg(pParent)
    dlg.show()
