#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage

Windows
-------
pip uninstall rtmidi
pip uninstall python-rtmidi
pip install mido
pip install python-rtmidi

"""
import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6 import QtGui
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from midi_main import ClassMidiMain
from midi_song import ClassMidiSong, states
from settings import ClassSettings
from informations import ShowInformation
from song_screen import UpdateSongScreen

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
from ui_mainwindow import Ui_MainWindow

application_path = os.path.dirname(os.path.realpath(__file__))
ICON_APPLICATION = application_path+'/icons/svg/i-like-chopin.svg'
# Define status icons
ICON_RED_LED = application_path+'/icons/led/led-red-on.png'
ICON_GREEN_LED = application_path+'/icons/led/green-led-on.png'
ICON_YELLOW_LED = application_path+'/icons/led/yellow-led-on.png'
ICON_LED_OFF = application_path+'/icons/led/led-off.png'

app = None

class MainWindow(QMainWindow):

    settings = ClassSettings()
    ChannelsButtonsList = []
    ChannelsList = [False]*16

    Inputs = []
    Outputs = []

    MidiFiles=[]
    MidifilesIndex = 0 # ?
    midi = None
    midisong = None # current midifile

    MidifileState = False

    ConnectInputState = False
    ConnectOutputState = False
    mode_playback = True

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.setFixedSize(504,434)
        self.ui.setupUi(self)

        # Application icon X.org->correct - Wayland->not implemented
        my_icon = QIcon()
        my_icon.addFile(ICON_APPLICATION)
        self.setWindowIcon(my_icon)

        #StatusBar
        self.ui.statusbar.setSizeGripEnabled(False)

        # Midi class
        self.midi = ClassMidiMain(self,self.ChannelsList)

        # Push Buttons
        self.ui.pushButton_Panic.clicked.connect(self.Panic)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)
        self.ui.pushButton_Info.clicked.connect(self.Informations)
        self.ui.pushButton_Mode.clicked.connect(self.Mode)
        self.ui.pushButton_Mode.setStyleSheet("QPushButton { background-color: rgb(30,80,30); }\n")

        # ComboBoxes Inputs/Outputs
        self.Inputs, self.Outputs, IOPorts = self.midi.GetDevices()
        Input = self.settings.GetInputDevice()
        Output = self.settings.GetOutputDevice()

        self.ui.InputDeviceCombo.addItem(Input)
        self.ui.InputDeviceCombo.addItems(self.Inputs)
        self.ui.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)

        self.ui.OutputDeviceCombo.addItem(Output)
        self.ui.OutputDeviceCombo.addItems(self.Outputs)
        self.ui.OutputDeviceCombo.currentIndexChanged.connect(self.OuputDeviceChanged)

        # Leds
        self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(ICON_LED_OFF))
        self.ui.labelStatusInput.setScaledContents(True)

        self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(ICON_LED_OFF))
        self.ui.labelStatusOuput.setScaledContents(True)

        self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(ICON_LED_OFF))
        self.ui.labelStatusMidifile.setScaledContents(True)

        # Midi Channels
        self.ui.pushButton_ChannelsNone.clicked.connect(self.ChannelsNone)
        self.ui.pushButton_ChannelsAll.clicked.connect(self.ChannelsAll)
        self.ui.pushButton_ChannelsFirst.clicked.connect(self.ChannelsFirst)

        grid = self.ui.gridLayout
        for n in range(8):
            self.ChannelsButtonsList.append(QPushButton(str(n+1)))
            self.ChannelsButtonsList[n].setCheckable(True);
            self.ChannelsButtonsList[n].clicked.connect(self.ReadChannels)
            self.ChannelsButtonsList[n].setStyleSheet("QPushButton:checked { background-color: rgb(50,100,50); }\n")
            grid.addWidget(self.ChannelsButtonsList[n],1,n)
        for n in range(8):
            self.ChannelsButtonsList.append(QPushButton(str(n+8+1)))
            self.ChannelsButtonsList[n+8].setCheckable(True);
            self.ChannelsButtonsList[n+8].clicked.connect(self.ReadChannels)
            self.ChannelsButtonsList[n+8].setStyleSheet("QPushButton:checked { background-color: rgb(50,100,50); }\n")
            grid.addWidget(self.ChannelsButtonsList[n+8],2,n)

        self.ChannelsFirst()
        # Special color for drums channel
        self.ChannelsButtonsList[9].setStyleSheet("QPushButton:checked { background-color: rgb(100,50,50); }\n")

        # Datas
        self.ChannelsList[0] = True # active first channel
        self.MidiFiles = self.midi.GetMidiFiles()
        self.midisong = ClassMidiSong(self.settings.GetMidifile())

        # Connections
        self.midi.ConnectInput(Input)
        self.midi.ConnectOutput(Output)
        self.midi.SetMidiSong(self.midisong)

        # Midifiles
        self.ui.FileCombo.addItems(self.MidiFiles)
        self.ui.FileCombo.setCurrentText(self.midisong.GetFilename())
        self.ui.FileCombo.currentIndexChanged.connect(self.MidifileChanged)

        # Drop file
        self.ui.FileCombo.installEventFilter(self)

        # Timer
        # UpdateSongScreen(self,self.midisong)
        timer = QTimer(self)
        timer.timeout.connect(self.timer)
        timer.start(2000)
        #self.timer()

    def timer(self):

        if self.midi.ConnectInputState() and not self.ConnectInputState :
            self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(ICON_GREEN_LED))
            self.ConnectInputState = True
        elif not self.midi.ConnectInputState():
            self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(ICON_RED_LED))
            self.ConnectInputState = False

        if self.midi.ConnectOutputState() and not self.ConnectOutputState:
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(ICON_GREEN_LED))
            self.ConnectOutputState = True
        elif not self.midi.ConnectOutputState():
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(ICON_RED_LED))
            self.ConnectOutputState = False

        # A revoir : UpdateSongScreen tout le temps

        if self.midisong.GetState() >= states['ready']:
            self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(ICON_GREEN_LED))
            self.MidifileState = True
            UpdateSongScreen(self,self.midisong)

        elif self.midisong.GetState() == states['cueing']:
           self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(ICON_YELLOW_LED))

        else:
           self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(ICON_RED_LED))
           self.MidifileState = False
           UpdateSongScreen(self,self.midisong)

    def InputDeviceChanged(self):
        self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(ICON_RED_LED))
        self.ConnectInputState = False
        in_device = self.ui.InputDeviceCombo.currentText()
        self.settings.SaveInputDevice(in_device)
        self.midi.ConnectInput(in_device)

    def OuputDeviceChanged(self):
        self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(ICON_RED_LED))
        self.ConnectOutputState = False
        out_device = self.ui.OutputDeviceCombo.currentText()
        self.settings.SaveOutputDevice(out_device)
        self.midi.ConnectOutput(out_device)
        self.midi.SetMidiSong(self.midisong)

    def MidifileChanged(self):
        self.MidifileChange(os.path.join(self.settings.GetMidiPath(),self.ui.FileCombo.currentText()))

    def MidifileChange(self, filepath):
        self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(ICON_YELLOW_LED))
        self.MidifileState = False
        self.midisong = ClassMidiSong(filepath)
        self.settings.SaveMidifile(self.midisong.Getfilepath())
        self.Tracks = self.midi.SetMidiSong(self.midisong)
        UpdateSongScreen(self,self.midisong)
        self.SetWindowName()

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

    def ChannelsColorize(self):

        for i in range(len(self.ChannelsButtonsList)):
            self.ChannelsButtonsList[i].setStyleSheet("QPushButton:checked { background-color: rgb(50,100,50); } QPushButton {color: grey}")

        channels = self.midisong.GetChannels()
        for key in channels:
            if channels[key]:
                self.ChannelsButtonsList[int(key)].setStyleSheet("");
                self.ChannelsButtonsList[int(key)].setStyleSheet("QPushButton:checked { background-color: rgb(50,100,50); }")

    def ReadChannels(self):
        for n in range(len(self.ChannelsButtonsList)):
            if self.ChannelsButtonsList[n].isChecked():
                self.ChannelsList[n] = True
            else:
                self.ChannelsList[n] = False

    # Status Bar

    def PrintStatusBar(self,message):
        self.ui.statusbar.showMessage(message)

    def PrintSpeed(self,speed): #0 to 126
        if speed :
            self.ui.pushButton_Speed.setText(f"Speed -{speed}")
        else:
            self.ui.pushButton_Speed.setText("Speed")

    def PrintHumanize(self,value):
        if value :
            self.ui.pushButton_Humanize.setText(f"Humanize {value}")
        else:
            self.ui.pushButton_Humanize.setText("Humanize")

    def ChangeMidiFile(self,value): # External Midi command
        # value 0-127
        step = int(128/len(self.MidiFiles))
        self.MidifilesIndex = min(int(value/step),len(self.MidiFiles)-1)
        self.ui.pushButton_FileIndex.setText(f"MidiFile {self.MidifilesIndex+1}/{len(self.MidiFiles)}")
        self.midi.Panic()
        self.ui.FileCombo.setCurrentText(self.MidiFiles[self.MidifilesIndex])

    def Mode(self):

        if self.mode_playback :
            self.mode_playback = False
            self.ui.pushButton_Mode.setText("Passthrough")
            self.ui.pushButton_Mode.setChecked(True)
            self.ui.pushButton_Mode.setStyleSheet("QPushButton { background-color: rgb(100,0,0); }\n")
        else:
            self.mode_playback = True
            self.ui.pushButton_Mode.setText("Playback")
            self.ui.pushButton_Mode.setChecked(False)
            self.ui.pushButton_Mode.setStyleSheet("QPushButton { background-color: rgb(30,80,30); }\n")
        self.midi.Mode(self.mode_playback)

    def Panic(self):
        self.midi.Panic()

    def SetWindowName(self):
        self.setWindowTitle(f"I Like Chopin : {self.midisong.GetName()}")

    def Informations(self):
        ShowInformation(self)

    def SongScreen(self):
        UpdateSongScreen(self, self.midisong)

    # End

    def closeEvent(self, event): # overwritten
        self.midi.quit()

    def Quit(self):
        self.midi.quit()
        app.quit()

def start():
    global app
    if not QApplication.instance():
        app = QApplication(sys.argv)
        app.setStyle('Fusion') # Windows dark theme
    else:
        app = QApplication.instance()
    widget = MainWindow()
    # For Linux Wayland, must be .desktop filename = Set QMainWindow icon
    app.setDesktopFileName("org.obook.i-like-chopin");
    widget.show()
    sys.exit(app.exec())

