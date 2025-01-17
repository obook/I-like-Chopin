#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import uuid
from PySide6.QtWidgets import QDialog
from ui_settings_dialog import Ui_DialogSettings


class SettingsDlg(Ui_DialogSettings, QDialog):
    __uuid = None
    Midi = None
    Settings = None

    Inputs = []
    Outputs = []
    InputsOutputs = []

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__uuid = uuid.uuid4()
        print(f"SettingsDlg {self.__uuid} created")
        self.Midi = parent.Midi
        self.Controller = parent.midi_controller  # Class Controller
        self.Settings = parent.Settings
        self.setupUi(self)
        self.setFixedSize(501, 289)
        self.setWindowTitle("Settings")

        self.pushButton_Close.clicked.connect(self.Quit)

        # ComboBoxes Inputs/Outputs
        Input = self.Settings.GetInputDevice()
        Output = self.Settings.GetOutputDevice()
        ControllerIN = self.Settings.GetControllertDeviceIN()
        ControllerOUT = self.Settings.GetControllertDeviceOUT()
        DefaultApi = self.Settings.GetMidiApi()

        self.Inputs, self.Outputs, self.InputsOutputs = self.Midi.GetDevices()
        MidiApis = self.Midi.GetMidiApi()

        self.InputDeviceCombo.addItem(Input)
        self.InputDeviceCombo.addItems(self.Inputs)

        self.OutputDeviceCombo.addItem(Output)
        self.OutputDeviceCombo.addItems(self.Outputs)

        if ControllerOUT: # to controller INPUT
            self.ControllerDeviceComboOUT.addItem(ControllerOUT)
            self.ControllerDeviceComboOUT.addItem("")
        else:
            self.ControllerDeviceComboOUT.addItem("")

        self.ControllerDeviceComboOUT.addItems(self.Outputs)

        if ControllerIN: # from controller OUTPUT
            self.ControllerDeviceComboIN.addItem(ControllerIN)
            self.ControllerDeviceComboIN.addItem("")
        else:
            self.ControllerDeviceComboIN.addItem("")

        self.ControllerDeviceComboIN.addItems(self.Inputs)

        self.ApiCombo.addItem(DefaultApi)
        self.ApiCombo.addItems(MidiApis)

        # not used, we use 'Save' action
        #self.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)
        #self.OutputDeviceCombo.currentIndexChanged.connect(self.OuputDeviceChanged)

        self.checkBox_ForceIntrument0.setChecked(self.Settings.GetForceIntrument())
        self.checkBox_ForceIntrument0.setText(
            f"Force piano (prog {self.Settings.GetPianoProgram()})"
        )

        self.checkBox_DebugMSG.setChecked(self.Settings.GetDebugMsg())

    def __del__(self):
        self.ApiComboChanged()  # first, change API
        self.InputDeviceChanged()
        self.OuputDeviceChanged()
        self.ControllerDeviceINChanged()
        self.ControllerDeviceOUTChanged()
        self.Settings.SaveForceIntrument(self.checkBox_ForceIntrument0.isChecked())
        self.Settings.SaveDebugMsg(self.checkBox_DebugMSG.isChecked())
        print(f"SettingsDlg {self.__uuid} destroyed")

    def InputDeviceChanged(self):
        # self.pParent.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
        self.ConnectInputState = False
        in_device = self.InputDeviceCombo.currentText()
        if in_device == "":
            in_device = None
        else:
            self.Midi.ConnectInput(in_device)
        self.Settings.SaveInputDevice(in_device)

    def OuputDeviceChanged(self):
        # self.pParent.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
        self.ConnectOutputState = False
        out_device = self.OutputDeviceCombo.currentText()
        if out_device == "":
            out_device = None
        else:
            self.Midi.ConnectOutput(out_device)
        self.Settings.SaveOutputDevice(out_device)

    def ControllerDeviceINChanged(self):
        controller_deviceIN = self.ControllerDeviceComboIN.currentText()
        if controller_deviceIN == "":
            controller_deviceIN = None
        else:
            self.Controller.open_controller()
        self.Settings.SaveControllertDeviceIN(controller_deviceIN)

    def ControllerDeviceOUTChanged(self):
        controller_deviceOUT = self.ControllerDeviceComboOUT.currentText()
        if controller_deviceOUT == "":
            controller_deviceOUT = None
        else:
            self.Controller.open_controller()
        self.Settings.SaveControllertDeviceOUT(controller_deviceOUT)

    def ApiComboChanged(self):
        current_api = self.ApiCombo.currentText()
        self.Settings.SaveMidiApi(current_api)

    def SaveForceIntrument(self):
        self.Settings.SaveForceIntrument(self.checkBox_ForceIntrument0.isChecked())

    def Quit(self):
        # WARNING HERE -> Send now force piano to device if set ?
        self.close()
        self.deleteLater()

def CleanDeviceName(device):
    if device:
        if ":" in device:
            device_explode = device.split(":")
            max_length, device = max([(len(x), x) for x in (device_explode)])
    return device


def ShowSettingsDlg(pParent):
    dlg = SettingsDlg(pParent)
    dlg.show()
