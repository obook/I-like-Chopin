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

    def web_start(self):
        # Web server
        self.Web_server = ClassWebServer(self)
        self.Web_server.start()

    def OpenBrowser(self):
        webbrowser.open(f"http://127.0.0.1:{self.Settings.GetServerPort()}")
