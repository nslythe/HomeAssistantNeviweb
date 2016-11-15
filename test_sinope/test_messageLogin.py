import unittest
import sinope.message


class test_messageLogin(unittest.TestCase):

    def test_create_1(self):
        message = sinope.message.messageLogin()
        self.assertEqual(message.getCommand(), b"\x01\x10")
        message.setId("1122334455667788")
        self.assertEqual(message.getId(), b"\x11\x22\x33\x44\x55\x66\x77\x88")
        message.setApiKey(b"\x11\x22\x33\x44\x55\x66\x77\x88")
        self.assertEqual(message.getApiKey(), b"\x11\x22\x33\x44\x55\x66\x77\x88")

    def test_create_1(self):
        message = sinope.message.messageLoginAnswer()
        self.assertEqual(message.getCommand(), b"\x01\x11")
        message.setStatus(12)
        message.setBackoff(22)
        message.setVersionMajor(1)
        message.setVersionMinor(2)
        message.setVersionBug(3)
        message.setDeviceId(b"\x11\x22\x33\x44")

        self.assertEqual(message.getStatus(), 12)
        self.assertEqual(message.getBackoff(), 22)
        self.assertEqual(message.getVersionMajor(), 1)
        self.assertEqual(message.getVersionMinor(), 2)
        self.assertEqual(message.getVersionBug(), 3)
        self.assertEqual(message.getDeviceId(), b"\x11\x22\x33\x44")
