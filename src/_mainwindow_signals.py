#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from PySide6 import QtGui


class signals:

    # Signal receiver
    def SetStatusBar(self, message):
        self.ui.statusbar.showMessage(message)

    # Signal receiver
    def SetLedInput(self, value):  # value (0 or 1)
        if self.Midi:
            if self.Midi.keys["key_on"] > 0:
                self.ui.labelStatusInput.setPixmap(
                    QtGui.QPixmap(self.ICON_GREEN_LIGHT_LED)
                )
            else:
                self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))

    # Signal receiver
    def SetLedOutput(self, value):  # 0 or 1
        if value and self.Midi.GetOuputPort():
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LIGHT_LED))
        else:
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))

    # Signal receiver
    def SetLedFile(self, value):  # -1, 0 or 1
        if value < 0:
            self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
        elif value:
            self.ui.labelStatusMidifile.setPixmap(
                QtGui.QPixmap(self.ICON_GREEN_LIGHT_LED)
            )
        else:
            self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))
