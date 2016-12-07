
import unittest
import sinope.message
import sinope.messageCreator
import test_sinope.StreamMoc

class StreamMocTest(unittest.TestCase):
    def test_read_1(self):
        stream = test_sinope.StreamMoc.StreamMoc(bytearray.fromhex("00 55"))
        self.assertEqual(stream.read(1), b"\x00")
        self.assertEqual(stream.read(1), b"\x55")
        self.assertEqual(stream.read(1), "")

    def test_read_2(self):
        stream = test_sinope.StreamMoc.StreamMoc(bytearray.fromhex("00 55"))
        self.assertEqual(stream.read(2), b'\x00\x55')


class messageCreateTest(unittest.TestCase):
    def test_create_1(self):
        stream = test_sinope.StreamMoc.StreamMoc(b"\x55\x00\x0A\x00\x0A\x01\xEF\xCD\xAB\x89\x67\x45\x23\x01\xDA")
        sinope.messageCreator.read(stream)

    def test_create_2(self):
        stream = test_sinope.StreamMoc.StreamMoc(b"\x56\x00\x0A\x00\x0A\x01\xEF\xCD\xAB\x89\x67\x45\x23\x01\xDA")
        with self.assertRaises(Exception):
            sinope.message.message.read(stream)

    def test_create_3(self):
        stream = test_sinope.StreamMoc.StreamMoc(b"\x56\x00\x0A")
        with self.assertRaises(Exception):
            sinope.message.message.read(stream)

    def test_create_4(self):
        stream = test_sinope.StreamMoc.StreamMoc(b"\x56\x00\x0A\x00\x0A")
        with self.assertRaises(Exception):
            sinope.message.message.read(stream)

    def test_create_5(self):
        stream = test_sinope.StreamMoc.StreamMoc(b"\x55\x00\x0A\x00\x0A\x01\xEF\xCD\xAB\x89\x67\x45\x23\x01\xDB")
        with self.assertRaises(Exception):
            sinope.message.message.read(stream)

