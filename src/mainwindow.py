# This Python file uses the following encoding: utf-8
'''
PySide6

CapLinux:
! Passer par QTCreator ou (moins bien)
pip3 install pyside6

'''
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import QTimer, QThread
from PySide6.QtGui import QIcon

#from midi_numbers import number_to_note

# Important but not user under QTCreator :
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from threading import Thread
from midimain import GetDevices, GetMidiFiles, ThreadPlayer, MidiStop, MidiStatus, MidiPanic
from settings import GetInputDeviceId, SaveInputDeviceId, GetOutputDeviceId,SaveOutputDeviceId,GetmidifileId,SavemidifileId
import time

class FireAndForget(QThread):
    bGlobalStatusRun = False

    def __init__(self, max, sleep, label):
        super().__init__()
        self.label = label
        self.max = max
        self.sleep = sleep
        print("FireAndForget __init__")

    def run(self):
        print("FireAndForget run")
        '''
        while True:
            print("FireAndForget run")

            ThreadPlayerStatus, ThreadKeyBoardStatus = MidiStatus()
            if ThreadPlayerStatus or ThreadKeyBoardStatus: # All running
                if self.bGlobalStatusRun == False :
                    self.ui.pushButton_Quit.setEnabled(False)
                    self.ui.pushButton_Start.setEnabled(False)
                    self.ui.InputDeviceCombo.setEnabled(False)
                    self.ui.OutputDeviceCombo.setEnabled(False)
                    self.ui.FileCombo.setEnabled(False)
                    self.bGlobalStatusRun = True
            elif not ThreadPlayerStatus and not ThreadKeyBoardStatus: # All stopped
                if self.bGlobalStatusRun == True:
                    self.ui.pushButton_Quit.setEnabled(True)
                    self.ui.pushButton_Start.setEnabled(True)
                    self.ui.InputDeviceCombo.setEnabled(True)
                    self.ui.OutputDeviceCombo.setEnabled(True)
                    self.ui.FileCombo.setEnabled(True)
                    self.ui.statusbar.showMessage(u"Ready.")
                    self.bGlobalStatusRun = False
            '''
        time.sleep(3)

    '''
        print("FireAndForget run")
        self.label.setText(f"{self.max} {self.sleep}")

        for x in range(self.max):
            self.label.text = f"Count {x}"
            time.sleep(self.sleep)  # or use self.msleep(ms) as alternative
    '''

