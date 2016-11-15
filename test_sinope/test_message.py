import unittest
import sinope.message

class messageTest(unittest.TestCase):
    def test_getName_1(self):
        message = sinope.message.message("test_message")
        self.assertEqual(message.getName(), "test_message")

    def test_getName_2(self):
        with self.assertRaises(Exception):
            message = sinope.message.message(1234)

    def test_setCommand_1(self):
        message = sinope.message.message("test_message")
        message.setCommand(b"\x44\x44")
        self.assertEqual(message.getCommand(), b"\x44\x44")
        self.assertEqual(str(message), "test_message 550002004444")

    def test_setCommand_2(self):
        message = sinope.message.message("test_message")
        message.setCommand(b"\xFF\x00")
        self.assertEqual(message.getCommandRaw(), bytearray.fromhex("00FF"))
        self.assertEqual(message.getCommand(), b"\xFF\x00")

    def test_setCommand_3(self):
        with self.assertRaises(Exception):
            message.setCommand("test")
        with self.assertRaises(Exception):
            message.setCommand("test", raw = True)

    def test_setCommand_4(self):
        message = sinope.message.message("test_message")
        message.setCommandRaw(b"\xFF\x00")
        self.assertEqual(message.getCommandRaw(), bytearray.fromhex("FF00"))
        self.assertEqual(message.getCommand(), b"\x00\xFF")

    def test_setCommand_6(self):
        with self.assertRaises(Exception):
            message.setCommand(bytearray.fromhex("00FF"))
   
    def test_get_payLoad_2(self):
        message = sinope.message.message("test_message")
        message.setCommand(b"\xFF\x00")
        self.assertEqual(message.getPayload(), b"\x55\x00\x02\x00\x00\xff\xba")
