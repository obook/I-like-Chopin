#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 11:01:21 2024
@author: obooklage
Make virt.env : python3.8 -m venv midoplayer
source bin/activate
pip install spyder-kernels==3.0.* mido pynput
Spyder run : bash -c '~/.local/spyder-6/envs/spyder-runtime/bin/spyder'
Spyder Set Python : ~/midoplayer/bin/python

Todo : sustain is not good count
"""

import os
import glob
import time
import random
from pynput.keyboard import Key, Listener
from mido import MidiFile, open_output

next_song = False
paused = False


def on_press(key):
    global paused
    if key == Key.space:
        if paused:
            paused = False
        else:
            paused = True
            print("Paused...")


def on_release(key):
    global next_song
    if key == Key.esc:
        next_song = True
        # Stop listener
        # return False


def GetRamdom(files, device):
    print("START GetRamdom")
    global next_song
    animation = ["-", "/", "-", "\\"]
    animation_index = 0
    while len(files):
        print(f"Searching {animation[animation_index]} "
              "({len(files)-1})\r", end="")
        animation_index += 1
        if animation_index > len(animation)-1:
            animation_index = 0
        index = random.randint(0, len(files)-1)
        file = files[index]
        tracks, sustain = SystainPedalCheck(file)
        if sustain > 20 and tracks <= 3:
            print(f"FOUND {file}, press Esc for next song...")
            print(f"tracks={tracks} sustain={sustain}")
            Play(file, device)
            next_song = False
            files.pop(index)
        else:
            print(f"REJECTED {file} tracks={tracks} sustain={sustain}")


def Play(file, device):
    print("Playing... Press Esc for next song or space for pause\r", end="")
    error_counter = 0
    start_song = False
    # Player
    for msg in MidiFile(file):

        while paused:
            time.sleep(0.1)

        if not start_song and msg.type == "note_on":
            start_song = True
        if start_song:
            time.sleep(msg.time)
        try:
            device.send(msg)
        except Exception as error:
            # print(f"Player error {error_counter}: {error}", end="")
            error_counter += 1
        if next_song:
            print("Stop !    ")
            device.panic()
            device.reset()
            break


def SystainPedalCheck(file):
    # print(f"START SystainPedalCheck {file}")
    sustain = 0
    tracks = 0
    try:
        # Tracks
        midi = MidiFile(file)
        for i, track in enumerate(midi.tracks):
            tracks += 1

        for msg in MidiFile(file):
            if msg.type == "control_change":
                sustain += 1
    except Exception as error:
        print(f"|!| CAN NOT READ {file} {error}")
        sustain = 0
        tracks = 0

    # print(f"End of SystainPedalCheck, tracks={tracks} sustain={sustain}")

    return tracks, sustain


my_path = os.path.expanduser("~/MUSIQUE")  # Put your midi path here
files = sorted(glob.glob(os.path.join(my_path, "**", "*.mid"), recursive=True))

print(f"Scan for {len(files)} files in {my_path}")

# Connect to synth
device = open_output("Midi Through:Midi Through Port-0", autoreset=True)

# Keyboard
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()

# Play
GetRamdom(files, device)

print("stop")
device.close()
