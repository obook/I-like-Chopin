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

player_thread = None
keyboard_thread = None

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

    keys['key_on'] = 0

    player_thread = MidiPlayer(out_device, midifile, keys, pParent)
    player_thread.start()

    keyboard_thread = MidiKeyboard(in_device, keys, pParent)
    keyboard_thread.start()

def MidiStop():
    global player_thread
    global keyboard_thread

    keys['key_on'] = 0
    keys['run'] = False
    player_thread = None
    keyboard_thread = None

def MidiStatus():
    return keys['MidiPlayerRunning'],keys['MidiKeyboardRunning']

def MidiPanic():
    keys['key_on'] = 0
    if player_thread :
        player_thread.Panic()

