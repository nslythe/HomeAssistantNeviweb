import enum
import struct
import sinope.crc
import sinope.str

class DataType(enum.Enum):
    char = "c"
    byte = "b"
    ubyte = "B"
    short = "h"
    ushort = "H"
    integer = "i"
    uinteger = "I"


class dataBuffer(object):
    def __init__(self):
        self.__size = 0
        self.__data = bytearray(self.__size)
        self.__crc = None
        self.refreshListener = []

    def __refreshSize(self):
        self.__size = len(self.__data)

    def __refreshCrc(self):
        crc = sinope.crc.crc8()
        self.__crc = struct.pack("B", crc.crc(self.__data))

    def __refresh(self):
        self.__refreshSize()
        self.__refreshCrc()
        self.didRefresh()

    def clone(self, other):
        self.__data = bytearray(other.__data)
        self.__refresh()

    def didRefresh(self):
        pass

#    def __checkSize(self, neededSize):
#        if neededSize > len(self.__data):
#            for x in range(len(self.__data), neededSize):
#                self.__data.append(0)
    
    def getSize(self):
        return self.__size

    def getData(self, offset, length):
        dataToReturn = None
        if isinstance(length, DataType):
            strFormat = "<%s" % length.value
            dataToReturn = struct.unpack_from(strFormat, self.__data, offset)[0]
        elif isinstance(length, int):
            dataToReturn = self.__data[offset : offset + length]
            dataToReturn.reverse()
        else:
            raise Exception("Parameter type not valid")
        return dataToReturn

    def getDataRaw(self, offset = -1, length = -1):
        if offset == -1 or length == -1:
            return bytearray(self.__data)
        else:
            return self.__data[offset : offset + length]

    def setData(self, offset, data, dataType = None):
        dataToWrite = None
        if dataType != None:
            if not isinstance(dataType, DataType):
                raise Exception("Valid datatype expected")
            strFormat = "<%s" % dataType.value
            dataToWrite = struct.pack(strFormat, data)
        elif isinstance(data, bytearray) or isinstance(data, bytes):
            dataToWrite = bytearray(data)
            dataToWrite.reverse()
        else:
            raise Exception("Parameter type not valid")
        self.__data[offset : offset + len(dataToWrite)] = dataToWrite
        self.__refresh()

    def setDataRaw(self, offset, data):
        if not isinstance(data, bytes) and not isinstance(data, bytearray):
            raise Exception("Data argument not a bytes")
        if len(data) > 0:
            self.__data[offset : offset + len(data)] = bytearray(data)
        self.__refresh()

    def getCrc(self):
        return self.__crc

    def __str__(self):
        return sinope.str.bytesToString(self.__data)

    def __len__(self):
        return len(self.__data)
