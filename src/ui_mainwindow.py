# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
    QGridLayout,
    QGroupBox,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(504, 400)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_Quit = QPushButton(self.centralwidget)
        self.pushButton_Quit.setObjectName("pushButton_Quit")
        self.pushButton_Quit.setGeometry(QRect(390, 340, 100, 30))
        self.groupBoxDevices = QGroupBox(self.centralwidget)
        self.groupBoxDevices.setObjectName("groupBoxDevices")
        self.groupBoxDevices.setGeometry(QRect(10, 4, 481, 111))
        self.label_File = QLabel(self.groupBoxDevices)
        self.label_File.setObjectName("label_File")
        self.label_File.setGeometry(QRect(20, 36, 81, 22))
        self.label_File.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.label_Ouput = QLabel(self.groupBoxDevices)
        self.label_Ouput.setObjectName("label_Ouput")
        self.label_Ouput.setGeometry(QRect(322, 80, 91, 22))
        self.label_Ouput.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.label_Input = QLabel(self.groupBoxDevices)
        self.label_Input.setObjectName("label_Input")
        self.label_Input.setGeometry(QRect(10, 80, 81, 22))
        self.label_Input.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.labelStatusInput = QLabel(self.groupBoxDevices)
        self.labelStatusInput.setObjectName("labelStatusInput")
        self.labelStatusInput.setGeometry(QRect(100, 81, 20, 20))
        self.labelStatusOuput = QLabel(self.groupBoxDevices)
        self.labelStatusOuput.setObjectName("labelStatusOuput")
        self.labelStatusOuput.setGeometry(QRect(420, 81, 20, 20))
        self.labelStatusMidifile = QLabel(self.groupBoxDevices)
        self.labelStatusMidifile.setObjectName("labelStatusMidifile")
        self.labelStatusMidifile.setGeometry(QRect(255, 80, 20, 20))
        self.pushButton_Files = QPushButton(self.groupBoxDevices)
        self.pushButton_Files.setObjectName("pushButton_Files")
        self.pushButton_Files.setGeometry(QRect(110, 30, 331, 31))
        self.pushButton_Files.setAcceptDrops(True)
        self.pushButton_Files.setFlat(False)
        self.progressBar = QProgressBar(self.groupBoxDevices)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setGeometry(QRect(110, 60, 331, 6))
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)
        self.label_Ouput_2 = QLabel(self.groupBoxDevices)
        self.label_Ouput_2.setObjectName("label_Ouput_2")
        self.label_Ouput_2.setGeometry(QRect(155, 78, 91, 22))
        self.label_Ouput_2.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 118, 481, 141))
        self.gridLayoutWidget = QWidget(self.groupBox_2)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 70, 461, 71))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ChannelsAll = QPushButton(self.groupBox_2)
        self.pushButton_ChannelsAll.setObjectName("pushButton_ChannelsAll")
        self.pushButton_ChannelsAll.setGeometry(QRect(190, 30, 97, 30))
        self.pushButton_ChannelsFirst = QPushButton(self.groupBox_2)
        self.pushButton_ChannelsFirst.setObjectName("pushButton_ChannelsFirst")
        self.pushButton_ChannelsFirst.setGeometry(QRect(10, 30, 91, 30))
        self.pushButton_ChannelsNone = QPushButton(self.groupBox_2)
        self.pushButton_ChannelsNone.setObjectName("pushButton_ChannelsNone")
        self.pushButton_ChannelsNone.setGeometry(QRect(375, 30, 97, 30))
        self.pushButton_Panic = QPushButton(self.centralwidget)
        self.pushButton_Panic.setObjectName("pushButton_Panic")
        self.pushButton_Panic.setGeometry(QRect(10, 340, 100, 30))
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 260, 481, 71))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.pushButton_FileIndex = QPushButton(self.groupBox_3)
        self.pushButton_FileIndex.setObjectName("pushButton_FileIndex")
        self.pushButton_FileIndex.setEnabled(True)
        self.pushButton_FileIndex.setGeometry(QRect(245, 30, 100, 30))
        self.pushButton_FileIndex.setCheckable(False)
        self.pushButton_Speed = QPushButton(self.groupBox_3)
        self.pushButton_Speed.setObjectName("pushButton_Speed")
        self.pushButton_Speed.setGeometry(QRect(135, 30, 100, 30))
        self.pushButton_Humanize = QPushButton(self.groupBox_3)
        self.pushButton_Humanize.setObjectName("pushButton_Humanize")
        self.pushButton_Humanize.setEnabled(True)
        self.pushButton_Humanize.setGeometry(QRect(26, 30, 100, 30))
        self.pushButton_Mode = QPushButton(self.groupBox_3)
        self.pushButton_Mode.setObjectName("pushButton_Mode")
        self.pushButton_Mode.setGeometry(QRect(355, 30, 100, 30))
        self.pushButton_Mode.setCheckable(True)
        self.pushButton_Info = QPushButton(self.centralwidget)
        self.pushButton_Info.setObjectName("pushButton_Info")
        self.pushButton_Info.setGeometry(QRect(264, 340, 100, 30))
        self.pushButton_Settings = QPushButton(self.centralwidget)
        self.pushButton_Settings.setObjectName("pushButton_Settings")
        self.pushButton_Settings.setGeometry(QRect(136, 340, 100, 30))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButton_Quit.setDefault(False)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "I LIKE CHOPIN", None)
        )
        self.pushButton_Quit.setText(
            QCoreApplication.translate("MainWindow", "Quit", None)
        )
        self.groupBoxDevices.setTitle(
            QCoreApplication.translate("MainWindow", "MIDI Devices", None)
        )
        self.label_File.setText(QCoreApplication.translate("MainWindow", "File", None))
        self.label_Ouput.setText(
            QCoreApplication.translate("MainWindow", "Synthesizer", None)
        )
        self.label_Input.setText(
            QCoreApplication.translate("MainWindow", "Keyboard", None)
        )
        self.labelStatusInput.setText(
            QCoreApplication.translate("MainWindow", "LED", None)
        )
        self.labelStatusOuput.setText(
            QCoreApplication.translate("MainWindow", "LED", None)
        )
        self.labelStatusMidifile.setText(
            QCoreApplication.translate("MainWindow", "LED", None)
        )
        self.pushButton_Files.setText(
            QCoreApplication.translate("MainWindow", "PushButton", None)
        )
        self.label_Ouput_2.setText(
            QCoreApplication.translate("MainWindow", "Engine", None)
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("MainWindow", "MIDI Channels", None)
        )
        self.pushButton_ChannelsAll.setText(
            QCoreApplication.translate("MainWindow", "All", None)
        )
        self.pushButton_ChannelsFirst.setText(
            QCoreApplication.translate("MainWindow", "First", None)
        )
        self.pushButton_ChannelsNone.setText(
            QCoreApplication.translate("MainWindow", "None", None)
        )
        self.pushButton_Panic.setText(
            QCoreApplication.translate("MainWindow", "Panic", None)
        )
        self.groupBox_3.setTitle(
            QCoreApplication.translate("MainWindow", "MIDI Controller", None)
        )
        self.pushButton_FileIndex.setText(
            QCoreApplication.translate("MainWindow", "Midifile", None)
        )
        self.pushButton_Speed.setText(
            QCoreApplication.translate("MainWindow", "Speed", None)
        )
        self.pushButton_Humanize.setText(
            QCoreApplication.translate("MainWindow", "Humanize", None)
        )
        self.pushButton_Mode.setText(
            QCoreApplication.translate("MainWindow", "Playback", None)
        )
        self.pushButton_Info.setText(
            QCoreApplication.translate("MainWindow", "More", None)
        )
        self.pushButton_Settings.setText(
            QCoreApplication.translate("MainWindow", "Settings", None)
        )

    # retranslateUi
