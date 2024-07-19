# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets

from PySide6.QtWidgets import QDialog
from ui_big_screen import Ui_BigScreenDlg

class BigScreenDlg(Ui_BigScreenDlg, QDialog):
    global info_midifile

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("MidiFile")
        self.pushButtonClose.clicked.connect(self.quit)


    def quit(self):
        self.close()

def ShowBigScreen(pParent,midifile):
    global info_midifile
    info_midifile = midifile
    dlg = BigScreenDlg(pParent)
    dlg.show()
