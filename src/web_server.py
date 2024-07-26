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

server_midifiles = []
server_parent = None

class ClassWebConfig:
    pass

class Handler(BaseHTTPRequestHandler):
    uuid = uuid.uuid4()

    def do_GET(self):
        print(f"MyHttpRequestHandler {self.uuid} do_GET")
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

        html += f"<h1><span class='title'>{os.path.basename(name)}</span></h1>"

        html +="<div class='.container'>"
        for midifile in server_midifiles:
            path = pathlib.PurePath(midifile)
            html += f"<div class='folder'>{path.parent.name}</div> <div class='song'><a href='?name={midifile}'>{os.path.basename(midifile)}</a></div>"
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
        Thread.__init__( self )
        server_parent = parent
        print(f"WebServer {self.uuid} created")

        for file in sorted(glob.glob(os.path.join(parent.settings.GetMidiPath(),"**", "*.mid"), recursive = True)):
            # print(f"WebServer {self.uuid} MIDI FOUND [{file}]")
            server_midifiles.append(file)

    def __del__(self):
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        interfaces = get_interfaces(True, False)
        for interface in interfaces :
            print(f"WebServer {self.uuid} serve http://{interface['ip']}:{self.port} [{server_parent.settings.GetMidiPath()}]")
        try:
            self.server = ThreadingHTTPServer(('0.0.0.0', self.port), Handler)
            self.server.allow_reuse_address = True
            self.server.serve_forever()
        except:
            print(f"/!\ WebServer {self.uuid} CAN NOT SERVE ON PORT {self.port}")

    def stop(self):
        print(f"WebServer {self.uuid} stop")
        if self.server:
            self.server.server_close()
            self.server.shutdown()
            self.server = None

"""
import os
import uuid
from threading import Thread
import http.server
import glob
import pathlib

from urllib.parse import urlparse
from urllib.parse import parse_qs
import socketserver
from web_interfaces import get_interfaces

server_path = '.'
pParent = None
allmidifiles = []

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    uuid = uuid.uuid4()

    def do_GET(self):
        global server_path
        global allmidifiles
        print(f"MyHttpRequestHandler {self.uuid} do_GET")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Extract query param
        name = 'MIDIFILES'
        query_components = parse_qs(urlparse(self.path).query)
        if 'name' in query_components:
            name = query_components["name"][0]
            filepath = os.path.join(server_path,name)
            print(f"WebServer {self.uuid} request [{filepath}]")
            pParent.MidifileChange(filepath)

        html = '''
        <!DOCTYPE html>
        <html><head>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <style>

        body {
            background-color:#000000;
        }

        .title{
            font-size: calc(.5em + 3vw);
            color:#339933;
            background-color:#333333;
            text-transform: uppercase;
        }

        .song{
            color:#fdf6f6;
            font-size: calc(.5em + 1vw);
            background-color:#333333;
            text-transform: uppercase;
            text-decoration: none;
        }

        .song a{
            font-size: calc(.5em + 1vw);
            color:#333333;
            background-color:#fdf6f6;
            text-transform: uppercase;
            text-decoration: none;
            align-content: right;
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

        html += f"<h1><span class='title'>{os.path.basename(name)}</span></h1>"

        html +="<div class='.container'>"
        for midifile in allmidifiles:
            path = pathlib.PurePath(midifile)
            html += f"<div class='song'>{path.parent.name} - <a href='?name={midifile}'>{os.path.basename(midifile)}</a></div>"
        html += "</div>"

        html += "</body></html>"
        self.wfile.write(bytes(html, "utf8"))
        return

class ClassThreadWebServer(Thread):
    uuid = None
    midipath = None
    my_server = None
    port = 8888
    myhandler = None

    def __init__(self,Parent):
        global server_path
        global pParent
        global allmidifiles
        Thread.__init__( self )
        pParent = Parent
        self.midipath = pParent.settings.GetMidiPath()
        server_path = pParent.settings.GetMidiPath()
        self.uuid = uuid.uuid4()
        self.myhandler = MyHttpRequestHandler

        for file in sorted(glob.glob(os.path.join(server_path,"**", "*.mid"), recursive = True)):
            # print(f"WebServer {self.uuid} MIDI FOUND IN {path.parent.name} =[{file}]")
            allmidifiles.append(file)

    def __del__(self):
        if self.my_server:
            self.my_server.server_close()
            self.my_server.shutdown()
            self.my_server = None
        print(f"WebServer {self.uuid} destroyed")

    def run(self):
        try:
            self.my_server = socketserver.TCPServer(("", self.port), self.myhandler)
            self.my_server.allow_reuse_address = True
            interfaces = get_interfaces(True, False)
            for interface in interfaces :
                print(f"WebServer {self.uuid} serve http://{interface['ip']}:{self.port} [{server_path}]")
            self.my_server.serve_forever()
        except:
            print(f"/!\ WebServer {self.uuid} CAN NOT SERVE ON THIS PORT {self.port}")

    def quit(self):
        if self.my_server:
            self.my_server.server_close()
            self.my_server.shutdown()
            self.my_server = None
"""
