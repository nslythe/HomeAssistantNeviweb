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
        self.setData(0, int(temp * 100), sinope.dataBuffer.DataType.short)

    def getTemperature(self):
        return self.getData(0, sinope.dataBuffer.DataType.short) / 100

class localTime(applicationData):
    name = "LocalTime"
    dataId = b"\x00\x00\x06\x00"

    def __init__(self):
        super(localTime, self).__init__(localTime.name)
        self.setDataId(localTime.dataId)
        self.setTime(0, 0, 0, False)

    def setTime(self, hour, minute, second, dayLightSaving):
        self.setData(0, second, sinope.dataBuffer.DataType.ubyte)
        self.setData(1, minute, sinope.dataBuffer.DataType.ubyte)
        adjustTime = hour
        if (dayLightSaving):
            adjustTime = adjustTime | 128
        self.setData(2, adjustTime, sinope.dataBuffer.DataType.ubyte)


class localDate(applicationData):
    name = "LocalDate"
    dataId = b"\x00\x00\x06\x01"

    def __init__(self):
        super(localDate, self).__init__(localDate.name)
        self.setDataId(localDate.dataId)
        self.setDate(0, 0, 0, 0)

    def setDate(self, year, month, day, dayOfWeek):
        self.setData(0, dayOfWeek, sinope.dataBuffer.DataType.ubyte)
        self.setData(1, day, sinope.dataBuffer.DataType.ubyte)
        self.setData(2, month, sinope.dataBuffer.DataType.ubyte)
        self.setData(3, year, sinope.dataBuffer.DataType.ubyte)


class ocupancySetback(applicationData):
    name = "OcupancySetback"
    dataId = b"\x00\x00\x07\x00"

    def __init__(self):
        super(ocupancySetback, self).__init__(ocupancySetback.name)
        self.setDataId(ocupancySetback.dataId)

class roomTemperature(applicationData):
    name = "RoomTemperature"
    dataId = b"\x00\x00\x02\x03"

    def __init__(self):
        super(roomTemperature, self).__init__(roomTemperature.name)
        self.setDataId(roomTemperature.dataId)

    def getTemperature(self):
        return self.getData(0, sinope.dataBuffer.DataType.short) / 100
