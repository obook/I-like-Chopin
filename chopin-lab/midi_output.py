# This Python file uses the following encoding: utf-8

from threading import Thread
from mido import open_output

class midi_output(Thread):
    outport = None
    def __init__(self, keys, pParent):
        Thread.__init__( self )
        self.keys = keys
        self.pParent = pParent

    def SetOutput(self, out_device):
        self.out_device = out_device

    def run(self):
        print("midi_output:run")
        if self.outport :
            self.outport.close()
        self.outport = open_output(self.out_device)


