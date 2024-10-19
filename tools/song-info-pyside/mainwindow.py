# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtCore import QEvent
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("PySide6 Sample")

        self.ui.pushButton_Load.clicked.connect(self.Load)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)

    def Load(self):
        fname = QFileDialog.getOpenFileName(
                    self,
                    "Open Midi File",
                    "",
                    "MIDI Files (*.mid) ;; All Files (*)",
                )
        if fname:
            print(fname[0])

    def eventFilter(self, o, e):  # drop files
        if e.type() == QEvent.DragEnter:  # remember to accept the enter event
            e.acceptProposedAction()
            return True
        if e.type() == QEvent.Drop:
            data = e.mimeData()
            urls = data.urls()
            if urls and urls[0].scheme() == "file":
                print(urls[0].toLocalFile())
            return True
        return False  # remember to return false for other event types

    def Quit(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
