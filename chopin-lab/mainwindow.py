# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from midi_main import midi_main

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.midi = midi_main(self)

        Inputs, Outputs = self.midi.GetDevices()
        self.ui.InputDeviceCombo.addItems(Inputs)

        self.ui.pushButton_Quit.clicked.connect(self.Quit)
        self.ui.textBrowser.insertPlainText("HELLO")

        self.midi.NewInput()
        self.midi.NewOutput()

    def Quit(self):
        self.midi.quit()
        app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
