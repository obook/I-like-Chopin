#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6 import QtGui
from PySide6.QtCore import QEvent

from informations import ShowInformation
from midi_song import modes

import _mainwindow_init
import _mainwindow_signals
import _mainwindow_timers
import _mainwindow_web
import _mainwindow_midi

# Outside QTCreator = Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
from ui_mainwindow import Ui_MainWindow


class Mainwindow(
    QMainWindow,
    _mainwindow_init._init,
    _mainwindow_midi.midi,
    _mainwindow_signals.signals,
    _mainwindow_web.web,
    _mainwindow_timers.timers,
):

    ConnectInputState = False
    ConnectOutputState = False
    PlayingState = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.setFixedSize(504, 413)
        self.ui.setupUi(self)

        # Imported methods
        self._SetInterface()
        self._midi_init()

        # Force playback mode
        self.Settings.SaveMode(modes["playback"])
        self.SetPlayerModeButtons()

        # ComboBoxes Inputs/Outputs
        Input = self.Settings.GetInputDevice()
        Output = self.Settings.GetOutputDevice()

        self.ui.InputDeviceCombo.addItem(Input)
        self.ui.InputDeviceCombo.addItems(self.Inputs)
        self.ui.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)

        self.ui.OutputDeviceCombo.addItem(Output)
        self.ui.OutputDeviceCombo.addItems(self.Outputs)
        self.ui.OutputDeviceCombo.currentIndexChanged.connect(self.OuputDeviceChanged)

        # Datas
        self.ChannelsList[0] = True  # active first channel
        """
        self.MidiFiles = self.Midi.GetMidiFiles()
        """
        # Connections
        self.Midi.ConnectInput(Input)
        self.Midi.ConnectOutput(Output)
        self.MidifileChange(self.Settings.GetMidifile())
        self.lastmidifile = self.Settings.GetMidifile()
        self.nextmidifile = self.nextmidifile

        # Midifiles
        if self.midisong:
            self.ui.pushButton_Files.setText(self.midisong.GetCleanName())

        self.midifiles_dict = self.Midifiles.ScanFiles(self.Settings.GetMidiPath())

        self.web_start()
        self.SetTimer()

    def InputDeviceChanged(self):
        self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
        self.ConnectInputState = False
        in_device = self.ui.InputDeviceCombo.currentText()
        self.Settings.SaveInputDevice(in_device)
        self.Midi.ConnectInput(in_device)

    def OuputDeviceChanged(self):
        self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
        self.ConnectOutputState = False
        out_device = self.ui.OutputDeviceCombo.currentText()
        self.Settings.SaveOutputDevice(out_device)
        self.Midi.ConnectOutput(out_device)

    def MidifileChange(
        self, filepath
    ):  # ! WARNING ! DO NOT TOUCH INTERFACE (Called by Threads)
        if filepath != self.lastmidifile:
            self.Settings.SaveMidifile(filepath)
            self.midisong = self.Midi.SetMidiSong(filepath)

            print(f"--->MidifileChange {self.midisong.Getfilepath()}")

            self.lastmidifile = filepath
            self.History.AddHistory(filepath)

    def MidifileReplay(self):  # ! WARNING ! DO NOT TOUCH INTERFACE (Called by Threads)
        if self.lastmidifile:
            self.midisong = self.Midi.SetMidiSong(self.lastmidifile)
    """
    def NextMidifile(
        self,
    ):  # from web server ! WARNING ! DO NOT TOUCH INTERFACE (Called by Threads)
        files = self.History.GetHistory()
        self.history_index += 1
        if self.history_index > len(files) - 1:
            self.history_index = len(files)
        self.ui.pushButton_FileIndex.setText(
            f"MidiFile {self.history_index+1}/{len(files)}"
        )
        self.MidifileChange(files[self.history_index])

    def PreviousMidifile(self):
        files = self.History.GetHistory()
        self.history_index -= 1
        if self.history_index < 0:
            self.history_index = 0

        print(f" ---> PreviousMidifile index={self.history_index}/{len(files)}")

        self.ui.pushButton_FileIndex.setText(
            f"MidiFile {self.history_index+1}/{len(files)}"
        )
        self.MidifileChange(files[self.history_index])
    """

    def ShuffleMidifile(self):
        newfile = self.Midifiles.GetRandomSong()
        self.MidifileChange(newfile)

    # Midi command
    def ChangeMidiFile(self, value):  # External Midi command
        # print("--> ChangeMidiFile NOT ACTIVE FOR INSTANCE")
        # value 0-127
        files = self.History.GetHistory()
        step = int(128 / len(files))
        FilesIndex = min(int(value / step), len(files) - 1)
        if self.lastmidifile != files[FilesIndex]:
            self.ui.pushButton_FileIndex.setText(
                f"MidiFile {FilesIndex+1}/{len(files)}"
            )
            # clean_name = self.History.GetCleanName(FilesIndex)

            self.ui.pushButton_Files.setText(
                self.History.GetCleanName(FilesIndex)
            )  # est écrasé, par timer ?

            # print(f"--> nextmidifile index {FilesIndex} file {files[FilesIndex]}")
            # self.nextmidifile = files[FilesIndex]

            # il faut afficher le titre, puis au bout d'une seconde s'il n'a pas changé, charger la chanson
            # parce qu'il charge et décharge pour rien le reader à chaque fois

            self.Midi.Panic()
            self.lastmidifile = files[FilesIndex]
            self.MidifileChange(files[FilesIndex])

    # Channels
    def ChannelsNone(self):
        for n in range(len(self.ChannelsButtonsList)):
            self.ChannelsButtonsList[n].setChecked(False)
        self.ReadChannels()

    def ChannelsAll(self):
        for n in range(len(self.ChannelsButtonsList)):
            self.ChannelsButtonsList[n].setChecked(True)
        self.ReadChannels()

    def ChannelsFirst(self):
        self.ChannelsNone()
        self.ChannelsButtonsList[0].setChecked(True)
        self.ReadChannels()

    def ChannelsSetButtons(self):
        if self.midisong:
            # Cleanup
            for i in range(len(self.ChannelsButtonsList)):
                self.ChannelsButtonsList[i].setStyleSheet("")
                if i == 9:
                    self.ChannelsButtonsList[i].setStyleSheet(
                        "QPushButton:checked { background-color: rgb(50,100,50); } QPushButton {color: rgb(100,50,50); background-color: rgb(100,50,50);}"
                    )
                else:
                    self.ChannelsButtonsList[i].setStyleSheet(
                        "QPushButton:checked { background-color: rgb(50,100,50); } QPushButton {color: grey}"
                    )
            # Set
            channels = self.midisong.GetChannels()
            for key in channels:
                if channels[key]:  # Show button
                    self.ChannelsButtonsList[int(key)].setStyleSheet("")
                    if int(key) == 9:
                        self.ChannelsButtonsList[int(key)].setStyleSheet(
                            "QPushButton:checked { background-color: rgb(50,100,50); } QPushButton {background-color: rgb(100,50,50);}"
                        )
                    else:
                        self.ChannelsButtonsList[int(key)].setStyleSheet(
                            "QPushButton:checked { background-color: rgb(50,100,50); }"
                        )

    def ReadChannels(self):
        for n in range(len(self.ChannelsButtonsList)):
            if self.ChannelsButtonsList[n].isChecked():
                self.ChannelsList[n] = True
            else:
                self.ChannelsList[n] = False

    def SetPlayerModeButtons(self):
        if self.Settings.IsMode(modes["playback"]):
            self.ui.pushButton_Mode.setStyleSheet(
                "QPushButton { background-color: rgb(30,80,30); }\n"
            )
            self.ui.pushButton_Mode.setText("Playback")
            self.ui.pushButton_Mode.setChecked(False)

        elif self.Settings.IsMode(modes["passthrough"]):
            self.ui.pushButton_Mode.setStyleSheet(
                "QPushButton { background-color: rgb(30,80,80); }\n"
            )
            self.ui.pushButton_Mode.setText("Passthrough")
            self.ui.pushButton_Mode.setChecked(False)

        elif self.Settings.IsMode(modes["player"]):
            self.ui.pushButton_Mode.setStyleSheet(
                "QPushButton { background-color: rgb(46,82,168); }\n"
            )
            self.ui.pushButton_Mode.setText("Player")
            self.ui.pushButton_Mode.setChecked(False)
        elif self.Settings.IsMode(modes["random"]):
            self.ui.pushButton_Mode.setStyleSheet(
                "QPushButton { background-color: rgb(0,0,0); }\n"
            )
            self.ui.pushButton_Mode.setText("Random")
            self.ui.pushButton_Mode.setChecked(False)

    def ChangePlayerMode(self):  # button mode pressed

        if self.Settings.IsMode(modes["playback"]):
            self.Settings.SaveMode(modes["passthrough"])

        elif self.Settings.IsMode(modes["passthrough"]):
            self.Settings.SaveMode(modes["player"])

        elif self.Settings.IsMode(modes["player"]):
            self.Settings.SaveMode(modes["random"])
            self.timer_random_song()

        elif self.Settings.IsMode(modes["random"]):
            self.Settings.SaveMode(modes["playback"])

        self.SetPlayerModeButtons()
        self.Midi.ChangeMidiMode(self.Settings.GetMode())

    def TooglePlayerMode(self): # Just player/passthrough, only called by midi_input

        print(f"self.Settings.GetMode={self.Settings.GetMode()}")

        if self.Settings.IsMode(modes["passthrough"]):
            self.Settings.SaveMode(modes["random"])
        else:
            self.Settings.SaveMode(modes["playback"])
        self.ChangePlayerMode()

    def SetFileButtonText(self):
        if self.midisong:
            # self.setWindowTitle(f"I Like Chopin : {self.midisong.GetCleanName()}")
            self.ui.pushButton_Files.setText(self.midisong.GetCleanName())

    def Informations(self):
        ShowInformation(self)

    def eventFilter(self, o, e):  # drop files
        if e.type() == QEvent.DragEnter:  # remember to accept the enter event
            e.acceptProposedAction()
            return True
        if e.type() == QEvent.Drop:
            data = e.mimeData()
            urls = data.urls()
            if urls and urls[0].scheme() == "file":
                self.MidifileChange(urls[0].path())
            return True
        return False  # remember to return false for other event types

    # End
    def closeEvent(self, event):  # overwritten
        self.Quit()

    def Quit(self):

        self.StopTimers()

        if self.Web_server:
            self.Web_server.stop()
        self.Web_server = None

        if self.Midi:
            self.Midi.quit()
            self.Midi = None

        QApplication.quit()


def start():
    if not QApplication.instance():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")  # Windows dark theme
    else:
        app = QApplication.instance()
    widget = Mainwindow()
    # For Linux/Wayland, must be .desktop filename (here org.obook.i-like-chopin.dektop) => Set mainwindow icon
    app.setDesktopFileName("org.obook.i-like-chopin")
    widget.show()
    sys.exit(app.exec())
