# This Python file uses the following encoding: utf-8
import sys
import platform
from PySide6.QtWidgets import (QApplication, QMainWindow)
from PySide6.QtCore import Signal
from PySide6.QtGui import (QTextCursor)
import mido

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):

    in_port = None
    log_activity = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.Inputs, self.Outputs, self.InputsOutputs = self.GetDevices()
        self.ui.InputDeviceCombo.addItems(self.InputsOutputs)
        self.ui.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)
        self.ui.plainTextEdit.setMaximumBlockCount(50)
        self.log_activity.connect(self.LogMessage)

    def GetDevices(self):
        """ Liste des devices midi connectés à l'équipement """
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
        text = ""

        if msg.type == 'note_on' or msg.type == 'note_off':
            text += f"{msg.type} channel {msg.channel} note {msg.note} velocity {msg.velocity}"

        elif msg.type == 'control_change':
             text += f"{msg.type} channel {msg.channel} control {msg.control} value {msg.value} time {msg.time}"

        elif msg.type == 'pitchwheel':
            text += f"{msg.type} channel {msg.channel} pitch {msg.pitch} time {msg.time}"

        elif msg.type == 'polytouch':
             text += f"{msg.type} channel {msg.channel} note {msg.note} value {msg.value} time {msg.time}"

        elif msg.type == 'sysex':
              text += f"{msg.type} data {msg.data}"

        else:
            print("---> PLEASE ADD : ", msg)
            text += f"{msg.type}"

        self.log_activity.emit(text)

    def LogMessage(self, text):
        self.ui.plainTextEdit.appendPlainText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
