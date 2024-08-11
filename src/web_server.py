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
from web_interfaces import get_interfaces
from string import Template


class RequestHandler(BaseHTTPRequestHandler):
    uuid = None
    midisong = None
    # get from init
    pParent = None
    midifiles_dict = {}
    qrcodes_list = []

    def __init__(self, parent, midifiles_dict, qrcodes_list, *args, **kwargs):
        self.uuid = uuid.uuid4()
        self.pParent = parent
        self.midisong = parent.Midi.GetMidiSong()
        self.midifiles_dict = midifiles_dict
        self.qrcodes_list = qrcodes_list
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # if midisong ?
        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)

        if self.path == "/status.json":
            self.send_response(200)
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
                    }
                )

                self.wfile.write(data.encode(encoding="utf_8"))

                if not self.wfile.closed:
                    self.wfile.flush()

            return

        if "play" in query_components:
            midifile = query_components["play"][0]
            print(f"WebServer {self.uuid} request [{midifile}]")
            if self.pParent:
                try:
                    self.pParent.MidifileChange(midifile)  # DANGEROUS ?
                except:
                    pass

        elif "do" in query_components:
            action = query_components["do"][0]
            if self.pParent and action == "stop":
                try:
                    self.pParent.Midi.StopPlayer()  # DANGEROUS ?
                except:
                    pass
            elif self.pParent and action == "shuffle": # ex "next"
                try:
                    self.pParent.ShuffleMidifile()  # DANGEROUS ?
                except:
                    pass
            elif self.pParent and action == "replay":
                try:
                    self.pParent.MidifileReplay()  # DANGEROUS ?
                except:
                    pass
            elif self.pParent and action == "mode":
                try:
                    self.pParent.ChangePlayerMode()  # DANGEROUS ?
                except:
                    pass
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            return

        # send index.html
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        try:
            self.end_headers()
        except:
            pass

        # Files
        midilist_html = ""
        for key in self.pParent.midifiles_dict.keys():  # self.midifiles_dict.keys():
            midilist_html += (
                f"<button class='accordion'>{key}</button><div class='panel'>"
            )
            list = self.pParent.midifiles_dict[key]
            for midifile in sorted(list, key=lambda s: s.lower()):
                midiname = pathlib.Path(midifile).stem
                midiname = midiname.replace("_", " ")
                midiname = midiname.replace("-", " ")
                midiname.upper()
                midilist_html += f"<p><a href='?play={quote(midifile)}'> &nbsp; {midiname} &nbsp; </a></p>\n"

            midilist_html += "</div>"

        # QRcodes
        images = ""
        for code in self.qrcodes_list:
            images += code.replace("<?xml version='1.0' encoding='UTF-8'?>", "")

        # Fill template
        file = open(self.pParent.Settings.GetIndexTemplate(), "r")  # DANGEROUS ?
        template = Template(file.read())
        file.close()

        index_html = template.substitute(
            name=self.midisong.GetCleanName(),
            folder=self.midisong.GetParent(),
            duration="",
            midifiles=midilist_html,
            qrcodes=images,
        )

        try:
            self.wfile.write(bytes(index_html, "utf8"))
        except:  # web browser disconnected
            pass
        return

        if not self.wfile.closed:
            self.wfile.flush()

    def log_message(self, format, *args):  # no message in terminal
        pass


class ClassWebServer(QThread):
    uuid = None
    server = None
    port = 8888

    pParent = None
    midifiles_dict = {}
    serverURLs = []
    qrcodes_list = []

    def __init__(self, parent):
        QThread.__init__(self)
        self.uuid = uuid.uuid4()
        self.pParent = parent
        self.port = self.pParent.Settings.GetServerPort()
        print(f"WebServer {self.uuid} created")
        interfaces_list = get_interfaces(True, False)
        for interface in interfaces_list:
            url = f"http://{interface['ip']}:{self.port}"
            self.serverURLs.append(url)

            print(
                f"WebServer {self.uuid} {url} serve [{self.pParent.Settings.GetMidiPath()}]"
            )
            '''
            if not "127.0.0.1" in url:
                img = qrcode.make(
                    url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10
                )
            '''
            img = qrcode.make(
                url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10
            )
            buffer = io.BytesIO()
            img.save(buffer)
            buffer.seek(0)
            buffer_img = buffer.getvalue().decode("utf-8")
            self.qrcodes_list.append(buffer_img)

    def __del__(self):
        if self.server:
            self.server.server_close()
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        try:
            handler = partial(
                RequestHandler, self.pParent, self.midifiles_dict, self.qrcodes_list
            )
            self.server = ThreadingHTTPServer(("0.0.0.0", self.port), handler)
            self.server.allow_reuse_address = True
            self.server.serve_forever()
        except:
            print(f"|!| WebServer {self.uuid} CAN NOT SERVE ON PORT {self.port}")
            self.pParent.Midi.SendStatusBar(f"WEB SERVER PORT {self.port} BUSY !")

    def GetPort(self):
        return self.port

    def GetServerURLs(self):
        return self.serverURLs

    def GetQRCodeSVG(self):
        return self.qrcodes_list

    def stop(self):
        if self.server:
            self.server.server_close()
            self.server.shutdown()
