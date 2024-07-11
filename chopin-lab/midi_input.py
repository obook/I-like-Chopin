# This Python file uses the following encoding: utf-8

from mido import open_input
from threading import Thread

class midi_input(Thread):
    inport = None
    running = False

    def __init__(self, keys, CallbackInput, pParent):
        Thread.__init__( self )
        self.keys = keys
        self.CallbackInput = CallbackInput
        self.pParent = pParent

    def SetInput(self, in_device):
        self.in_device = in_device

    def run(self):
        self.stop()
        self.inport = open_input(self.in_device, callback=self.CallbackInput)
        self.running = True

    def stop(self):
        self.running = False
        if self.inport :
            self.inport.close()
            self.inport = None

    def quit(self):
        print("midi_input:quit")
        self.stop()
        exit(0)
