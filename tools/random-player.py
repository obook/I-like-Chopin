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
from pynput.keyboard import Key, Listener
from mido import MidiFile, open_output

end = False

def on_release(key):
    global end
    if key == Key.esc:
        end = True
        # Stop listener
        return False

my_path = os.path.expanduser("~/MUSIQUE/MIDI-02")
files = glob.glob(my_path + '/**/*.mid', recursive=True)
file = files[0] # Just first for tests

# Connect to synth
device = open_output("Midi Through:Midi Through Port-0", autoreset=True)

listener = Listener(on_release=on_release)
listener.start()
error_counter = 1
print("play, press Esc for quit")
# Player
for msg in MidiFile(file):
    time.sleep(msg.time)
    try:
        device.send(msg)
    except Exception as error:
        print(f"Player error {error_counter}: {error}")
        error_counter += 1
    if end:
        break

print("stop")
