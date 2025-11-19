#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:30:43 2024
@author: obooklage
"""

import os
import uuid
import json
from typing import Any, cast
from PySide6.QtCore import QThread, Signal
from bottle import run, route, static_file, response, request, redirect, abort, ServerAdapter, hook
from web_network import ClassWebNetwork

'''
Class MyWSGIRefServer from original bottle.py code
Homepage and documentation: http://bottlepy.org/
Copyright (c) 2009-2024, Marcel Hellkamp.
License: MIT (see LICENSE for details)
'''
class MyWSGIRefServer(ServerAdapter):
    quiet = True  # ADD SILENT MODE.
    def run(self, handler):  # pragma: no cover
        from wsgiref.simple_server import make_server
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        import socket

        class FixedHandler(WSGIRequestHandler):

            def address_string(self):  # Prevent reverse DNS lookups please.
                return self.client_address[0]

            def log_request(self, *args, **kw):
                if not MyWSGIRefServer.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)
                else:
                    return None

        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls = self.options.get('server_class', WSGIServer)

        if ':' in self.host:  # Fix wsgiref for IPv6 addresses.
            if getattr(server_cls, 'address_family') == socket.AF_INET:

                class _IPv6Server(server_cls):
                    address_family = socket.AF_INET6
                server_cls = _IPv6Server

        # If port is busy !
        try:
            self.srv = make_server(self.host, self.port, handler, server_cls, handler_cls)
            self.port = self.srv.server_port  # update port actual port (0 means random)
        except Exception as error:
            print(f"|!| WEBSERVER CAN NOT START : {error}")
            self.srv= None
            return

        ''' We do not use KeyboardInterrupt
        try:
            self.srv.serve_forever()
        except KeyboardInterrupt:
            self.srv.server_close()  # Prevent ResourceWarning: unclosed socket
            raise
        '''

        self.srv.serve_forever()

    def shutdown(self):  # ADD SHUTDOWN METHOD.
        if self.srv:
            try:  # bug under Windows, sometimes...
                self.srv.server_close()
                self.srv.shutdown()
            except:
                pass


class MyBottleServer:

    # pLauncher = None
    # pParent = None
    # Settings = None
    # Midi = None

    def __init__(self, host, port, launcher):
        self.uuid = uuid.uuid4()
        self.pLauncher = launcher
        self.pParent = launcher.pParent
        self.Settings = self.pParent.Settings
        self.Midi = self.pParent.Midi
        self.server = MyWSGIRefServer(host=host, port=port)
        # Ne pas démarrer le serveur ici : run() enregistrera d'abord routes/hooks puis lancera le serveur.
        # Thread(target=self.begin).start()
        # print(f"MyBottleServer {self.uuid} started")

    def __del__(self):
        print(f"MyBottleServer {self.uuid} destroyed")

    def begin(self):
        run(server=self.server)  # type: ignore[arg-type]

    def end(self):
        self.server.shutdown()

    def run(self):

        # Appliquer une CSP sur toutes les réponses
        @hook('after_request')
        def apply_csp():
            # Supprimer un éventuel header report-only provenant d'ailleurs
            response.headers.pop('Content-Security-Policy-Report-Only', None)

            # Politique réelle : autoriser scripts depuis self et éléments <script>
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "script-src-elem 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; "
                "connect-src 'self' http: https: ws:;"
            )
            response.headers['Content-Security-Policy'] = csp

        @route('/')
        def index():
            apply_csp()
            redirect("/static/index.html")

        @route('/static/<filepath:path>')
        def server_static(filepath):
            uipath = self.Settings.GetUIPath()
            result = static_file(filepath, root=uipath)
            apply_csp()
            return result

        @route('/status.json')
        def _status():
            midisong = self.Midi.GetMidiSong()
            if midisong:
                status = {
                         "uuid":str(midisong.Getuuid()),
                         "played":midisong.GetPlayed(),
                         "duration":round(midisong.GetDuration(), 2),
                         "name":midisong.GetFilename(),
                         "nameclean":midisong.GetCleanName(),
                         "score":midisong.GetScore(),
                         "folder":midisong.GetParent(),
                         "state":midisong.GetState(),
                         "mode":midisong.GetMode(),
                         "tracks":midisong.GetTracks(),
                         "channels":midisong.GetChannels(),
                         "sustain":midisong.GetSustain(),
                     }
                response.content_type = 'application/json'
                try:
                    apply_csp()
                    return json.dumps(status)  # crash then pgm shutdown
                except Exception as error:
                    print(f"|!| BottleServer {self.uuid} error send status {error}")

        @route('/interfaces.json')
        def _interfaces():
            Network = ClassWebNetwork(self.pParent)
            interfaces = Network.GetWebUrls()
            response.content_type = 'application/json'
            apply_csp()
            return json.dumps(interfaces)

        @route('/files.json')
        def _files():
            file_dic = self.pParent.Midifiles.GetFiles()
            response.content_type = 'application/json'
            apply_csp()
            return json.dumps(file_dic)

        @route('/playlist.json')
        def _playlist():
            file_dic = self.pParent.Playlist.GetPlayList()
            response.content_type = 'application/json'
            apply_csp()
            return json.dumps(file_dic)

        @route('/play')
        def _play():
            query_params = cast(Any, request.query)
            midifile = query_params.get('song')
            print(f"BottleServer {self.uuid} request [{midifile}]")
            self.pLauncher.ChangeSong(midifile)

        @route('/do')
        def _do():
            query_params = cast(Any, request.query)
            action = query_params.get('action')
            if self.pParent and action == "stop":
                self.pLauncher.StopSong()
            elif self.pParent and action == "shuffle":
                self.pLauncher.ShuffleSong()
            elif self.pParent and action == "replay":
                self.pLauncher.ReplaySong()

        @route('/player')
        def _player():
            query_params = cast(Any, request.query)
            mode = query_params.get('mode')
            self.pLauncher.ChangeMode(mode)

        @route('/add')
        def _add():
            query_params = cast(Any, request.query)
            quality = query_params.get('quality')
            self.pLauncher.AddToPlaylist(quality)

        @route('/score')
        def _score():
            query_params = cast(Any, request.query)
            pdf = query_params.get('pdf')
            file = os.path.join(self.Settings.GetMidiPath(), pdf)
            if os.path.isfile(file):
                f = open(file, 'rb')
                data = f.read()
                f.close
                response.content_type = 'application/pdf'
                apply_csp()
                return data
            else:
                print(f"|!| BottleServer {self.uuid} request score {file} note exists")
                abort(404, "Sorry, file not found.")

        # Démarrer le serveur APRÈS enregistrement des routes/hooks (bloquant)
        self.begin()
        print(f"MyBottleServer {self.uuid} started")

class ClassWebServer(QThread):

    # uuid = None
    # pParent = None

    SignalReplay = Signal()
    SignalShuffle = Signal()
    SignalStop = Signal()
    SignalMidifileChange = Signal(str)
    SignalChangePlayerMode = Signal(str)
    SignalAddToPlaylist = Signal(str)

    def __init__(self, parent):
        QThread.__init__(self)
        self.uuid = uuid.uuid4()
        self.pParent = parent

        # Signals
        self.SignalShuffle.connect(self.pParent.SignalShuffleMidifile)  # type: ignore
        self.SignalReplay.connect(self.pParent.SignalReplayMidifile)  # type: ignore
        self.SignalStop.connect(self.pParent.SignalStop)  # type: ignore
        self.SignalMidifileChange.connect(self.pParent.SignalMidifileChange)  # type: ignore
        self.SignalChangePlayerMode.connect(self.pParent.SignalChangePlayerMode)  # type: ignore
        self.SignalAddToPlaylist.connect(self.pParent.SignalAddToPlaylist)  # type: ignore

        print(f"WebServer {self.uuid} started")

    def __del__(self):
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        server_port = self.pParent.Settings.GetServerPort()  # type: ignore
        self.server = MyBottleServer(host="0.0.0.0", port=server_port, launcher=self)
        self.server.run()

    def stop(self):
        print(f"WebServer {self.uuid} stop")
        self.server.end()

    # Signals to parent
    def ReplaySong(self):
        self.SignalReplay.emit()

    def ChangeSong(self, file):
        self.SignalMidifileChange.emit(file)

    def ShuffleSong(self):
        self.SignalShuffle.emit()

    def StopSong(self):
        print(f"WebServer {self.uuid} StopSong signal emitted")
        self.SignalStop.emit()

    def ChangeMode(self, mode):
        self.SignalChangePlayerMode.emit(mode)

    def AddToPlaylist(self, quality):
        self.SignalAddToPlaylist.emit(quality)
