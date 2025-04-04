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
from threading import Thread
import platform
import os
import time
import mido

key_on = 0
# device = "Arturia KeyLab Essential 61 MID"
device_from = "out"  # VMPK
device_to = "Midi Through Port-0"
midisong = os.path.expanduser("~/Documents/GitHub/midi/MOZART WOLFGANG AMADEUS/Piano Sonata No. 11 in A major, KV 331_3_Alla turca-Allegretto.mid")

# Au moyen d'une classe
class LoopThread(Thread):
    def __init__(self, loop=1):
        super().__init__()
        self.loop = loop

    def run(self):
        print(self.loop)


# Thread direct
def threaded_output(name):
    global midisong, out_port
    started = False

    for msg in mido.MidiFile(midisong):

        # Wait keyboard
        start_time_loop = time.time()

        while not key_on:
            pass

        wait_time = time.time() - start_time_loop

        # Changer le temps à zéro si boucle attente suppérieure à msg.time
        if wait_time < msg.time:
            time.sleep(msg.time)

        try:
            if msg.type == "note_on" or msg.type == "note_off":
                if msg.channel == 0:
                    out_port.send(msg)
            else:
                out_port.send(msg)
        except:
           pass

    print("threaded_player %s: finishing", name)


def keyboard(msg):
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

    # print(f"Keys PRESSED = [{key_on}]", msg)


print("********* DEVICES OUTPUT")
for i, port_name in enumerate(mido.get_input_names()):
    if platform.system() == "Linux":  # cleanup linux ports
        port_name = port_name[: port_name.rfind(" ")]
    print(port_name)
print("********* DEVICES INPUT")
for i, port_name in enumerate(mido.get_output_names()):
    if platform.system() == "Linux":  # cleanup linux ports
        port_name = port_name[: port_name.rfind(" ")]
    print(port_name)
print("*********")

x = Thread(target=threaded_output, args=(1,))
x.start()

try:
    print(f"Connect from {device_from}")
    in_port = mido.open_input(device_from, callback=keyboard)
except Exception as error:
    raise f"ERROR INPUT {error}"

try:
    print(f"Connect to {device_to}")
    out_port = mido.open_output(device_to)
except Exception as error:
    in_port.close()
    raise f"ERROR OUTPUT {error}"

print("Ready...")
while True:
    pass

# x.join()
