# This Python file uses the following encoding: utf-8

import uuid
import qrcode
import qrcode.image.svg
import io

from web_interfaces import get_interfaces # ?


class ClassWebNetwork:
    __uuid = None
    pParent = None
    port = 8888
    serverURLs_list = []
    qrcodes_list = []
    def __init__(self,parent):
        self.__uuid = uuid.uuid4()
        self.pParent = parent
        self.Settings = parent.Settings
        interfaces_list = get_interfaces(True, False)
        self.serverURLs_list = []
        self.qrcodes_list = []
        for interface in interfaces_list:
            url = f"http://{interface['ip']}:{self.Settings.GetServerPort()}"
            self.serverURLs_list.append(url)
            '''
            #print(
            #    f"WebServer {self.__uuid} {url} serve [{self.pParent.Settings.GetMidiPath()}]"
            #)
            if not "127.0.0.1" in url:
                img = qrcode.make(
                    url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10
                )
                buffer = io.BytesIO()
                img.save(buffer)
                buffer.seek(0)
                buffer_img = buffer.getvalue().decode("utf-8")
                self.qrcodes_list.append(buffer_img)
            '''
        print(f"ClassWebNetwork {self.__uuid} created")

    def __del__(self):
        print(f"ClassWebNetwork {self.__uuid} destroyed")

    def GetWebUrls(self):
        return self.serverURLs_list
    '''
    def GetWebQRCodes(self):
        return self.qrcodes_list
    '''
