# This Python file uses the following encoding: utf-8

import mido
from midi_input import midi_input
from midi_output import midi_output

class midi_main:
    midi_input = None
    midi_output = None
    def __init__(self, pParent):
        self.pParent = pParent
        self.GetDevices()
        self.keys={"key_on":0,'run':False,'MidiPlayerRunning':False,'MidiKeyboardRunning':False}

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

    def ConnectInput(self, in_device):
        # print("New NewInput")
        if self.midi_input:
            self.midi_input.stop()

        self.midi_input = midi_input(self.keys, self.CallbackInput, self.pParent)
        self.midi_input.SetInput(in_device)
        self.midi_input.start()

    def CallbackInput(self, message):
        filter =['clock','stop','note_off']
        if message.type not in filter:
            print(f"midi_main:{message}")

        try:
            self.midi_output.send(message)
        except:
            printr("ERROR")

        '''
        for key in self.inport:
            if key.type == 'note_on':
                print(f"NOTE={key.note}")
        '''

    def ConnectOutput(self, out_device):
        # print("New NewOutput")
        if self.midi_output:
            self.midi_output.stop()

        self.midi_output = midi_output(self.keys, self.pParent)
        self.midi_output.SetOutput(out_device)
        self.midi_output.start()

    def PassThrough(self):
        pass

    def quit(self):
        print("midi_main:quit")
        self.midi_input.quit()
        self.midi_output.quit()
        exit(0)

