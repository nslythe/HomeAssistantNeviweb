import unittest
import sinope.message

class test_messageAuthenticationKeyAnswer(unittest.TestCase):

    def test_create_1(self):
        message = sinope.message.messageAuthenticationKeyAnswer()
        message.setData(b"\x01\x00\x00\x11\x22\x33\x44\x55\x66\x77\x88")
        self.assertEqual(message.getApiKey(), b"\x88\x77\x66\x55\x44\x33\x22\x11")
        self.assertEqual(message.getStatus(), 1)
        self.assertEqual(message.getBackoff(), 0)