class MainWindow(QMainWindow):
    bGlobalStatusRun = False
    ChannelButtonsList = []
    ChannelList = [False]*16

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        # self.ui.setFixedSize(self.ui.sizeHint())
        # self.ui.setWindowFlags(QMainWindow.Dialog | QMainWindow.MSWindowsFixedSizeDialogHint)
        # vérrouille mais pas à la bonne taille
        # self.setFixedSize(self.size())

        # Ok
        self.setFixedSize(509,413)

        self.ui.setupUi(self)

        # Wayland -> not implemented yet :
        # X.org -> correct
        my_icon = QIcon()
        my_icon.addFile('dummy_piano_player.png')
        self.setWindowIcon(my_icon)

        self.ui.pushButton_Start.clicked.connect(self.Start)
        self.ui.pushButton_Stop.clicked.connect(self.Stop)
        self.ui.pushButton_Quit.clicked.connect(self.Quit)
        self.ui.pushButton_Mode.clicked.connect(self.Mode)

        self.ui.pushButton_ChannelNone.clicked.connect(self.ChannelNone)
        self.ui.pushButton_ChannelAll.clicked.connect(self.ChannelAll)
        self.ui.pushButton_ChannelFirst.clicked.connect(self.ChannelFirst)

        self.ui.pushButton_Panic.clicked.connect(self.Panic)

        self.ui.pushButton_Stop.setEnabled(False)

        Inputs, Outputs = GetDevices()

        self.ui.InputDeviceCombo.addItems(Inputs)
        try:
            self.ui.InputDeviceCombo.setCurrentIndex(GetInputDeviceId())
        except:
            pass

        self.ui.OutputDeviceCombo.addItems(Outputs)
        try:
            self.ui.OutputDeviceCombo.setCurrentIndex(GetOutputDeviceId())
        except:
            pass

        MidiFiles = GetMidiFiles()
        self.ui.FileCombo.addItems(MidiFiles)
        try:
            self.ui.FileCombo.setCurrentIndex(GetmidifileId())
        except:
            pass

        self.ui.pushButton_Mode.setText(u"Midi Auto Player")

        # grid
        grid = self.ui.gridLayout
        for n in range(8):
            self.ChannelButtonsList.append(QPushButton(str(n+1)))
            self.ChannelButtonsList[n].setCheckable(True);
            self.ChannelButtonsList[n].clicked.connect(self.ReadChannel)
            self.ChannelButtonsList[n].setStyleSheet("QPushButton:checked { background-color: rgb(0,200,0); }\n")
            grid.addWidget(self.ChannelButtonsList[n],1,n)
        for n in range(8):
            self.ChannelButtonsList.append(QPushButton(str(n+8+1)))
            self.ChannelButtonsList[n+8].setCheckable(True);
            self.ChannelButtonsList[n+8].clicked.connect(self.ReadChannel)
            self.ChannelButtonsList[n+8].setStyleSheet("QPushButton:checked { background-color: rgb(0,200,0); }\n")
            grid.addWidget(self.ChannelButtonsList[n+8],2,n)

        self.ChannelFirst()

        timer = QTimer(self)
        timer.timeout.connect(self.Timer)
        timer.start(3000) # Refesh Rate in milliseconds, problems with QSampler ?

        '''
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.progress.connect(self.reportProgress)
        # Start the thread
        self.thread.start()
        # Final resets
        #self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            #lambda: self.longRunningBtn.setEnabled(True)
            lambda: print("SetEnabled(True)")
        )
        self.thread.finished.connect(
            lambda: print("finished.connect")
        )
        '''

        '''
        self.ui.label1.setText("LABEL #1")
        self.ui.label2.setText("LABEL #2")

        self.t = FireAndForget(7, 1, self.ui.label1)
        self.t2 = FireAndForget(50, .15, self.ui.label2)
        self.t.run()
        self.t2.run()
        '''

    def Start(self):
        in_device = self.ui.InputDeviceCombo.currentText()
        out_device = self.ui.OutputDeviceCombo.currentText()
        midifile = self.ui.FileCombo.currentText()

        player_thread = Thread(target=ThreadPlayer, args=(in_device, out_device, midifile,self))
        player_thread.start()

        self.ui.pushButton_Stop.setEnabled(True)
        self.ui.pushButton_Start.setEnabled(False)
        self.ui.pushButton_Quit.setEnabled(False)
        self.HideDevices()

    def Stop(self):
        MidiStop()
        SaveInputDeviceId(self.ui.InputDeviceCombo.currentIndex())
        SaveOutputDeviceId(self.ui.OutputDeviceCombo.currentIndex())
        SavemidifileId(self.ui.FileCombo.currentIndex())
        self.ui.pushButton_Start.setEnabled(True)
        self.ui.pushButton_Stop.setEnabled(False)
        self.ShowDevices()

    def Timer(self):
        ThreadPlayerStatus, ThreadKeyBoardStatus = MidiStatus()
        if ThreadPlayerStatus or ThreadKeyBoardStatus: # All running
            self.HideDevices()
        elif not ThreadPlayerStatus and not ThreadKeyBoardStatus: # All stopped
            self.ShowDevices()

    def HideDevices(self):
        if self.bGlobalStatusRun == False :
            self.ui.pushButton_Quit.setEnabled(False)
            self.ui.pushButton_Start.setEnabled(False)
            self.ui.InputDeviceCombo.setEnabled(False)
            self.ui.OutputDeviceCombo.setEnabled(False)
            self.ui.FileCombo.setEnabled(False)
            self.ui.statusbar.showMessage(u"Running...")
            self.bGlobalStatusRun = True

    def ShowDevices(self):
        if self.bGlobalStatusRun == True:
            self.ui.pushButton_Quit.setEnabled(True)
            self.ui.pushButton_Start.setEnabled(True)
            self.ui.InputDeviceCombo.setEnabled(True)
            self.ui.OutputDeviceCombo.setEnabled(True)
            self.ui.FileCombo.setEnabled(True)
            self.ui.statusbar.showMessage(u"Ready.")
            self.bGlobalStatusRun = False

    def Quit(self):
        self.Stop()
        app.quit()

    def Mode(self):
        print("Mode")

    def Led(self, iChannel,sStatus, notenum):
        '''
        # On a de zéro à ?
        #
        try:

            note, octave = number_to_note(notenum)
            # print("Channel ", iChannel, "status", sStatus,"note", notenum)
            self.ui.statusbar.showMessage(f"CH{iChannel+1} {note}{octave}" )

            # BOF self.ChannelButtonsList[iChannel].setChecked(True) # prend trop de temps, on loupe des notes du clavier

            # Crash because come from other thread
            if sStatus == 'note_on':
                self.ChannelButtonsList[iChannel].setStyleSheet('QPushButton {color: red;}')
            elif sStatus == 'note_off':
                self.ChannelButtonsList[iChannel].setStyleSheet('QPushButton {color: normal;}')

        except:
            '''
        pass

    def ChannelNone(self):
        for n in range(len(self.ChannelButtonsList)):
            self.ChannelButtonsList[n].setChecked(False)
        self.ReadChannel()

    def ChannelAll(self):
        for n in range(len(self.ChannelButtonsList)):
            self.ChannelButtonsList[n].setChecked(True)
        self.ReadChannel()

    def ChannelFirst(self):
        self.ChannelNone()
        self.ChannelButtonsList[0].setChecked(True)
        self.ReadChannel()

    def ReadChannel(self):
        for n in range(len(self.ChannelButtonsList)):
            if self.ChannelButtonsList[n].isChecked():
                self.ChannelList[n] = True
            else:
                self.ChannelList[n] = False

    def ChannelIsActive(self,n):
        return(self.ChannelList[n])

    def Panic(self):
        MidiPanic()

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    widget = MainWindow()
    widget.setWindowTitle("Dummy Piano Player")
    print("desktopFileName=", app.desktopFileName())
    app.setDesktopFileName("dummy_piano_player")
    print("desktopFileName=", app.desktopFileName())
    widget.show()
    sys.exit(app.exec())




