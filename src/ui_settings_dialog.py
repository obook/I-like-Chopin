# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QGroupBox, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_DialogSettings(object):
    def setupUi(self, DialogSettings):
        if not DialogSettings.objectName():
            DialogSettings.setObjectName(u"DialogSettings")
        DialogSettings.resize(501, 289)
        self.groupBoxDevices = QGroupBox(DialogSettings)
        self.groupBoxDevices.setObjectName(u"groupBoxDevices")
        self.groupBoxDevices.setGeometry(QRect(10, 10, 481, 161))
        self.InputDeviceCombo = QComboBox(self.groupBoxDevices)
        self.InputDeviceCombo.setObjectName(u"InputDeviceCombo")
        self.InputDeviceCombo.setGeometry(QRect(110, 30, 331, 30))
        self.OutputDeviceCombo = QComboBox(self.groupBoxDevices)
        self.OutputDeviceCombo.setObjectName(u"OutputDeviceCombo")
        self.OutputDeviceCombo.setGeometry(QRect(110, 60, 331, 30))
        self.label_Ouput = QLabel(self.groupBoxDevices)
        self.label_Ouput.setObjectName(u"label_Ouput")
        self.label_Ouput.setGeometry(QRect(4, 65, 91, 20))
        self.label_Ouput.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_Input = QLabel(self.groupBoxDevices)
        self.label_Input.setObjectName(u"label_Input")
        self.label_Input.setGeometry(QRect(15, 34, 81, 22))
        self.label_Input.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.pushButton_Close = QPushButton(DialogSettings)
        self.pushButton_Close.setObjectName(u"pushButton_Close")
        self.pushButton_Close.setGeometry(QRect(210, 250, 81, 25))
        self.groupBox = QGroupBox(DialogSettings)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 176, 481, 60))
        self.checkBox_ForceIntrument0 = QCheckBox(self.groupBox)
        self.checkBox_ForceIntrument0.setObjectName(u"checkBox_ForceIntrument0")
        self.checkBox_ForceIntrument0.setGeometry(QRect(10, 30, 141, 23))
        self.ApiCombo = QComboBox(self.groupBox)
        self.ApiCombo.setObjectName(u"ApiCombo")
        self.ApiCombo.setEnabled(False)
        self.ApiCombo.setGeometry(QRect(310, 26, 131, 30))
        self.label_Ouput_3 = QLabel(self.groupBox)
        self.label_Ouput_3.setObjectName(u"label_Ouput_3")
        self.label_Ouput_3.setEnabled(False)
        self.label_Ouput_3.setGeometry(QRect(200, 29, 100, 22))
        self.label_Ouput_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.checkBox_DebugMSG = QCheckBox(self.groupBox)
        self.checkBox_DebugMSG.setObjectName(u"checkBox_DebugMSG")
        self.checkBox_DebugMSG.setGeometry(QRect(172, 32, 91, 20))
        self.ControllerDeviceComboIN = QComboBox(DialogSettings)
        self.ControllerDeviceComboIN.setObjectName(u"ControllerDeviceComboIN")
        self.ControllerDeviceComboIN.setGeometry(QRect(120, 100, 331, 30))
        self.label_Ouput_2 = QLabel(DialogSettings)
        self.label_Ouput_2.setObjectName(u"label_Ouput_2")
        self.label_Ouput_2.setGeometry(QRect(6, 103, 100, 22))
        self.label_Ouput_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.ControllerDeviceComboOUT = QComboBox(DialogSettings)
        self.ControllerDeviceComboOUT.setObjectName(u"ControllerDeviceComboOUT")
        self.ControllerDeviceComboOUT.setGeometry(QRect(120, 130, 331, 30))
        self.label_Ouput_4 = QLabel(DialogSettings)
        self.label_Ouput_4.setObjectName(u"label_Ouput_4")
        self.label_Ouput_4.setGeometry(QRect(7, 133, 100, 22))
        self.label_Ouput_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.retranslateUi(DialogSettings)

        QMetaObject.connectSlotsByName(DialogSettings)
    # setupUi

    def retranslateUi(self, DialogSettings):
        DialogSettings.setWindowTitle(QCoreApplication.translate("DialogSettings", u"Dialog", None))
        self.groupBoxDevices.setTitle(QCoreApplication.translate("DialogSettings", u"MIDI Devices", None))
        self.label_Ouput.setText(QCoreApplication.translate("DialogSettings", u"Synthesizer", None))
        self.label_Input.setText(QCoreApplication.translate("DialogSettings", u"Keyboard", None))
        self.pushButton_Close.setText(QCoreApplication.translate("DialogSettings", u"Close", None))
        self.groupBox.setTitle(QCoreApplication.translate("DialogSettings", u"Options", None))
        self.checkBox_ForceIntrument0.setText(QCoreApplication.translate("DialogSettings", u"Force Piano (Prog 0)", None))
        self.label_Ouput_3.setText(QCoreApplication.translate("DialogSettings", u"API", None))
        self.checkBox_DebugMSG.setText(QCoreApplication.translate("DialogSettings", u"Debug MSG", None))
        self.label_Ouput_2.setText(QCoreApplication.translate("DialogSettings", u"Controller Input", None))
        self.label_Ouput_4.setText(QCoreApplication.translate("DialogSettings", u"Controller Ouput", None))
    # retranslateUi

