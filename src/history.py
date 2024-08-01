# This Python file uses the following encoding: utf-8

import os
import json
import uuid

class ClassHistory:
    uuid = None
    applicationpath = os.path.dirname(os.path.realpath(__file__))
    settingspath = os.path.join(os.path.expanduser("~"), ".config")
    historyfile = os.path.join(settingspath, "i-like-chopin-history.json")
    history = []

    def __init__(self):
        self.uuid = uuid.uuid4()
        self.LoadHistory()
        print(f"History {self.uuid} read [{self.historyfile}]")

    def __del__(self):
        print(f"History {self.uuid} destroyed [{self.historyfile}]")

    # Globals

    def LoadHistory(self):
        try:
            with open(self.historyfile, "r") as f:
                self.history = json.load(f)
                f.close
        except: # not yet exists
            pass

    def SaveHistory(self):
        try:
            with open(self.historyfile, "w") as f:
                json.dump(self.history, f)
                f.close
        except:
            return False
        return True

    # Midi files
    def AddHistory(self, midifile):
        if not midifile in self.history:
            if len(self.history) > 127:
                self.history.pop(0) # remove fist
            self.history.append(midifile)
            self.SaveHistory()

    def GetHistory(self):
        ''' trop de problèmes pour l'instant

        reversed = self.history
        reversed.reverse() # last first
        '''
        return self.history




