import os
import sinope.messageHandler
import sinope.message
import sinope.str
import sinope.logger


class sessionManager(sinope.messageHandler.messageHandler):
    def __init__(self):
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
            self.__apiKey = message.getApiKey()
            f = open(self.__filePath, 'wb')
            f.write(self.__apiKey)
            f.close()

    def isAuthenticated(self):
        return self.__apiKey != None
