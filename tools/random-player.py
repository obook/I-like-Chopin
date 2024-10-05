#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 11:01:21 2024
@author: obooklage
Make virt.env : python3.8 -m venv midoplayer
source bin/activate
Spyder : pip install spyder-kernels==3.0.*
Spyder run : bash -c '~/.local/spyder-6/envs/spyder-runtime/bin/spyder'
Spyder Set Python : ~/midoplayer/bin/python
pip install mido pynput
"""

import os
import glob
import time
import random
from pynput.keyboard import Key, Listener
from mido import MidiFile, open_output

next_song = False


def on_release(key):
    global next_song
    if key == Key.esc:
        next_song = True
        # Stop listener
        return False


def PlayRandom(files):
    error_counter = 1
    index = random.randint(0, len(files))
    file = files[index]
    print(file)
    # Player
    for msg in MidiFile(file):
        time.sleep(msg.time)
        try:
            device.send(msg)
        except Exception as error:
            print(f"Player error {error_counter}: {error}")
            error_counter += 1
        if next_song:
            break


def SystainPedalCheck(file):
    sustain = 0
    tracks = 0

    try:
        # Tracks
        midi = MidiFile(file)
        for i, track in enumerate(midi.tracks):
            tracks += 1

        for msg in MidiFile(file):
            if msg.type == "control_change":
                # The sustain pedal sends CC 64 127
                # and CC 64 0 messages on channel 1
                if msg.value == 64:
                    sustain += 1
    except Exception as error:
        print(f"|!| CAN NOT READ {file} {error}")
        sustain = 0
        tracks = 0
        pass

    return tracks, sustain


my_path = os.path.expanduser("~/MUSIQUE/MIDI-02")
files = glob.glob(my_path + '/**/*.mid', recursive=True)
index = random.randint(0, len(files))

# Connect to synth
device = open_output("Midi Through:Midi Through Port-0", autoreset=True)

# Keyboard
listener = Listener(on_release=on_release)
listener.start()

# Play
PlayRandom(files)

print("stop")
device.close()
