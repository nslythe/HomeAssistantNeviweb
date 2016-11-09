import struct
import sinope.crc
import sinope.str

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

    def read(server):
        header = server.receive(HEADER_SIZE)
        size = server.receive(SIZE_SIZE)
        command = server.receive(COMMAND_SIZE)
        if header != None and size != None and command != None:
            message = sinope.message.create(header, size, command)

            if message != None:
                data = server.receive(message.getSize() - COMMAND_SIZE)
                if data != None:
                    message.data = data

                crc = server.receive(CRC_SIZE)
                if crc != None:
                    if message.checkCrc(crc):
                        return message
        return None


    def __init__(self, name):
        self.__header = struct.pack("<BB", 0x55, 0x00)
        self.__name = name
        self.size = None
        self.command = None
        self.data = None
        self.crc = None

    def __calculateSize(self):
        tmpSize = 0
        tmpSize += len(self.command)
        if self.data != None:
            tmpSize += len(self.data);
        self.size = struct.pack("<h", tmpSize)

    def __calculateCrc(self):
        self.__calculateSize()
        crc = sinope.crc.crc8()
        data = self.__header + self.size + self.command
        if self.data != None:
            data += self.data
        return struct.pack("<B", crc.crc(data))

    def getSize(self):
        return struct.unpack("<h", self.size)[0]

    def setSize(self, size):
        self.size = struct.pack("<h", size)

    def getCommand(self):
        return struct.unpack("<h", self.command)[0]

    def setCommand(self, command):
        self.command = struct.pack("<h", command)

    def getData(self):
        return self.data

    def setData(self, data):
        data.reverse()
        self.data = data

    def checkCrc(self, crc):
        self.crc = self.__calculateCrc()
        return self.crc == crc

    def getPayload(self):
        self.size = self.__calculateSize()
        self.crc = self.__calculateCrc()
        payload = self.__header + self.size + self.command;
        if self.data != None:
            payload += self.data
        payload += self.crc
        return payload 

    def __str__(self):
        s = self.__name
        s += " " 
        s += sinope.str.bytesToString(self.__header)

        if self.size != None:
            s += " | "
            s += sinope.str.bytesToString(self.size)

        if self.command != None:
            s += " | "
            s += sinope.str.bytesToString(self.command)

        if self.data != None:
            s += " | "
            s += sinope.str.bytesToString(self.data)

        if self.crc != None:
            s += " | "
            s += sinope.str.bytesToString(self.crc)
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
    
    def __init__(self, key):
        super(messageAuthenticationKey, self).__init__(messageAuthenticationKey.name)
        self.setCommand(messageAuthenticationKey.command)
        self.setData(bytearray.fromhex(key))

class messageAuthenticationKeyAnswer(message):
    command = 0x010B
    name = "AuthenticationKeyReply"
    
    def __init__(self):
        message.__init__(self, messageAuthenticationKeyAnswer.name)
        self.setCommand(messageAuthenticationKeyAnswer.command)

    def getStatus(self):
        return struct.unpack("<bh8c", self.getData())[0]

    def getBackout(self):
        return struct.unpack("<bH8c", self.getData())[1]

    def getApiKey(self):
        data = bytearray()
        maping = struct.unpack(">bH8B", self.getData())
        data.append(maping[2])
        data.append(maping[3])
        data.append(maping[4])
        data.append(maping[5])
        data.append(maping[6])
        data.append(maping[7])
        data.append(maping[8])
        data.append(maping[9])
        return data
