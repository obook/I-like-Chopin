# This Python file uses the following encoding: utf-8
'''
Require : PySide6 mido python-rtmidi
'''
import sys
import platform
from PySide6.QtWidgets import (QApplication, QMainWindow)
from PySide6.QtCore import Signal
import mido

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)
ERRORS = {
    "program": "Bad input, please refer this spec-\n"
    "http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/program_change.htm",
    "notes": "Bad input, please refer this spec-\n"
    "http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm",
}


def number_to_note(number: int) -> str:
    octave = number // NOTES_IN_OCTAVE
    assert octave in OCTAVES, ERRORS["notes"]
    assert 0 <= number <= 127, ERRORS["notes"]
    note = NOTES[number % NOTES_IN_OCTAVE]
    return note + str(octave-1)  # octave start to zero


class MainWindow(QMainWindow):
    """Main class."""

    in_port = None
    log_activity = Signal(str)

    def __init__(self, parent=None):
        """Initialise la classe."""
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.Inputs, self.Outputs, self.InputsOutputs = self.GetDevices()
        self.ui.InputDeviceCombo.addItems(self.InputsOutputs)
        self.ui.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)
        self.ui.plainTextEdit.setMaximumBlockCount(50)
        self.log_activity.connect(self.LogMessage)

    def GetDevices(self):
        """Retourne la liste des devices midi connectés à l'équipement."""
        Inputs = []
        Outputs = []
        IOPorts = []

        for i, port_name in enumerate(mido.get_output_names()):
            if platform.system() == "Linux":  # cleanup linux ports
                port_name = port_name[: port_name.rfind(" ")]
            Outputs.append(port_name)

        for i, port_name in enumerate(mido.get_input_names()):
            if platform.system() == "Linux":  # cleanup linux ports
                port_name = port_name[: port_name.rfind(" ")]
            Inputs.append(port_name)

        for i, port_name in enumerate(mido.get_ioport_names()):  # not used
            if platform.system() == "Linux":  # cleanup linux ports
                port_name = port_name[: port_name.rfind(" ")]
            IOPorts.append(port_name)

        return Inputs, Outputs, IOPorts

    def InputDeviceChanged(self):
        """Open the MIDI port selected."""
        in_device = self.ui.InputDeviceCombo.currentText()
        if self.in_port:
            self.in_port.close()
        self.ui.plainTextEdit.clear()
        try:
            self.in_port = mido.open_input(in_device, callback=self.callback)
            self.log_activity.emit(f"Listen {in_device}")
        except Exception as error:
            self.log_activity.emit(f"{in_device} : {error}")

    def callback(self, msg):
        """Handle MIDI events from device."""

        """
        See : https://github.com/NicoG60/TouchMCU/blob/main/doc/mackie_control_protocol.md

        Play 	A#6 	94 	5E
        Stop 	A6 	93 	5D
        Record 	B6 	95 	5F
        Cycle 	D6 	86 	56
        Rewind 	G6 	91 	5B
        Forward 	G#6 	92 	5C
        Save 	G#5 	80 	50
        Undo 	A5 	81 	51
        Click 	F6 	89 	59 (metronome)

        Punch is a sequence:
            note_on channel 0 note D#6 [87,0x57] velocity 127
            note_on channel 0 note E6 [88,0x58] velocity 127
            note_on channel 0 note D#6 [87,0x57] velocity 0
            note_on channel 0 note E6 [88,0x58] velocity 0
        """

        text = f"{msg.type} "

        if msg.type == 'note_on' or msg.type == 'note_off':
            text += f"channel {msg.channel} note {number_to_note(msg.note)} [{msg.note},{hex(msg.note)}] velocity {msg.velocity}"

            # For fun
            if msg.channel == 0:
                if msg.note == 94 and msg.velocity:
                    self.log_activity.emit("Play")
                elif msg.note == 93 and msg.velocity:
                    self.log_activity.emit("Stop")
                elif msg.note == 95 and msg.velocity:
                    self.log_activity.emit("Record")
                elif msg.note == 86 and msg.velocity:
                    self.log_activity.emit("Cycle")
                elif msg.note == 91 and msg.velocity:
                    self.log_activity.emit("Rewind")
                elif msg.note == 92 and msg.velocity:
                    self.log_activity.emit("Forward")
                elif msg.note == 80 and msg.velocity:
                    self.log_activity.emit("Save")
                elif msg.note == 81 and msg.velocity:
                    self.log_activity.emit("Undo")
                elif msg.note == 89 and msg.velocity:
                    self.log_activity.emit("Click")

        elif msg.type == 'control_change':
            text += f"channel {msg.channel} control {msg.control} value {msg.value} time {msg.time}"

        elif msg.type == 'pitchwheel':
            text += f"channel {msg.channel} pitch {msg.pitch} time {msg.time}"

        elif msg.type == 'polytouch':
            text += f"channel {msg.channel} note {msg.note} value {msg.value} time {msg.time}"

        elif msg.type == 'sysex':
            text += f"data {msg.data}"

        else:
            print("---> PLEASE ADD : ", msg)

        self.log_activity.emit(text)

    def LogMessage(self, text):
        """Print message in QplainTextEdit (Signal)."""
        self.ui.plainTextEdit.appendPlainText(text)


if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
