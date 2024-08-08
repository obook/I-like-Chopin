# This Python file uses the following encoding: utf-8

import webbrowser


class browser:
    Web_server = None

    def OpenBrowser(self):
        webbrowser.open(f"http://127.0.0.1:{self.Web_server.GetPort()}")
