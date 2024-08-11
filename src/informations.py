#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import platform
import mido

from PySide6.QtCore import QByteArray, QSize
from PySide6.QtWidgets import QDialog, QLabel
from PySide6.QtGui import QImage
from PySide6.QtSvgWidgets import QSvgWidget

from ui_informations import Ui_DialogInformation


class InformationsDlg(Ui_DialogInformation, QDialog):
    pParent = None
    Settings = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pParent = parent
        self.Settings = self.pParent.Settings
        self.setupUi(self)
        self.setFixedSize(481, 361)
        self.setWindowTitle("Informations")
        self.pushButton_Close.clicked.connect(self.quit)
        style = " style='color:#FFFFFF;background-color:#333333;'"
        text = ""
        text += f"<p{style}>SYSTEM</p>"
        text += f"{platform.system()}"

        text += f"<p{style}>WEB SERVER</p>"
        for interface in self.pParent.server_urls:  # UGLY
            text += f"<div>{interface}</div>"

        for qrcode in self.pParent.server_qrcode:
            svgWidget = QSvgWidget()
            svgWidget.setStyleSheet("QSvgWidget {background-color:white;}")
            svgWidget.load(QByteArray(qrcode.encode()))
            svgWidget.setFixedWidth(134)
            svgWidget.setFixedHeight(134)

            self.formLayout.addRow(svgWidget)
            self.formLayout.addRow(QLabel(""))

        text += f"<p{style}>CONFIG FILE</p>"
        text += f"{self.Settings.GetConfigPath()}"

        text += f"<p{style}>MIDIFILES LIBRARY PATH</p>"
        text += f"{self.Settings.GetMidiPath()}"

        text += f"<p{style}>BACKEND USED</p>"
        text += f"{mido.backend.name}\n"

        text += f"<p{style}>API USED</p>"
        backend = str(mido.backend)
        backend.replace("<", "")
        backend.replace(">", "")
        text += f"{mido.backend.module.get_api_names()[mido.backend.module._get_api_id()]}\n"

        text += f"<p{style}>API AVAILABLE</p>"
        backend = str(mido.backend)
        backend.replace("<", "")
        backend.replace(">", "")
        text += f"{mido.backend.module.get_api_names()}\n"

        text += f"<p{style}>OUTPUTS</p>"
        for device in self.pParent.Inputs:
            text += f"<div>{device}</div>"

        text += f"<p{style}>INPUTS</p>"
        for device in self.pParent.Outputs:
            text += f"<div>{device}</div>"

        text += f"<p{style}>INPUTS/OUTPUTS</p>"
        for device in self.pParent.InputsOutputs:
            text += f"<div>{device}</div>"

        text += f"<p{style}>HUMANIZE</p>"
        text += "control_change:control 71 - set your midi-device"

        text += f"<p{style}>SPEED CONTROL</p>"
        text += "control_change:control 76  - set your midi-device"
        """
        text += f"<p{style}>MIDIFILE SELECT</p>"
        text += "control_change:control 1 (modulation) - set your midi-device"
        """
        text += f"<p{style}>MODE TOGGLE PLAYBACK / PASSTHROUGH</p>"
        text += "control_change:control 51 (set your midi-device)"

        text += "<p style='color:#FF8888;'>PROJECT : <a href='https://github.com/obook/I-like-Chopin'>https://github.com/obook/I-like-Chopin</a></p>"
        self.textBrowser.setAcceptRichText(True)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.insertHtml(text)

        # layout = QGridLayout(self)
        # label = QLabel(self)
        # self.addWidget(label)

        cursor = self.textBrowser.textCursor()
        cursor.setPosition(0)
        self.textBrowser.setTextCursor(cursor)

        self.checkBox_ForceIntrument0.setChecked(self.Settings.GetForceIntrument())
        self.checkBox_ForceIntrument0.setText(
            f"Force piano (prog {self.Settings.GetPianoProgram()})"
        )

        # WARNING HERE -> Send now force piano to device if set

    def quit(self):
        self.Settings.SaveForceIntrument(self.checkBox_ForceIntrument0.isChecked())
        self.close()


def ShowInformation(pParent):
    dlg = InformationsDlg(pParent)
    dlg.show()
