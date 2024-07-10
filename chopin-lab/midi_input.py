# This Python file uses the following encoding: utf-8

from mido import open_input
from threading import Thread

class midi_input(Thread):
    inport = None
    running = False

    def __init__(self, keys, pParent):
        Thread.__init__( self )
        self.keys = keys
        self.pParent = pParent

    def SetInput(self, in_device):
        self.in_device = in_device

    def run(self):
        self.stop()

        '''
        try:
            self.inport = open_input(self.in_device)
        except:
            self.inport = None
            print(f"midi_input open [{self.in_device}] ERROR")
            return

        print(f"midi_input:run open_input [{self.in_device}] READY")
        '''

        self.inport = open_input(self.in_device, callback=self.callback)
        self.running = True

        '''
        try:
            while self.running == True : # non-blocking
                for key in self.inport.iter_pending():
                    if key.type == 'note_on':
                        print(f"NOTE={key.note}")
        except:
            print(f"midi_input:run open_input [{self.in_device}] CLOSED")
        '''

    def callback(self, message):
        print(message)
        '''
        for key in self.inport:
            if key.type == 'note_on':
                print(f"NOTE={key.note}")
        '''

    def stop(self):
        self.running = False
        if self.inport :
            self.inport.close()
            self.inport = None

    def quit(self):
        print("midi_input:quit")
        self.stop()
        exit(0)
