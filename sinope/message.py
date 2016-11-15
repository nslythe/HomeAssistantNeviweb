import enum
import inspect
import random
import struct
import sys
import sinope.crc
import sinope.str
import sinope.messageCreator
import sinope.dataBuffer

class message(sinope.dataBuffer.dataBuffer):
    def getSizeFromRawData(size):
        return struct.unpack("<H", size)[0]

    def __init__(self, name):
        super(message, self).__init__()
        if not isinstance(name, str):
            raise Exception("name argument not a string")
        self.__refreshingSize = False
        self.__name = name
        super(message, self).setData(0, b"\x55")
        super(message, self).setData(1, b"\x00")
        super(message, self).setData(2, 0, sinope.dataBuffer.DataType.ushort)

    def clone(self, other):
        super(message, self).clone(other)
        self.name = other.__name

    def getName(self):
        return self.__name

    def getCommandRaw(self):
        return bytearray(super(message, self).getDataRaw(4, 2))

    def getCommand(self):
        return bytearray(super(message, self).getData(4,2))

    def setCommandRaw(self, command):
        super(message, self).setDataRaw(4, command)

    def setCommand(self, command):
        super(message, self).setData(4, command)

    def setData(self, offset, data, dataType = None):
        super(message, self).setData(offset + 6, data, dataType)

    def getData(self, offset, length):
        return super(message, self).getData(offset + 6, length)

    def getPayload(self):
        payload = super(message, self).getDataRaw()
        payload += self.getCrc()
        return payload 

    def didRefresh(self):
        if not self.__refreshingSize:
            self.__refreshingSize = True
            if self.getSize() >= 4:
               super(message, self).setData(2, self.getSize() - 4, sinope.dataBuffer.DataType.ushort)
            self.__refreshingSize = False

    def __str__(self):
        s = self.__name
        s += " " 
        s += super(message, self).__str__()
        return s

class messagePing(message):
    command = b"\x00\x12"
    name = "Ping"
    
    def __init__(self):
        message.__init__(self, messagePing.name)
        self.setCommand(messagePing.command)

class messagePingAnswer(message):
    command = b"\x00\x13"
    name = "PingReply"
    
    def __init__(self):
        message.__init__(self, messagePingAnswer.name)
        self.setCommand(messagePingAnswer.command)
        
class messageAuthenticationKey(message):
    command = b"\x01\x0A"
    name = "AuthenticationKey"
    
    def __init__(self):
        super(messageAuthenticationKey, self).__init__(messageAuthenticationKey.name)
        self.setCommand(messageAuthenticationKey.command)

    def setId(self, id):
        if not isinstance(id, str):
            raise Exception("Id must be a str")
        if len(id) != 16:
            raise Exception("Id must be 8 length long")
        self.setData(0, bytearray.fromhex(id))

    def getId(self):
        return sinope.str.bytesToString(self.getData(0, 8))
 

class messageAuthenticationKeyAnswer(message):
    command = b"\x01\x0B"
    name = "AuthenticationKeyReply"
    
    def __init__(self):
        super(messageAuthenticationKeyAnswer, self).__init__(messageAuthenticationKeyAnswer.name)
        self.setCommand(messageAuthenticationKeyAnswer.command)

    def getStatus(self):
        return self.getData(0, sinope.dataBuffer.DataType.byte)

    def setStatus(self, status):
        self.setData(0, status, sinope.dataBuffer.DataType.byte)

    def getBackoff(self):
        return self.getData(1, sinope.dataBuffer.DataType.ushort)

    def setBackoff(self, backoff):
        self.setData(1, backoff, sinope.dataBuffer.DataType.ushort)

    def getApiKey(self):
        return self.getData(3, 8)

    def setApiKey(self, apiKey):
        self.setData(3, apiKey)

class messageLogin(message):
    command = b"\x01\x10"
    name = "ApiLogin"
    
    def __init__(self):
        super(messageLogin, self).__init__(messageLogin.name)
        self.setCommand(messageLogin.command)

    def setId(self, id):
        data = bytearray.fromhex(id)
        self.setData(0, data)

    def getId(self):
        return self.getData(0, 8)

    def setApiKey(self, apiKey):
        self.setData(8, apiKey)

    def getApiKey(self):
        return self.getData(8, 8)

class messageLoginAnswer(message):
    command = b"\x01\x11"
    name = "ApiLoginAnswer"
    
    def __init__(self):
        super(messageLoginAnswer, self).__init__(messageLoginAnswer.name)
        self.setCommand(messageLoginAnswer.command)

    def getStatus(self):
        return self.getDataFormat(0, sinope.dataBuffer.DataType.byte)

    def getStatus(self):
        return self.getData(1, sinope.dataBuffer.DataType.ushort)

    def getVersionMajor(self):
        return self.getData(3, sinope.dataBuffer.DataType.ubyte)

    def getVersionMinor(self):
        return self.getData(4, sinope.dataBuffer.DataType.ubyte)

    def getVersionBug(self):
        return self.getData(5, sinope.dataBuffer.DataType.ubyte)

    def getDeviceId(self):
        return self.getData(6,4)

class messageDeviceLinkReport(message):
    command = b"\x01\x16"
    name = "DeviceLinkReport"

    def __init__(self):
        super(messageDeviceLinkReport, self).__init__(messageDeviceLinkReport.name)
        self.setCommand(messageDeviceLinkReport.command)
        
    def getStatus(self):
        return self.getDataFormat(DataType.byte, 0)[0]

    def getDeviceId(self):        
        return self.getDataBuffer(1,4)

messagesequence = None
def getMessageSequence():
    global messagesequence
    if messagesequence == None:
        random.seed()
        messagesequence = random.randrange(0, pow(2, 32) -1)
    else:
        messagesequence += 1

    if messagesequence > pow(2,32) - 1:
        messagesequence = 0

    return messagesequence

class messageDataReadRequest(message):
    command = b"\x02\x40"
    name = "DataReadRequest"

    def __init__(self):
        super(messageDataReadRequest, self).__init__(messageDataReadRequest.name)
        self.setCommand(messageDataReadRequest.command)
        self.__setSequence(getMessageSequence())
        self.__setRequestType(0)
        self.__serReserve1(0)
        self.__serReserve2(0)
        self.__serReserve3(0)
        self.__serReserve4(0)

    def __setSequence(self, seq):
        self.setData(0, seq, sinope.dataBuffer.DataType.uinteger)

    def __setRequestType(self, requestType):
        self.setData(4, requestType, sinope.dataBuffer.DataType.ubyte)

    def __serReserve1(self, val):
        self.setData(5, val, sinope.dataBuffer.DataType.ubyte)

    def __serReserve2(self, val):
        self.setData(6, val, sinope.dataBuffer.DataType.ubyte)

    def __serReserve3(self, val):
        self.setData(7, val, sinope.dataBuffer.DataType.ushort)

    def __serReserve4(self, val):
        self.setData(9, val, sinope.dataBuffer.DataType.ushort)

    def setDeviceId(self, deviceId):
        self.setData(11, deviceId)

    def getSequence(self):
        return self.getData(0, sinope.dataBuffer.DataType.uinteger)

    def getDeviceId(self):
        return self.getData(11,4)

    def getApplicationDataSize(self):
        return self.getData(15, sinope.dataBuffer.DataType.ubyte)

    def getApplicationData(self):
        appData = self.getData(16, getApplicationDataSize())
        return applicationDataCreator.create(appData)

    def setApplicationData(self, appData):
        self.setData(DataType.ubyte, 15, appData.size)
        self.setData(16, appData.data)
