#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:30:43 2024
@author: obooklage
"""

import os
import uuid
import json
from bottle import Bottle, static_file, response, request, redirect
from PySide6.QtCore import QThread
from web_network import ClassWebNetwork

# Project :

'''
########################################################################
# Run a WSGI application in a daemon thread

import bottle
import threading
import socket
import time as _time

class Server(bottle.WSGIRefServer):
    def run(self, handler): # pragma: no cover
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            base = self.options.get('handler_class', WSGIRequestHandler)
            class QuietHandler(base):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.srv = make_server(self.host, self.port, handler, **self.options)
        self.srv.serve_forever(poll_interval=0.1)

def start_bottle_server(app, port, **kwargs):
    server_thread = ServerThread(app, port, kwargs)
    server_thread.daemon = True
    server_thread.start()

    ok = False
    for i in range(10):
        try:
            conn = socket.create_connection(('127.0.0.1', port), 0.1)
        except socket.error as e:
            _time.sleep(0.1)
        else:
            conn.close()
            ok = True
            break
    if not ok:
        import warnings
        warnings.warn('Server did not start after 1 second')

    return server_thread.server

class ServerThread(threading.Thread):
    def __init__(self, app, port, server_kwargs):
        threading.Thread.__init__(self)
        self.app = app
        self.port = port
        self.server_kwargs = server_kwargs
        self.server = Server(host='localhost', port=self.port, **self.server_kwargs)

    def run(self):
        bottle.run(self.app, server=self.server, quiet=True)

def app_runner_setup(*specs):
    Returns setup and teardown methods for running a list of WSGI
    applications in a daemon thread.

    Each argument is an (app, port) pair.

    Return value is a (setup, teardown) function pair.

    The setup and teardown functions expect to be called with an argument
    on which server state will be stored.

    Example usage with nose:

    >>> setup_module, teardown_module = \
        webracer.utils.runwsgi.app_runner_setup((app_module.app, 8050))


    def setup(self):
        self.servers = []
        for spec in specs:
            if len(spec) == 2:
                app, port = spec
                kwargs = {}
            else:
                app, port, kwargs = spec
            self.servers.append(start_bottle_server(app, port, **kwargs))

    def teardown(self):
        for server in self.servers:
            server.srv.shutdown()

    return [setup, teardown]

########################################################################
# Not used
class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        # self.server.server_close() <--- alternative but causes bad fd exception
        self.server.shutdown()

'''

# Used, but never stop
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
        # self._app.route('/midi/<filepath:path>',callback=self._server_midi)
        self._app.route('/status.json',callback=self._status)
        self._app.route('/interfaces.json',callback=self._interfaces)
        self._app.route('/files.json',callback=self._files)
        self._app.route('/play',callback=self._play)
        self._app.route('/do',callback=self._do)
        self._app.route('/player',callback=self._player)
        self._app.route('/score',callback=self._score)

    def start(self):
            # BLOCKING !
            self.server = self._app.run(host=self._host, port=self._port, debug=True, quiet=True)

    def _index(self):
        redirect("/static/index.html")

    def _server_static(self, filepath):
        uipath = self.pParent.Settings.GetUIPath()
        return static_file(filepath, root=uipath)
    '''
    def _server_midi(self, filepath):
        midipath = self.pParent.Settings.GetMidiPath()
        return static_file(filepath, root=midipath)
    '''
    def _status(self):
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

    def _score(self):
        pdf = request.query.pdf
        file = os.path.join(self.pParent.Settings.GetMidiPath(), pdf)
        if os.path.isfile(file):
            print(f"REQUEST SCORE={file} EXISTS")
            f = open(file, 'rb')
            data = f.read()
            f.close
            response.content_type = 'application/pdf'
            return data
        else:
            print(f"REQUEST SCORE={file} NOT EXISTS")

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
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        self.server = BottleServer(host="0.0.0.0", port=self.port, parent=self.pParent)
        # print(f"**** DEBUG={self.server}")
        self.server.start()
        '''
        self.server_process = Process(target=self.startserver)
        self.server_process.start()


    def startserver(self):
        print(f"WebServer {self.uuid} start")
        self.server = BottleServer(host="0.0.0.0", port=self.port, parent=self.pParent)
        self.server.start()
        print(f"WebServer {self.uuid} stop")
        '''
    def stop(self):
        print(f"WebServer {self.uuid} stop")
        # self.server_process.terminate()
        pass
