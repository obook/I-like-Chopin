# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'big_screen.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, QSizePolicy,
    QWidget)

class Ui_BigScreenDlg(object):
    def setupUi(self, BigScreenDlg):
        if not BigScreenDlg.objectName():
            BigScreenDlg.setObjectName(u"BigScreenDlg")
        BigScreenDlg.resize(400, 300)
        self.pushButtonClose = QPushButton(BigScreenDlg)
        self.pushButtonClose.setObjectName(u"pushButtonClose")
        self.pushButtonClose.setGeometry(QRect(310, 260, 80, 25))

        self.retranslateUi(BigScreenDlg)

        QMetaObject.connectSlotsByName(BigScreenDlg)
    # setupUi

    def retranslateUi(self, BigScreenDlg):
        BigScreenDlg.setWindowTitle(QCoreApplication.translate("BigScreenDlg", u"Dialog", None))
        self.pushButtonClose.setText(QCoreApplication.translate("BigScreenDlg", u"Close", None))
    # retranslateUi

