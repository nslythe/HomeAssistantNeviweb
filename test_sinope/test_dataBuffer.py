import unittest
import sinope.dataBuffer

class test_dataBuffer(unittest.TestCase):
    def test_crc_1(self):
        data = sinope.dataBuffer.dataBuffer()
        data.setDataRaw(0, b"\x55\x00\x0A\x00\x0A\x01\xEF\xCD\xAB\x89\x67\x45\x23\x01")
        self.assertEqual(data.getSize(), 14)
        self.assertEqual(data.getDataRaw(0), b"\x55\x00\x0A\x00\x0A\x01\xEF\xCD\xAB\x89\x67\x45\x23\x01")
        self.assertEqual(data.getCrc(), 0xDA)

    def test_crc_1(self):
        data = sinope.dataBuffer.dataBuffer()
        data.setData(0, b"\x00\x11")
        self.assertEqual(data.getDataRaw(0), b"\x11\x00")
