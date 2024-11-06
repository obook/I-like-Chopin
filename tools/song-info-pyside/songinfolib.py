#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:17:57 2024
@author: obooklage
! Channels are from 0 to 15
"""
from mido import MidiFile, MetaMessage

class MidiSong:
    tracks = []
    duration = 0
    total_notes_on = 0
    channels_notes_on = {}
    sustain = 0

    def __init__(self, file):
        self.file = file
        self.tracks = []
        self.duration = 0
        self.total_notes_on = 0
        self.channels_notes_on = {}
        self.sustain = 0
        self.set_tempo = 0
        self.GetInfo()

    def GetInfo(self):

        # Tracks Informations

        try:
            midi = MidiFile(self.file)  # , debug=True  # PUT IN MIDI_SONG
        except:
            return False  # Bad Midifile (value > 127 ?)

        self.duration = midi.length / 60
        for i, track in enumerate(midi.tracks):
            self.tracks.append(track.name)

        # Notes in selected channels (0-15)
        for msg in MidiFile(self.file):

            if msg.type == "note_on":
                if msg.velocity:
                    self.total_notes_on += 1
                    key = int(msg.channel)
                    if key not in self.channels_notes_on.keys():
                        self.channels_notes_on[int(key)] = 0
                    self.channels_notes_on[int(key)] += 1

            if msg.type == "control_change":
                # The sustain pedal sends CC 64 127
                # and CC 64 0 messages on channel 1
                if msg.control == 64:  # bug fixed, is not value, but control
                    self.sustain += 1

            elif isinstance(msg, MetaMessage):
                if msg.type == 'set_tempo':
                    self.set_tempo += 1

            # meta : set_tempo
            # elif msg.control == 64:

        self.channels_notes_on = dict(
            sorted(self.channels_notes_on.items())
        )
