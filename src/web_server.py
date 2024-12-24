#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:30:43 2024
@author: obooklage
"""

import os
import uuid
import json
from threading import Thread
from bottle import run, route, static_file, response, request, redirect, abort, ServerAdapter
from PySide6.QtCore import QThread, Signal
from web_network import ClassWebNetwork

'''
From original bottle.py code
Homepage and documentation: http://bottlepy.org/
Copyright (c) 2009-2024, Marcel Hellkamp.
License: MIT (see LICENSE for details)
'''
class MyWSGIRefServer(ServerAdapter):
    quiet = True  # ADD SILENT MODE.
    def run(self, app):  # pragma: no cover
        from wsgiref.simple_server import make_server
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        import socket

        class FixedHandler(WSGIRequestHandler):
            def address_string(self):  # Prevent reverse DNS lookups please.
                return self.client_address[0]

            def log_request(*args, **kw):
                if not self.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)

        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls = self.options.get('server_class', WSGIServer)

        if ':' in self.host:  # Fix wsgiref for IPv6 addresses.
            if getattr(server_cls, 'address_family') == socket.AF_INET:

                class server_cls(server_cls):
                    address_family = socket.AF_INET6

        self.srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        self.port = self.srv.server_port  # update port actual port (0 means random)

        ''' We do not use KeyboardInterrupt
        try:
            self.srv.serve_forever()
        except KeyboardInterrupt:
            self.srv.server_close()  # Prevent ResourceWarning: unclosed socket
            raise
        '''

        self.srv.serve_forever()

    def shutdown(self):  # ADD SHUTDOWN METHOD.
        self.srv.server_close()
        self.srv.shutdown()

class MyBottleServer:

    pLauncher = None
    pParent = None

    def __init__(self, host, port, launcher):
        self.uuid = uuid.uuid4()
        self.pLauncher = launcher
        self.pParent = launcher.pParent
        self.server = MyWSGIRefServer(host=host, port=port)
        Thread(target=self.begin).start()
        print(f"MyBottleServer {self.uuid} started")

    def __del__(self):
        print(f"MyBottleServer {self.uuid} destroyed")

    def begin(self):
        run(server=self.server)

    def end(self):
        self.server.shutdown()

    def run(self):

        @route('/')
        def index():
            redirect("/static/index.html")

        @route('/static/<filepath:path>')
        def server_static(filepath):
            uipath = self.pParent.Settings.GetUIPath()
            return static_file(filepath, root=uipath)

        @route('/status.json')
        def _status():
            midisong = self.pParent.Midi.GetMidiSong()
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
                return json.dumps(status)  # crash then pgm shutdown
            except Exception as error:
                print(f"|!| BottleServer {self.uuid} error send status {error}")

        @route('/interfaces.json')
        def _interfaces():
            Network = ClassWebNetwork(self.pParent)
            interfaces = Network.GetWebUrls()
            response.content_type = 'application/json'
            return json.dumps(interfaces)

        @route('/files.json')
        def _files():
            file_dic = self.pParent.Midifiles.GetFiles()
            response.content_type = 'application/json'
            return json.dumps(file_dic)

        @route('/play')
        def _play():
            midifile = request.query.song
            print(f"BottleServer {self.uuid} request [{midifile}]")
            if self.pParent:
                '''
                 try:
                     self.pParent.MidifileChange(midifile)  # DANGEROUS ?
                 except:
                     pass
                '''
                self.pParent.MidifileChange(midifile)  # DANGEROUS ?

        @route('/do')
        def _do():
            action = request.query.action

            if self.pParent and action == "stop":
                self.pLauncher.StopSong()
            elif self.pParent and action == "shuffle":
                self.pLauncher.ShuffleSong()
            elif self.pParent and action == "replay":
                self.pLauncher.ReplaySong()

        @route('/player')
        def _player():
            mode = request.query.mode
            # print(f"REQUEST MODE={mode}")
            '''
            try:
                pParent.ChangePlayerMode(mode)  # DANGEROUS ?
            except:
                pass
            '''
            self.pParent.ChangePlayerMode(mode)  # DANGEROUS ?

        @route('/score')
        def _score():
            pdf = request.query.pdf
            file = os.path.join(self.pParent.Settings.GetMidiPath(), pdf)
            if os.path.isfile(file):
                f = open(file, 'rb')
                data = f.read()
                f.close
                response.content_type = 'application/pdf'
                return data
            else:
                print(f"|!| BottleServer {self.uuid} request score {file} note exists")
                abort(404, "Sorry, file not found.")

class ClassWebServer(QThread):

    uuid = None
    pParent = None

    replay_activity = Signal()
    shuffle_activity = Signal()
    SignalStop = Signal()

    def __init__(self, parent):
        QThread.__init__(self)
        self.uuid = uuid.uuid4()
        self.pParent = parent

        # Signals
        self.shuffle_activity.connect(self.pParent.SignalShuffleMidifile)
        self.replay_activity.connect(self.pParent.SignalReplayMidifile)
        self.SignalStop.connect(self.pParent.SignalStop)

        print(f"WebServer {self.uuid} started")

    def __del__(self):
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        server_port = self.pParent.Settings.GetServerPort()
        self.server = MyBottleServer(host="0.0.0.0", port=server_port, launcher=self)
        self.server.run()

    # Signals to parent
    def ReplaySong(self):
        print("---> DEBUG ClassWebServer send ReplaySong...")
        self.replay_activity.emit()

    def ShuffleSong(self):
        print("---> DEBUG ClassWebServer send ShuffleSong...")
        self.shuffle_activity.emit()

    def StopSong(self):
        print("---> DEBUG ClassWebServer send StopSong...")
        self.SignalStop.emit()

    def stop(self):
        print(f"WebServer {self.uuid} stop")
        self.server.end()
