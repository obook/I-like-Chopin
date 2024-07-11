#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from midi_main import midi_main
from settings import Settings

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):

    settings = Settings()
    ChannelButtonsList = []
    ChannelList = [False]*16

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.midi = midi_main(self)

        Inputs, Outputs = self.midi.GetDevices()
        Input = self.settings.GetInputDevice()
        Output = self.settings.GetOutputDevice()
        MidiFiles = self.midi.GetMidiFiles()
        Midifile = self.settings.GetMidifile()

        self.ui.InputDeviceCombo.addItem(Input)
        self.ui.InputDeviceCombo.addItems(Inputs)
        self.ui.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)

        self.ui.OutputDeviceCombo.addItem(Output)
        self.ui.OutputDeviceCombo.addItems(Outputs)
        self.ui.OutputDeviceCombo.currentIndexChanged.connect(self.OuputDeviceChanged)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)

        self.ui.pushButton_ChannelNone.clicked.connect(self.ChannelNone)
        self.ui.pushButton_ChannelAll.clicked.connect(self.ChannelAll)
        self.ui.pushButton_ChannelFirst.clicked.connect(self.ChannelFirst)

        self.ui.textBrowser.insertPlainText("Ready")

        #self.midi_input.SetInput('Arturia KeyStep 37:Arturia KeyStep 37 MIDI 1 28:0') # 28:0 peut changer !
        #self.midi_input.SetInput('Arturia KeyStep 37 MIDI 1')
        self.midi.ConnectInput(Input)

        #self.midi_output.SetOutput('FLUID Synth (Titanic):Synth input port (Titanic:0) 131:0') # 131:0 peut changer !
        #self.midi_output.SetOutput('Synth input port (Titanic:0)')
        self.midi.ConnectOutput(Output)


        self.ui.FileCombo.addItem(Midifile)
        self.ui.FileCombo.addItems(MidiFiles)
        try:
            self.ui.FileCombo.setCurrentIndex(self.settings.GetMidifileId())
        except:
            pass
        self.ui.FileCombo.currentIndexChanged.connect(self.MidifileChanged)

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

        self.ui.pushButton_Panic.clicked.connect(self.Panic)

        midifile = self.settings.GetMidifile()
        self.midi.SetMidifile(self.settings.GetMidiPath()+"/"+midifile)


    def InputDeviceChanged(self):
        in_device = self.ui.InputDeviceCombo.currentText()
        self.settings.SaveInputDevice(in_device)
        self.midi.ConnectInput(in_device)

    def OuputDeviceChanged(self):
        out_device = self.ui.OutputDeviceCombo.currentText()
        print(out_device)
        self.settings.SaveOutputDevice(out_device)
        self.midi.ConnectOutput(out_device)

    def MidifileChanged(self):
        file = self.ui.FileCombo.currentText()
        print(f"MidifileChanged:[{file}]")
        self.settings.SaveMidifile(file)
        self.midi.SetMidifile(self.settings.GetMidiPath()+"/"+file)

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

    def PrintKeys(self,n):
        self.ui.statusbar.showMessage("Keys:"+str(n))

    def Panic(self):
        pass

    def Quit(self):
        self.midi.quit()
        app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.setWindowTitle("Chopin Lab")
    widget.show()
    sys.exit(app.exec())
