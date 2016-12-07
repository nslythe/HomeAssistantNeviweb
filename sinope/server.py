import enum
import select
import signal
import sys
import socket
import threading
import time

import sinope.message
import sinope.messageCreator
import sinope.str
import sinope.logger

class serverWatchdog(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.__server = server
        self.__stop = False
        self.__pause = False

    def stop(self):
        self.__stop = True
        self.__server.logger.debug("Watchdog stopping")

    def pause(self, b):
        self.__pause = b

    def run(self):
        self.__server.logger.debug("Watchdog started")
        while not self.__stop:
            if not self.__pause:
                if self.__server.state != ServerState.connected:
                    self.__server.restart()

            time.sleep(0.1)
        self.__server.logger.debug("Watchdog stopped")

class serverPingner(threading.Thread, sinope.messageHandler):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.__server = server
        self.__stop = False
        self.__pingDelay = 20
        self.__lastPingTime = 0
        self.__lastReceivedPingTime = 0
        self.__lastWarningPing = 0

    def stop(self):
        self.__stop = True
        self.__server.logger.debug("Pigner stopping")

    def run(self):
        self.__server.logger.debug("Pigner started")
        self.__lastReceivedPingTime = time.time()
        while not self.__stop:
            if time.time() - self.__lastPingTime >= self.__pingDelay:
                message = sinope.message.messagePing()
                self.__server.sendMessage(message)
                self.__lastPingTime = time.time()

            if time.time() - self.__lastReceivedPingTime >= self.__pingDelay * 2:
                if time.time() - self.__lastWarningPing >= self.__pingDelay:
                    self.__server.logger.warning("Server did not respond for while")
                    self.__lastWarningPing = time.time()
            if time.time() - self.__lastReceivedPingTime >= self.__pingDelay * 4:
                self.__server.logger.error("Server did not respond for while")
                self.__server.state = ServerState.failed
                self.__stop = True

            time.sleep(0.1)
        self.__server.logger.debug("Pigner stopped")

    def handleMessage(self, message):
        self.__lastReceivedPingTime = time.time()

class serverListener(threading.Thread, sinope.messageHandler):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.__server = server
        self.__stop = False

    def stop(self):
        self.__stop = True
        self.__server.logger.debug("Listener stopping")

    def run(self):
        self.__server.logger.debug("Listener started")
        while not self.__stop:
            message = sinope.messageCreator.read(self.__server)

            if message == None:
                continue

            self.__server.logger.debug("Received message : %s", message)
            self.__server.handleMessage(message)

        self.__server.logger.debug("Listener stopped")

class ServerState(enum.Enum):
    initialized = 0
    connected = 1
    failed = 2
    closed = 3

class server:
    def __init__(self, address, port):
        self.__messageHandler = []
        self.__address = address
        self.__port = port
        self.state = ServerState.initialized
        self.__serverListener = serverListener(self)
        self.__serverPingner = serverPingner(self)
        self.__serveirWatchdog = serverWatchdog(self)
        self.addMessageHandler(self.__serverPingner, sinope.message.messagePingAnswer.command)
        self.logger = sinope.logger.logger

        signal.signal(signal.SIGTERM, self.__terminate)
        signal.signal(signal.SIGINT, self.__terminate)

    def addMessageHandler(self, handler, command):
        self.__messageHandler.append((handler, command))

    def handleMessage(self, message):
        for h in self.__messageHandler:
            if h[1] == message.getCommand():
                h[0].handleMessage(message)

    def connect(self):
        connected = False
        self.__closing = False
        while not connected and not self.__closing:
            try:
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__socket.connect((self.__address, self.__port))
                self.state = ServerState.connected
                self.logger.debug("Connected %s", self.__socket.getpeername())
                connected = True
                if not self.__serverListener.isAlive():
                    self.__serverListener.start()
                if not self.__serverPingner.isAlive():
                    self.__serverPingner.start()
                if not self.__serveirWatchdog.isAlive():
                    self.__serveirWatchdog.start()
            except OSError:
                self.logger.warning("Failed to connect retrying")
                pass


    def __terminate(self, _signo, _stack_frame):
        self.close()
        self.logger.debug("terminated")

    def close(self):
        self.logger.debug("Stopping")
        if not self.__closing:
            self.__closing = True
            if self.__serverListener.isAlive():
                self.__serverListener.stop()
            if self.__serverPingner.isAlive():
                self.__serverPingner.stop()
            if self.__serveirWatchdog.isAlive():
                self.__serveirWatchdog.stop()
            self.__socket.close()
            self.state = ServerState.closed
            self.logger.debug("Stopped")

    def restart(self):
        self.__serveirWatchdog.pause(True)
        self.logger.warning("Restarting server")
        if self.__serverListener.isAlive():
            self.__serverListener.stop()
        if self.__serverPingner.isAlive():
            self.__serverPingner.stop()
        self.__socket.close() 
        self.__serverListener.join()
        self.__serverPingner.join()
        self.__serverListener = serverListener(self)
        self.__serverPingner = serverPingner(self)
        self.addMessageHandler(self.__serverPingner, sinope.message.messagePingAnswer.command)
        self.connect()
        self.__serveirWatchdog.pause(False)

    def wait(self):
        self.logger.debug("Waiting for all server threads to finish")
        if self.__serverListener.isAlive():
            self.__serverListener.join()
        if self.__serverPingner.isAlive():
            self.__serverPingner.join()
        if self.__serveirWatchdog.isAlive():
            self.__serveirWatchdog.join()

    def sendMessage(self, message):
        """
        Send a message to the peer
        
        Arguments
        ---------
        message : sinope.message, bytes, bytearray
            The message to send, if the message is a sinope.message message.getPayload() will be sent
        """
        buff = None
        if isinstance(message, sinope.message.message):
            buff = message.getPayload()
        else:
            buff = message
        try:
            while self.__socket.fileno() >= 0:
                (rios, wios, xios) = select.select([], [self.__socket], [], 0.1)
                if len(wios) > 0:
                    self.__socket.send(buff)
                    self.logger.debug("Send : %s", message)
                    break
        except BrokenPipeError:
            self.state = ServerState.failed

    def read(self, size):
        """
        Read number of data in a binary string
        
        If an error ocured the string returned is empty
        """
        try:
            while self.__socket.fileno() >= 0:
                (rios, wios, xios) = select.select([self.__socket], [], [], 0.1)
                if len(rios) > 0:
                    data = self.__socket.recv(size)
                    if data == None:
                        return b""
                    return data
            return b""
        except ConnectionResetError:
            self.state = ServerState.failed
        except OSError:
            self.state = ServerState.failed
