import struct
import sinope.crc

CRC_SIZE = 1
HEADER55 = 0x55
HEADER00 = 0x00
HEADER_SIZE = 2
SIZE_SIZE = 2
COMMAND_SIZE = 2

def create(headerRaw, sizeRaw, commandRaw):
    message = None
    (header55, header00) = struct.unpack("<BB", headerRaw)
    size = struct.unpack("<h", sizeRaw)[0]
    command = struct.unpack("<h", commandRaw)[0]

    if header55 == HEADER55 and header00 == HEADER00:
        if command == messagePingAnswer.command:
            message = messagePingAnswer()
        if command == messageAuthenticationKeyAnswer.command:
            message = messageAuthenticationKeyAnswer()

    if message != None:
        message.setSize(size)

    return message

class message(object):
    def __init__(self, name):
        self.__header = struct.pack("<BB", 0x55, 0x00)
        self.__name = name
        self.size = None
        self.command = None
        self.__data = None
        self.crc = None

    def __calculateSize(self):
        tmpSize = 0
        if self.command != None:
            tmpSize += len(self.command)
        if self.__data != None:
            tmpSize += len(self.__data);
        self.size = struct.pack("<h", tmpSize)

    def getSize(self):
        return struct.unpack("<h", self.size)[0]

    def setSize(self, size):
        self.size = struct.pack("<h", size)

    def getCommand(self):
        return struct.unpack("<h", self.command)[0]

    def setCommand(self, command):
        self.command = struct.pack("<h", command)

    def setData(self, data):
        data.reverse()
        self.__data = data

    def __calculateCrc(self):
        self.__calculateSize()
        crc = sinope.crc.crc8()
        data = self.__header + self.size + self.command
        if self.__data != None:
            data += self.__data
        return struct.pack("B", crc.crc(data))

    def checkCrc(self):
        return self.crc == self.__calculateCrc()

    def getPayload(self):
        self.crc = self.__calculateCrc()
        payload = self.__header + self.size + self.command;
        if self.__data != None:
            payload += self.__data
        payload += self.crc
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

        if self.crc != None:
            s += " | "
            s += self.__bytesToString(self.crc)
        return s

class messageRequest(message):
    def __init__(self, name):
        super(messageRequest, self).__init__(name)


class messageAnswer(message):
    def __init__(self, name):
        super(messageAnswer, self).__init__(name)


class messagePing(messageRequest):
    command = 0x0012
    name = "Ping"
    
    def __init__(self):
        messageRequest.__init__(self, messagePing.name)
        self.setCommand(messagePing.command)

class messagePingAnswer(messageAnswer):
    command = 0x0013
    name = "PingReply"
    
    def __init__(self):
        messageAnswer.__init__(self, messagePingAnswer.name)
        self.setCommand(messagePingAnswer.command)
        
class messageAuthenticationKey(messageRequest):
    command = 0x010A
    name = "AuthenticationKey"
    
    def __init__(self, key):
        super(messageAuthenticationKey, self).__init__(messageAuthenticationKey.name)
        self.setCommand(messageAuthenticationKey.command)
        self.setData(bytearray.fromhex(key))

class messageAuthenticationKeyAnswer(messageAnswer):
    command = 0x010B
    name = "AuthenticationKeyReply"
    
    def __init__(self):
        messageAnswer.__init__(self, messageAuthenticationKeyAnswer.name)
        self.setCommand(messageAuthenticationKeyAnswer.command)
