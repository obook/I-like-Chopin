# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from midi_main import midi_main
from settings import Settings

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):

    settings = Settings()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.midi = midi_main(self)

        Inputs, Outputs = self.midi.GetDevices()
        Input = self.settings.GetInputDevice()
        Output = self.settings.GetOutputDevice()

        self.ui.InputDeviceCombo.addItem(Input)
        self.ui.InputDeviceCombo.addItems(Inputs)
        self.ui.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)

        self.ui.OutputDeviceCombo.addItem(Output)
        self.ui.OutputDeviceCombo.addItems(Outputs)
        self.ui.OutputDeviceCombo.currentIndexChanged.connect(self.OuputDeviceChanged)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)

        self.ui.textBrowser.insertPlainText("Ready")

        #self.midi_input.SetInput('Arturia KeyStep 37:Arturia KeyStep 37 MIDI 1 28:0') # 28:0 peut changer !
        #self.midi_input.SetInput('Arturia KeyStep 37 MIDI 1')
        self.midi.ConnectInput(Input)

        #self.midi_output.SetOutput('FLUID Synth (Titanic):Synth input port (Titanic:0) 131:0') # 131:0 peut changer !
        #self.midi_output.SetOutput('Synth input port (Titanic:0)')
        self.midi.ConnectOutput(Output)

    def InputDeviceChanged(self):
        in_device = self.ui.InputDeviceCombo.currentText()
        self.settings.SaveInputDevice(in_device)
        self.midi.ConnectInput(in_device)

    def OuputDeviceChanged(self):
        out_device = self.ui.OutputDeviceCombo.currentText()
        print(out_device)
        self.settings.SaveOutputDevice(out_device)
        self.midi.ConnectOutput(out_device)

    def Quit(self):
        self.midi.quit()
        app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
