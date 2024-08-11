#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:19:14 2024
@author: obooklage
"""
import webbrowser
from web_server import ClassWebServer


class web:
    Web_server = None
    server_urls = None
    server_qrcode = None

    def web_start(self):
        # Web server
        self.Web_server = ClassWebServer(self)
        self.server_urls = self.Web_server.GetServerURLs()
        self.server_qrcode = self.Web_server.GetQRCodeSVG()
        self.Web_server.start()

    def OpenBrowser(self):
        webbrowser.open(f"http://127.0.0.1:{self.Web_server.GetPort()}")
