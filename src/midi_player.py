# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

import mido
from mido import MidiFile
import time

# Send midi to synth if keys from keyboard are on
def ThreadPlayer(out_device, midifile,  keys, pParent): # pParent = QMainWindow
    global outport

    print("ThreadPlayer")

    keys['run'] = True
    keys['note_on'] = 0

    try:
        outport = mido.open_output(out_device)
    except:
        print(f'Error connect to output "{out_device}"')
        exit()

    print(f'Connected to "{out_device}"')

    keys['ThreadPlayer'] = True

    midi = MidiFile(midifile)

    print("Duration=", round(midi.length/60,2), "min")

    for msg in mido.MidiFile(midifile):
        time.sleep(msg.time)

        # Pause ?
        if msg.type == 'note_on':
            while not keys['note_on']:
               time.sleep(msg.time)

        # meta messages can't be send to ports
        # Play
        try:
            if pParent.ChannelIsActive(msg.channel):
                outport.send(msg)
        except:
            pass

        # Stop ?
        if not keys['run']:
            print('ThreadPlayer closing port and stop.')
            outport.panic()
            outport.close()
            keys['ThreadPlayer'] = False
            return

    # End of song
    keys['run'] = False
    keys['ThreadPlayer'] = False
    outport.panic()
    outport.close()
    print("ThreadPlayer:Midifile ended.")
