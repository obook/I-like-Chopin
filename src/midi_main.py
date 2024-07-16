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
from midi_file import ClassThreadMidiFile
from settings import ClassSettings

class ClassMidiMain:

    keys={"key_on":0,"playback":True,"tempo":0,"humanize":0}

    # Threads
    ThreadInput = None
    ThreadOutput = None
    ThreadMidiFile = None

    midifile = None
    tracks = None

    settings = ClassSettings()

    def __init__(self, pParent, tracks):
        self.pParent = pParent
        self.tracks = tracks

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

        for i, port_name in enumerate(mido.get_ioport_names()):
            clean_port_name = port_name[:port_name.rfind(' ')]
            IOPorts.append(clean_port_name)

        print("IOPorts=",IOPorts)

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

        self.SetMidifile(self.midifile)

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

    def SetMidifile(self, filename):
        self.midifile = filename

        if self.ThreadMidiFile:
            self.ThreadMidiFile.stop()
            self.ThreadMidiFile = None

        self.ThreadMidiFile = ClassThreadMidiFile(self.keys, self.tracks)
        self.ThreadMidiFile.SetMidiFile(filename)

        if self.ThreadOutput:
            port = self.ThreadOutput.getport()
            self.ThreadMidiFile.SetMidiPort(port)
            self.ThreadMidiFile.start()

    def MidifileState(self):
        if self.ThreadMidiFile:
            return(self.ThreadMidiFile.active())
        return False

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

    def quit(self):
        print("midi_main:quit")

        if self.ThreadMidiFile:
            self.ThreadMidiFile.SetMidiPort(None) # stop send
            self.ThreadMidiFile.stop()
            self.ThreadMidiFile = None

        if self.ThreadInput:
            self.ThreadInput.stop()
            self.ThreadInput = None

        if self.ThreadOutput:
            self.ThreadOutput.panic
            self.ThreadOutput.stop()
            self.ThreadOutput = None



