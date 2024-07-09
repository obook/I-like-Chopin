# This Python file uses the following encoding: utf-8

import mido
from midi_input import midi_input
from midi_output import midi_output

class midi_main:
    def __init__(self, pParent):
        self.pParent = pParent
        self.GetDevices()
        self.midi_input = None
        self.keys={"key_on":0,'run':False,'MidiPlayerRunning':False,'MidiKeyboardRunning':False}

    def GetDevices(self):
        Inputs = []
        Outputs = []
        for i, port_name in enumerate(mido.get_output_names()):
            Outputs.append(port_name)
        for i, port_name in enumerate(mido.get_input_names()):
            Inputs.append(port_name)
        # print("Inputs=", Inputs)
        # print("Outputs=", Outputs)
        return Inputs, Outputs

    def NewInput(self):
        print("New NewInput")

        self.midi_input = midi_input(self.keys, self.pParent)
        self.midi_input.SetInput('Arturia KeyStep 37:Arturia KeyStep 37 MIDI 1 28:0')
        self.midi_input.start()

    def NewOutput(self):
        print("New NewOutput")

        self.midi_output = midi_output(self.keys, self.pParent)
        self.midi_output.SetOutput('FLUID Synth (Titanic):Synth input port (Titanic:0) 131:0')
        self.midi_output.start()

