#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from PySide6.QtWidgets import QDialog, QLabel
from PySide6 import QtGui
from ui_settings_dialog import Ui_DialogSettings


class SettingsDlg(Ui_DialogSettings, QDialog):
    pParent = None
    Midi = None
    Settings = None

    Inputs = []
    Outputs = []
    InputsOutputs = []

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pParent = parent
        self.Midi = parent.Midi
        self.Settings = self.pParent.Settings
        self.setupUi(self)
        self.setFixedSize(501, 240)
        self.setWindowTitle("Settings")

        self.pushButton_Close.clicked.connect(self.Quit)

        # ComboBoxes Inputs/Outputs
        Input = self.Settings.GetInputDevice()
        Output = self.Settings.GetOutputDevice()
        self.Inputs, self.Outputs, self.InputsOutputs = self.Midi.GetDevices()

        self.InputDeviceCombo.addItem(Input)
        self.InputDeviceCombo.addItems(self.Inputs)

        self.OutputDeviceCombo.addItem(Output)
        self.OutputDeviceCombo.addItems(self.Outputs)

        self.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)
        self.OutputDeviceCombo.currentIndexChanged.connect(self.OuputDeviceChanged)

        self.checkBox_ForceIntrument0.setChecked(self.Settings.GetForceIntrument())
        self.checkBox_ForceIntrument0.setText(
            f"Force piano (prog {self.Settings.GetPianoProgram()})"
        )

    def InputDeviceChanged(self):
        # self.pParent.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
        self.ConnectInputState = False
        in_device = self.InputDeviceCombo.currentText()
        self.Settings.SaveInputDevice(in_device)
        self.Midi.ConnectInput(in_device)
        # self.pParent.ui.labelInput.setText(CleanDeviceName(in_device))

    def OuputDeviceChanged(self):
        # self.pParent.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
        self.ConnectOutputState = False
        out_device = self.OutputDeviceCombo.currentText()
        self.Settings.SaveOutputDevice(out_device)
        self.Midi.ConnectOutput(out_device)
        # self.pParent.ui.labelOutput.setText(CleanDeviceName(out_device))

    def Quit(self):
        self.Settings.SaveForceIntrument(self.checkBox_ForceIntrument0.isChecked())
        self.close()


def CleanDeviceName(device):
    if ":" in device:
        device_explode = device.split(":")
        max_length, device = max([(len(x), x) for x in (device_explode)])
    return device


def ShowSettingsDlg(pParent):
    dlg = SettingsDlg(pParent)
    dlg.show()
