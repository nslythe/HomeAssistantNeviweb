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
        self.__server.addMessageHandler(self, sinope.message.messageLoginAnswer.command)
        self.__authenticateEvent = threading.Event()
        self.__loginEvent = threading.Event()

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

        # Login message handler
        if isinstance(message, sinope.message.messageLoginAnswer):
            if message.getStatus() < 0:
                #TODO set backof
                if message.getStatus() == -1:
                    raise Exception("Authentication failed")

                elif message.getStatus() == -2:
                    raise Exception("Reserved status")

                elif message.getStatus() == -3:
                    raise Exception("Reserved status")

                elif message.getStatus() == -4:
                    raise Exception("Client blacklisted / banned")

                else:
                    raise Exception("Unknown login status %d" % message.getStatus())

            elif message.getStatus() == 0:
                sinope.logger.logger.info("Logged to Server %s version %d.%d.%d" %
                    (sinope.str.bytesToString(message.getDeviceId()),
                    message.getVersionMajor(), message.getVersionMinor(), message.getVersionBug()))
                self.__loginEvent.set()

            else:
                raise Exception("Unknown login status %d" % message.getStatus())

    def isAuthenticated(self):
        return self.__apiKey != None

    def authenticate(self, hardwareId):
        self.__hardwareId = hardwareId
        if not self.isAuthenticated():
            self.__authenticateEvent.clear()
            message = sinope.message.messageAuthenticationKey()
            message.setId(self.__hardwareId)
            self.__server.sendMessage(message)
            self.__authenticateEvent.wait()
            sinope.logger.logger.info("Sinope session authenticated")        

    def login(self):
        if not self.isAuthenticated():
            raise Exception("Not authenticated")
        message = sinope.message.messageLogin()
        message.setId(self.__hardwareId)
        message.setApiKey(self.__apiKey)
        self.__server.sendMessage(message)
        self.__loginEvent.wait()
        sinope.logger.logger.info("Sinope session loggedin")
      
        
