#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# if __name__ == "__main__":
#     pass

import mido
import glob
from os import path
#from midi_numbers import number_to_note
from midi_keyboard import MidiKeyboard
from midi_player import MidiPlayer

# wHAt?!
outport = False
inport = True # permet de quitter (sortir de la boucle) sans

keys={"key_on":0,'run':False,'MidiPlayerRunning':False,'MidiKeyboardRunning':False}

def GetDevices():

    Inputs = []
    Outputs = []

    for i, port_name in enumerate(mido.get_output_names()):
        Outputs.append(port_name)
    for i, port_name in enumerate(mido.get_input_names()):
        Inputs.append(port_name)

    return Inputs, Outputs

# List of midifiles from folder midi
def GetMidiFiles():
    midifiles = []
    for file in sorted(glob.glob("midi/*.mid")):
        midifiles.append(path.splitext(path.basename(file))[0])
    return midifiles

def MidiStart(in_device, out_device, midifile, pParent):
    print("MidiStart")

    player_thread = MidiPlayer(out_device, midifile, keys, pParent)
    player_thread.start()

    keyboard_thread = MidiKeyboard(in_device, keys, pParent)
    keyboard_thread.start()

def MidiStop():
    keys['key_on'] = 1 # get midifile first data
    keys['run'] = False

def MidiStatus():
    return keys['MidiPlayerRunning'],keys['MidiKeyboardRunning']

def MidiPanic():
    keys['key_on'] = 0
    if outport :
        outport.panic()

