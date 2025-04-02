#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import os
import glob
import platform
import uuid
import time

import mido
from midi_input import ClassThreadInput
from midi_output import ClassThreadOutput
from midi_reader import ClassThreadMidiReader
from midi_song import modes

from PySide6.QtCore import QObject, Signal


class ClassMidiMain(QObject):
    """Main Midi Class
    key_on = a key from keybaord is pressed
    offset = change note ...
    """

    keys = {"key_on": 0, "speed": 0, "humanize": 0, "offset": 0}

    # Threads
    ThreadInput = None
    ThreadOutput = None
    ThreadMidiReader = None

    midisong = None
    channels = None
    uuid = None
    statusbar_activity = Signal(str)
    readerstop_activity = Signal()

    Settings = None

    def __init__(self, pParent, channels):
        QObject.__init__(self)
        self.uuid = uuid.uuid4()
        self.pParent = pParent
        self.Settings = self.pParent.Settings
        self.channels = channels
        self.statusbar_activity.connect(self.pParent.SetStatusBar)
        print(f"MidiMain {self.uuid} created")

    def __del__(self):
        print(f"MidiMain {self.uuid} destroyed")

    def GetMidiApi(self):
        return mido.backend.module.get_api_names()

    def GetDevices(self):
        Inputs = []
        Outputs = []
        IOPorts = []

        for i, port_name in enumerate(mido.get_output_names()):
            if platform.system() == "Linux":  # cleanup linux ports
                port_name = port_name[: port_name.rfind(" ")]
            Outputs.append(port_name)

        for i, port_name in enumerate(mido.get_input_names()):
            if platform.system() == "Linux":  # cleanup linux ports
                port_name = port_name[: port_name.rfind(" ")]
            Inputs.append(port_name)

        for i, port_name in enumerate(mido.get_ioport_names()):  # not used
            if platform.system() == "Linux":  # cleanup linux ports
                port_name = port_name[: port_name.rfind(" ")]
            IOPorts.append(port_name)

        if self.Settings.GetDebugMsg():
            print("*************** Outputs")  # from Python to device
            print(Outputs)

            print("*************** Inputs")  # from device to Python
            print(Inputs)

            print("*************** IOPorts")
            print(IOPorts)

        return Inputs, Outputs, IOPorts

    def ConnectInput(self, in_device):
        if self.ThreadInput:
            self.ThreadInput.stop()
            while self.ThreadInput.isRunning():
                time.sleep(0.01)
        self.keys["key_on"] = 0
        self.ThreadInput = ClassThreadInput(in_device, self.keys, self.pParent)
        self.ThreadInput.start()

    def GetInputPort(self):
        if self.ThreadInput:
            return self.ThreadInput.getport()
        return None

    def ConnectOutput(self, out_device):
        if self.ThreadOutput:
            self.ThreadOutput.reset()
            self.ThreadOutput.stop()
            while self.ThreadOutput.isRunning():
                time.sleep(0.01)
        self.ThreadOutput = ClassThreadOutput(out_device, self.pParent)
        self.ThreadOutput.start()

    def GetOuputPort(self):
        if self.ThreadOutput:
            return self.ThreadOutput.getport()
        return None

    def SendOutput(self, msg):
        try:  # ThreadOutput ready ? Exists ?
            return self.ThreadOutput.send(msg)
        except Exception as error:
            print(f"ERROR MidiMain {self.uuid} can not SendOutput {error}")
        return None

    def SetMidiSong(self, midifile):

        if self.ThreadMidiReader:
            self.readerstop_activity.emit()
            self.ThreadMidiReader.stop()  # test
            while self.ThreadMidiReader.isRunning():
                time.sleep(0.01)
        self.keys["key_on"] = 0
        self.ThreadMidiReader = ClassThreadMidiReader(
            midifile, self.keys, self.channels, self.pParent
        )

        # 3 modes = player (just midi player) , chopin (wait keyboard) and passthrough
        self.midisong = self.ThreadMidiReader.LoadMidiSong(self.Settings.GetMode())

        if self.ThreadOutput:
            port = self.ThreadOutput.getport()

            if self.ThreadInput:
                self.ThreadInput.SetOutPort(port)

            self.ThreadMidiReader.SetMidiPort(port)
            self.ThreadMidiReader.start()

        self.pParent.SetFileButtonText()

        self.readerstop_activity.connect(self.ThreadMidiReader.stop)

        return self.midisong

    def ChangeMidiMode(self, mode):
        self.keys["key_on"] = 0
        self.midisong.SetMode(mode)

    def GetMidiSong(self):
        if not self.ThreadMidiReader:
            return None
        return self.ThreadMidiReader.midisong

    def Playback(self):
        self.keys["key_on"] = 0
        self.ThreadMidiReader.start()

    def Mode(self, playback=True):
        out_port = self.ThreadOutput.getport()
        self.ThreadInput.SetOutPort(out_port)
        self.keys["playback"] = playback

    # Send signals
    def SendStatusBar(self, msg):
        self.statusbar_activity.emit(msg)

    def StopPlayer(self):
        self.keys["key_on"] = 0
        if self.ThreadMidiReader:
            self.ThreadMidiReader.stop()  # test
            # self.ThreadMidiReader = None
        self.readerstop_activity.emit()

    def Stop(self):
        self.keys["key_on"] = 0
        if self.ThreadMidiReader:
            self.ThreadMidiReader.stop()
            self.ThreadMidiReader = None

    def Panic(self):
        if self.ThreadOutput:
            self.ThreadOutput.panic()
        self.keys["key_on"] = 0
        self.statusbar_activity.emit("")

    def ResetOutput(self):
        self.keys["key_on"] = 0
        if self.ThreadOutput:
            self.ThreadOutput.reset()

    def quit(self):

        if self.ThreadMidiReader:
            self.readerstop_activity.emit() # ????
            self.ThreadMidiReader.stop()
            while self.ThreadMidiReader.isRunning():
                time.sleep(0.01)
            self.ThreadMidiReader = None

        if self.ThreadInput:
            self.ThreadInput.stop()
            while self.ThreadInput.isRunning():
                time.sleep(0.01)
            self.ThreadInput = None

        if self.ThreadOutput:
            self.ThreadOutput.reset()
            self.ThreadOutput.stop()
            while self.ThreadOutput.isRunning():
                time.sleep(0.01)
            self.ThreadOutput = None
