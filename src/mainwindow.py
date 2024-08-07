#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import sys
import os
import webbrowser

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6 import QtGui
from PySide6.QtCore import QTimer, QEvent
from PySide6.QtGui import QIcon

from midi_main import ClassMidiMain
from midi_song import states, modes
from midi_files import ClassMidiFiles
from settings import ClassSettings
from informations import ShowInformation
from web_server import ClassWebServer
from history import ClassHistory

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
from ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):

    Settings = ClassSettings()
    History = ClassHistory()
    Midifiles = ClassMidiFiles()
    midifiles_dict = {}

    Web_server = None
    title_rotation = 0

    ChannelsButtonsList = []
    ChannelsList = [False] * 16

    Inputs = []
    Outputs = []
    InputsOutputs = []

    Midi = None # Main midi class
    midisong = None  # current midisong
    lastmidifile = None
    nextmidifile = None
    history_index = -1

    ConnectInputState = False
    ConnectOutputState = False
    PlayingState = False

    application_path = os.path.dirname(os.path.realpath(__file__))
    ICON_APPLICATION = os.path.join(application_path,"icons","svg","i-like-chopin.svg")

    # Define status icons
    ICON_RED_LED = application_path + "/icons/led/led-red-on.png"
    ICON_GREEN_LED = application_path + "/icons/led/green-led-on.png"
    ICON_GREEN_LIGHT_LED = application_path + "/icons/led/greenlight-led-on.png"
    ICON_YELLOW_LED = application_path + "/icons/led/yellow-led-on.png"
    ICON_BLUE_LED = application_path + "/icons/led/blue-led-on.png"
    ICON_LED_OFF = application_path + "/icons/led/led-off.png"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.setFixedSize(504, 413)
        self.ui.setupUi(self)

        # Application icon X.org->correct - Wayland->not implemented
        my_icon = QIcon()
        my_icon.addFile(self.ICON_APPLICATION)
        self.setWindowIcon(my_icon)

        # StatusBar
        self.ui.statusbar.setSizeGripEnabled(False)

        # Midi class
        self.Midi = ClassMidiMain(self, self.ChannelsList)

        # Push Buttons
        self.ui.pushButton_Panic.clicked.connect(self.Panic)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)
        self.ui.pushButton_Info.clicked.connect(self.Informations)
        self.ui.pushButton_Mode.clicked.connect(self.ChangePlayerMode)
        self.ui.pushButton_Files.clicked.connect(self.OpenBrowser)
        self.ui.pushButton_Files.installEventFilter(self)  # drop files

        # Force playback mode
        self.Settings.SaveMode(modes["playback"])
        self.SetPlayerModeButtons()

        # ComboBoxes Inputs/Outputs
        self.Inputs, self.Outputs, self.InputsOutputs = self.Midi.GetDevices()
        Input = self.Settings.GetInputDevice()
        Output = self.Settings.GetOutputDevice()

        self.ui.InputDeviceCombo.addItem(Input)
        self.ui.InputDeviceCombo.addItems(self.Inputs)
        self.ui.InputDeviceCombo.currentIndexChanged.connect(self.InputDeviceChanged)

        self.ui.OutputDeviceCombo.addItem(Output)
        self.ui.OutputDeviceCombo.addItems(self.Outputs)
        self.ui.OutputDeviceCombo.currentIndexChanged.connect(self.OuputDeviceChanged)

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

        # Leds
        self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_LED_OFF))
        self.ui.labelStatusInput.setScaledContents(True)

        self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_LED_OFF))
        self.ui.labelStatusOuput.setScaledContents(True)

        self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_LED_OFF))
        self.ui.labelStatusMidifile.setScaledContents(True)

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

        # Datas
        self.ChannelsList[0] = True  # active first channel
        '''
        self.MidiFiles = self.Midi.GetMidiFiles()
        '''

        # Connections
        self.Midi.ConnectInput(Input)
        self.Midi.ConnectOutput(Output)
        self.MidifileChange(self.Settings.GetMidifile())
        self.lastmidifile = self.Settings.GetMidifile()
        self.nextmidifile = self.nextmidifile

        # Midifiles
        if self.midisong:
            self.ui.pushButton_Files.setText(self.midisong.GetCleanName())

        self.midifiles_dict = self.Midifiles.ScanFiles(self.Settings.GetMidiPath())

        # Web server
        self.Web_server = ClassWebServer(self)
        self.server_interfaces = self.Web_server.GetInterfaces()
        self.Web_server.start()

        # Timers
        timer = QTimer(self)
        timer.timeout.connect(self.timer)
        timer.start(2000)

        timer = QTimer(self)
        timer.timeout.connect(self.timer_title)
        timer.start(10000)

        timer = QTimer(self)
        timer.timeout.connect(self.timer_random_song)
        timer.start(30000)

    def timer(self):
        if self.Midi.GetInputPort() and not self.ConnectInputState:
            self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))
            self.ConnectInputState = True
        elif not self.Midi.GetInputPort():
            self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
            self.ConnectInputState = False

        if self.Midi.GetOuputPort() and not self.ConnectOutputState:
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))
            self.ConnectOutputState = True
        elif not self.Midi.GetOuputPort():
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
            self.ConnectOutputState = False

        self.midisong = self.Midi.GetMidiSong()

        if self.midisong:
            if self.midisong.IsState(states["cueing"]):
                self.PlayingState = False
                self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_YELLOW_LED))
                self.SetStatusBar("Cueing...")

            elif self.midisong.GetState() > states["cueing"] and not self.PlayingState:
                self.PlayingState = True
                # We lose Del animation
                # self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))
                # We lose 'waiting...' message and other
                # self.SetStatusBar("")

            elif self.midisong.GetState() < states['cueing']:
                self.PlayingState = False
                self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
                if self.midisong.IsState(states["notracktoplay"]):
                    self.SetStatusBar("! No notes in selected channels")

            self.ui.progressBar.setValue(self.midisong.GetPlayed())

            self.SetFileButtonText()
            self.ChannelsSetButtons()
            # just for led off
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))

    def timer_title(self):
        if self.Web_server:
            interfaces = self.Web_server.GetInterfaces()
            self.title_rotation +=1
            if self.title_rotation >= len(interfaces):
                self.title_rotation = -1
                self.setWindowTitle("I LIKE CHOPIN")
            else :
                self.setWindowTitle(interfaces[self.title_rotation])

    def timer_random_song(self):
        self.midisong = self.Midi.GetMidiSong()
        if not self.midisong.IsState(states['playing']) and self.Settings.IsMode(modes["random"]):
            self.MidifileChange(self.Midifiles.GetRandomSong())

    def InputDeviceChanged(self):
        self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
        self.ConnectInputState = False
        in_device = self.ui.InputDeviceCombo.currentText()
        self.Settings.SaveInputDevice(in_device)
        self.Midi.ConnectInput(in_device)

    def OuputDeviceChanged(self):
        self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_RED_LED))
        self.ConnectOutputState = False
        out_device = self.ui.OutputDeviceCombo.currentText()
        self.Settings.SaveOutputDevice(out_device)
        self.Midi.ConnectOutput(out_device)

    def MidifileChange(
        self, filepath
    ):  # ! WARNING ! DO NOT TOUCH INTERFACE (Called by Threads)
        if filepath != self.lastmidifile:
            self.Settings.SaveMidifile(filepath)
            self.midisong = self.Midi.SetMidiSong(filepath)
            self.lastmidifile = filepath
            self.History.AddHistory(filepath)

    def MidifileReplay(self):  # ! WARNING ! DO NOT TOUCH INTERFACE (Called by Threads)
        if self.lastmidifile:
            self.midisong = self.Midi.SetMidiSong(self.lastmidifile)

    def NextMidifile(
        self,
    ):  # from web server ! WARNING ! DO NOT TOUCH INTERFACE (Called by Threads)
        files = self.History.GetHistory()
        self.history_index += 1
        if self.history_index > len(files) - 1:
            self.history_index = len(files)
        self.ui.pushButton_FileIndex.setText(
            f"MidiFile {self.history_index+1}/{len(files)}"
        )
        self.MidifileChange(files[self.history_index])

    def PreviousMidifile(self):
        files = self.History.GetHistory()
        self.history_index -= 1
        if self.history_index<0:
            self.history_index = 0

        print(f" ---> PreviousMidifile index={self.history_index}/{len(files)}")

        self.ui.pushButton_FileIndex.setText(
            f"MidiFile {self.history_index+1}/{len(files)}"
        )
        self.MidifileChange(files[self.history_index])

    # Midi command
    def ChangeMidiFile(self, value):  # External Midi command
        # print("--> ChangeMidiFile NOT ACTIVE FOR INSTANCE")

        # value 0-127
        files = self.History.GetHistory()
        step = int(128 / len(files))
        FilesIndex = min(int(value / step), len(files) - 1)
        if self.lastmidifile != files[FilesIndex]:
            self.ui.pushButton_FileIndex.setText(
                f"MidiFile {FilesIndex+1}/{len(files)}"
            )
            # clean_name = self.History.GetCleanName(FilesIndex)

            self.ui.pushButton_Files.setText(
                self.History.GetCleanName(FilesIndex)
            )  # est écrasé, par timer ?

            # print(f"--> nextmidifile index {FilesIndex} file {files[FilesIndex]}")
            # self.nextmidifile = files[FilesIndex]

            # il faut afficher le titre, puis au bout d'une seconde s'il n'a pas changé, charger la chanson
            # parce qu'il charge et décharge pour rien le reader à chaque fois

            self.Midi.Panic()
            self.lastmidifile = files[FilesIndex]
            self.MidifileChange(files[FilesIndex])

    # Channels
    def ChannelsNone(self):
        for n in range(len(self.ChannelsButtonsList)):
            self.ChannelsButtonsList[n].setChecked(False)
        self.ReadChannels()

    def ChannelsAll(self):
        for n in range(len(self.ChannelsButtonsList)):
            self.ChannelsButtonsList[n].setChecked(True)
        self.ReadChannels()

    def ChannelsFirst(self):
        self.ChannelsNone()
        self.ChannelsButtonsList[0].setChecked(True)
        self.ReadChannels()

    def ChannelsSetButtons(self):
        if self.midisong:
            # Cleanup
            for i in range(len(self.ChannelsButtonsList)):
                self.ChannelsButtonsList[i].setStyleSheet("")
                if i == 9:
                    self.ChannelsButtonsList[i].setStyleSheet(
                        "QPushButton:checked { background-color: rgb(50,100,50); } QPushButton {color: rgb(100,50,50); background-color: rgb(100,50,50);}"
                    )
                else:
                    self.ChannelsButtonsList[i].setStyleSheet(
                        "QPushButton:checked { background-color: rgb(50,100,50); } QPushButton {color: grey}"
                    )
            # Set
            channels = self.midisong.GetChannels()
            for key in channels:
                if channels[key]:  # Show button
                    self.ChannelsButtonsList[int(key)].setStyleSheet("")
                    if int(key) == 9:
                        self.ChannelsButtonsList[int(key)].setStyleSheet(
                            "QPushButton:checked { background-color: rgb(50,100,50); } QPushButton {background-color: rgb(100,50,50);}"
                        )
                    else:
                        self.ChannelsButtonsList[int(key)].setStyleSheet(
                            "QPushButton:checked { background-color: rgb(50,100,50); }"
                        )

    def ReadChannels(self):
        for n in range(len(self.ChannelsButtonsList)):
            if self.ChannelsButtonsList[n].isChecked():
                self.ChannelsList[n] = True
            else:
                self.ChannelsList[n] = False

    # Midi control buttons
    def PrintSpeed(self, speed):  # 0 to 126
        if speed:
            self.ui.pushButton_Speed.setText(f"Speed -{speed}")
        else:
            self.ui.pushButton_Speed.setText("Speed")

    def PrintHumanize(self, value):
        if value:
            self.ui.pushButton_Humanize.setText(f"Humanize {value}")
        else:
            self.ui.pushButton_Humanize.setText("Humanize")

    def SetPlayerModeButtons(self):
        if self.Settings.IsMode(modes["playback"]):
            self.ui.pushButton_Mode.setStyleSheet(
                "QPushButton { background-color: rgb(30,80,30); }\n"
            )
            self.ui.pushButton_Mode.setText("Playback")
            self.ui.pushButton_Mode.setChecked(False)

        elif self.Settings.IsMode(modes["passthrough"]):
            self.ui.pushButton_Mode.setStyleSheet(
                "QPushButton { background-color: rgb(30,80,80); }\n"
            )
            self.ui.pushButton_Mode.setText("Passthrough")
            self.ui.pushButton_Mode.setChecked(False)

        elif self.Settings.IsMode(modes["player"]):
            self.ui.pushButton_Mode.setStyleSheet(
                "QPushButton { background-color: rgb(46,82,168); }\n"
            )
            self.ui.pushButton_Mode.setText("Player")
            self.ui.pushButton_Mode.setChecked(False)
        elif self.Settings.IsMode(modes["random"]):
            self.ui.pushButton_Mode.setStyleSheet(
                "QPushButton { background-color: rgb(0,0,0); }\n"
            )
            self.ui.pushButton_Mode.setText("Random")
            self.ui.pushButton_Mode.setChecked(False)
            self.timer_random_song()

    def ChangePlayerMode(self):  # button mode pressed or called by midi_inpout

        if self.Settings.GetMode() == modes["playback"]:
            self.Settings.SaveMode(modes["passthrough"])

        elif self.Settings.GetMode() == modes["passthrough"]:
            self.Settings.SaveMode(modes["player"])

        elif self.Settings.GetMode() == modes["player"]:
            self.Settings.SaveMode(modes["random"])

        elif self.Settings.GetMode() == modes["random"]:
            self.Settings.SaveMode(modes["playback"])

        self.SetPlayerModeButtons()
        self.Midi.ChangeMidiMode(self.Settings.GetMode())

    # Signal receiver
    def SetLedInput(self, value):  # value (0 or 1)
        if self.Midi:
            if self.Midi.keys["key_on"] > 0:
                self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LIGHT_LED))
            else:
                self.ui.labelStatusInput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))

    # Signal receiver
    def SetLedOutput(self, value):  # 0 or 1
        if value and self.Midi.GetOuputPort():
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LIGHT_LED))
        else:
            self.ui.labelStatusOuput.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))

    # Signal receiver
    def SetLedFile(self, value):  # 0 or 1
        if value:
            self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LIGHT_LED))
        else:
            self.ui.labelStatusMidifile.setPixmap(QtGui.QPixmap(self.ICON_GREEN_LED))

    # Signal receiver
    def SetStatusBar(self, message):
        self.ui.statusbar.showMessage(message)

    def OpenBrowser(self):
        webbrowser.open(f"http://127.0.0.1:{self.Web_server.GetPort()}")

    def Panic(self):
        self.Midi.Panic()

    def SetFileButtonText(self):
        if self.midisong:
            # self.setWindowTitle(f"I Like Chopin : {self.midisong.GetCleanName()}")
            self.ui.pushButton_Files.setText(self.midisong.GetCleanName())

    def Informations(self):
        ShowInformation(self)

    def eventFilter(self, o, e):  # drop files
        if e.type() == QEvent.DragEnter:  # remember to accept the enter event
            e.acceptProposedAction()
            return True
        if e.type() == QEvent.Drop:
            data = e.mimeData()
            urls = data.urls()
            if urls and urls[0].scheme() == "file":
                self.MidifileChange(urls[0].path())
            return True
        return False  # remember to return false for other event types

    # End
    def closeEvent(self, event):  # overwritten
        self.Quit()

    def Quit(self):

        if self.Web_server:
            self.Web_server.stop()
        self.Web_server = None

        if self.Midi:
            self.Midi.quit()
            self.Midi = None

        qApp.quit();

def start():
    if not QApplication.instance():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")  # Windows dark theme
    else:
        app = QApplication.instance()
    widget = MainWindow()
    # For Linux Wayland, must be .desktop filename = Set QMainWindow icon
    app.setDesktopFileName("org.obook.i-like-chopin")
    widget.show()
    sys.exit(app.exec())
