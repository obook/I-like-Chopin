# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'informations.ui'
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
    QCheckBox,
    QDialog,
    QGroupBox,
    QPushButton,
    QSizePolicy,
    QTextBrowser,
    QWidget,
)


class Ui_DialogInformation(object):
    def setupUi(self, DialogInformation):
        if not DialogInformation.objectName():
            DialogInformation.setObjectName("DialogInformation")
        DialogInformation.resize(479, 365)
        self.pushButton_Close = QPushButton(DialogInformation)
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.pushButton_Close.setGeometry(QRect(200, 330, 81, 25))
        self.groupBox = QGroupBox(DialogInformation)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setGeometry(QRect(10, 260, 461, 61))
        self.checkBox_ForceIntrument0 = QCheckBox(self.groupBox)
        self.checkBox_ForceIntrument0.setObjectName("checkBox_ForceIntrument0")
        self.checkBox_ForceIntrument0.setGeometry(QRect(140, 30, 191, 23))
        self.textBrowser = QTextBrowser(DialogInformation)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 461, 241))

        self.retranslateUi(DialogInformation)

        QMetaObject.connectSlotsByName(DialogInformation)

    # setupUi

    def retranslateUi(self, DialogInformation):
        DialogInformation.setWindowTitle(
            QCoreApplication.translate("DialogInformation", "Dialog", None)
        )
        self.pushButton_Close.setText(
            QCoreApplication.translate("DialogInformation", "Close", None)
        )
        self.groupBox.setTitle(
            QCoreApplication.translate("DialogInformation", "Options", None)
        )
        self.checkBox_ForceIntrument0.setText(
            QCoreApplication.translate(
                "DialogInformation", "Force Piano (Prog 0)", None
            )
        )

    # retranslateUi
