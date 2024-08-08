# This Python file uses the following encoding: utf-8

import webbrowser
from web_server import ClassWebServer

class browser:
    Web_server = None

    def web_start(self):
        # Web server
        self.Web_server = ClassWebServer(self)
        self.server_interfaces = self.Web_server.GetInterfaces()
        self.Web_server.start()

    def OpenBrowser(self):
        webbrowser.open(f"http://127.0.0.1:{self.Web_server.GetPort()}")
