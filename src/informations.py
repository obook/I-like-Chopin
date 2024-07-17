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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = ClassSettings()
        self.setupUi(self)
        self.setFixedSize(400,361)
        self.setWindowTitle("Informations")
        self.pushButton_Close.clicked.connect(self.quit)
        text = ""
        text += f"SYSTEM\n{platform.system()}\n\n"
        text += f"CONFIG FILE\n{self.settings.GetConfigPath()}\n\n"
        text += f"MIDIFILES PATH\n{self.settings.GetMidiPath()}\n\n"
        text += "HUMANIZE\ncontrol_change:control 71 (set your midi-keyboard)\n\n"
        text += "SPEED CONTROL\ncontrol_change:control 76 (set your midi-keyboard)\n\n"
        text += "MIDIFILE SELECT\ncontrol_change:control 77 (set your midi-keyboard)\n\n"
        text += "MODE TOGGLE PLAYBACK/PASSTHROUGH\ncontrol_change:control 51 (set your midi-keyboard)\n\n"
        text += "\n"
        text += "PROJECT\nhttps://github.com/obook/I-like-Chopin\n"
        self.textEdit.setText(text)

        self.checkBox_PrintTerminalMsg.setChecked(self.settings.GetPrintTerm())
        self.checkBox_ForceIntrument0.setChecked(self.settings.GetForceIntrument())

    def quit(self):
        self.settings.SetPrintTerm(self.checkBox_PrintTerminalMsg.isChecked())
        self.settings.SetForceIntrument(self.checkBox_ForceIntrument0.isChecked())
        self.close()

def ShowInformation(pParent):
    dlg = InformationsDlg(pParent)
    dlg.show()
