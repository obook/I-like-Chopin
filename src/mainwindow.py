#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
'''
PySide6

CapLinux:
! Passer par QTCreator ou (moins bien)
pip3 install pyside6

or (24.04LTS)

cd /usr/lib/python3.XX
sudo rm EXTERNALLY-MANAGED
pip3 install pyside6

Windows
-------
pip uninstall rtmidi
pip uninstall python-rtmidi
pip install mido
pip install python-rtmidi

Important but not user under QTCreator :
You need to run the following command to generate the ui_form.py file
pyside6-uic form.ui -o ui_form.py, or
pyside2-uic form.ui -o ui_form.py
'''

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QIcon

from ui_form import Ui_MainWindow
from midi_main import MidiMain
from settings import GetInputDeviceId, SaveInputDeviceId, GetOutputDeviceId,SaveOutputDeviceId,GetMidifileId,SaveMidifileId, GetMidiPath
#from logger import QPlainTextEditLogger

app = None

class MainWindow(QMainWindow):
    bGlobalStatusRun = False
    bPassthrough = False
    TracksButtonsList = []
    TracksList = [False]*16

    def __init__(self, parent=None):
        super().__init__(parent)

        self.midi = MidiMain(self)

        self.ui = Ui_MainWindow()
        self.setFixedSize(509,504)
        self.ui.setupUi(self)

        # X.org -> correct
        # Wayland -> not implemented yet :
        my_icon = QIcon()
        my_icon.addFile('i-like-chopin.png')
        self.setWindowIcon(my_icon)

        self.ui.pushButton_Start.clicked.connect(self.Start)
        self.ui.pushButton_Stop.clicked.connect(self.Stop)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)
        self.ui.pushButton_Mode.clicked.connect(self.Mode)

        self.ui.pushButton_TracksNone.clicked.connect(self.TracksNone)
        self.ui.pushButton_TracksAll.clicked.connect(self.TracksAll)
        self.ui.pushButton_TracksFirst.clicked.connect(self.TracksFirst)

        self.ui.pushButton_Panic.clicked.connect(self.Panic)

        self.ui.pushButton_Stop.setEnabled(False)

        Inputs, Outputs = self.midi.GetDevices()

        self.ui.InputDeviceCombo.addItems(Inputs)
        try:
            self.ui.InputDeviceCombo.setCurrentIndex(GetInputDeviceId())
            self.ui.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)
        except:
            pass

        self.ui.OutputDeviceCombo.addItems(Outputs)
        try:
            self.ui.OutputDeviceCombo.setCurrentIndex(GetOutputDeviceId())
            self.ui.OutputDeviceCombo.currentIndexChanged.connect(self.OuputDeviceChanged)
        except:
            pass

        MidiFiles = self.midi.GetMidiFiles()
        self.ui.FileCombo.addItems(MidiFiles)
        try:
            self.ui.FileCombo.setCurrentIndex(GetMidifileId())
        except:
            pass

        self.ui.pushButton_Mode.setText(u"AutoPlay")

        # grid
        grid = self.ui.gridLayout
        for n in range(8):
            self.TracksButtonsList.append(QPushButton(str(n+1)))
            self.TracksButtonsList[n].setCheckable(True);
            self.TracksButtonsList[n].clicked.connect(self.ReadTracks)
            self.TracksButtonsList[n].setStyleSheet("QPushButton:checked { background-color: rgb(0,200,0); }\n")
            grid.addWidget(self.TracksButtonsList[n],1,n)
        for n in range(8):
            self.TracksButtonsList.append(QPushButton(str(n+8+1)))
            self.TracksButtonsList[n+8].setCheckable(True);
            self.TracksButtonsList[n+8].clicked.connect(self.ReadTracks)
            self.TracksButtonsList[n+8].setStyleSheet("QPushButton:checked { background-color: rgb(0,200,0); }\n")
            grid.addWidget(self.TracksButtonsList[n+8],2,n)

        self.TracksFirst()

        # self.ui.textBrowser.setAcceptRichText(False)
        # self.ui.textBrowser.append("Welcome")

        # log_handler = QPlainTextEditLogger(self)
        # logging.getLogger().addHandler(log_handler)

    def Start(self):

        self.ui.pushButton_Stop.setEnabled(True)
        self.ui.pushButton_Start.setEnabled(False)
        self.ui.pushButton_Quit.setEnabled(False)
        self.HideDevices()

        in_device = self.ui.InputDeviceCombo.currentText()
        out_device = self.ui.OutputDeviceCombo.currentText()
        midifile = self.ui.FileCombo.currentText()

        self.midi.MidiStart(in_device, out_device, GetMidiPath()+"/"+midifile+".mid", self)

    def Stop(self):
        self.midi.MidiStop()
        SaveInputDeviceId(self.ui.InputDeviceCombo.currentIndex())
        SaveOutputDeviceId(self.ui.OutputDeviceCombo.currentIndex())
        SaveMidifileId(self.ui.FileCombo.currentIndex())
        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Stop.setEnabled(False)
        self.ShowDevices()

    def HideDevices(self):
        if self.bGlobalStatusRun == False :
            self.ui.pushButton_Quit.setEnabled(False)
            self.ui.pushButton_Start.setEnabled(False)
            self.ui.InputDeviceCombo.setEnabled(False)
            self.ui.OutputDeviceCombo.setEnabled(False)
            self.ui.FileCombo.setEnabled(False)
            self.ui.pushButton_Mode.setEnabled(False)
            self.ui.statusbar.showMessage(u"Waiting:"+self.ui.InputDeviceCombo.currentText()+"...")
            self.bGlobalStatusRun = True

    def ShowDevices(self):
        if self.bGlobalStatusRun == True:
            self.ui.pushButton_Quit.setEnabled(True)
            self.ui.pushButton_Start.setEnabled(True)
            self.ui.InputDeviceCombo.setEnabled(True)
            self.ui.OutputDeviceCombo.setEnabled(True)
            self.ui.FileCombo.setEnabled(True)
            self.ui.pushButton_Mode.setEnabled(True)
            self.ui.statusbar.showMessage(u"Ready")
            self.bGlobalStatusRun = False

    def Quit(self):
        self.Stop()
        app.quit()


    def InputDeviceChanged(self):
        print("InputDeviceChanged")

    def OuputDeviceChanged(self):
         print("OuputDeviceChanged")

    def Mode(self):
        if not self.bPassthrough:
            self.ui.pushButton_Mode.setText("Passthrough")
            in_device = self.ui.InputDeviceCombo.currentText()
            out_device = self.ui.OutputDeviceCombo.currentText()
            self.midi.MidiPassthroughStart(in_device, out_device)
            self.bPassthrough = True
        else:
            self.ui.pushButton_Mode.setText("AutoPlay")
            self.midi.MidiPassthroughStop()
            self.bPassthrough = False

    def PrintKeys(self,n):
        self.ui.statusbar.showMessage("Keys:"+str(n))

    def PrintBrowser(self, text):
        # crash en sortie
        # self.ui.textBrowser.insertPlainText(text)
        # test
        # self.ui.textBrowser.moveCursor(QTextCursor.End)
        print(text)

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

    def Panic(self):
        self.midi.MidiPanic()

def start():
    global app

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    widget = MainWindow()
    widget.setWindowTitle("I Like Chopin")
    # m_icon = pParent->windowIcon().pixmap(32, 32);
    widget.show()
    sys.exit(app.exec())


