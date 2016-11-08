import logging
import select
import signal
import sys
import socket
import threading
import time
import sinope.message

class serverWatchdog(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.__server = server
        self.__stop = False
        self.__delay = 10

    def stop(self):
        self.__stop = True
        self.__server.logger.debug("Watchdog thread stopping")

    def run(self):
        while not self.__stop:
            message = sinope.message.messagePing()
            self.__server.sendMessage(message)
            self.__server.logger.debug("Send : %s", message)
            for x in range(0, 10 * self.__delay):
                if self.__stop:
                    break
                time.sleep(0.1)
        self.__server.logger.debug("Watchdog thread stopped")

class serverListener(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.__server = server
        self.__stop = False

    def stop(self):
        self.__stop = True
        self.__server.logger.debug("Listener thread stopping")

    def run(self):
        while not self.__stop:
            data = self.__server.receive(
                sinope.message.HEADER_SIZE +
                sinope.message.SIZE_SIZE +
                sinope.message.COMMAND_SIZE)
            if data != None:
                message = sinope.message.create(data)
                if message != None:
                    data = self.__server.receive(
                        message.getSize() +
                        sinope.message.CRC_SIZE -
                        sinope.message.COMMAND_SIZE)
                    if data != None:
                        pass
                self.__server.logger.debug("Received : %s", message)
        self.__server.logger.debug("Listener thread stopped")

class server:
    def __init__(self, address, port):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = address
        self.__port = port
        self.__serverListener = serverListener(self)
        self.__serverWatchdog = serverWatchdog(self)
        self.logger = logging.getLogger("sinope.server")

    def connect(self):
        self.__socket.connect((self.__address, self.__port))
        self.logger.debug("Connected %s", self.__socket.getpeername())
        self.__serverListener.start()
        self.__serverWatchdog.start()
        signal.signal(signal.SIGTERM, self.__terminate)
        signal.signal(signal.SIGINT, self.__terminate)

    def __terminate(self, _signo, _stack_frame):
        self.close()

    def close(self):
        self.logger.debug("Stopping")
        self.__serverListener.stop()
        self.__serverWatchdog.stop()
        self.__socket.close()

    def wait(self):
        self.__serverListener.join()
        self.__serverWatchdog.join()

    def sendMessage(self, message):
        buff = None
        if isinstance(message, sinope.message.message):
            buff = message.getPayload()
        else:
            buff = messagei

        while self.__socket.fileno() >= 0:
            (rios, wios, xios) = select.select([], [self.__socket], [], 0.1)
            if len(wios) > 0:
                self.__socket.send(buff)
                break

    def receive(self, size):
        while self.__socket.fileno() >= 0:
            (rios, wios, xios) = select.select([self.__socket], [], [], 0.1)
            if len(rios) > 0:
                data = self.__socket.recv(size)
                return data
