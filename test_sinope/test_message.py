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
        with self.assertRaises(Exception):
            message.setCommand("test", raw = True)

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
        self.assertEqual(message.getRawData(), bytearray.fromhex("123456789ABCDE"))
        self.assertEqual(message.getData(0, 2), bytearray.fromhex("3412"))
        self.assertEqual(message.getData(3, 2), bytearray.fromhex("9A78"))
        self.assertEqual(message.getSize(), 7 + sinope.messageCreator.COMMAND_SIZE)
        self.assertEqual(message.getSize(raw = True), b"\x09\x00")

    def test_setData_4(self):
        message = sinope.message.message("test_message")
        with self.assertRaises(Exception):
            message.setData(b"\xAA\xBB\xCC", raw = True)

    def test_get_payLoad_1(self):
        message = sinope.message.message("test_message")
        message.setCommand(0xFF00)
        message.setData(b"\x12")
        self.assertEqual(str(message), "test_message 5500 | 0300 | 00ff | 12 | 33")
        self.assertEqual(message.getPayload(), b"\x55\x00\x03\x00\x00\xff\x12\x33")

    def test_get_payLoad_2(self):
        message = sinope.message.message("test_message")
        message.setCommand(0xFF00)
        self.assertEqual(message.getPayload(), b"\x55\x00\x02\x00\x00\xff\xba")
