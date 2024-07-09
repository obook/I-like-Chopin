# This Python file uses the following encoding: utf-8

from mido import open_input
from threading import Thread

class midi_input(Thread):
    inport = None

    def __init__(self, keys, pParent):
        Thread.__init__( self )
        self.keys = keys
        self.pParent = pParent

    def SetInput(self, in_device):
        self.in_device = in_device

    def run(self):
        if self.inport :
            self.inport.close()
        try:
            self.inport = open_input(self.in_device)
        except:
            self.inport = None

        print("midi_input:run open_input")

        while True: # non-blocking
            for key in self.inport.iter_pending():
                if key.type == 'note_on':
                    print(f"NOTE={key.note}")
