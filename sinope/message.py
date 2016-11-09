import struct
import sinope.crc
import sinope.str

CRC_SIZE = 1
HEADER55 = 0x55
HEADER00 = 0x00
HEADER_SIZE = 2
SIZE_SIZE = 2
COMMAND_SIZE = 2

class message(object):
    def create(headerRaw, commandRaw):
        msg = None
        (header55, header00) = struct.unpack("<BB", headerRaw)
        command = struct.unpack("<H", commandRaw)[0]

        if header55 != HEADER55 or header00 != HEADER00:
            raise Exception("Header not valid")

        msg = message("UnknownCommand")
        msg.setCommand(commandRaw, raw = True)

        return msg

    def read(stream):
        header = stream.read(HEADER_SIZE)
        size = stream.read(SIZE_SIZE)
        command = stream.read(COMMAND_SIZE)

        message = None

        if header == "" or size == "" or command == "":
            raise Exception("Unable to read packet headers")

        message = sinope.message.message.create(header, command)
        data = stream.read(sinope.message.message.getSizeFromRaw(size) - COMMAND_SIZE)
        message.setData(data, raw = True)

        crc = stream.read(CRC_SIZE)
        if message.getCrc() != crc:
            raise Exception("Failed to read message")

        return message

    def getSizeFromRaw(size):
        return struct.unpack("<H", size)[0]

    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("name argument not a string")
        self.__header = struct.pack("<BB", 0x55, 0x00)
        self.__name = name
        self.__size = None
        self.__command = None
        self.__data = None
        self.__crc = None

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
            return sinope.message.message.getSizeFromRaw(self.__size)

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

    def getData(self, raw = False):
        if raw:
            return self.__data
        else:
            data = bytearray(self.__data)
            data.reverse()
            return data

    def setData(self, data, raw = False):
        if not isinstance(data, bytes):
            raise Exception("Data argument not a bytes")
        if len(data) > 0:
            if raw:
                self.__data = bytearray(data)
            else:
                self.__data = bytearray(data)
                self.__data.reverse()
        self.__refresh()

    def getCrc(self):
        return self.__crc

    def getPayload(self):
        payload = bytearray()
        payload.add(self.__header)
        payload.add(self.__size)
        payload.add(self.__command)
        if self.__data != None:
            payload.add(self.__data)
        payload.add(self.crc)
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
