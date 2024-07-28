#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import platform

from PySide6.QtWidgets import QDialog
from ui_informations import Ui_DialogInformation

class InformationsDlg(Ui_DialogInformation, QDialog):
    pParent = None
    settings = None
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pParent = parent
        self.settings = self.pParent.settings
        self.setupUi(self)
        self.setFixedSize(481,361)
        self.setWindowTitle("Informations")
        self.pushButton_Close.clicked.connect(self.quit)
        style = " style='color:#FFFFFF;background-color:#333333;'"
        text = ""
        text += f"<p{style}>SYSTEM</p>"
        text += f"{platform.system()}"

        text += f"<p{style}>WEB SERVER</p>"
        for interface in self.pParent.server_interfaces:
            text += f"{interface}<br>"

        text += f"<p{style}>CONFIG FILE</p>"
        text += f"{self.settings.GetConfigPath()}"

        text += f"<p{style}>MIDIFILES LIBRARY PATH</p>"
        text += f"{self.settings.GetMidiPath()}"

        text += f"<p{style}>OUTPUTS</p>"
        for input in self.pParent.Inputs:
            text += f"{input}<br>"

        text += f"<p{style}>INPUTS</p>"
        for output in self.pParent.Outputs:
            text += f"{output}<br>"

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
        cursor = self.textBrowser.textCursor()
        cursor.setPosition(0);
        self.textBrowser.setTextCursor(cursor);

        self.checkBox_PrintTerminalMsg.setChecked(self.settings.GetPrintTerm())
        self.checkBox_ForceIntrument0.setChecked(self.settings.GetForceIntrument())

        self.checkBox_ForceIntrument0.setText(f"Force piano (prog {self.settings.GetPianoProgram()})")

        # WARNING HERE -> Send now force piano to device if set

    def quit(self):
        self.settings.SavePrintTerm(self.checkBox_PrintTerminalMsg.isChecked())
        self.settings.SaveForceIntrument(self.checkBox_ForceIntrument0.isChecked())
        self.close()

def ShowInformation(pParent):
    dlg = InformationsDlg(pParent)
    dlg.show()
