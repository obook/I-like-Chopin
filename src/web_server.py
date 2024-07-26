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
from threading import Thread
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs
from web_interfaces import get_interfaces

server_parent = None
server_midifiles = []
server_interfaces = []

class ClassWebConfig:
    pass

class Handler(BaseHTTPRequestHandler):
    uuid = uuid.uuid4()

    def do_GET(self):
        # print(f"MyHttpRequestHandler {self.uuid} do_GET")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Extract query param
        name = 'MIDIFILES'
        query_components = parse_qs(urlparse(self.path).query)
        if 'name' in query_components:
            name = query_components["name"][0]
            print(f"WebServer {self.uuid} request [{name}]")
            if server_parent:
                try:
                    server_parent.MidifileChange(name)
                except:
                    pass

        html = '''
        <!DOCTYPE html>
        <html><head>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <style>

        body {
            background-color:#000000;
            overflow-wrap: break-word;
        }

        .title{
            font-size: calc(.5em + 3vw);
            color:#339933;
            background-color:#333333;
            text-transform: uppercase;
        }

        .folder{
            color:#fdf6f6;
            font-size: calc(.5em + 2vw);
            background-color:#333333;
            text-transform: uppercase;
        }

        .song{
            color:#fdf6f6;
            font-size: calc(.5em + 2vw);
            background-color:#333333;
            text-transform: uppercase;
            text-decoration: none;
        }

        .song a{
            font-size: calc(.5em + 2vw);
            color:#333333;
            background-color:#fdf6f6;
            text-transform: uppercase;
            text-decoration: none;
        }

        .container {
            display: flex;
            flex-wrap: nowrap;
            /* OU wrap;
            OU wrap-reverse; */
        }

        </style>
        </head>
        <body>
        '''

        name = os.path.basename(name)
        name = name.replace('_',' ')
        name = name.replace('-',' ')

        html += f"<h1><span class='title'>{pathlib.Path(name).stem}</span></h1>"

        html +="<div class='.container'>"
        for midifile in server_midifiles:
            path = pathlib.PurePath(midifile)
            html += f"<div class='folder'>{path.parent.name}</div> <div class='song'><a href='?name={midifile}'>&nbsp;{pathlib.Path(midifile).stem}&nbsp; </a></div>"
        html += "</div>"

        html += "</body></html>"
        self.wfile.write(bytes(html, "utf8"))
        return

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

    def __del__(self):
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        try:
            self.server = ThreadingHTTPServer(('0.0.0.0', self.port), Handler)
            self.server.allow_reuse_address = True
            self.server.serve_forever()
        except:
            print(f"/!\ WebServer {self.uuid} CAN NOT SERVE ON PORT {self.port}")

    def GetInterfaces(self):
        return server_interfaces

    def stop(self):
        if self.server:
            self.server.server_close()
            self.server.shutdown()
            self.server = None
