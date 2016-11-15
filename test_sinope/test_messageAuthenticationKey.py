import unittest
import sinope.message

class test_messageAuthenticationKeyAnswer(unittest.TestCase):

    def test_create_1(self):
        message = sinope.message.messageAuthenticationKey()
        message.setId("1122334455667788")
        self.assertEqual(message.getId(), "1122334455667788")

    def test_create_2(self):
        message = sinope.message.messageAuthenticationKey()
        with self.assertRaises(Exception):
            message.setId(b"\x00\x11")

    def test_create_answer__2(self):
        message = sinope.message.messageAuthenticationKeyAnswer()
        message.setStatus(1)
        message.setBackoff(0)
        message.setApiKey(b"\x88\x77\x66\x55\x44\x33\x22\x11")
        self.assertEqual(message.getApiKey(), b"\x88\x77\x66\x55\x44\x33\x22\x11")
        self.assertEqual(message.getStatus(), 1)
        self.assertEqual(message.getBackoff(), 0)
