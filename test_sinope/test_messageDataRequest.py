import sinope
import unittest

class test_messageDataRequest(unittest.TestCase):
    def test_create_1(self):
        msg1 = sinope.message.messageDataRequestRead()
        msg2 = sinope.message.messageDataRequestRead()

        self.assertNotEqual(msg1.getSequence(), msg2.getSequence())
        msg1.setDeviceId(b"\x11\x22\x33\x44")
        self.assertEqual(msg1.getDeviceId(), b"\x11\x22\x33\x44")
