# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from mido import open_input

# Wait keys from keyboard
def ThreadKeyBoard(in_device, keys, pParent):
    global inport

    keys['ThreadKeyBoard'] = True

    # NON-BLOCKING
    inport = open_input(in_device)
    print(f'Wait keys from "{in_device}...')
    while True: # non-blocking
        if not keys['run']:
            print('ThreadKeyBoard closing port and stop.')
            inport.close()
            keys['ThreadKeyBoard'] = False
            return

        for key in inport.iter_pending():

            if key.type == 'note_on':
                keys['key_on'] +=1
                # Security ; press key C#4 (49) for pause
                if key.note == 49 :
                    keys['key_on'] = 0

            elif key.type == 'note_off':
                keys['key_on'] -=1

            if keys['key_on'] <0 : # rare, in case of missing key on
                keys['key_on'] = 0


            #print(f"keys on:{keys['key_on']}\r", end="")
            pParent.PrintKeys(str(keys['key_on']))

            #if key.type == 'key_on' or key.type == 'note_off':
            #    note, octave = number_to_note(key.note)
            #    print(f"{key.type} {note}{octave} ({key.note}) [{keys['key_on']} keys on]")

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
                    keys['key_on'] +=1
                    # note, octave = number_to_note(key.note)
                    # print(f"{key.note}={note}{octave}")
                    # Security ; press key C#4 (49) for pause
                    if key.note == 49 :
                        keys['key_on'] = 0

                elif key.type == 'note_off':
                    keys['key_on'] -=1

                if keys['key_on'] <0 : # rare, in case of missing key on
                    keys['key_on'] = 0

                print(f"keys on:{keys['key_on']}\r", end="")
    except:
        print(f'Error connect to input "{in_device}"')
  '''
    keys['ThreadKeyBoard'] = False
