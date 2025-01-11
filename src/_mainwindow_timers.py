#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from PySide6 import QtGui
from PySide6.QtCore import QTimer

from midi_song import states, modes


class timers:

    ConnectInputState = False
    ConnectOutputState = False

    window_title = []  # not used
    title_rotation = 0  # not used

    def SetTimer(self):

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.timer_song)
        self.timer1.start(2000)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.timer_title)
        self.timer2.start(8000)

        self.timer3 = QTimer(self)
        self.timer3.timeout.connect(self.timer_random_song)
        self.timer3.start(25000)

    def timer_song(self):
        if self.Midi.GetInputPort() and not self.ConnectInputState:
            self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))
            self.ConnectInputState = True
        elif not self.Midi.GetInputPort():
            self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
            self.ConnectInputState = False

        if self.Midi.GetOuputPort() and not self.ConnectOutputState:
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))
            self.ConnectOutputState = True
        elif not self.Midi.GetOuputPort():
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
            self.ConnectOutputState = False

        self.midisong = self.Midi.GetMidiSong()

        if self.midisong:
            if self.midisong.IsState(states["cueing"]):
                self.PlayingState = False
                self.ui.labelStatusMidifile.setPixmap(
                    QtGui.QPixmap(self.ICON_YELLOW_LED)
                )
                self.SetStatusBar("Cueing...")

            elif self.midisong.GetState() > states["cueing"] and not self.PlayingState:
                self.PlayingState = True
                # We lose Del animation
                self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))
                # We lose 'waiting...' message and other
                # self.SetStatusBar("")

            elif self.midisong.GetState() < states["cueing"]:
                self.PlayingState = False
                self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
                if self.midisong.IsState(states["notracktoplay"]):
                    self.SetStatusBar("! No notes in selected channels")

            self.ui.progressBar.setValue(self.midisong.GetPlayed())

            self.SetFileButtonText()
            self.ChannelsSetButtons()
            # just for led off
            if self.Midi.GetOuputPort():
                self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))


    def timer_title(self):
        # if not window_title:
        self.window_title = ["I LIKE CHOPIN"]

        if self.midisong:
            self.setWindowTitle(self.midisong.GetParent() + " " + str(round(self.midisong.GetDuration(), 2)) + "'")

        '''
        if self.Web_server:
            for url in self.Web_server.GetServerURLs():
                if not "127.0.0.1" in url:
                    self.window_title.append(url)

        if self.midisong:
            self.window_title.append(self.midisong.GetParent())
        self.setWindowTitle(self.window_title[self.title_rotation])
        self.title_rotation += 1
        if self.title_rotation >= len(self.window_title):
            self.title_rotation = 0
        '''

    def timer_random_song(self):
        self.midisong = self.Midi.GetMidiSong()
        if not self.midisong.IsState(states["playing"]) and self.Settings.IsMode(
            modes["random"]
        ):
            self.MidifileChange(self.Midifiles.GetRandomSong())

    def StopTimers(self):
        self.timer1.stop()
        self.timer2.stop()
        self.timer3.stop()
