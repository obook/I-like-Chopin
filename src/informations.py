# This Python file uses the following encoding: utf-8

import sys
from PySide6.QtWidgets import QApplication, QDialogButtonBox
from ui_informations import Ui_DialogInformation

'''

WORK IN PROGRES...

'''

class Informations(QDialogButtonBox):
    def __init__(self, parent=None):
        '''
        super(Ui_DialogInformation, self).__init__()
        self.initUI()
        '''

        super().__init__(parent)
        self.ui = Ui_DialogInformation()
        self.ui.setupUi(self)


    def accept(self):
        print("accept")

    def reject(self):
        print("reject")

def ShowInformation(app):
    print("Informations:ShowInformation")
    '''
    # app = QApplication(sys.argv)
    widget = Informations()
    widget.show()
    app.exec()
    '''
    form = Informations()
    form.show()
    # form.exec_()

