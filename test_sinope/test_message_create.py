
import unittest
import sinope.message

class StreamMoc:
    def __init__(self, data):
        self.data = data
        self.pt = 0

    def read(self, size):
        if self.pt + size > len(self.data):
            return ""
        returnValue = self.data[self.pt : self.pt + size]
        self.pt += size
        return bytes(returnValue)

class StreamMocTest(unittest.TestCase):
    def test_read_1(self):
        stream = StreamMoc(bytearray.fromhex("00 55"))
        self.assertEqual(stream.read(1), b"\x00")
        self.assertEqual(stream.read(1), b"\x55")
        self.assertEqual(stream.read(1), "")

    def test_read_2(self):
        stream = StreamMoc(bytearray.fromhex("00 55"))
        self.assertEqual(stream.read(2), b'\x00\x55')


class messageCreateTest(unittest.TestCase):
    def test_create_1(self):
        stream = StreamMoc(b"\x55\x00\x0A\x00\x0A\x01\xEF\xCD\xAB\x89\x67\x45\x23\x01\xDA")
        sinope.message.message.read(stream)
