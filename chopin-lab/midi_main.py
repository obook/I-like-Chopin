#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""

import mido
import glob
from os import path
from midi_input import ClassThreadInput
from midi_output import ClassThreadOutput
from midi_file import ClassThreadMidiFile
from settings import ClassSettings
from midi_numbers import number_to_note

from mido import MidiFile
import time

class midi_main:
    ThreadInput = None
    ThreadOutput = None
    ThreadMidiFile = None
    port_out = None
    keys={"key_on":0,"play":False}

    settings = ClassSettings()

    PassThrough = True

    temp_midifile = None

    def __init__(self, pParent):
        self.pParent = pParent
        self.GetDevices()
        self.keys={"key_on":0,"play":False}

        self.ThreadMidiFile = ClassThreadMidiFile(self.keys)

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
        self.ThreadMidiFile.SetMidiFile(filename)
        self.temp_midifile = filename

        self.keys['play']=True
        self.ThreadMidiFile.play(self.port_out)

    def ConnectInput(self, in_device):
        # print("New NewInput")
        if self.ThreadInput:
            self.ThreadInput.stop()

        self.ThreadInput = ClassThreadInput(self.keys, self.pParent)
        self.ThreadInput.SetInput(in_device)
        self.ThreadInput.start()
    '''
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


        for key in self.inport:
            if key.type == 'note_on':
                print(f"NOTE={key.note}")


        # Playback

        self.keys['play'] = True

        for msg in MidiFile(self.temp_midifile):
            time.sleep(msg.time)

            # Pause ?

            if msg.type == 'note_on':
                while not self.keys['key_on']: # Loop waiting keyboard
                    if not self.keys['play']:
                        break
                    time.sleep(msg.time)

            # Play
            try: # meta messages can't be send to ports
                if self.pParent.ChannelIsActive(msg.channel):
                    self.outport.send(msg)
            except:
                pass

            # Stop while running ?
            if not self.keys['play']:
                break

        # End of song
        self.Stop()


        # Informations

        if message.type == 'note_on' : # or message.type == 'note_off':
            note, octave = number_to_note(message.note)
            text=f" {note}{octave} [{message.note}]"
            self.pParent.PrintKeys(str(self.keys['key_on'])+text)
        elif message.type != 'note_off' :
            self.pParent.PrintKeys(message)
        '''
    def ConnectOutput(self, out_device):
        # print("New NewOutput")
        if self.ThreadOutput:
            self.ThreadOutput.stop()

        self.ThreadOutput = ClassThreadOutput(self.keys, self.pParent)
        self.ThreadOutput.SetOutput(out_device)
        self.port_out = self.ThreadOutput.start()

    def Playback(self):
        self.midi_file.start()

    def quit(self):
        print("midi_main:quit")
        self.ThreadInput.quit()
        self.ThreadOutput.quit()
        exit(0)

