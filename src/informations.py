#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

from PySide6.QtWidgets import QDialog, QTextBrowser
from ui_informations import Ui_DialogInformation
import platform
from settings import ClassSettings

class InformationsDlg(Ui_DialogInformation, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = ClassSettings()
        self.setupUi(self)
        self.setFixedSize(400,361)
        self.setWindowTitle("Informations")
        self.pushButton_Close.clicked.connect(self.quit)
        text = ""
        text += f"SYSTEM<br>\n{platform.system()}<br>\n<br>\n"
        text += f"CONFIG FILE<br>\n{self.settings.GetConfigPath()}<br>\n<br>\n"
        text += f"MIDIFILES PATH<br>\n{self.settings.GetMidiPath()}<br>\n<br>\n"
        text += "HUMANIZE<br>\ncontrol_change:control 71 (set your midi-device)<br>\n<br>\n"
        text += "SPEED CONTROL<br>\ncontrol_change:control 76 (set your midi-device)<br>\n<br>\n"
        text += "MIDIFILE SELECT<br>\ncontrol_change:control 77 (set your midi-device)<br>\n<br>\n"
        text += "MODE TOGGLE PLAYBACK/PASSTHROUGH<br>\ncontrol_change:control 51 (set your midi-device)<br>\n<br>\n"
        text += "PROJECT : <a href='https://github.com/obook/I-like-Chopin'>https://github.com/obook/I-like-Chopin</a>"
        self.textBrowser.setAcceptRichText(True)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.insertHtml(text)

        self.checkBox_PrintTerminalMsg.setChecked(self.settings.GetPrintTerm())
        self.checkBox_ForceIntrument0.setChecked(self.settings.GetForceIntrument())

    def quit(self):
        self.settings.SetPrintTerm(self.checkBox_PrintTerminalMsg.isChecked())
        self.settings.SetForceIntrument(self.checkBox_ForceIntrument0.isChecked())
        self.close()

def ShowInformation(pParent):
    dlg = InformationsDlg(pParent)
    dlg.show()
