import struct
import sinope.crc

CRC_SIZE = 1
HEADER55 = 0x55
HEADER00 = 0x00
HEADER_SIZE = 2
SIZE_SIZE = 2
COMMAND_SIZE = 2

def create(data):
    message = None
    (header55, header00, size, command) = struct.unpack("<BBhh", data)

    if header55 == HEADER55 and header00 == HEADER00:
        if command == messagePingAnswer.command:
            message = messagePingAnswer(size)

    return message

class message:
    def __init__(self, name):
        self.__header = struct.pack("<BB", 0x55, 0x00)
        self.__name = name
        self.size = None
        self.command = None
        self.__data = None
        self.__crc = None

    def __calculateSize(self):
        tmpSize = 0
        if self.command != None:
            tmpSize += len(self.command)
        if self.__data != None:
            tmpSize += len(self.__data);
        self.size = struct.pack("<h", tmpSize)

    def getSize(self):
        return struct.unpack("<h", self.size)[0]

    def __calculateCrc(self):
        self.__calculateSize()
        crc = sinope.crc.crc8()
        data = self.__header + self.size + self.command
        if self.__data != None:
            data += self.__data
        self.__crc = struct.pack("B", crc.crc(data))

    def getPayload(self):
        self.__calculateCrc()
        payload = self.__header + self.size + self.command;
        if self.__data != None:
            payload += self.__data
        payload += self.__crc
        return payload 


    def __bytesToString(self, bytesVar):
        s = ""
        for b in bytesVar:
            s += "%02x" % b
        return s

    def __str__(self):
        s = self.__name
        s += " " 
        s += self.__bytesToString(self.__header)

        if self.size != None:
            s += " | "
            s += self.__bytesToString(self.size)

        if self.command != None:
            s += " | "
            s += self.__bytesToString(self.command)

        if self.__data != None:
            s += " | "
            s += self.__bytesToString(self.__data)

        if self.__crc != None:
            s += " | "
            s += self.__bytesToString(self.__crc)
        return s

class messageRequest(message):
    def __init__(self, name):
        message.__init__(self, name)

    def setCommand(self, command):
        self.command = struct.pack("<h", command)

    def setData(self, data):
        pass

class messageAnswer(message):
    def __init__(self, size, name):
        message.__init__(self, name)
        self.size = struct.pack("<h", size)

class messagePing(messageRequest):
    command = 0x0012
    name = "Ping"
    
    def __init__(self):
        messageRequest.__init__(self, messagePing.name)
        self.setCommand(messagePing.command)

class messagePingAnswer(messageAnswer):
    command = 0x0013
    name = "PingReply"
    
    def __init__(self, size):
        messageAnswer.__init__(self, size, messagePingAnswer.name)
        
class messageAuthenticationKey(messageRequest):
    command = 0x010A
    name = "AuthenticationKey"
    
    def __init__(self):
        messageRequest.__init__(self, messageAuthenticationKey.name)
        self.setCommand(messageAuthenticationKey.command)
        self.__idHex = None
        
    def setId(self, idValue):
        self.__idHex = bytearray.fromhex(strid)


