# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

import mido
import glob
from threading import Thread
#from midi_numbers import number_to_note
from midi_keyboard import ThreadKeyBoard
from midi_player import ThreadPlayer

outport = False
inport = True # permet de quitter (sortir de la boucle) sans
keys={"note_on":0,'run':False,'ThreadPlayer':False,'ThreadKeyBoard':False}

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
        midifiles.append(file)
    return midifiles

def MidiStart(in_device, out_device, midifile, pParent):
    print("MidiStart")
    player_thread = Thread(target=ThreadPlayer, args=(out_device, midifile, keys, pParent))
    player_thread.start()
    keyboard_thread = Thread(target=ThreadKeyBoard, args=(in_device, keys, pParent))
    keyboard_thread.start()

def MidiStop():
    keys['note_on'] = 1
    keys['run'] = False

def MidiStatus():
    return keys['ThreadPlayer'],keys['ThreadKeyBoard']

def MidiPanic():
    keys['note_on'] = 0
    if outport :
        outport.panic()

