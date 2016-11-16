import sinope.dataBuffer

class applicationData(sinope.dataBuffer.dataBuffer):
    def __init__(self, name):
        super(applicationData, self).__init__()
        self.__name = name
        self.__refreshingSize = False
        super(applicationData, self).setData(0, b"\x00\x00\x00\x00")
        super(applicationData, self).setData(4, 0, sinope.dataBuffer.DataType.ubyte)

    def setData(self, offset, data, dataType = None):
        super(applicationData, self).setData(offset + 5, data, dataType)

    def getData(self, offset, length):
        return super(applicationData, self).getData(offset + 5, length)

    def setDataId(self, dataId):
        super(applicationData, self).setData(0, dataId)

    def getDataId(self):
        return super(applicationData, self).getData(0, 4)

    def didRefresh(self):
        if not self.__refreshingSize:
            self.__refreshingSize = True
            if self.getSize() >= 5:
               super(applicationData, self).setData(4, self.getSize() - 5, sinope.dataBuffer.DataType.ubyte)
            self.__refreshingSize = False


class outdoorTemperature(applicationData):
    name = "OutdoorTemperature"
    dataId = b"\x00\x00\x02\x04"

    def __init__(self):
        super(outdoorTemperature, self).__init__(outdoorTemperature.name)
        self.setDataId(outdoorTemperature.dataId)
        self.setTemperature(0)

    def setTemperature(self, temp):
        self.setData(0, temp, sinope.dataBuffer.DataType.short)

    def getTemperature(self):
        return self.getData(0, sinope.dataBuffer.DataType.short)
