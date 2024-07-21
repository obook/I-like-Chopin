#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import mido
import glob
import platform

from os import path
from midi_input import ClassThreadInput
from midi_output import ClassThreadOutput
from midi_reader import ClassThreadMidiReader
from settings import ClassSettings
import uuid

class ClassMidiMain:

    keys={"key_on":0,"playback":True,"speed":0,"humanize":0}

    # Threads
    ThreadInput = None
    ThreadOutput = None
    ThreadMidiFile = None

    midisong = None
    channels = None
    uuid = None

    settings = ClassSettings()

    def __init__(self, pParent, channels):
        self.pParent = pParent
        self.channels = channels
        self.uuid = uuid.uuid4()
        print(f"MidiMain {self.uuid} created")

    def __del__(self):
        print(f"MidiMain {self.uuid} destroyed")

    def GetDevices(self):
        Inputs = []
        Outputs = []
        IOPorts = []

        for i, port_name in enumerate(mido.get_output_names()):
            if platform.system() == "Linux": # cleanup linux ports
                port_name = port_name[:port_name.rfind(' ')]
            Outputs.append(port_name)

        for i, port_name in enumerate(mido.get_input_names()):
            if platform.system() == "Linux": # cleanup linux ports
                port_name = port_name[:port_name.rfind(' ')]
            Inputs.append(port_name)

        for i, port_name in enumerate(mido.get_ioport_names()): # not used
            if platform.system() == "Linux": # cleanup linux ports
                port_name = port_name[:port_name.rfind(' ')]
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

        if self.ThreadOutput:
            self.ThreadOutput.stop()

        self.ThreadOutput = ClassThreadOutput(out_device, self.keys, self.pParent)
        self.port_out = self.ThreadOutput.start()

        self.SetMidiSong(self.midisong)

    def ConnectOutputState(self):
        if self.ThreadOutput:
            return self.ThreadOutput.active()
        return False

    # List of midifiles from folder midi (see json file created)
    def GetMidiFiles(self):
        midifiles = []
        for file in sorted(glob.glob(self.settings.GetMidiPath()+"/*.mid")):
            midifiles.append(path.basename(file))
        return midifiles

    def SetMidiSong(self, midisong):
        self.midisong = midisong
        self.pParent.SetWindowName()

        if self.ThreadMidiFile:
            self.ThreadMidiFile.stop()
            self.ThreadMidiFile = None

        self.ThreadMidiFile = ClassThreadMidiReader(self.midisong, self.keys, self.channels)
        tracks = self.ThreadMidiFile.SetMidiSong(self.midisong)

        if self.ThreadOutput:
            port = self.ThreadOutput.getport()
            self.ThreadMidiFile.SetMidiPort(port)
            self.ThreadMidiFile.start()

        return tracks # array of tracks names

    def Playback(self):
        self.ThreadMidiFile.start()
        pass

    def Mode(self, playback=True):
        out_port = self.ThreadOutput.getport()
        self.ThreadInput.SetOutPort(out_port)
        self.keys['playback']= playback

    def Stop(self):
        if self.ThreadMidiFile :
            self.ThreadMidiFile.quit()
            self.ThreadMidiFile = None

    def Panic(self):
        if self.ThreadOutput:
            self.ThreadOutput.panic()
        self.keys['key_on'] = 0

    def quit(self):
        if self.ThreadMidiFile:
            self.ThreadMidiFile.SetMidiPort(None) # stop send
            self.ThreadMidiFile.stop()
            self.ThreadMidiFile = None

        if self.ThreadInput:
            self.ThreadInput.stop()
            self.ThreadInput = None

        if self.ThreadOutput:
            self.ThreadOutput.panic()
            self.ThreadOutput.stop()
            self.ThreadOutput = None

        if self.midisong:
            self.midisong.SetActive(False)
            self.midisong = None

