# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
    QStatusBar, QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(511, 495)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 360, 481, 71))
        self.pushButton_Quit = QPushButton(self.centralwidget)
        self.pushButton_Quit.setObjectName(u"pushButton_Quit")
        self.pushButton_Quit.setGeometry(QRect(410, 440, 80, 31))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 0, 481, 201))
        self.pushButton_Mode = QPushButton(self.groupBox)
        self.pushButton_Mode.setObjectName(u"pushButton_Mode")
        self.pushButton_Mode.setGeometry(QRect(70, 150, 401, 30))
        self.label_File = QLabel(self.groupBox)
        self.label_File.setObjectName(u"label_File")
        self.label_File.setGeometry(QRect(30, 114, 71, 22))
        self.InputDeviceCombo = QComboBox(self.groupBox)
        self.InputDeviceCombo.setObjectName(u"InputDeviceCombo")
        self.InputDeviceCombo.setGeometry(QRect(70, 30, 401, 30))
        self.OutputDeviceCombo = QComboBox(self.groupBox)
        self.OutputDeviceCombo.setObjectName(u"OutputDeviceCombo")
        self.OutputDeviceCombo.setGeometry(QRect(70, 70, 401, 30))
        self.label_Mode = QLabel(self.groupBox)
        self.label_Mode.setObjectName(u"label_Mode")
        self.label_Mode.setGeometry(QRect(18, 154, 71, 22))
        self.label_Ouput = QLabel(self.groupBox)
        self.label_Ouput.setObjectName(u"label_Ouput")
        self.label_Ouput.setGeometry(QRect(15, 74, 71, 22))
        self.label_Input = QLabel(self.groupBox)
        self.label_Input.setObjectName(u"label_Input")
        self.label_Input.setGeometry(QRect(20, 34, 71, 22))
        self.FileCombo = QComboBox(self.groupBox)
        self.FileCombo.setObjectName(u"FileCombo")
        self.FileCombo.setGeometry(QRect(70, 110, 401, 30))
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 200, 481, 141))
        self.gridLayoutWidget = QWidget(self.groupBox_2)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 70, 461, 71))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ChannelAll = QPushButton(self.groupBox_2)
        self.pushButton_ChannelAll.setObjectName(u"pushButton_ChannelAll")
        self.pushButton_ChannelAll.setGeometry(QRect(190, 30, 97, 30))
        self.pushButton_ChannelFirst = QPushButton(self.groupBox_2)
        self.pushButton_ChannelFirst.setObjectName(u"pushButton_ChannelFirst")
        self.pushButton_ChannelFirst.setGeometry(QRect(10, 30, 91, 30))
        self.pushButton_ChannelNone = QPushButton(self.groupBox_2)
        self.pushButton_ChannelNone.setObjectName(u"pushButton_ChannelNone")
        self.pushButton_ChannelNone.setGeometry(QRect(375, 30, 97, 30))
        self.pushButton_Panic = QPushButton(self.centralwidget)
        self.pushButton_Panic.setObjectName(u"pushButton_Panic")
        self.pushButton_Panic.setGeometry(QRect(10, 440, 97, 30))
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
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Devices", None))
        self.pushButton_Mode.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_File.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.label_Mode.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.label_Ouput.setText(QCoreApplication.translate("MainWindow", u"Ouput", None))
        self.label_Input.setText(QCoreApplication.translate("MainWindow", u"Input", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Channels", None))
        self.pushButton_ChannelAll.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.pushButton_ChannelFirst.setText(QCoreApplication.translate("MainWindow", u"First", None))
        self.pushButton_ChannelNone.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.pushButton_Panic.setText(QCoreApplication.translate("MainWindow", u"Panic", None))
    # retranslateUi

