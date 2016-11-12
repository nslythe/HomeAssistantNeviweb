import inspect
import struct
import sys
import sinope.crc
import sinope.str
import sinope.messageCreator

class message(object):
    def getSizeFromRawData(size):
        return struct.unpack("<H", size)[0]

    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("name argument not a string")
        self.__header = struct.pack("<BB", 0x55, 0x00)
        self.__name = name
        self.__size = None
        self.__command = None
        self.__data = bytearray()
        self.__crc = None

    def clone(self, other):
        self.__size = other.__size
        self.__command = other.__command
        self.__data = other.__data
        self.__crc = other.__crc

    def __refreshSize(self):
        if self.__command == None:
            raise Exception("Command not set")
        tmpSize = 0
        tmpSize += len(self.__command)
        if self.__data != None:
            tmpSize += len(self.__data);
        self.__size = struct.pack("<H", tmpSize)

    def __refreshCrc(self):
        if self.__command == None:
            raise Exception("Command not set")
        if self.__size == None:
            raise Exception("Size not set")
        crc = sinope.crc.crc8()
        data = self.__header + self.__size + self.__command
        if self.__data != None:
            data += self.__data
        self.__crc = struct.pack("<B", crc.crc(data))

    def __refresh(self):
        self.__refreshSize()
        self.__refreshCrc()

    def getName(self):
        return self.__name

    def getSize(self, raw = False):
        if raw:
            return self.__size
        else:
            return sinope.message.message.getSizeFromRawData(self.__size)

    def getCommand(self, raw = False):
        if raw:
            return self.__command
        else:
            return struct.unpack("<H", self.__command)[0]

    def setCommand(self, command, raw = False):
        if raw:
            if not isinstance(command, bytes):
                raise Exception("Command argument not a bytes")
            self.__command = command
        else:
            if not isinstance(command, int):
                raise Exception("Command argument not a int")
            self.__command = struct.pack("<H", command)
        self.__refresh()

    def getDataFormat(self, fmt, offset):
        strFormat = "<%s" % fmt
        return struct.unpack_from(strFormat, self.__data, offset)

    def getDataBuffer(self, pt, length):
        data = self.__data[pt : pt + length]
        data.reverse()
        return data

    def getDataRaw(self):
        return self.__data

    def setDataFormat(self, fmt, offset, data):
        strFormat = "<%s" % fmt
        struct.pack_into(strFormat, self.__data, offset, data)
        self.__refresh()

    def setDataBuffer(self, data, offset):
        if not isinstance(data, bytes) and not isinstance(data, bytearray):
            raise Exception("Data argument not a bytes")
        if len(data) > 0:
            data.reverse()
            self.__data[offset:] = data
        self.__refresh()

    def setDataRaw(self, data):
        if not isinstance(data, bytes) and not isinstance(data, bytearray):
            raise Exception("Data argument not a bytes")
        if len(data) > 0:
            self.__data = bytearray(data)
        self.__refresh()


    def getCrc(self):
        return self.__crc

    def getPayload(self):
        payload = bytearray()
        payload += self.__header
        payload += self.__size
        payload += self.__command
        if self.__data != None:
            payload += self.__data
        payload += self.__crc
        return payload 

    def __str__(self):
        s = self.__name
        s += " " 
        s += sinope.str.bytesToString(self.__header)

        if self.__size != None:
            s += " | "
            s += sinope.str.bytesToString(self.__size)

        if self.__command != None:
            s += " | "
            s += sinope.str.bytesToString(self.__command)

        if self.__data != None:
            s += " | "
            s += sinope.str.bytesToString(self.__data)

        if self.__crc != None:
            s += " | "
            s += sinope.str.bytesToString(self.__crc)
        return s

class messagePing(message):
    command = 0x0012
    name = "Ping"
    
    def __init__(self):
        message.__init__(self, messagePing.name)
        self.setCommand(messagePing.command)

class messagePingAnswer(message):
    command = 0x0013
    name = "PingReply"
    
    def __init__(self):
        message.__init__(self, messagePingAnswer.name)
        self.setCommand(messagePingAnswer.command)
        
class messageAuthenticationKey(message):
    command = 0x010A
    name = "AuthenticationKey"
    
    def __init__(self):
        super(messageAuthenticationKey, self).__init__(messageAuthenticationKey.name)
        self.setCommand(messageAuthenticationKey.command)

    def setId(self, id):
        self.setDataBuffer(bytearray.fromhex(id), 0)
 

class messageAuthenticationKeyAnswer(message):
    command = 0x010B
    name = "AuthenticationKeyReply"
    
    def __init__(self):
        message.__init__(self, messageAuthenticationKeyAnswer.name)
        self.setCommand(messageAuthenticationKeyAnswer.command)

    def getStatus(self):
        return self.getDataFormat("B", 0)[0]

    def getBackoff(self):
        return self.getDataFormat("H", 1)[0]

    def getApiKey(self):
        return self.getDataBuffer(3,8)

class messageLogin(message):
    command = 0x0110
    name = "ApiLogin"
    
    def __init__(self):
        super(messageAuthenticationKey, self).__init__(messageAuthenticationKey.name)
        self.setCommand(messageAuthenticationKey.command)

    def setId(self, id):
        data = bytearray.fromhex(id)
        data.reverse()
        self.setRawData(bytes(data))

    def setApiKey(self, apiKey):
        data = bytearray.fromhex(apiKey)
        data.reverse()
        self.setRawData(bytes(data))

