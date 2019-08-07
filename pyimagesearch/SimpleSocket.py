from typing import Any, Union
from SimpleWebSocketServer import SimpleExampleServer, WebSocket

import cv2
import math

clients = [], server = None

class RunSocket():
    def __init__(self):
        pass
    def RUN(self):
        class SimpleWSServer(WebSocket):
            def handleConnected(self):
                clients.append(self)

            def handleClose(self):
                clients.remove(self)

    def run_server():
        global server
        server = SimpleWebSocketServer( 9000, SimpleWSServer,
                                          selectInterval = (1000.0 / 15) / 1000)
        server.serveforever()

    t = threading.Thread(target=run_server)
    t.start()