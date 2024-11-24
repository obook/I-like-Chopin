#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:30:43 2024
@author: obooklage
@Todo : quiet do not works
"""

import os
import uuid
import json
from threading import Thread
from bottle import run, route, static_file, response, request, redirect, abort, ServerAdapter
from PySide6.QtCore import QThread
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

        self.srv = make_server(self.host, self.port, app, server_cls,
                               handler_cls)
        self.port = self.srv.server_port  # update port actual port (0 means random)
        try:
            self.srv.serve_forever()
        except KeyboardInterrupt:
            self.srv.server_close()  # Prevent ResourceWarning: unclosed socket
            raise

    def shutdown(self):  # ADD SHUTDOWN METHOD.
        self.srv.server_close()
        self.srv.shutdown()

# VERY DURTY !
_MyBottleServerSetup = {"uuid": None, 'parent': None}

class MyBottleServer:
    def __init__(self, host, port, parent):
        global _MyBottleServerSetup
        self.uuid = uuid.uuid4()
        print(f"MyBottleServer {self.uuid} started")
        self.pParent = parent
        _MyBottleServerSetup['uuid'] = self.uuid
        _MyBottleServerSetup['parent'] = parent
        # self._app = Bottle()
        # self._route()
        self.server = MyWSGIRefServer(host=host, port=port)
        Thread(target=self.begin).start()

    def __del__(self):
        print(f"MyBottleServer {self.uuid} destroyed")

    def _route(self):
        self._app.route('/', callback=self._index)
        self._app.route('/static/<filepath:path>',callback=self._server_static)
        # self._app.route('/midi/<filepath:path>',callback=self._server_midi)
        self._app.route('/status.json',callback=self._status)
        self._app.route('/interfaces.json',callback=self._interfaces)
        self._app.route('/files.json',callback=self._files)
        self._app.route('/play',callback=self._play)
        self._app.route('/do',callback=self._do)
        self._app.route('/player',callback=self._player)
        self._app.route('/score',callback=self._score)

    def begin(self):
        run(server=self.server)

    def end(self):
        self.server.shutdown()

    @route('/')
    def index():
        redirect("/static/index.html")

    @route('/static/<filepath:path>')
    def server_static(filepath):
        global _MyBottleServerSetup
        uipath = "/home/obooklage/Documents/GitHub/I-like-Chopin/src/ui/"
        return static_file(filepath, root=uipath)

    @route('/status.json')
    def _status():
        global _MyBottleServerSetup
        uuid = _MyBottleServerSetup['uuid']
        pParent =  _MyBottleServerSetup['parent']
        midisong = pParent.Midi.GetMidiSong()
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
            print(f"|!| BottleServer {uuid} error send status {error}")

    @route('/interfaces.json')
    def _interfaces():
        global _MyBottleServerSetup
        pParent =  _MyBottleServerSetup['parent']
        Network = ClassWebNetwork(pParent)
        interfaces = Network.GetWebUrls()
        response.content_type = 'application/json'
        return json.dumps(interfaces)

    @route('/files.json')
    def _files():
        global _MyBottleServerSetup
        pParent =  _MyBottleServerSetup['parent']
        file_dic = pParent.Midifiles.GetFiles()
        response.content_type = 'application/json'
        return json.dumps(file_dic)

    @route('/play')
    def _play():
        global _MyBottleServerSetup
        pParent =  _MyBottleServerSetup['parent']
        uuid = _MyBottleServerSetup['uuid']
        midifile = request.query.song
        print(f"BottleServer {uuid} request [{midifile}]")
        if pParent:
             try:
                 pParent.MidifileChange(midifile)  # DANGEROUS ?
             except:
                 pass

    @route('/do')
    def _do():
        global _MyBottleServerSetup
        pParent =  _MyBottleServerSetup['parent']
        action = request.query.action
        print(f"REQUEST DO={action}")
        if pParent and action == "stop":
            try:
                pParent.Midi.StopPlayer()  # DANGEROUS ?
            except:
                pass
        elif pParent and action == "shuffle":  # ex "next"
            try:
                pParent.ShuffleMidifile()  # DANGEROUS ?
            except:
                pass
        elif pParent and action == "replay":
            try:
                pParent.MidifileReplay()  # DANGEROUS ?
            except:
                pass

    @route('/player')
    def _player():
        global _MyBottleServerSetup
        pParent =  _MyBottleServerSetup['parent']
        mode = request.query.mode
        print(f"REQUEST MODE={mode}")
        try:
            pParent.ChangePlayerMode(mode)  # DANGEROUS ?
        except:
            pass

    @route('/score')
    def _score():
        global _MyBottleServerSetup
        pParent =  _MyBottleServerSetup['parent']
        uuid = _MyBottleServerSetup['uuid']
        pdf = request.query.pdf
        file = os.path.join(pParent.Settings.GetMidiPath(), pdf)
        if os.path.isfile(file):
            f = open(file, 'rb')
            data = f.read()
            f.close
            response.content_type = 'application/pdf'
            return data
        else:
            print(f"|!| BottleServer {uuid} request score {file} note exists")
            abort(404, "Sorry, file not found.")

class ClassWebServer(QThread):
    uuid = None
    pParent = None
    Settings = None

    def __init__(self, parent):
        QThread.__init__(self)
        self.uuid = uuid.uuid4()
        print(f"WebServer {self.uuid} started")
        self.pParent = parent
        self.Settings = parent.Settings
        self.port = self.Settings.GetServerPort()

    def __del__(self):
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        self.server = MyBottleServer(host="0.0.0.0", port=self.port, parent=self.pParent)

    def stop(self):
        print(f"WebServer {self.uuid} stop")
        self.server.end()
