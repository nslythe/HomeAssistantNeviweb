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
