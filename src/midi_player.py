#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# if __name__ == "__main__":
#     pass

from mido import MidiFile, open_output
import time
from threading import Thread

# Send midi to synth if keys from keyboard are on
class MidiPlayer( Thread ):
    outport = None

    def __init__( self, out_device, midifile,  keys, pParent ):
        Thread.__init__( self )
        self.out_device = out_device
        self.midifile = midifile
        self.keys = keys
        self.pParent = pParent

    def run( self ):

        self.keys['run'] = True
        self.keys['key_on'] = 0

        try:
            self.outport = open_output(self.out_device)
            self.pParent.PrintBrowser(f'MidiPlayer to [{self.out_device}]')
        except:
            self.pParent.PrintBrowser(f"MidiPlayer:Error connect to {self.out_device}")
            return

        self.keys['MidiPlayerRunning'] = True

        midi = MidiFile(self.midifile)

        self.pParent.PrintBrowser(f"{self.midifile} = {round(midi.length/60,2)} minutes ")

        for i, track in enumerate(midi.tracks):
            self.pParent.PrintBrowser('Track {}: {}'.format(i, track.name))

        for msg in MidiFile(self.midifile):
            time.sleep(msg.time)

            # Pause ?
            if msg.type == 'note_on':
                while not self.keys['key_on']:
                    # Stop while pausing ?
                    if not self.keys['run']:
                        break
                    time.sleep(msg.time)

            # Play
            try: # meta messages can't be send to ports
                if self.pParent.ChannelIsActive(msg.channel):
                    self.outport.send(msg)
            except:
                pass

            # Stop while running ?
            if not self.keys['run']:
                break

        # End of song
        self.Stop()


    def Panic(self):
        if self.outport:
            self.outport.panic()

    def Stop(self):

        if self.outport:
            self.pParent.PrintBrowser('MidiPlayer stop')
            self.outport.panic()
            self.outport.close()
            self.outport = None

        self.keys['MidiPlayerRunning'] = False

