# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(504, 442)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton_Quit = QPushButton(self.centralwidget)
        self.pushButton_Quit.setObjectName(u"pushButton_Quit")
        self.pushButton_Quit.setGeometry(QRect(410, 380, 80, 31))
        self.groupBoxDevices = QGroupBox(self.centralwidget)
        self.groupBoxDevices.setObjectName(u"groupBoxDevices")
        self.groupBoxDevices.setGeometry(QRect(10, 0, 481, 151))
        self.label_File = QLabel(self.groupBoxDevices)
        self.label_File.setObjectName(u"label_File")
        self.label_File.setGeometry(QRect(30, 114, 71, 22))
        self.InputDeviceCombo = QComboBox(self.groupBoxDevices)
        self.InputDeviceCombo.setObjectName(u"InputDeviceCombo")
        self.InputDeviceCombo.setGeometry(QRect(70, 30, 371, 30))
        self.OutputDeviceCombo = QComboBox(self.groupBoxDevices)
        self.OutputDeviceCombo.setObjectName(u"OutputDeviceCombo")
        self.OutputDeviceCombo.setGeometry(QRect(70, 70, 371, 30))
        self.label_Ouput = QLabel(self.groupBoxDevices)
        self.label_Ouput.setObjectName(u"label_Ouput")
        self.label_Ouput.setGeometry(QRect(15, 74, 71, 22))
        self.label_Input = QLabel(self.groupBoxDevices)
        self.label_Input.setObjectName(u"label_Input")
        self.label_Input.setGeometry(QRect(20, 34, 71, 22))
        self.FileCombo = QComboBox(self.groupBoxDevices)
        self.FileCombo.setObjectName(u"FileCombo")
        self.FileCombo.setGeometry(QRect(70, 110, 371, 30))
        self.FileCombo.setAcceptDrops(True)
        self.labelStatusInput = QLabel(self.groupBoxDevices)
        self.labelStatusInput.setObjectName(u"labelStatusInput")
        self.labelStatusInput.setGeometry(QRect(449, 35, 20, 20))
        self.labelStatusOuput = QLabel(self.groupBoxDevices)
        self.labelStatusOuput.setObjectName(u"labelStatusOuput")
        self.labelStatusOuput.setGeometry(QRect(450, 74, 20, 20))
        self.labelStatusMidifile = QLabel(self.groupBoxDevices)
        self.labelStatusMidifile.setObjectName(u"labelStatusMidifile")
        self.labelStatusMidifile.setGeometry(QRect(450, 113, 20, 20))
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 150, 481, 141))
        self.gridLayoutWidget = QWidget(self.groupBox_2)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 70, 461, 71))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ChannelsAll = QPushButton(self.groupBox_2)
        self.pushButton_ChannelsAll.setObjectName(u"pushButton_ChannelsAll")
        self.pushButton_ChannelsAll.setGeometry(QRect(190, 30, 97, 30))
        self.pushButton_ChannelsFirst = QPushButton(self.groupBox_2)
        self.pushButton_ChannelsFirst.setObjectName(u"pushButton_ChannelsFirst")
        self.pushButton_ChannelsFirst.setGeometry(QRect(10, 30, 91, 30))
        self.pushButton_ChannelsNone = QPushButton(self.groupBox_2)
        self.pushButton_ChannelsNone.setObjectName(u"pushButton_ChannelsNone")
        self.pushButton_ChannelsNone.setGeometry(QRect(375, 30, 97, 30))
        self.pushButton_Panic = QPushButton(self.centralwidget)
        self.pushButton_Panic.setObjectName(u"pushButton_Panic")
        self.pushButton_Panic.setGeometry(QRect(11, 380, 97, 30))
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 300, 481, 71))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.pushButton_FileIndex = QPushButton(self.groupBox_3)
        self.pushButton_FileIndex.setObjectName(u"pushButton_FileIndex")
        self.pushButton_FileIndex.setEnabled(True)
        self.pushButton_FileIndex.setGeometry(QRect(245, 30, 101, 30))
        self.pushButton_FileIndex.setCheckable(False)
        self.pushButton_Speed = QPushButton(self.groupBox_3)
        self.pushButton_Speed.setObjectName(u"pushButton_Speed")
        self.pushButton_Speed.setGeometry(QRect(135, 30, 101, 30))
        self.pushButton_Humanize = QPushButton(self.groupBox_3)
        self.pushButton_Humanize.setObjectName(u"pushButton_Humanize")
        self.pushButton_Humanize.setEnabled(True)
        self.pushButton_Humanize.setGeometry(QRect(26, 30, 100, 30))
        self.pushButton_Mode = QPushButton(self.groupBox_3)
        self.pushButton_Mode.setObjectName(u"pushButton_Mode")
        self.pushButton_Mode.setGeometry(QRect(355, 30, 101, 30))
        self.pushButton_Mode.setCheckable(True)
        self.pushButton_Info = QPushButton(self.centralwidget)
        self.pushButton_Info.setObjectName(u"pushButton_Info")
        self.pushButton_Info.setGeometry(QRect(200, 380, 101, 30))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_Quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.groupBoxDevices.setTitle(QCoreApplication.translate("MainWindow", u"MIDI Devices", None))
        self.label_File.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.label_Ouput.setText(QCoreApplication.translate("MainWindow", u"Ouput", None))
        self.label_Input.setText(QCoreApplication.translate("MainWindow", u"Input", None))
        self.labelStatusInput.setText(QCoreApplication.translate("MainWindow", u"LED", None))
        self.labelStatusOuput.setText(QCoreApplication.translate("MainWindow", u"LED", None))
        self.labelStatusMidifile.setText(QCoreApplication.translate("MainWindow", u"LED", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"MIDI Channels", None))
        self.pushButton_ChannelsAll.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.pushButton_ChannelsFirst.setText(QCoreApplication.translate("MainWindow", u"First", None))
        self.pushButton_ChannelsNone.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.pushButton_Panic.setText(QCoreApplication.translate("MainWindow", u"Panic", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"MIDI Controller", None))
        self.pushButton_FileIndex.setText(QCoreApplication.translate("MainWindow", u"Midifile", None))
        self.pushButton_Speed.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.pushButton_Humanize.setText(QCoreApplication.translate("MainWindow", u"Humanize", None))
        self.pushButton_Mode.setText(QCoreApplication.translate("MainWindow", u"Playback", None))
        self.pushButton_Info.setText(QCoreApplication.translate("MainWindow", u"More", None))
    # retranslateUi

