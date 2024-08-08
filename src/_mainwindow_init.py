# This Python file uses the following encoding: utf-8
import os
from PySide6.QtGui import QIcon
from PySide6 import QtGui
from PySide6.QtWidgets import QPushButton


class _initialize:

    application_path = os.path.dirname(os.path.realpath(__file__))

    # Define status icons
    ICON_RED_LED = application_path + "/icons/led/led-red-on.png"
    ICON_GREEN_LED = application_path + "/icons/led/green-led-on.png"
    ICON_GREEN_LIGHT_LED = application_path + "/icons/led/greenlight-led-on.png"
    ICON_YELLOW_LED = application_path + "/icons/led/yellow-led-on.png"
    ICON_BLUE_LED = application_path + "/icons/led/blue-led-on.png"
    ICON_LED_OFF = application_path + "/icons/led/led-off.png"

    def __init__(self):  # as is the first subclass in list, it's called
        # OK print("---> _initialize __init__")
        pass

    def _SetInterface(self):

        ICON_APPLICATION = os.path.join(
            self.application_path, "icons", "svg", "i-like-chopin.svg"
        )

        # Application icon X.org->correct - Wayland->not implemented
        my_icon = QIcon()
        my_icon.addFile(ICON_APPLICATION)
        self.setWindowIcon(my_icon)

        # StatusBar
        self.ui.statusbar.setSizeGripEnabled(False)

        # Push Buttons
        self.ui.pushButton_Panic.clicked.connect(self.Panic)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)
        self.ui.pushButton_Info.clicked.connect(self.Informations)
        self.ui.pushButton_Mode.clicked.connect(self.ChangePlayerMode)
        self.ui.pushButton_Files.clicked.connect(self.OpenBrowser)
        self.ui.pushButton_Files.installEventFilter(self)  # drop files

        # Leds
        self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_LED_OFF))
        self.ui.labelStatusInput.setScaledContents(True)

        self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_LED_OFF))
        self.ui.labelStatusOuput.setScaledContents(True)

        self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_LED_OFF))
        self.ui.labelStatusMidifile.setScaledContents(True)

        # ProgressBar
        self.ui.progressBar.setRange(0, 100)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setStyleSheet(
            "QProgressBar {"
            "border: 2px;"
            "border-radius: 30px;"
            "}"
            "QProgressBar::chunk {"
            "margin: 4px;"
            "background-color: qlineargradient("
            "x0: 0, x2: 1, "
            "stop: 0 green, stop: 0.6 green, "
            "stop: 0.8 orange, "
            "stop: 1 red);"
            "}"
        )

        # Midi Channels
        self.ui.pushButton_ChannelsNone.clicked.connect(self.ChannelsNone)
        self.ui.pushButton_ChannelsAll.clicked.connect(self.ChannelsAll)
        self.ui.pushButton_ChannelsFirst.clicked.connect(self.ChannelsFirst)

        grid = self.ui.gridLayout
        for n in range(8):
            self.ChannelsButtonsList.append(QPushButton(str(n + 1)))
            self.ChannelsButtonsList[n].setCheckable(True)
            self.ChannelsButtonsList[n].clicked.connect(self.ReadChannels)
            self.ChannelsButtonsList[n].setStyleSheet(
                "QPushButton:checked { background-color: rgb(50,100,50); }\n"
            )
            grid.addWidget(self.ChannelsButtonsList[n], 1, n)
        for n in range(8):
            self.ChannelsButtonsList.append(QPushButton(str(n + 8 + 1)))
            self.ChannelsButtonsList[n + 8].setCheckable(True)
            self.ChannelsButtonsList[n + 8].clicked.connect(self.ReadChannels)
            self.ChannelsButtonsList[n + 8].setStyleSheet(
                "QPushButton:checked { background-color: rgb(50,100,50); }\n"
            )
            grid.addWidget(self.ChannelsButtonsList[n + 8], 2, n)

        self.ChannelsFirst()
        # Special color for drums channel
        self.ChannelsButtonsList[9].setStyleSheet(
            "QPushButton {background-color: rgb(100,50,50);}"
        )

    """
        # Web server
        self.Web_server = ClassWebServer(self)
        self.server_interfaces = self.Web_server.GetInterfaces()
        self.Web_server.start()

    # Channels
    def _mainwindow____ChannelsNone(self):
        for n in range(len(self.ChannelsButtonsList)):
            self.ChannelsButtonsList[n].setChecked(False)
        self.ReadChannels()
    """
