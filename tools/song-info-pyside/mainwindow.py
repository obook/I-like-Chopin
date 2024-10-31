# This Python file uses the following encoding: utf-8
import sys
import os
from pathlib import Path, PurePath
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QEvent
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from song_info import MidiSong
from song_graph import graph_notes


class MainWindow(QMainWindow):
    ''' QT main window '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("MIDI Song info")

        self.ui.pushButton_Load.clicked.connect(self.load_file)
        self.ui.pushButton_Quit.clicked.connect(self.quit_application)
        self.setAcceptDrops(True)
        self.installEventFilter(self)  # drop files on readonly PlainTextEdit

    def load_file(self):
        ''' file dialog '''
        fname = QFileDialog.getOpenFileName(
                self,
                "Open Midi File",
                "",
                "MIDI Files (*.mid) ;; All Files (*)",
                )
        if fname:
            file = fname[0]
            self.print_info(file)

    def print_info(self, file):
        ''' print informations in QPlainEditText '''
        name = os.path.basename(file)
        self.setWindowTitle(name)
        song = MidiSong(file)
        duration = round(song.duration, 2)
        tracks = song.tracks
        sustain = song.sustain

        self.ui.plainTextEdit.clear()

        self.ui.plainTextEdit.appendPlainText(f"** File : {name}")
        self.ui.plainTextEdit.appendPlainText(f"** Sustain : {sustain}")
        self.ui.plainTextEdit.appendPlainText(f"** Duration : {duration} min.")
        self.ui.plainTextEdit.appendPlainText("** TRACKS **")
        for index in range(len(tracks)):
            track = tracks[index]
            self.ui.plainTextEdit.appendPlainText(f"{index} {track}")

        parent = PurePath(file).parent.name
        graph_notes(file, parent)

    def eventFilter(self, o, e):
        ''' intercept files dropped '''
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
        ''' Windows closed by desktop '''
        print("closeEvent")
        self.quit_application()

    def quit_application(self):
        ''' The end '''
        print("quit_application")
        # self.deleteLater()
        QApplication.quit()


if __name__ == "__main__":
    # BUG : fnot closed under Qt Python virtual env
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
