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
        message.setCommand(b"\xFF\xFF")
        self.assertEqual(message.getCommand(), b"\xFF\xFF")

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
   
    def test_setData_1(self):
        message = sinope.message.message("test_message")
        with self.assertRaises(Exception):
            message.setRawData("dsdasdas")

    def test_setData_2(self):
        message = sinope.message.message("test_message")
        message.setCommand(b"\xFF\x00")
        message.setDataRaw(b"\x12\x34\x56\x78\x9A\xBC\xDE")
        self.assertEqual(message.getDataRaw(), bytearray.fromhex("123456789ABCDE"))
        self.assertEqual(message.getDataFormat(sinope.message.DataType.ushort, 0)[0], 13330)
        self.assertEqual(message.getDataFormat(sinope.message.DataType.ushort, 3)[0], 39544)
        self.assertEqual(message.getSize(), 7 + sinope.messageCreator.COMMAND_SIZE)
        self.assertEqual(message.getSize(raw = True), b"\x09\x00")

    def test_setData_4(self):
        message = sinope.message.message("test_message")
        with self.assertRaises(Exception):
            message.setRawData(b"\xAA\xBB\xCC", raw = True)

    def test_setData_5(self):
        message = sinope.message.message("test_message")
        message.setCommand(b"\xFF\x00")
        message.setDataFormat(sinope.message.DataType.ushort, 0, 10)
        self.assertEqual(message.getDataFormat(sinope.message.DataType.ushort, 0,)[0], 10)
        self.assertEqual(message.getDataBuffer(0, 2), b'\x00\x0A')
        self.assertEqual(message.getDataRaw(), b'\x0A\x00')
        message.setDataFormat(sinope.message.DataType.ushort, 2, 20)
        self.assertEqual(message.getDataFormat(sinope.message.DataType.ushort, 0,)[0], 10)
        self.assertEqual(message.getDataFormat(sinope.message.DataType.ushort, 2,)[0], 20)
        message.setDataBuffer(b"\x11\x22\x33\x44\x55", 4)
        self.assertEqual(message.getDataBuffer(4, 5), b'\x11\x22\x33\x44\x55')
        

    def test_get_payLoad_1(self):
        message = sinope.message.message("test_message")
        message.setCommand(b"\xFF\x00")
        message.setDataRaw(b"\x12")
        self.assertEqual(str(message), "test_message 5500 | 0300 | 00ff | 12 | 33")
        self.assertEqual(message.getPayload(), b"\x55\x00\x03\x00\x00\xff\x12\x33")

    def test_get_payLoad_2(self):
        message = sinope.message.message("test_message")
        message.setCommand(b"\xFF\x00")
        self.assertEqual(message.getPayload(), b"\x55\x00\x02\x00\x00\xff\xba")
