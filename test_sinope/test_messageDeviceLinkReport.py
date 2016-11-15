import unittest
import sinope

class test_messageLinkReport(unittest.TestCase):
    def test_create_1(self):
        message = sinope.message.messageDeviceLinkReport()
        message.setStatus(10)
        message.setDeviceId(b"\x11\x22\x33\x44")
        self.assertEqual(message.getStatus(), 10)
        self.assertEqual(message.getDeviceId(), b"\x11\x22\x33\x44")

