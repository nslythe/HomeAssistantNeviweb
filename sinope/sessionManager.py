import os
import threading
import sinope.messageHandler
import sinope.message
import sinope.str
import sinope.logger


class sessionManager(sinope.messageHandler.messageHandler):
    def __init__(self, server, dataManager):
        self.__server = server
        self.__dataManager = dataManager
        self.__server.addMessageHandler(self, sinope.message.messageAuthenticationKeyAnswer.command)
        self.__server.addMessageHandler(self, sinope.message.messageLoginAnswer.command)
        self.__authenticateEvent = threading.Event()
        self.__loginEvent = threading.Event()

        self.__dataManager.newValue(self, "api_key")
        self.__dataManager.newValue(self, "hardware_id")
        print (self.__dataManager.getData())


    def handleMessage(self, message):
        if isinstance(message, sinope.message.messageAuthenticationKeyAnswer):
            if message.getStatus() < 0:
                raise Exception("Authentication key faied")
                #TODO set backoff value to session manager

            elif message.getStatus() == 2:
                sinope.logger.logger.info("Authentication key deleted")
                self.__dataManager.setValue(self, "api_key", None)

            elif message.getStatus() == 1:
                apiKey = message.getApiKey()
                self.__dataManager.setValue(self, "api_key", apiKey)
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
        return self.__dataManager.getValue(self, "api_key") != None

    def authenticate(self, hardwareId = None):
        if hardwareId != None:
            self.__dataManager.setValue(self, "hardware_id", hardwareId)
        if not self.isAuthenticated():
            self.__authenticateEvent.clear()
            message = sinope.message.messageAuthenticationKey()
            message.setId(self.__dataManager.getValue(self, "hardware_id"))
            self.__server.sendMessage(message)
            self.__authenticateEvent.wait()
            sinope.logger.logger.info("Sinope session authenticated")        

    def login(self):
        if not self.isAuthenticated():
            raise Exception("Not authenticated")
        message = sinope.message.messageLogin()
        message.setId(self.__dataManager.getValue(self, "hardware_id"))
        message.setApiKey(self.__dataManager.getValue(self, "api_key"))
        self.__server.sendMessage(message)
        self.__loginEvent.wait()
        sinope.logger.logger.info("Sinope session loggedin")
      
        
