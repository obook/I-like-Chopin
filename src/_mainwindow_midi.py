#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
from midi_main import ClassMidiMain
from midi_files import ClassMidiFiles


class midi:

    Midi = None  # Main engine
    midisong = None  # current midisong
    lastmidifile = None
    nextmidifile = None
    history_index = -1
    midifiles_dict = {}
    Midifiles = ClassMidiFiles()

    ChannelsList = [False] * 16

    # Devices
    Inputs = []
    Outputs = []
    InputsOutputs = []
    midi_controller = None

    def _midi_init(self):
        # Midi class
        self.Midi = ClassMidiMain(self, self.ChannelsList)
        self.Inputs, self.Outputs, self.InputsOutputs = self.Midi.GetDevices()

    def Panic(self):
        self.Midi.Panic()
