import os
import threading
import sinope.messageHandler
import sinope.message
import sinope.str
import sinope.logger


class sessionManager(sinope.messageHandler.messageHandler):
    def __init__(self, server):
        self.__server = server
        self.__server.addMessageHandler(self, sinope.message.messageAuthenticationKeyAnswer.command)
        self.__authenticateEvent = threading.Event()

        self.__filePath = "api.key"
        self.__apiKey = None
        if os.path.exists(self.__filePath):
            f = open(self.__filePath, 'rb')
            self.__apiKey = f.read()       
            f.close()
            if len(self.__apiKey) != 8:
                sinope.logger.logger.warning("api.key format failed")
                os.unlink(self.__filePath)
                self.__apiKey = None


    def handleMessage(self, message):
        if isinstance(message, sinope.message.messageAuthenticationKeyAnswer):
            if message.getStatus() < 0:
                raise Exception("Authentication key faied")
                #TODO set backoff value to session manager

            elif message.getStatus() == 2:
                sinope.logger.logger.info("Authentication key deleted")
                if os.path.exists(self.__filePath):
                    os.unlink(self.__filePath)

            elif message.getStatus() == 1:
                self.__apiKey = message.getApiKey()
                f = open(self.__filePath, 'wb')
                f.write(self.__apiKey)
                f.close()
                self.__authenticateEvent.set()

            else:
                sinope.logger.logger.info("Unknown authentication status %d" % message.getStatus())

    def isAuthenticated(self):
        return self.__apiKey != None

    def authenticate(self, hardwareId):
        if not self.isAuthenticated():
            self.__authenticateEvent.clear()
            message = sinope.message.messageAuthenticationKey()
            message.setKey(hardwareId)
            self.__server.sendMessage(message)
            self.__authenticateEvent.wait()
        

    def login(self):
        if not self.isAuthenticated():
            raise Exception("Not authenticated")
