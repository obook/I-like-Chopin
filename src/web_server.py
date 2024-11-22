#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:30:43 2024
@author: obooklage
"""

import uuid
import json
from bottle import Bottle, static_file, response, request, redirect
from PySide6.QtCore import QThread
from web_network import ClassWebNetwork


class BottleServer:
    def __init__(self, host, port, parent):
        self.uuid = uuid.uuid4()
        print(f"BottleServer {self.uuid} started")
        self._host = host
        self._port = port
        self.pParent = parent
        self._app = Bottle()
        self._route()

    def __del__(self):
        print(f"BottleServer {self.uuid} destroyed")

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/static/<filepath:path>',callback=self._server_static)
        self._app.route('/status.json',callback=self._status)
        self._app.route('/interfaces.json',callback=self._interfaces)
        self._app.route('/files.json',callback=self._files)
        self._app.route('/play',callback=self._play)
        self._app.route('/do',callback=self._do)
        self._app.route('/player',callback=self._player)

    def start(self):
            self.server = self._app.run(host=self._host, port=self._port, debug=True, quiet=True)

    def _index(self):
        redirect("/static/index.html")

    def _server_static(self, filepath):
        uipath = self.pParent.Settings.GetUIPath()
        return static_file(filepath, root=uipath)

    def _status(self):
        midisong = self.pParent.Midi.GetMidiSong()
        if midisong:
            status = {
                     "uuid":str(midisong.Getuuid()),
                     "played":midisong.GetPlayed(),
                     "duration":round(midisong.GetDuration(), 2),
                     "nameclean":midisong.GetCleanName(),
                     "folder":midisong.GetParent(),
                     "state":midisong.GetState(),
                     "mode":midisong.GetMode(),
                     "tracks":midisong.GetTracks(),
                     "channels":midisong.GetChannels(),
                     "sustain":midisong.GetSustain(),
                 }
        response.content_type = 'application/json'
        try:
            return json.dumps(status)  # crash then pgm shutdown
        except Exception as error:
            print(f"|!| BottleServer {self.uuid} error send status {error}")

    def _interfaces(self):
        Network = ClassWebNetwork(self.pParent)
        interfaces = Network.GetWebUrls()
        response.content_type = 'application/json'
        return json.dumps(interfaces)

    def _files(self):
        file_dic = self.pParent.Midifiles.GetFiles()
        response.content_type = 'application/json'
        return json.dumps(file_dic)

    def _play(self):
        midifile = request.query.song
        print(f"BottleServer {self.uuid} request [{midifile}]")
        if self.pParent:
             try:
                 self.pParent.MidifileChange(midifile)  # DANGEROUS ?
             except:
                 pass

    def _do(self):
        action = request.query.action
        print(f"REQUEST DO={action}")
        if self.pParent and action == "stop":
            try:
                self.pParent.Midi.StopPlayer()  # DANGEROUS ?
            except:
                pass
        elif self.pParent and action == "shuffle":  # ex "next"
            try:
                self.pParent.ShuffleMidifile()  # DANGEROUS ?
            except:
                pass
        elif self.pParent and action == "replay":
            try:
                self.pParent.MidifileReplay()  # DANGEROUS ?
            except:
                pass

    def _player(self):
        mode = request.query.mode
        print(f"REQUEST MODE={mode}")
        try:
            self.pParent.ChangePlayerMode(mode)  # DANGEROUS ?
        except:
            pass

class ClassWebServer(QThread):
    uuid = None
    pParent = None
    Settings = None

    def __init__(self, parent):
        QThread.__init__(self)
        self.uuid = uuid.uuid4()
        self.pParent = parent
        self.Settings = parent.Settings
        self.port = self.Settings.GetServerPort()

    def __del__(self):
        if self.server:
            self.server.server_close()
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        self.server = BottleServer(host="0.0.0.0", port=self.port, parent=self.pParent)
        self.server.start()
        pass

    def stop(self):
        self.server = None
        pass # comment quitter proprement ?
