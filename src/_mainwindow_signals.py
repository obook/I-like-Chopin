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

    # Signal receiver, Star mean quality
    def SetStarFile(self, value=0):  # -1=red 0=off 2=yellow, 3=green
        if value == 0:
            self.ui.labelLedQuality.setPixmap(QtGui.QPixmap(self.ICON_CHECK_OFF))
        elif value == 1:
            self.ui.labelLedQuality.setPixmap(QtGui.QPixmap(self.ICON_CHECK_YELLOW))
        elif value == 2:
            self.ui.labelLedQuality.setPixmap(QtGui.QPixmap(self.ICON_CHECK_GREEN))
        else:
            self.ui.labelLedQuality.setPixmap(QtGui.QPixmap(self.ICON_CHECK_RED))

    # Some probleme qui raw commands from webserver. So tests here...

    # Signal receivers
    def SignalShuffleMidifile(self):
        self.ShuffleMidifile()

    def SignalReplayMidifile(self):
        self.MidifileReplay()

    def SignalTooglePlayerMode(self): # Playback/Passthrough
        self.TooglePlayerMode()

    def SignalStop(self):
        self.Midi.StopPlayer()

    def SignalMidifileChange(self, midifile):
        self.MidifileChange(midifile)

    def SignalChangePlayerMode(self, mode):
        self.ChangePlayerMode(mode)
