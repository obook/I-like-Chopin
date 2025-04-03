#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 09:49:16 2025
@author: obooklage

Test USB3 midi input for raspberry pi5 and Arturia Keylab 61 :

    -> missing keys (USB3 midi event) with QT6/QThread (throttle)
    -> NO missing keys with this program

A USB bug with QT6 and pi5 (8Go) ?

"""
import platform
import mido

key_on = 0


def mycallback(msg):
    global key_on
    # Keys pressed counter
    if msg.type == "note_on":
        if msg.velocity:
            key_on += 1
        else:
            # A MIDI Note On with a velocity of 0 is regarded as a Note Off.
            # That is part of the MIDI Standard
            key_on -= 1

    elif msg.type == "note_off":
        key_on -= 1
        if key_on < 0:
            key_on = 0

    # Rares cases
    if key_on < 0:
        key_on = 0

    print(f"Keys PRESSED = [{key_on}]", msg)


print("********* DEVICES OUTPUT")
for i, port_name in enumerate(mido.get_input_names()):
    if platform.system() == "Linux":  # cleanup linux ports
        port_name = port_name[: port_name.rfind(" ")]
    print(port_name)
print("*********")

try:
    in_port = mido.open_input("Arturia KeyLab Essential 61 MID", callback=mycallback)
except Exception as error:
    raise f"ERROR {error}"

while True:
    pass
