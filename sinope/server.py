import sys
import socket
import threading
import time
import sinope.message

class serverThread(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.__server = server

    def run(self):
        while True:
            data = self.__server.socket.recv(6)
            message = sinope.message.create(data)
            print (message)
        

class server:
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = address
        self.__port = port
        self.__serverThread = serverThread(self)

    def connect(self):
        self.socket.connect((self.__address, self.__port))
        self.__serverThread.start()

    def close(self):
        self.socket.close()

    def sendMessage(self, message):
        buff = None
        if isinstance(message, sinope.message.message):
            buff = message.getPayload()
        else:
            buff = messagei
        self.socket.send(buff)


