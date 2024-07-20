# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'informations.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGroupBox,
    QPushButton, QSizePolicy, QTextBrowser, QWidget)

class Ui_DialogInformation(object):
    def setupUi(self, DialogInformation):
        if not DialogInformation.objectName():
            DialogInformation.setObjectName(u"DialogInformation")
        DialogInformation.resize(481, 373)
        self.pushButton_Close = QPushButton(DialogInformation)
        self.pushButton_Close.setObjectName(u"pushButton_Close")
        self.pushButton_Close.setGeometry(QRect(200, 330, 81, 25))
        self.groupBox = QGroupBox(DialogInformation)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 260, 461, 61))
        self.checkBox_PrintTerminalMsg = QCheckBox(self.groupBox)
        self.checkBox_PrintTerminalMsg.setObjectName(u"checkBox_PrintTerminalMsg")
        self.checkBox_PrintTerminalMsg.setGeometry(QRect(290, 30, 141, 23))
        self.checkBox_ForceIntrument0 = QCheckBox(self.groupBox)
        self.checkBox_ForceIntrument0.setObjectName(u"checkBox_ForceIntrument0")
        self.checkBox_ForceIntrument0.setGeometry(QRect(10, 30, 141, 23))
        self.checkBox_ShowSongInfo = QCheckBox(self.groupBox)
        self.checkBox_ShowSongInfo.setObjectName(u"checkBox_ShowSongInfo")
        self.checkBox_ShowSongInfo.setGeometry(QRect(160, 30, 141, 23))
        self.textBrowser = QTextBrowser(DialogInformation)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 461, 241))

        self.retranslateUi(DialogInformation)

        QMetaObject.connectSlotsByName(DialogInformation)
    # setupUi

    def retranslateUi(self, DialogInformation):
        DialogInformation.setWindowTitle(QCoreApplication.translate("DialogInformation", u"Dialog", None))
        self.pushButton_Close.setText(QCoreApplication.translate("DialogInformation", u"Close", None))
        self.groupBox.setTitle(QCoreApplication.translate("DialogInformation", u"Options", None))
        self.checkBox_PrintTerminalMsg.setText(QCoreApplication.translate("DialogInformation", u"Print msg to Terminal", None))
        self.checkBox_ForceIntrument0.setText(QCoreApplication.translate("DialogInformation", u"Force Piano (Prog 0)", None))
        self.checkBox_ShowSongInfo.setText(QCoreApplication.translate("DialogInformation", u"Open Song info", None))
    # retranslateUi

