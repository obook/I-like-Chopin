#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
For MIDI Controler, see settings
Tested with Arturia KeyLab 61 Essential
(port [Arturia KeyLab Essential 61:Arturia KeyLab Essential 61 DAW] )
"""

import uuid
from mido import (open_input, open_output, Message)
from PySide6.QtCore import (QThread, QTimer, Signal)

class ClassMidiController(QThread):

    uuid = None
    pParent = None
    device = None
    from_controller = None
    to_controller = None
    timer_controller = None
    running = False
    current_keys_list = []

    SignalReplay = Signal()
    SignalShuffle = Signal()
    SignalStop = Signal()
    SignalMidifileChange = Signal(str)
    SignalTooglePlayerMode = Signal()
    SignalAddToPlaylist = Signal(str)

    KEYLAB_LCD_PRE = [0x00, 0x20, 0x6B, 0x7F, 0x42, 0x04, 0x00, 0x60, 0x01]
    KEYLAB_LCD_SEP = [0x00, 0x02]
    KEYLAB_LCD_END = [0x00]

    def __init__(self, pParent):
        QThread.__init__(self)
        self.pParent = pParent
        self.device = pParent.Settings.GetControllerDevice()
        self.uuid = uuid.uuid4()

        # Signals
        self.SignalShuffle.connect(self.pParent.SignalShuffleMidifile)
        self.SignalReplay.connect(self.pParent.SignalReplayMidifile)
        self.SignalStop.connect(self.pParent.SignalStop)
        self.SignalMidifileChange.connect(self.pParent.SignalMidifileChange)
        self.SignalTooglePlayerMode.connect(self.pParent.SignalTooglePlayerMode)
        self.SignalAddToPlaylist.connect(self.pParent.SignalAddToPlaylist)

        # Timer
        self.timer_controller = QTimer(self)
        self.timer_controller.timeout.connect(self.timer)
        self.timer_controller.start(3000)  # 3 seconds

        print(f"ClassMidiController {self.uuid} created [{self.device}]")

    def __del__(self):
        print(f"ClassMidiController {self.uuid} destroyed [{self.device}]")

    def open_controller(self):

        if self.from_controller:
            self.from_controller.close()
        if self.to_controller:
            self.to_controller.close()

        self.device = self.pParent.Settings.GetControllerDevice()

        try:
            self.from_controller = open_input(self.device, callback=self.callback)
        except Exception as error:
            print(f"|!| ClassMidiController {self.uuid} open_input {error}")
            return False

        try:
            self.to_controller = open_output(self.device)
        except Exception as error:
            print(f"|!| ClassMidiController {self.uuid} open_input {error}")
            self.from_controller.close()
            return False

        return True

    def run(self):

        if not self.open_controller():
            return

        self.ClearSurfaceKeyboard(True)

        self.running = True

        while self.running:
            self.sleep(1)

        self.ClearSurfaceKeyboard(True)

        self.from_controller.close()
        self.to_controller.close()

    def callback(self, msg):

        """Handle MIDI events from device."""

        """
        See : https://github.com/NicoG60/TouchMCU/blob/main/doc/mackie_control_protocol.md

        Play 	A#6 	94 	5E
        Stop 	A6 	93 	5D
        Record 	B6 	95 	5F
        Cycle 	D6 	86 	56
        Rewind 	G6 	91 	5B
        Forward 	G#6 	92 	5C
        Save 	G#5 	80 	50
        Undo 	A5 	81 	51
        Click 	F6 	89 	59 (metronome)

        Punch is a sequence:
            note_on channel 0 note D#6 [87,0x57] velocity 127
            note_on channel 0 note E6 [88,0x58] velocity 127
            note_on channel 0 note D#6 [87,0x57] velocity 0
            note_on channel 0 note E6 [88,0x58] velocity 0
        """

        if msg.type == 'note_on':  # or msg.type == 'note_off':
            if msg.channel == 0:

                # Key : Play = rewind to start and wait
                if msg.note == 94 and msg.velocity:
                    self.ClearSurfaceKeyboard()
                    msg = Message('note_on', note=msg.note)
                    self.to_controller.send(msg)
                    self.SignalReplay.emit()
                    self.current_keys_list.append(msg.note)

                # Key : Stop = stop the song
                elif msg.note == 93 and msg.velocity:
                    self.ClearSurfaceKeyboard()
                    msg = Message('note_on', note=msg.note)
                    self.to_controller.send(msg)
                    self.SignalStop.emit()
                    self.current_keys_list.append(msg.note)

                # Key : Cycle : shuffle a new song
                elif msg.note == 86 and msg.velocity:
                    self.ClearSurfaceKeyboard()
                    msg = Message('note_on', note=msg.note)
                    self.to_controller.send(msg)
                    self.SignalShuffle.emit()
                    self.current_keys_list.append(msg.note)

                # Key : Record : switch Playback/Passthrough
                elif msg.note == 95 and msg.velocity:
                    self.ClearSurfaceKeyboard()
                    msg = Message('note_on', note=msg.note)
                    self.to_controller.send(msg)
                    self.SignalTooglePlayerMode.emit()
                    self.current_keys_list.append(msg.note)

                if self.pParent.Settings.GetDebugMsg():
                    print("--> ClassMidiController receive:", msg)

    def ClearSurfaceKeyboard(self, force = False):
        """Shutdown lights from surface control (Arturia)."""
        if self.to_controller:
            if len(self.current_keys_list):
                for key in self.current_keys_list:
                    msg = Message('note_on', note=key, velocity=0)
                    self.to_controller.send(msg)
                    self.current_keys_list.remove(key)

            elif force:
                self.current_keys_list = []
                keys = [94, 93, 95, 86, 91, 92, 80, 81, 89, 95]
                for key in keys:
                    msg = Message('note_on', note=key, velocity=0)  # note_off do not works
                    self.to_controller.send(msg)

    def LCD_StringToDec(self, line):
        dec = []
        for c in line:
            if ord(c) > 127:  # only ASCII please...
                c=" "
            dec.append(int(ord(c)))
            if len(dec) > 15:  # no more 16 chars please...
                break
        return dec

    def LCD_Message(self, line1, line2):
        if self.to_controller:
            msg = Message('sysex', data=[])
            msg.data += self.KEYLAB_LCD_PRE
            msg.data += self.LCD_StringToDec(line1)
            msg.data += self.KEYLAB_LCD_SEP
            msg.data += self.LCD_StringToDec(line2)
            msg.data += self.KEYLAB_LCD_END

            self.to_controller.send(msg)

    def timer(self):
            self.ClearSurfaceKeyboard()

    # Signals
    def SignalLightPlay(self):
        if self.to_controller:
            self.current_keys_list.append(94)
            msg = Message('note_on', note=(94))
            self.to_controller.send(msg)

    def SignalLightStop(self):
        if self.to_controller:
            self.current_keys_list.append(93)
            msg = Message('note_on', note=(93))
            self.to_controller.send(msg)

    def stop(self):
        self.running = False
