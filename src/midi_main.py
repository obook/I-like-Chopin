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

import mido
from midi_input import ClassThreadInput
from midi_output import ClassThreadOutput
from midi_reader import ClassThreadMidiReader


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

    settings = None

    def __init__(self, pParent, channels):
        self.pParent = pParent
        self.settings = self.pParent.settings
        self.channels = channels
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

    def ConnectInputState(self):
        if self.ThreadInput:
            return self.ThreadInput.active()
        return False

    def ConnectOutput(self, out_device):

        if self.ThreadMidiReader:
            self.ThreadMidiReader.SetMidiPort(None)

        self.ThreadOutput = ClassThreadOutput(out_device, self.pParent)
        self.ThreadOutput.start()

    def ConnectOutputState(self):
        if self.ThreadOutput:
            return self.ThreadOutput.active()
        return False

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
            self.ThreadMidiReader.stop()
            self.ThreadMidiReader = None

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

    def Stop(self):
        if self.ThreadMidiReader:
            self.ThreadMidiReader.stop()
            self.ThreadMidiReader = None

    def Panic(self):
        if self.ThreadOutput:
            self.ThreadOutput.panic()
        self.keys["key_on"] = 0
        self.pParent.SetStatusBar("") # via slot ?

    def quit(self):
        if self.ThreadMidiReader:
            self.ThreadMidiReader.stop()
            # self.ThreadMidiReader.SetMidiPort(None)  # stop send
            # NOT recommanded self.ThreadMidiReader.terminate();
            self.ThreadMidiReader = None

        if self.ThreadInput:
            self.ThreadInput.stop()
            self.ThreadInput = None

        if self.ThreadOutput:
            self.ThreadOutput.panic()
            self.ThreadOutput.stop()
            self.ThreadOutput = None
