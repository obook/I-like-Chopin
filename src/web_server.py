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

        elif 'name' in query_components:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            name = query_components["name"][0]
            print(f"WebServer {self.uuid} request [{name}]")
            if server_parent:
                try:
                    server_parent.MidifileChange(name) # Crash
                    pass
                except:
                    pass

        html = f"""<!DOCTYPE html>
<html><head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>I Like Chopin</title>
<style>

:root {{
  --success: #00b894;
  --progress: #e17055;
}}

body {{
    font-size: calc(.5em + 2vw);
    color:#ffffff;
    background-color:#554455;
    overflow-wrap: break-word;
    text-transform: uppercase;
}}

.title{{
    font-size: calc(.5em + 3vw);
    color:#ffff00;
    background-color:#000000;
    border-radius: 10px;
    text-indent:10px;
}}

.container {{
    display: flex;
    flex-wrap: nowrap;
    flex-direction: column;
    font-size: calc(.5em + 2vw);
    background-color:#333333;
    border-radius: 10px;
    text-indent: 10px;
    /* OU wrap;
    OU wrap-reverse; */
}}

a {{
    font-size: calc(.5em + 2vw);
    background-color:#ffffff;
    color:#333333;
    text-decoration: none;
    border-radius: 5px;
}}

.inline,
.block {{
  line-height: 100px;
  font-size: 12px;
  letter-spacing: 20px;
  white-space: nowrap;
  margin: 10px 0;
  border-radius: 10px;
}}

.block progress {{
  display: block;
  width: 100%;
}}

</style>
</head>
<body>

<div class='title'>
    &nbsp;<span id='name'>{server_parent.midisong.GetCleanName()}</span>&nbsp;
    <div>Duration : <span ud='duration'>{round(server_parent.midisong.GetDuration(),2)}</span> minutes</div>
</div>

<div class="block"><progress id='bar' value='0' max='100'>0%</progress></div>

        """

        # Files
        html += "<div class='container'>\n"
        for midifile in server_midifiles:
            path = pathlib.PurePath(midifile)
            name = pathlib.Path(midifile).stem
            name = name.replace('_',' ')
            name = name.replace('-',' ')
            html += f"<div class='folder'>{path.parent.name}</div> <div class='song'><a href='?name={midifile}'> &nbsp; {name} &nbsp; </a></div>\n"
        html += "</div>\n"

        html += '''<script>
async function getStats() {
    const response = await fetch('/status.json');
    const data = await response.json();
    console.log(data)
    document.getElementById('bar').value=data.played
    document.getElementById('name').textContent=data.nameclean
    if (data.state <0)
        document.getElementById('name').style.color = '#ff0000';
    else if (data.state <2)
        document.getElementById('name').style.color = '#ffff00';
    else
        document.getElementById('name').style.color = '#00ff00';
}
setInterval(getStats, 2000);
</script>

</body></html>
    '''

        self.wfile.write(bytes(html, "utf8"))
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
