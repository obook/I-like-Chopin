# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtCore import QEvent
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from songinfolib import MidiSong

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("MIDI Song info")

        self.ui.pushButton_Load.clicked.connect(self.Load)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)
        self.setAcceptDrops(True)
        self.installEventFilter(self)  # drop files on readonly PlainTextEdit

    def Load(self):
        fname = QFileDialog.getOpenFileName(
                    self,
                    "Open Midi File",
                    "",
                    "MIDI Files (*.mid) ;; All Files (*)",
                )
        if fname:
            file = fname[0]
            self.PrintInfo(file)

    def PrintInfo(self, file):
            name = os.path.basename(file)
            self.setWindowTitle(name)
            song = MidiSong(file)
            duration = round(song.duration, 2)
            tracks = song.tracks
            sustain = song.sustain
            set_tempo = song.set_tempo

            self.ui.plainTextEdit.clear()

            self.ui.plainTextEdit.appendPlainText(f"** File : {name}")
            self.ui.plainTextEdit.appendPlainText(f"** Sustain : {sustain}")
            self.ui.plainTextEdit.appendPlainText(f"** Tempo change : {set_tempo}")
            self.ui.plainTextEdit.appendPlainText(f"** Duration : {duration} min.")
            self.ui.plainTextEdit.appendPlainText("** TRACKS **")
            for index in range(len(tracks)):
                track = tracks[index]
                self.ui.plainTextEdit.appendPlainText(f"{index} {track}")

    def eventFilter(self, o, e):  # drop files
        if e.type() == QEvent.DragEnter:  # remember to accept the enter event
            e.acceptProposedAction()
            return True
        if e.type() == QEvent.Drop:
            data = e.mimeData()
            urls = data.urls()
            if urls and urls[0].scheme() == "file":
                self.PrintInfo(urls[0].toLocalFile())
            return True
        return False  # remember to return false for other event types

    def closeEvent(self, event):  # overwritten
        self.Quit()

    def Quit(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
