import sinope.message

class applicationObjectManager(object):
    def __init__(self, server):
        self.server = server
        self.server.addMessageHandler(self, sinope.message.messageDataAnswerRead.command)
        self.server.addMessageHandler(self, sinope.message.messageDataAnswerReport.command)
        self.server.addMessageHandler(self, sinope.message.messageDataAnswerWrite.command)

    def handleMessage(self, message):
        if message.getStatus() == 10:
            appData = message.getApplicationData()

    def report(self, appData, device):
        message = sinope.message.messageDataRequestRead()
        message.setDeviceId(device.deviceId)
        message.setApplicationData(appData)
        self.server.sendMessage(message)

