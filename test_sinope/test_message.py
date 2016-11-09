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
        message.setCommand(0xFFFF)
        self.assertEqual(message.getCommand(), 0xFFFF)

    def test_setCommand_2(self):
        message = sinope.message.message("test_message")
        message.setCommand(0xFF00)
        self.assertEqual(message.getCommand(raw = True), bytearray.fromhex("00FF"))
        self.assertEqual(message.getCommand(), 0xFF00)

    def test_setCommand_3(self):
        with self.assertRaises(Exception):
            message.setCommand("test")

    def test_setCommand_4(self):
        message = sinope.message.message("test_message")
        message.setCommand(b"\xFF\x00", raw = True)
        self.assertEqual(message.getCommand(raw = True), bytearray.fromhex("FF00"))
        self.assertEqual(message.getCommand(), 0x00FF)

    def test_setCommand_5(self):
        with self.assertRaises(Exception):
            message.setCommand(0xFF00, raw = True)

    def test_setCommand_6(self):
        with self.assertRaises(Exception):
            message.setCommand(bytearray.fromhex("00FF"))

    def test_setData_1(self):
        message = sinope.message.message("test_message")
        with self.assertRaises(Exception):
            message.setData("dsdasdas")

    def test_setData_2(self):
        message = sinope.message.message("test_message")
        message.setCommand(0xFF00)
        message.setData(b"\x12\x34\x56\x78\x9A\xBC\xDE")
        self.assertEqual(message.getData(raw = False), bytearray.fromhex("123456789ABCDE"))
        self.assertEqual(message.getData(raw = False), bytearray.fromhex("123456789ABCDE"))
        self.assertEqual(message.getData(raw = True), bytearray.fromhex("DE BC 9A 78 56 34 12"))
        self.assertEqual(message.getSize(), 7 + sinope.message.COMMAND_SIZE)

    def test_setData_3(self):
        message = sinope.message.message("test_message")
        message.setCommand(0xFF00)
        message.setData(b"\xAA\xBB\xCC", raw = True)
        self.assertEqual(message.getData(raw = False), bytearray.fromhex("CCBBAA"))
        self.assertEqual(message.getData(raw = False), bytearray.fromhex("CCBBAA"))