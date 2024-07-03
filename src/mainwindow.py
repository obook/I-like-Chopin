#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
PySide6

CapLinux:
! Passer par QTCreator ou (moins bien)
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
#from midi_numbers import number_to_note


from ui_form import Ui_MainWindow
from midi_main import MidiMain
from settings import GetInputDeviceId, SaveInputDeviceId, GetOutputDeviceId,SaveOutputDeviceId,GetmidifileId,SavemidifileId
#from logger import QPlainTextEditLogger

class MainWindow(QMainWindow):
    bGlobalStatusRun = False
    bPassthrough = False
    ChannelButtonsList = []
    ChannelList = [False]*16

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

        self.ui.pushButton_ChannelNone.clicked.connect(self.ChannelNone)
        self.ui.pushButton_ChannelAll.clicked.connect(self.ChannelAll)
        self.ui.pushButton_ChannelFirst.clicked.connect(self.ChannelFirst)

        self.ui.pushButton_Panic.clicked.connect(self.Panic)

        self.ui.pushButton_Stop.setEnabled(False)

        Inputs, Outputs = self.midi.GetDevices()

        self.ui.InputDeviceCombo.addItems(Inputs)
        try:
            self.ui.InputDeviceCombo.setCurrentIndex(GetInputDeviceId())
        except:
            pass

        self.ui.OutputDeviceCombo.addItems(Outputs)
        try:
            self.ui.OutputDeviceCombo.setCurrentIndex(GetOutputDeviceId())
        except:
            pass

        MidiFiles = self.midi.GetMidiFiles()
        self.ui.FileCombo.addItems(MidiFiles)
        try:
            self.ui.FileCombo.setCurrentIndex(GetmidifileId())
        except:
            pass

        self.ui.pushButton_Mode.setText(u"Midi Auto Player")

        # grid
        grid = self.ui.gridLayout
        for n in range(8):
            self.ChannelButtonsList.append(QPushButton(str(n+1)))
            self.ChannelButtonsList[n].setCheckable(True);
            self.ChannelButtonsList[n].clicked.connect(self.ReadChannel)
            self.ChannelButtonsList[n].setStyleSheet("QPushButton:checked { background-color: rgb(0,200,0); }\n")
            grid.addWidget(self.ChannelButtonsList[n],1,n)
        for n in range(8):
            self.ChannelButtonsList.append(QPushButton(str(n+8+1)))
            self.ChannelButtonsList[n+8].setCheckable(True);
            self.ChannelButtonsList[n+8].clicked.connect(self.ReadChannel)
            self.ChannelButtonsList[n+8].setStyleSheet("QPushButton:checked { background-color: rgb(0,200,0); }\n")
            grid.addWidget(self.ChannelButtonsList[n+8],2,n)

        self.ChannelFirst()

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

        self.midi.MidiStart(in_device, out_device, "midi/"+midifile+".mid", self)

    def Stop(self):
        self.midi.MidiStop()
        SaveInputDeviceId(self.ui.InputDeviceCombo.currentIndex())
        SaveOutputDeviceId(self.ui.OutputDeviceCombo.currentIndex())
        SavemidifileId(self.ui.FileCombo.currentIndex())
        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Stop.setEnabled(False)
        self.ShowDevices()
        # Only on blocking mode
        # self.ui.statusbar.showMessage(u"Press any key on piano for stop...")

    def HideDevices(self):
        if self.bGlobalStatusRun == False :
            self.ui.pushButton_Quit.setEnabled(False)
            self.ui.pushButton_Start.setEnabled(False)
            self.ui.InputDeviceCombo.setEnabled(False)
            self.ui.OutputDeviceCombo.setEnabled(False)
            self.ui.FileCombo.setEnabled(False)
            self.ui.statusbar.showMessage(u"Waiting:"+self.ui.InputDeviceCombo.currentText()+"...")
            self.bGlobalStatusRun = True

    def ShowDevices(self):
        if self.bGlobalStatusRun == True:
            self.ui.pushButton_Quit.setEnabled(True)
            self.ui.pushButton_Start.setEnabled(True)
            self.ui.InputDeviceCombo.setEnabled(True)
            self.ui.OutputDeviceCombo.setEnabled(True)
            self.ui.FileCombo.setEnabled(True)
            self.ui.statusbar.showMessage(u"Ready")
            self.bGlobalStatusRun = False

    def Quit(self):
        self.Stop()
        app.quit()

    def Mode(self): # not used
        if not self.bPassthrough:
            print("Passthrough ON")
            in_device = self.ui.InputDeviceCombo.currentText()
            out_device = self.ui.OutputDeviceCombo.currentText()
            self.midi.MidiPassthroughStart(in_device, out_device)
            self.bPassthrough = True
        else:
            print("Passthrough OFF")
            self.midi.MidiPassthroughStop()
            self.bPassthrough = False

        print("Mode")

    def PrintKeys(self,n):
        self.ui.statusbar.showMessage("Keys:"+str(n))

    def PrintBrowser(self, text):
        # crash en sortie
        # self.ui.textBrowser.insertPlainText(text)
        # test
        # self.ui.textBrowser.moveCursor(QTextCursor.End)
        print(text)

    def ChannelNone(self):
        for n in range(len(self.ChannelButtonsList)):
            self.ChannelButtonsList[n].setChecked(False)
        self.ReadChannel()

    def ChannelAll(self):
        for n in range(len(self.ChannelButtonsList)):
            self.ChannelButtonsList[n].setChecked(True)
        self.ReadChannel()

    def ChannelFirst(self):
        self.ChannelNone()
        self.ChannelButtonsList[0].setChecked(True)
        self.ReadChannel()

    def ReadChannel(self):
        for n in range(len(self.ChannelButtonsList)):
            if self.ChannelButtonsList[n].isChecked():
                self.ChannelList[n] = True
            else:
                self.ChannelList[n] = False

    def ChannelIsActive(self,n):
        return(self.ChannelList[n])

    def Panic(self):
        self.midi.MidiPanic()

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    widget = MainWindow()
    widget.setWindowTitle("I Like Chopin")
    widget.show()
    sys.exit(app.exec())




