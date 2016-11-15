import unittest
import socket
import threading
import sinope.server

class mockServer(threading.Thread):
    def __init__(self):
        super(mockServer, self).__init__()
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.socket.bind(("127.0.0.1", 4550))
        self.socket.listen(10)
        self.__stop = False

    def stop(self):
        self.__server.logger.debug("Watchdog stopping")

    def run(self):
        conn, addr = self.socket.accept()


class test_server(unittest.TestCase):
    def test_connect(self):
        mockserver = mockServer()
        mockserver.start()
        server = sinope.server.server("127.0.0.1", 4550)
        server.connect()
        server.close()
        server.wait()       
