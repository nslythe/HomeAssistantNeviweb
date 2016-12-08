import sinope.message

class applicationObjectManager(object):
    def __init__(self, server):
        server.addMessageHandler(self, sinope.message.messageDataAnswerRead.command)
        server.addMessageHandler(self, sinope.message.messageDataAnswerReport.command)
        server.addMessageHandler(self, sinope.message.messageDataAnswerWrite.command)

    def handleMessage(self, message):
        if message.getStatus() == 10:
            appData = message.getApplicationData()
            print (type(appData))
            print(appData.getTemperature())
