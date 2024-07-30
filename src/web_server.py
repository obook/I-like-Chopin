"""
Created on Fri Jul 26 07:12:28 2024
@author: obooklage
"""

"""Custom response code server by Cees Timmerman, 2023-07-11.
Run and visit http://localhost:4444/300 for example."""

import os
import uuid
import glob
import pathlib
import json
from threading import Thread
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
from web_interfaces import get_interfaces
from string import Template

server_parent = None
server_midifiles = []
server_interfaces = []
server_mididict = {}

class ClassWebConfig:
    pass

class Handler(BaseHTTPRequestHandler):
    uuid = uuid.uuid4()
    global server_parent
    midisong = None

    def do_GET(self):
        global server_midifiles_files # old
        global server_mididict

        # print(f"MyHttpRequestHandler {self.uuid} do_GET")
        self.midisong = server_parent.midisong

        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)

        if self.path == '/status.json':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            data=json.dumps(
                {
                    "played":self.midisong.GetPlayed(),
                    "duration":round(self.midisong.GetDuration(),2),
                    "nameclean":self.midisong.GetCleanName(),
                    "state":self.midisong.GetState(),
                    "mode":self.midisong.GetMode()
                }
            )

            self.wfile.write(data.encode(encoding='utf_8'))
            return

        elif 'play' in query_components:
            midifile = query_components["play"][0]
            print(f"WebServer {self.uuid} request [{midifile}]")
            if server_parent:
                try:
                    server_parent.MidifileChange(midifile)
                except:
                    pass

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        file = open(server_parent.settings.GetIndexTemplate(), "r")
        template = Template(file.read())
        file.close()

        # Files
        midilist_html = ""
        for key in server_mididict.keys():
            midilist_html += f"<button class='accordion'>{key}</button><div class='panel'>"
            list = server_mididict[key]
            for midifile in list:
                midiname = pathlib.Path(midifile).stem
                midiname = midiname.replace('_',' ')
                midiname = midiname.replace('-',' ')
                midiname.upper()
                midilist_html +=f"<p><a href='?play={quote(midifile)}'> &nbsp; {midiname} &nbsp; </a></p>"

            midilist_html +="</div>"

        index_html = template.substitute(name=server_parent.midisong.GetCleanName(),duration="",midifiles=midilist_html)
        try:
            self.wfile.write(bytes(index_html, "utf8"))
        except: # web browser disconnected
            pass
        return

    def log_message(self, format, *args): # no message in terminal
            pass

class ClassWebServer(Thread):
    uuid = uuid.uuid4()
    server = None
    port = 8888

    def __init__(self,parent):
        global server_midifiles
        global server_parent
        global server_interfaces

        global server_mididict

        Thread.__init__( self )
        server_parent = parent
        self.port = server_parent.settings.GetServerPort()
        print(f"WebServer {self.uuid} created")

        for file in sorted(glob.glob(os.path.join(parent.settings.GetMidiPath(),"**", "*.mid"), recursive = True)):
            path = pathlib.PurePath(file)
            server_midifiles.append(file) # ancienne méthode

            if not any(path.parent.name in keys for keys in server_mididict): # not in dictionnary
                server_mididict[path.parent.name] = [file]
            else: # in dictionnary
                list = server_mididict[path.parent.name]
                list.append(file)

        interfaces = get_interfaces(True, False)
        for interface in interfaces :
            url = f"http://{interface['ip']}:{self.port}"
            server_interfaces.append(url)
            print(f"WebServer {self.uuid} {url} serve [{server_parent.settings.GetMidiPath()}]")

    def __del__(self):
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        try:
            self.server = ThreadingHTTPServer(('0.0.0.0', self.port), Handler)
            self.server.allow_reuse_address = True
            self.server.serve_forever()
        except:
            print(f"|!| WebServer {self.uuid} CAN NOT SERVE ON PORT {self.port}")

    def GetPort(self):
        return self.port

    def GetInterfaces(self):
        return server_interfaces

    def stop(self):
        if self.server:
            self.server.server_close()
            self.server.shutdown()
            self.server = None
