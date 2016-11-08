import struct
import sinope.crc

def create(data):
    header = struct.unpack("<BBhh", data)
    print (header)


class message:
    def __init__(self):
        self.__header = struct.pack("<BB", 0x55, 0x00)
        self.__size = None
        self.__command = None
        self.__data = None
        self.__crc = None

    def setCommand(self, command):
        self.__command = struct.pack("<h", command)
        self.__calculateSize()
        self.__calculateCrc()

    def __calculateSize(self):
        tmpSize = 0
        if self.__command != None:
            tmpSize += len(self.__command)
        if self.__data != None:
            tmpSize += len(self.__data);
        self.__size = struct.pack("<h", tmpSize)
    
    def __calculateCrc(self):
        self.__calculateSize()
        crc = sinope.crc.crc8()
        data = self.__header + self.__size + self.__command
        if self.__data != None:
            data += self.__data
        self.__crc = struct.pack("B", crc.crc(data))

    def getPayload(self):
        self.__calculateSize()
        self.__calculateCrc()
        payload = self.__header + self.__size + self.__command;
        if self.__data != None:
            payload += self.__data
        payload += self.__crc
        return payload 

    def setData(self, data):
        self.__calculateSize()
        self.__calculateCrc()

    def __bytesToString(self, bytesVar):
        s = ""
        for b in bytesVar:
            s += "%02x " % b
        return s

    def __str__(self):
        s = self.__bytesToString(self.__header)
        s += " | "
        s += self.__bytesToString(self.__size)
        s += " | "
        s += self.__bytesToString(self.__command)
        if self.__data != None:
            s += " | "
            s += self.__bytesToString(self.__data)
        s += " | "
        s += self.__bytesToString(self.__crc)
        return s

class messagePing(message):
    command = 0x0012
    
    def __init__(self):
        message.__init__(self)
        self.setCommand(command)
        
class messageAuthenticationKey(message):
    command = 0x010A
    
    def __init__(self):
        message.__init__(self)
        self.setCommand(command)
        self.__idHex = None
        
    def setId(self, idValue):
        self.__idHex = bytearray.fromhex(strid)


