import sinope.message
import sinope.device
import sinope.str
import sinope.logger

class deviceManager(object):
    def __init__(self, server, dataManager):
        self.__server = server
        self.__server.addMessageHandler(self, sinope.message.messageLoginAnswer.command)
        self.__server.addMessageHandler(self, sinope.message.messageDeviceLinkReport.command)
        self.serverDevice = None
        self.devices = []

    def handleMessage(self, message):
        if isinstance(message, sinope.message.messageLoginAnswer):
            if message.getStatus() == 0:
                self.serverDevice = self.addDevice(message.getDeviceId())

        if isinstance(message, sinope.message.messageDeviceLinkReport):
            if message.getStatus() == 0 or message.getStatus() == 1:
                self.addDevice(message.getDeviceId())
            if message.getStatus() == - 1:
                self.removeDevice(message.getDeviceId())

    def addDevice(self, deviceId):
        device = sinope.device.device(deviceId)
        self.devices.append(device)
        sinope.logger.logger.info("New device added %s" % sinope.str.bytesToString(deviceId))
        return device

    def removeDevice(self, deviceId):
        for device in self.devices:
            if device.deviceId == deviceId:
                self.devices.remove(device)
                sinope.logger.logger.info("Device removed %s" % sinope.str.bytesToString(deviceId))
                break
