import sinope.messageHandler
import sinope.message


class sessionManager(sinope.messageHandler.messageHandler):
    def __init__(self):
        self.__filePath = "api.key"

    def handleMessage(self, message):
        f = open(self.__filePath, 'wb')
        f.write(message.getData())
        f.close()
