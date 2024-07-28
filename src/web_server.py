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
from urllib.parse import urlparse
from urllib.parse import parse_qs
from web_interfaces import get_interfaces
from midi_song import states
from string import Template

server_parent = None
server_midifiles = []
server_interfaces = []

class ClassWebConfig:
    pass

class Handler(BaseHTTPRequestHandler):
    uuid = uuid.uuid4()
    global server_parent
    midisong = None

    def do_GET(self):
        # print(f"MyHttpRequestHandler {self.uuid} do_GET")
        self.midisong = server_parent.midisong

        # Extract query param
        name = 'MIDIFILES'
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
                    "state":self.midisong.GetState()
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
        fileslist = ""
        for midifile in server_midifiles:
            path = pathlib.PurePath(midifile)
            midiname = pathlib.Path(midifile).stem
            midiname = midiname.replace('_',' ')
            midiname = midiname.replace('-',' ')
            fileslist += f"<div class='folder'>{path.parent.name}</div> <div class='song'><a href='?play={midifile}'> &nbsp; {midiname} &nbsp; </a></div>\n"

        index = template.substitute(name=server_parent.midisong.GetCleanName(),duration="",midifiles=fileslist)
        self.wfile.write(bytes(index, "utf8"))
        return


    def log_message(self, format, *args):
            pass


class ClassWebServer(Thread):
    uuid = uuid.uuid4()
    port = 8888
    server = None

    def __init__(self,parent):
        global server_midifiles
        global server_parent
        global server_interfaces

        Thread.__init__( self )
        server_parent = parent
        print(f"WebServer {self.uuid} created")

        for file in sorted(glob.glob(os.path.join(parent.settings.GetMidiPath(),"**", "*.mid"), recursive = True)):
            # print(f"WebServer {self.uuid} MIDI FOUND [{file}]")
            server_midifiles.append(file)

        interfaces = get_interfaces(True, False)
        for interface in interfaces :
            url = f"http://{interface['ip']}:{self.port}"
            server_interfaces.append(url)
            print(f"WebServer {self.uuid} {url} serve [{server_parent.settings.GetMidiPath()}]")

        #print(f"WebServer {self.uuid} ready")

    def __del__(self):
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        #print(f"WebServer {self.uuid} run")
        try:
            self.server = ThreadingHTTPServer(('0.0.0.0', self.port), Handler)
            self.server.allow_reuse_address = True
            self.server.serve_forever()
        except:
            print(f"/!\ WebServer {self.uuid} CAN NOT SERVE ON PORT {self.port}")

    def GetPort(self):
        return self.port

    def GetInterfaces(self):
        return server_interfaces

    def stop(self):
        if self.server:
            self.server.server_close()
            self.server.shutdown()
            self.server = None
