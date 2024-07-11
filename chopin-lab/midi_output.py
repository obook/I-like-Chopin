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

        self.stop()
        try:
            self.outport = open_output(self.out_device)
        except:
            self.outport = None
            print(f"midi_output open [{self.out_device}] ERROR")
            return

        print(f"midi_output:run open_output [{self.out_device}] READY")

    def stop(self):
        if self.outport :
            self.outport.close()
            self.outport = None

    def send(self, message):
        self.outport.send(message)

    def quit(self):
        print("midi_output:quit")
        self.stop()
        exit(0)
