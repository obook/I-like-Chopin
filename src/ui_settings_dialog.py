# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
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
    QComboBox,
    QDialog,
    QGroupBox,
    QLabel,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class Ui_DialogSettings(object):
    def setupUi(self, DialogSettings):
        if not DialogSettings.objectName():
            DialogSettings.setObjectName("DialogSettings")
        DialogSettings.resize(501, 192)
        self.groupBoxDevices = QGroupBox(DialogSettings)
        self.groupBoxDevices.setObjectName("groupBoxDevices")
        self.groupBoxDevices.setGeometry(QRect(10, 10, 481, 131))
        self.InputDeviceCombo = QComboBox(self.groupBoxDevices)
        self.InputDeviceCombo.setObjectName("InputDeviceCombo")
        self.InputDeviceCombo.setGeometry(QRect(110, 30, 331, 30))
        self.OutputDeviceCombo = QComboBox(self.groupBoxDevices)
        self.OutputDeviceCombo.setObjectName("OutputDeviceCombo")
        self.OutputDeviceCombo.setGeometry(QRect(110, 60, 331, 30))
        self.label_Ouput = QLabel(self.groupBoxDevices)
        self.label_Ouput.setObjectName("label_Ouput")
        self.label_Ouput.setGeometry(QRect(4, 60, 91, 22))
        self.label_Ouput.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.label_Input = QLabel(self.groupBoxDevices)
        self.label_Input.setObjectName("label_Input")
        self.label_Input.setGeometry(QRect(15, 34, 81, 22))
        self.label_Input.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.pushButton_Close = QPushButton(DialogSettings)
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.pushButton_Close.setGeometry(QRect(210, 150, 81, 25))

        self.retranslateUi(DialogSettings)

        QMetaObject.connectSlotsByName(DialogSettings)

    # setupUi

    def retranslateUi(self, DialogSettings):
        DialogSettings.setWindowTitle(
            QCoreApplication.translate("DialogSettings", "Dialog", None)
        )
        self.groupBoxDevices.setTitle(
            QCoreApplication.translate("DialogSettings", "MIDI Devices", None)
        )
        self.label_Ouput.setText(
            QCoreApplication.translate("DialogSettings", "Synthesizer", None)
        )
        self.label_Input.setText(
            QCoreApplication.translate("DialogSettings", "Keyboard", None)
        )
        self.pushButton_Close.setText(
            QCoreApplication.translate("DialogSettings", "Close", None)
        )

    # retranslateUi
