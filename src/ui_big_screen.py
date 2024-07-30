# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'big_screen.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QGridLayout,
    QPushButton,
    QSizePolicy,
    QTextBrowser,
    QWidget,
)


class Ui_BigScreenDlg(object):
    def setupUi(self, BigScreenDlg):
        if not BigScreenDlg.objectName():
            BigScreenDlg.setObjectName("BigScreenDlg")
        BigScreenDlg.resize(394, 304)
        self.gridLayout = QGridLayout(BigScreenDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.textBrowser = QTextBrowser(BigScreenDlg)
        self.textBrowser.setObjectName("textBrowser")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textBrowser)

        self.pushButtonClose = QPushButton(BigScreenDlg)
        self.pushButtonClose.setObjectName("pushButtonClose")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pushButtonClose)

        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(BigScreenDlg)

        QMetaObject.connectSlotsByName(BigScreenDlg)

    # setupUi

    def retranslateUi(self, BigScreenDlg):
        BigScreenDlg.setWindowTitle(
            QCoreApplication.translate("BigScreenDlg", "Dialog", None)
        )
        self.pushButtonClose.setText(
            QCoreApplication.translate("BigScreenDlg", "Close", None)
        )

    # retranslateUi
