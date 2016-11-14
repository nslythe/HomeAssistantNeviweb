import unittest
import sinope

class test_messageSequence(unittest.TestCase):
    def test_seq_1(self):
        seq = sinope.message.getMessageSequence()
        self.assertEqual(seq+1, sinope.message.getMessageSequence())
        self.assertEqual(seq+2, sinope.message.getMessageSequence())

    def test_seq_1(self):
        sinope.message.messagesequence = pow(2,32) - 1
        self.assertEqual(sinope.message.getMessageSequence(), 0)
        self.assertEqual(sinope.message.getMessageSequence(), 1)
