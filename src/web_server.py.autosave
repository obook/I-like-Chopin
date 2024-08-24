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


class RequestHandler(BaseHTTPRequestHandler):
    uuid = None
    midisong = None
    # get from init
    pParent = None
    midifiles_dict = {}

    def __init__(self, parent, midifiles_dict, *args, **kwargs):
        self.uuid = uuid.uuid4()
        self.pParent = parent
        self.midisong = parent.Midi.GetMidiSong()
        self.midifiles_dict = midifiles_dict
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    def do_POST(self, *args, **kwargs):
        print("--> do_POST")

    def do_GET(self):
        print(f"--> do_GET [{self.path}]")

        # Extract query param

        # json files

        if self.path == "/status.json":
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            if self.midisong:
                data = json.dumps(
                    {
                        "played": self.midisong.GetPlayed(),
                        "duration": round(self.midisong.GetDuration(), 2),
                        "nameclean": self.midisong.GetCleanName(),
                        "folder": self.midisong.GetParent(),
                        "state": self.midisong.GetState(),
                        "mode": self.midisong.GetMode(),
                        "tracks": self.midisong.GetTracks(),
                        "channels": self.midisong.GetChannels(),
                        "sustain":self.midisong.GetSustain(),
                    }
                )

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
            return

        elif "do" in query_components:
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

            self.send_response(302)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Location", "/")
            try:
                self.end_headers()
            except:
                pass
            return

        elif "mode" in query_components:
            mode = query_components["mode"][0]
            try:
                self.pParent.ChangePlayerMode(mode)  # DANGEROUS ?
            except:
                pass
            self.send_response(302)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Location", "/")
            try:
                self.end_headers()
            except:
                pass
            return

        # Other files


        uipath = self.pParent.Settings.GetUIPath()

        if self.path == "/" or self.path == "/index.html":

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            try:
                self.end_headers()
            except:
                pass

            with open(os.path.join(uipath,'index.html'), 'rb') as file:
                self.wfile.write(file.read()) # Read the file and send the contents
        else:
            file = uipath+self.path
            if os.path.isfile(file):

                print(f"SENDING = [{file}]")

                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                try:
                    self.end_headers()
                except:
                    pass

                with open(file, 'rb') as file: # BUG with os.path.join ??
                    self.wfile.write(file.read()) # Read the file and send the contents
            else: # 404
                self.send_response(404)
                self.send_header('Access-Control-Allow-Origin', '*')
                try:
                    self.end_headers()
                except:
                    pass
                print(f"WARNING : file [{file}] DO NOT EXISTS")

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
