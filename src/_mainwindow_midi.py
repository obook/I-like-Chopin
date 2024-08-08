# This Python file uses the following encoding: utf-8

from midi_main import ClassMidiMain
from midi_song import states, modes
from midi_files import ClassMidiFiles


class _midi:

    Midi = None  # Main engine
    midisong = None  # current midisong
    lastmidifile = None
    nextmidifile = None
    history_index = -1
    midifiles_dict = {}
    Midifiles = ClassMidiFiles()

    def _midi_init(self):
        # Midi class
        self.Midi = ClassMidiMain(self, self.ChannelsList)

    # Midi control buttons
    def PrintSpeed(self, speed):  # 0 to 126
        if speed:
            self.ui.pushButton_Speed.setText(f"Speed -{speed}")
        else:
            self.ui.pushButton_Speed.setText("Speed")

    def PrintHumanize(self, value):
        if value:
            self.ui.pushButton_Humanize.setText(f"Humanize {value}")
        else:
            self.ui.pushButton_Humanize.setText("Humanize")

    def Panic(self):
        self.Midi.Panic()
