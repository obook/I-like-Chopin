# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'song_screen.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QGridLayout,
    QSizePolicy, QTextBrowser, QWidget)

class Ui_SongScreenDlg(object):
    def setupUi(self, SongScreenDlg):
        if not SongScreenDlg.objectName():
            SongScreenDlg.setObjectName(u"SongScreenDlg")
        SongScreenDlg.resize(394, 304)
        self.gridLayout = QGridLayout(SongScreenDlg)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.textBrowser = QTextBrowser(SongScreenDlg)
        self.textBrowser.setObjectName(u"textBrowser")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textBrowser)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)


        self.retranslateUi(SongScreenDlg)

        QMetaObject.connectSlotsByName(SongScreenDlg)
    # setupUi

    def retranslateUi(self, SongScreenDlg):
        SongScreenDlg.setWindowTitle(QCoreApplication.translate("SongScreenDlg", u"Dialog", None))
    # retranslateUi

