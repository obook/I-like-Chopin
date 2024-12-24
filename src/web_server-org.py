#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 07:12:28 2024
@author: obooklage
Custom response code server by Cees Timmerman, 2023-07-11.
"""
import os
import uuid
import glob
import pathlib
import json
import qrcode
import qrcode.image.svg
import io
from functools import partial

from PySide6.QtCore import QThread, Signal

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
from web_network import ClassWebNetwork
from string import Template

'''
Please debug : (04/10/2024)
----------------------------------------
Exception occurred during processing of request from ('127.0.0.1', 41446)
Traceback (most recent call last):
  File "/usr/lib/python3.10/socketserver.py", line 683, in process_request_thread
    self.finish_request(request, client_address)
  File "/usr/lib/python3.10/socketserver.py", line 360, in finish_request
    self.RequestHandlerClass(request, client_address, self)
  File "~/Dev/GitHub/I-like-Chopin/src/web_server.py", line 39, in __init__
    super().__init__(*args, **kwargs)
  File "/usr/lib/python3.10/socketserver.py", line 747, in __init__
    self.handle()
  File "/usr/lib/python3.10/http/server.py", line 433, in handle
    self.handle_one_request()
  File "/usr/lib/python3.10/http/server.py", line 421, in handle_one_request
    method()
  File "~/Dev/GitHub/I-like-Chopin/src/web_server.py", line 222, in do_GET
    self.wfile.write(file.read()) # Read the file and send the contents
  File "/usr/lib/python3.10/socketserver.py", line 826, in write
    self._sock.sendall(b)
BrokenPipeError: [Errno 32] Relais brisé (pipe)
----------------------------------------
'''

class RequestHandler(BaseHTTPRequestHandler):
    uuid = None
    midisong = None
    # get from init
    pParent = None
    midisong = None
    midifiles_dict = {}

    def __init__(self, parent, midifiles_dict, *args, **kwargs):
        self.uuid = uuid.uuid4()
        self.pParent = parent
        self.midisong = parent.Midi.GetMidiSong()
        self.midifiles_dict = midifiles_dict
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self):
        pass
        '''
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()
        '''

    def do_POST(self, *args, **kwargs):
        print("--> do_POST")

    def do_GET(self):

        # json files
        if self.path == "/status.json":

            if self.midisong:
                data = json.dumps(
                    {
                        "uuid":str(self.midisong.Getuuid()),
                        "played":self.midisong.GetPlayed(),
                        "duration":round(self.midisong.GetDuration(), 2),
                        "nameclean":self.midisong.GetCleanName(),
                        "folder":self.midisong.GetParent(),
                        "state":self.midisong.GetState(),
                        "mode":self.midisong.GetMode(),
                        "tracks":self.midisong.GetTracks(),
                        "channels":self.midisong.GetChannels(),
                        "sustain":self.midisong.GetSustain(),
                    }
                )
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header("Content-Type", "application/json")
                # print('Content-Length: %d' % len(response))
                self.end_headers()
                self.wfile.write(data.encode(encoding="utf_8"))

                if not self.wfile.closed:
                    self.wfile.flush()

            return

        elif self.path == "/files.json":
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            file_dic = self.pParent.Midifiles.GetFiles()
            data = json.dumps(file_dic)
            self.wfile.write(data.encode(encoding="utf_8"))

            ''' NOTICE :
            file_dic is a dicrionnary as key:[list of complete filepath]
            {'ABBA': ['C:\...','C:\...'], 'BACH JOHANN SEBASTIAN': [C:\...,C:\...] }
            '''

            if not self.wfile.closed:
                self.wfile.flush()
            return

        elif self.path == "/interfaces.json":
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            Network = ClassWebNetwork(self.pParent)
            url_list = Network.GetWebUrls()
            data = json.dumps(url_list)
            self.wfile.write(data.encode(encoding="utf_8"))

            if not self.wfile.closed:
                self.wfile.flush()
            return


        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)

        # with parameters (?)

        if "play" in query_components:
            midifile = query_components["play"][0]
            print(f"WebServer {self.uuid} request [{midifile}]")
            if self.pParent:
                try:
                    self.pParent.MidifileChange(midifile)  # DANGEROUS ?
                except:
                    pass
            self.send_response(200)
            self.end_headers()
            return

        elif "do" in query_components:

            print(f"--> do_GET [{self.path}]")

            action = query_components["do"][0]
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

            self.send_response(200)
            self.end_headers()

            return

        elif "mode" in query_components:
            mode = query_components["mode"][0]
            try:
                self.pParent.ChangePlayerMode(mode)  # DANGEROUS ?
            except:
                pass
            self.send_response(200)
            self.end_headers()
            return

        # Other files from web interface

        uipath = self.pParent.Settings.GetUIPath()

        # index.html
        if self.path == "/" or self.path == "/index.html":
            index = os.path.join(uipath,'index.html')
            index_stats = os.stat(index)

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(index_stats.st_size))
            self.end_headers()

            with open(index, 'rb') as file:
                self.wfile.write(file.read()) # Read the file and send the contents

        else:
            path = self.path
            if len(path): # remove first "/" in self.path
                path = path[1:]

            file = os.path.join(uipath,path)
            if os.path.isfile(file):

                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')

                if(self.path.find(".js") != -1):
                    self.send_header("Content-type", "text/javascript")
                elif(self.path.find(".html") != -1):
                    self.send_header("Content-type", "text/html")
                elif(self.path.find(".css") != -1):
                    self.send_header("Content-type", "text/css")
                elif(self.path.find(".png") != -1):
                    self.send_header("Content-type", "image/png")
                elif(self.path.find(".gif") != -1):
                    self.send_header("Content-type", "image/gif")
                else:
                    print(f"missing content-type for [{self.path}]")

                file_stats = os.stat(file)
                self.send_header("Content-Length", str(file_stats.st_size))
                self.end_headers()

                with open(file, 'rb') as file: # BUG with os.path.join ??
                    self.wfile.write(file.read()) # Read the file and send the contents

            else: # 404
                print(f"|!| WARNING : web file [{file}] DO NOT EXISTS")
                self.send_response(404)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                return

        if not self.wfile.closed:
            self.wfile.flush()

    def log_message(self, format, *args):  # no message in terminal
        pass


class ClassWebServer(QThread):
    uuid = None
    pParent = None
    Settings = None

    server = None
    port = 8888

    midifiles_dict = {}
    serverURLs = []
    qrcodes_list = []

    def __init__(self, parent):
        QThread.__init__(self)
        self.uuid = uuid.uuid4()
        self.pParent = parent
        self.Settings = parent.Settings
        self.port = self.Settings.GetServerPort()
        Network = ClassWebNetwork(self.pParent)
        serverURLs_list = Network.GetWebUrls()
        for serverURL in serverURLs_list:
            print(
                f"WebServer {self.uuid} serve [{self.pParent.Settings.GetMidiPath()}] on {serverURL}"
            )
    def __del__(self):
        if self.server:
            self.server.server_close()
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        try:
            handler = partial(
                RequestHandler, self.pParent, self.midifiles_dict
            )
            self.server = ThreadingHTTPServer(("0.0.0.0", self.port), handler)
            self.server.allow_reuse_address = True
            self.server.serve_forever()
        except Exception as error:
            print(
                f"|!| WebServer {self.uuid} CAN NOT SERVE ON PORT {self.port} {error}"
            )
            self.pParent.Midi.SendStatusBar(f"WEB SERVER PORT {self.port} BUSY !")

    def stop(self):
        if self.server:
            self.server.server_close()
            self.server.shutdown()
