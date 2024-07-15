#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6 import QtGui
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from midi_main import ClassMidiMain
from settings import ClassSettings

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

# Define status icons
ICON_RED_LED = "./icons/led-red-on.png"
ICON_GREEN_LED = "./icons/green-led-on.png"
ICON_LED_OFF = "./icons/led-off.png"

class MainWindow(QMainWindow):

    settings = ClassSettings()
    TracksButtonsList = []
    TracksList = [False]*16

    ConnectInputState = False
    ConnectOutputState = False
    MidifileState = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Application icon X.org->correct - Wayland->not implemented
        my_icon = QIcon()
        my_icon.addFile('i-like-chopin.png')
        self.setWindowIcon(my_icon)

        # Midi class
        self.midi = ClassMidiMain(self,self.TracksList)

        # Datas
        Inputs, Outputs, IOPorts = self.midi.GetDevices()
        Input = self.settings.GetInputDevice()
        Output = self.settings.GetOutputDevice()
        MidiFiles = self.midi.GetMidiFiles()
        Midifile = self.settings.GetMidifile()

        # Push Buttons
        self.ui.pushButton_Panic.clicked.connect(self.Panic)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)
        self.ui.pushButton_Mode.setEnabled(False)

        # ComboBoxes
        self.ui.InputDeviceCombo.addItem(Input)
        self.ui.InputDeviceCombo.addItems(Inputs)
        self.ui.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)

        self.ui.OutputDeviceCombo.addItem(Output)
        self.ui.OutputDeviceCombo.addItems(Outputs)
        self.ui.OutputDeviceCombo.currentIndexChanged.connect(self.OuputDeviceChanged)

        self.ui.FileCombo.addItem(Midifile)
        self.ui.FileCombo.addItems(MidiFiles)
        try:
            self.ui.FileCombo.setCurrentIndex(self.settings.GetMidifileId())
        except:
            pass
        self.ui.FileCombo.currentIndexChanged.connect(self.MidifileChanged)

        # Leds
        self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(ICON_LED_OFF))
        self.ui.labelStatusInput.setScaledContents(True)

        self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(ICON_LED_OFF))
        self.ui.labelStatusOuput.setScaledContents(True)

        self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(ICON_LED_OFF))
        self.ui.labelStatusMidifile.setScaledContents(True)

        # Tracks
        self.ui.pushButton_TracksNone.clicked.connect(self.TracksNone)
        self.ui.pushButton_TracksAll.clicked.connect(self.TracksAll)
        self.ui.pushButton_TracksFirst.clicked.connect(self.TracksFirst)

        grid = self.ui.gridLayout
        for n in range(8):
            self.TracksButtonsList.append(QPushButton(str(n+1)))
            self.TracksButtonsList[n].setCheckable(True);
            self.TracksButtonsList[n].clicked.connect(self.ReadTracks)
            self.TracksButtonsList[n].setStyleSheet("QPushButton:checked { background-color: rgb(200,0,200); }\n")
            grid.addWidget(self.TracksButtonsList[n],1,n)
        for n in range(8):
            self.TracksButtonsList.append(QPushButton(str(n+8+1)))
            self.TracksButtonsList[n+8].setCheckable(True);
            self.TracksButtonsList[n+8].clicked.connect(self.ReadTracks)
            self.TracksButtonsList[n+8].setStyleSheet("QPushButton:checked { background-color: rgb(200,0,200); }\n")
            grid.addWidget(self.TracksButtonsList[n+8],2,n)

        self.TracksFirst()

        # Connections
        self.midi.ConnectInput(Input)
        self.midi.ConnectOutput(Output)
        midifile = self.settings.GetMidifile()
        self.midi.SetMidifile(self.settings.GetMidiPath()+"/"+midifile)

        # Timer
        timer = QTimer(self)
        timer.timeout.connect(self.timer)
        timer.start(2000)

        self.ui.textBrowser.insertPlainText("Ready")

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

        if self.midi.MidifileState() and not self.MidifileState:
            self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(ICON_GREEN_LED))
            self.MidifileState = True
        elif not self.midi.MidifileState():
            self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(ICON_RED_LED))
            self.MidifileState = False

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
        print(out_device)
        self.settings.SaveOutputDevice(out_device)
        self.midi.ConnectOutput(out_device)

    def MidifileChanged(self):
        self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(ICON_RED_LED))
        self.MidifileState = False
        file = self.ui.FileCombo.currentText()
        print(f"MidifileChanged:[{file}]")
        self.settings.SaveMidifile(file)
        self.midi.SetMidifile(self.settings.GetMidiPath()+"/"+file)

    def TracksNone(self):
        for n in range(len(self.TracksButtonsList)):
            self.TracksButtonsList[n].setChecked(False)
        self.ReadTracks()

    def TracksAll(self):
        for n in range(len(self.TracksButtonsList)):
            self.TracksButtonsList[n].setChecked(True)
        self.ReadTracks()

    def TracksFirst(self):
        self.TracksNone()
        self.TracksButtonsList[0].setChecked(True)
        self.ReadTracks()

    def ReadTracks(self):
        for n in range(len(self.TracksButtonsList)):
            if self.TracksButtonsList[n].isChecked():
                self.TracksList[n] = True
            else:
                self.TracksList[n] = False

    def TracksIsActive(self,n):
        return(self.TracksList[n])

    def PrintKeys(self,n):
        self.ui.statusbar.showMessage("Keys\t"+str(n))

    def PrintSlow(self,speed): #0 to 126
        self.ui.pushButton_Slow.setText("Slow "+str(speed))

    def Panic(self):
        self.midi.Panic()

    def Quit(self):
        self.midi.quit()
        app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.setWindowTitle("Chopin Lab")
    widget.show()
    sys.exit(app.exec())
