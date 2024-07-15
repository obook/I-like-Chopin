#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import mido
import glob
from os import path
#from midi_numbers import number_to_note
from midi_keyboard import MidiKeyboard
from midi_player import MidiPlayer
from midi_passthrough import MidiPassthrough
from settings import GetMidiPath, WarningNoMidifile
import platform

class MidiMain():
    player_thread = None
    keyboard_thread = None
    passthrough_thread = None
    keys = None

    def __init__( self, pParent ):
        self.pParent = pParent
        self.keys={"key_on":0,'run':False,'MidiPlayerRunning':False,'MidiKeyboardRunning':False}
        print(f"MidiMain:platform.system()=[{platform.system()}]") # tested = "Linux" , "Windows"

    def GetDevices(self):
        Inputs = []
        Outputs = []

        for i, port_name in enumerate(mido.get_output_names()):
            if platform.system() == "Linux": # cleanup linux ports
                port_name = port_name[:port_name.rfind(' ')]
            Outputs.append(port_name)

        for i, port_name in enumerate(mido.get_input_names()):
            if platform.system() == "Linux": # cleanup linux ports
                port_name = port_name[:port_name.rfind(' ')]
            Inputs.append(port_name)

        return Inputs, Outputs

    # List of midifiles from folder midi
    def GetMidiFiles(self):
        midifiles = []
        for file in sorted(glob.glob(GetMidiPath()+"/*.mid")):
            midifiles.append(path.splitext(path.basename(file))[0])
        if not midifiles:
            WarningNoMidifile()
        return midifiles

    def MidiStart(self, in_device, out_device, midifile, pParent):

        self.MidiStop()

        self.keys['key_on'] = 0 # 1 ?
        self.keys['run'] = True

        self.player_thread = MidiPlayer(out_device, midifile, self.keys, pParent)
        self.player_thread.start()

        self.keyboard_thread = MidiKeyboard(in_device, self.keys, self.pParent)
        self.keyboard_thread.start()

    def MidiPassthroughStart(self, in_device, out_device):
        self.MidiStop()
        self.keys['run'] = True
        self.passthrough_thread = MidiPassthrough(in_device, out_device, self.keys, self.pParent)
        self.passthrough_thread.start()

    def MidiPassthroughStop(self):
        self.MidiStop()
        self.keys['run'] = False

    def MidiStatus(self):
        return self.keys['MidiPlayerRunning'],self.keys['MidiKeyboardRunning']

    def MidiPanic(self):
        self.keys['key_on'] = 0
        if self.player_thread :
            self.player_thread.Panic()

    def MidiStop(self):
        self.keys['key_on'] = 0
        self.keys['run'] = False

        if self.player_thread:
            self.player_thread.Stop()
            self.player_thread = None

        if self.keyboard_thread :
            self.keyboard_thread.Stop()
            self.keyboard_thread = None

        if self.passthrough_thread:
            self.passthrough_thread.Stop()
            self.passthrough_thread = None

