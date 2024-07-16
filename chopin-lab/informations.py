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
        self.setupUi(self)
        self.setWindowTitle("Informations")
        self.pushButton_Close.clicked.connect(self.quit)

        settings = ClassSettings()

        text = ""
        text += f"SYSTEM\n{platform.system()}\n"
        text += f"CONFIG FILE\n{settings.GetConfigPath()}\n"
        text += f"MIDIFILES PATH\n{settings.GetMidiPath()}\n"
        text += "HUMANIZE\ncontrol_change:control 71 (set your midi-keyboard)\n"
        text += "SPEED CONTROL\ncontrol_change:control 76 (set your midi-keyboard)\n"
        text += "MIDIFILE SELECT\ncontrol_change:control 77 (set your midi-keyboard)\n"
        text += "\n"
        text += "PROJECT\nhttps://github.com/obook/I-like-Chopin\n"
        self.textEdit.setText(text)

    def quit(self):
        self.close()

def ShowInformation(pParent):
    dlg = InformationsDlg(pParent)
    dlg.show()
