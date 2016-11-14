import sinope
import unittest

class test_messageDataReadRequest(unittest.TestCase):
    def test_create_1(self):
        msg1 = sinope.message.messageDataReadRequest()
        msg2 = sinope.message.messageDataReadRequest()
        self.assertEqual(msg1.getSequence()+1, msg2.getSequence())
        msg1.setDeviceId(b"\x11\x22\x33\x44")
        self.assertEqual(msg1.getDeviceId(), b"\x11\x22\x33\x44")
