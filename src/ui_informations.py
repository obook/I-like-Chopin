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
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_DialogInformation(object):
    def setupUi(self, DialogInformation):
        if not DialogInformation.objectName():
            DialogInformation.setObjectName(u"DialogInformation")
        DialogInformation.resize(400, 361)
        self.pushButton_Close = QPushButton(DialogInformation)
        self.pushButton_Close.setObjectName(u"pushButton_Close")
        self.pushButton_Close.setGeometry(QRect(160, 330, 81, 25))
        self.textEdit = QTextEdit(DialogInformation)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 10, 381, 241))
        self.textEdit.setReadOnly(True)
        self.groupBox = QGroupBox(DialogInformation)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 260, 381, 61))
        self.checkBox_PrintTerminalMsg = QCheckBox(self.groupBox)
        self.checkBox_PrintTerminalMsg.setObjectName(u"checkBox_PrintTerminalMsg")
        self.checkBox_PrintTerminalMsg.setGeometry(QRect(220, 30, 141, 23))
        self.checkBox_ForceIntrument0 = QCheckBox(self.groupBox)
        self.checkBox_ForceIntrument0.setObjectName(u"checkBox_ForceIntrument0")
        self.checkBox_ForceIntrument0.setGeometry(QRect(20, 30, 171, 23))

        self.retranslateUi(DialogInformation)

        QMetaObject.connectSlotsByName(DialogInformation)
    # setupUi

    def retranslateUi(self, DialogInformation):
        DialogInformation.setWindowTitle(QCoreApplication.translate("DialogInformation", u"Dialog", None))
        self.pushButton_Close.setText(QCoreApplication.translate("DialogInformation", u"Close", None))
        self.textEdit.setHtml(QCoreApplication.translate("DialogInformation", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;NONE&gt;</p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("DialogInformation", u"Options", None))
        self.checkBox_PrintTerminalMsg.setText(QCoreApplication.translate("DialogInformation", u"Print msg to Terminal", None))
        self.checkBox_ForceIntrument0.setText(QCoreApplication.translate("DialogInformation", u"Force Piano (Prog 0)", None))
    # retranslateUi

