# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

import mido
import glob
from threading import Thread
import time
from midi_numbers import number_to_note

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

# Wait keys from keyboard
def ThreadKeyBoard(in_device, keys):
    global inport

    keys['ThreadKeyBoard'] = True

    '''
    # NON-BLOCKING
    inport = mido.open_input(in_device)
    print(f'Wait keys from "{in_device}...')
    while True: # non-blocking
        if not keys['run']:
            print('ThreadKeyBoard closing port and stop.')
            inport.close()
            keys['ThreadKeyBoard'] = False
            return

        for key in inport.iter_pending():
            print(f"KEY = {key}")
            if key.type == 'note_on':
                keys['note_on'] +=1

            elif key.type == 'note_off':
                keys['note_on'] -=1

            if keys['note_on'] <0 : # rare, in case of missing key on
                keys['note_on'] = 0

            #if key.type == 'note_on' or key.type == 'note_off':
            #    note, octave = number_to_note(key.note)
            #    print(f"{key.type} {note}{octave} ({key.note}) [{keys['note_on']} keys on]")
    '''

    # BLOCKING
    try:
        with mido.open_input(in_device) as inport:
            print(f'Wait keys from "{in_device}...')
            for key in inport: # attente clavier

                if not keys['run']:
                    print('ThreadKeyBoard closing port and stop.')
                    inport.close()
                    keys['ThreadKeyBoard'] = False
                    return

                elif key.type == 'note_on':
                    keys['note_on'] +=1
                    note, octave = number_to_note(key.note)
                    print(f"{key.note}={note}{octave}")
                    # Security ; press key C#4 (49) for pause
                    if key.note == 49 :
                        keys['note_on'] = 0

                elif key.type == 'note_off':
                    keys['note_on'] -=1

                if keys['note_on'] <0 : # rare, in case of missing key on
                    keys['note_on'] = 0

                print(f"keys on:{keys['note_on']}")
    except:
        print(f'Error connect to input "{in_device}"')

    keys['ThreadKeyBoard'] = False

# Send midi to synth if keys from keyboard are on
def ThreadPlayer(in_device, out_device, midifile, pParent): # pParent = QMainWindow
    global outport

    keys['run'] = True
    keys['note_on'] = 0

    try:
        outport = mido.open_output(out_device)
    except:
        print(f'Error connect to output "{out_device}"')
        exit()

    print(f'Connected to "{out_device}"')

    keyboard_thread = Thread(target=ThreadKeyBoard, args=(in_device, keys))
    keyboard_thread.start()

    keys['ThreadPlayer'] = True

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
            # print(f"exception msg={msg}")
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
    print("ThreadPlayer:Mdifile ended.")

def MidiStop():
    keys['note_on'] = 1
    keys['run'] = False

def MidiStatus():
    return keys['ThreadPlayer'],keys['ThreadKeyBoard']

def MidiPanic():
    keys['note_on'] = 0
    if outport :
        outport.panic()

