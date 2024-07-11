#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import mido
import glob
from os import path
from midi_input import midi_input
from midi_output import midi_output
from midi_file import midi_file
from settings import Settings
from  midi_numbers import number_to_note

class midi_main:
    midi_input = None
    midi_output = None
    midi_file =  midi_file()
    keys={"key_on":0}
    settings = Settings()

    PassThrough = False

    def __init__(self, pParent):
        self.pParent = pParent
        self.GetDevices()
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

    # List of midifiles from folder midi
    def GetMidiFiles(self):
        midifiles = []
        for file in sorted(glob.glob(self.settings.GetMidiPath()+"/*.mid")):
            midifiles.append(path.basename(file))
        return midifiles

    def SetMidifile(self, filename):
        self.midi_file.SetMidiFile(filename)

    def ConnectInput(self, in_device):
        # print("New NewInput")
        if self.midi_input:
            self.midi_input.stop()

        self.midi_input = midi_input(self.CallbackInput, self.pParent)
        self.midi_input.SetInput(in_device)
        self.midi_input.start()

    def CallbackInput(self, message):

        filter =['clock','stop','note_off']
        if message.type not in filter:
            print(f"midi_main:{message}")

        # Counter
        if message.type == 'note_on':
            self.keys['key_on'] +=1
        elif message.type == 'note_off':
            self.keys['key_on'] -=1

        # PassThrough
        if self.PassThrough:
            try:
                self.midi_output.send(message)
            except:
                print("ERROR")

        '''
        for key in self.inport:
            if key.type == 'note_on':
                print(f"NOTE={key.note}")
        '''

        # Playback



        # Informations

        if message.type == 'note_on' : # or message.type == 'note_off':
            note, octave = number_to_note(message.note)
            text=f" {note}{octave} [{message.note}]"
            self.pParent.PrintKeys(str(self.keys['key_on'])+text)
        elif message.type != 'note_off' :
            self.pParent.PrintKeys(message)

    def ConnectOutput(self, out_device):
        # print("New NewOutput")
        if self.midi_output:
            self.midi_output.stop()

        self.midi_output = midi_output(self.keys, self.pParent)
        self.midi_output.SetOutput(out_device)
        self.midi_output.start()

    def Playback(self):
        self.midi_file.start()

    def quit(self):
        print("midi_main:quit")
        self.midi_input.quit()
        self.midi_output.quit()
        exit(0)

