# This Python file uses the following encoding: utf-8
import sys
import os
import json

from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QAbstractItemView, QListWidgetItem
# from PySide6.QtGui import QAbstractItemView

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

        # Playlist file
        self.playlistfile = os.path.expanduser("~/.config/i-like-chopin/i-like-chopin-playlist.json")

        # QListWidget
        self.listWidget = self.ui.listWidget
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)  # Allow move items
        # self.listWidget.setSelectionMode(QAbstractItemView.XXXX) # Only one selected
        self.LoadPlaylist()

        # Buttons
        pushButton_Save = self.ui.pushButton_Save
        pushButton_Save.clicked.connect(self.Save)

        pushButton_Abort = self.ui.pushButton_Abort
        pushButton_Abort.clicked.connect(self.Quit)

        pushButton_Remove_Item = self.ui.pushButton_Remove_Item
        pushButton_Remove_Item.clicked.connect(self.RemoveItem)

    def LoadPlaylist(self):

        try:
            with open(self.playlistfile, "r") as f:
                self.playlist = json.load(f)
                f.close

        except Exception as error:  # not yet exists
            print(f"LoadPlaylist exception {error}")
            return

        for dic in self.playlist:
            item = QListWidgetItem(dic['artist'] + " ~ " + dic['title'])
            # 0x0100 : application-specific purposes.
            # See : https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum
            item.setData(0x0100, dic)
            self.listWidget.addItem(item)

    def Save(self):

        new_list = []
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            dic = item.data(0x0100)
            new_list.append(dic)
        try:
            with open(self.playlistfile, "w", encoding="utf-8", newline='\r\n') as outfile:
                json.dump(new_list, outfile, indent=4, sort_keys=True, ensure_ascii=False)
                outfile.close
        except:
            return False

        self.Quit()

    def RemoveItem(self):
        # Empty list if nothing selected
        if self.listWidget.selectedItems():
            item = self.listWidget.currentItem()
            dic = item.data(0x0100)
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)
            print("remove :", dic['path'])
        else:
            print("No item selected")

    def Quit(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
