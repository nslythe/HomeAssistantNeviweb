import sinope
import unittest
import test_sinope.StreamMoc
import sinope.message

class test_messageDataRequest(unittest.TestCase):
    def test_create_1(self):
        msg1 = sinope.message.messageDataRequestRead()
        msg2 = sinope.message.messageDataRequestRead()

        self.assertNotEqual(msg1.getSequence(), msg2.getSequence())
        msg1.setDeviceId(b"\x11\x22\x33\x44")
        self.assertEqual(msg1.getDeviceId(), b"\x11\x22\x33\x44")

    def test_getData_1(self):
        stream = test_sinope.StreamMoc.StreamMoc(b"\x55\x00\x16\x00\x40\x02\x78\x56\x34\x12\x00\x00\x00\x00\x00\x00\x00\x44\x04\x00\x00\x04\x03\x02\x00\x00\x29")
        msg = sinope.messageCreator.read(stream)

        self.assertEqual(msg.getCommand(), sinope.message.messageDataRequestRead.command)
        self.assertTrue(isinstance(msg, sinope.message.messageDataRequestRead))


        self.assertEqual(msg.getApplicationDataSize(), 4)
        appData = msg.getApplicationData()
        self.assertEqual(appData.getDataId(), b"\x00\x00\x02\x03")
