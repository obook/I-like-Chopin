#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import mido
import glob
from os import path
from midi_input import ClassThreadInput
from midi_output import ClassThreadOutput
from midi_file import ClassThreadMidiFile
from settings import ClassSettings

class ClassMidiMain:

    keys={"key_on":0}

    ThreadInput = None
    ThreadOutput = None
    ThreadMidiFile = None
    midifile = None
    port_out = None
    tracks = None

    settings = ClassSettings()

    PassThrough = True

    def __init__(self, pParent, tracks):
        self.pParent = pParent
        self.GetDevices()
        self.tracks = tracks
        self.keys={"key_on":0}

    def GetDevices(self):
        Inputs = []
        Outputs = []

        for i, port_name in enumerate(mido.get_output_names()):
            clean_port_name = port_name[:port_name.rfind(' ')]
            Outputs.append(clean_port_name)

        for i, port_name in enumerate(mido.get_input_names()):
            clean_port_name = port_name[:port_name.rfind(' ')]
            Inputs.append(clean_port_name)

        return Inputs, Outputs

    def ConnectInput(self, in_device):
        if self.ThreadInput:
            self.ThreadInput.stop()

        self.ThreadInput = ClassThreadInput(self.keys, self.pParent)
        self.ThreadInput.SetInput(in_device)
        self.ThreadInput.start()

    def ConnectOutput(self, out_device):
        if self.ThreadOutput:
            self.ThreadOutput.stop()
        if self.ThreadMidiFile:
            self.ThreadMidiFile.quit()

        self.ThreadOutput = ClassThreadOutput(self.keys, self.pParent)
        self.ThreadOutput.SetOutput(out_device)
        self.port_out = self.ThreadOutput.start()

        if self.SetMidifile :
            self.SetMidifile(self.midifile)

    # List of midifiles from folder midi (see json file created)
    def GetMidiFiles(self):
        midifiles = []
        for file in sorted(glob.glob(self.settings.GetMidiPath()+"/*.mid")):
            midifiles.append(path.basename(file))
        return midifiles

    def SetMidifile(self, filename):
        if self.ThreadMidiFile:
            self.ThreadMidiFile.quit()
            self.ThreadMidiFile = None

        self.ThreadMidiFile = ClassThreadMidiFile(self.keys)
        self.ThreadMidiFile.SetMidiFile(filename, self.tracks)
        self.midifile = filename

        if self.ThreadOutput:
            port = self.ThreadOutput.getport()
            self.ThreadMidiFile.SetMidiPort(port)
            self.ThreadMidiFile.start()

    def Playback(self):
        self.ThreadMidiFile.start()
        pass

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
            self.ThreadMidiFile.quit()
            self.ThreadMidiFile = None

        if self.ThreadInput:
            self.ThreadInput.quit()
            self.ThreadInput = None

        if self.ThreadOutput:
            self.ThreadOutput.panic
            self.ThreadOutput.quit()
            self.ThreadOutput = None



