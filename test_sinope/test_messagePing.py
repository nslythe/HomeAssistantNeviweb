import unittest
import sinope.message


class test_messagePing(unittest.TestCase):

    def test_create_1(self):
        message = sinope.message.messagePing()
        self.assertEqual(message.getCommand(), b"\x00\x12")
        
    def test_create_1(self):
        message = sinope.message.messagePingAnswer()
        self.assertEqual(message.getCommand(), b"\x00\x13")
