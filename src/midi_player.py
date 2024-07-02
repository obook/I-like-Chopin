# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from mido import MidiFile, open_output
import time
from threading import Thread

# Send midi to synth if keys from keyboard are on
class MidiPlayer( Thread ):

    def __init__( self, out_device, midifile,  keys, pParent ):
        Thread.__init__( self )
        self.out_device = out_device
        self.midifile = midifile
        self.keys = keys
        self.pParent = pParent

    def run( self ):
        global outport

        print("ThreadPlayer")

        self.keys['run'] = True
        self.keys['key_on'] = 0

        try:
            outport = open_output(self.out_device)
        except:
            print(f'Error connect to output "{self.out_device}"')
            exit()

        print(f'Connected to "{self.out_device}"')

        self.keys['MidiPlayerRunning'] = True

        midi = MidiFile(self.midifile)

        print("Duration=", round(midi.length/60,2), "min")

        for msg in MidiFile(self.midifile):
            time.sleep(msg.time)

            # Pause ?
            if msg.type == 'note_on':
                while not self.keys['key_on']:
                   time.sleep(msg.time)

            # meta messages can't be send to ports
            # Play
            try:
                if self.pParent.ChannelIsActive(msg.channel):
                    outport.send(msg)
            except:
                pass

            # Stop ?
            if not self.keys['run']:
                print('MidiPlayer closing port and stop.')
                outport.panic()
                outport.close()
                self.keys['MidiPlayerRunning'] = False
                return

        # End of song
        self.keys['run'] = False
        self.keys['MidiPlayerRunning'] = False
        outport.panic()
        outport.close()
        print("MidiPlayer:Midifile ended.")
        self.pParent.Stop()
