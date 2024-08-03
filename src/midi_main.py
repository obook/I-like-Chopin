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
    """Main Midi Class"""

    keys = {"key_on": 0, "speed": 0, "humanize": 0}

    # Threads
    ThreadInput = None
    ThreadOutput = None
    ThreadMidiReader = None

    midisong = None
    channels = None
    uuid = uuid.uuid4()
    statusbar_activity = Signal(str)
    led_file_activity = Signal(int)
    readerstop_activity = Signal()

    settings = None

    def __init__(self, pParent, channels):
        QObject.__init__(self)
        self.pParent = pParent
        self.settings = self.pParent.settings
        self.channels = channels
        self.statusbar_activity.connect(self.pParent.SetStatusBar)
        self.led_file_activity.connect(self.pParent.SetLedFile)
        print(f"MidiMain {self.uuid} created")

    def __del__(self):
        print(f"MidiMain {self.uuid} destroyed")

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

        return Inputs, Outputs, IOPorts

    def ConnectInput(self, in_device):
        if self.ThreadInput:
            self.ThreadInput.stop()

        self.ThreadInput = ClassThreadInput(in_device, self.keys, self.pParent)
        self.ThreadInput.start()

    def GetInputPort(self):
        if self.ThreadInput:
            return self.ThreadInput.getport()
        return None

    def ConnectOutput(self, out_device):

        if self.ThreadMidiReader:
            self.ThreadMidiReader.SetMidiPort(None)

        self.ThreadOutput = ClassThreadOutput(out_device, self.pParent)
        self.ThreadOutput.start()

    def GetOuputPort(self):
        if self.ThreadOutput:
            return self.ThreadOutput.getport()
        return None

    def SendOutput(self, msg):
        if self.ThreadOutput:
            if self.settings.IsMode(modes["passthrough"]):
                return self.ThreadOutput.send(msg)
            elif msg.type == "note_on" or msg.type == "note_off":
                if self.pParent.ChannelsList[msg.channel]:
                    return self.ThreadOutput.send(msg)
            else:
                return self.ThreadOutput.send(msg)
        return None

    # List of midifiles from folder midi (see json file created)
    def GetMidiFiles(self):
        midifiles = []
        for file in sorted(
            glob.glob(os.path.join(self.settings.GetMidiPath(), "*.mid"))
        ):
            midifiles.append(os.path.basename(file))
        return midifiles

    def SetMidiSong(self, midifile):

        if self.ThreadMidiReader:
            self.readerstop_activity.emit()
            self.ThreadMidiReader.stop() # test
            while self.ThreadMidiReader.isRunning():
                time.sleep(0.01)

        self.ThreadMidiReader = ClassThreadMidiReader(
            midifile, self.keys, self.channels, self.pParent
        )

        # 3 modes = player (just midi player) , chopin (wait keyboard) and passthrough
        self.midisong = self.ThreadMidiReader.LoadMidiSong(self.settings.GetMode())

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
        self.midisong.SetMode(mode)

    def GetMidiSong(self):
        if not self.ThreadMidiReader:
            return None
        return self.ThreadMidiReader.midisong

    def Playback(self):
        self.ThreadMidiReader.start()
        pass

    def Mode(self, playback=True):
        out_port = self.ThreadOutput.getport()
        self.ThreadInput.SetOutPort(out_port)
        self.keys["playback"] = playback

    # Send signals
    def SendStatusBar(self, msg):
        self.statusbar_activity.emit(msg)

    def SendLedFile(self, value):
        self.led_file_activity.emit(value)

    def StopPlayer(self):
        if self.ThreadMidiReader:
            self.ThreadMidiReader.stop() # test
        self.readerstop_activity.emit()

    def Stop(self):
        if self.ThreadMidiReader:
            self.ThreadMidiReader.stop()
            self.ThreadMidiReader = None

    def Panic(self):
        if self.ThreadOutput:
            self.ThreadOutput.panic()
        self.keys["key_on"] = 0
        self.statusbar_activity.emit("")

    def ResetOutput(self):
        if self.ThreadOutput:
             self.ThreadOutput.reset()

    def quit(self):
        if self.ThreadMidiReader:
            self.readerstop_activity.emit()
            self.ThreadMidiReader.stop() # test
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
