import unittest
import sinope.message
import sinope.classBrowser

class messageTest(unittest.TestCase):
    def test_getClass(self):
        self.assertTrue(sinope.classBrowser.getSubClassCommand(sinope.message.message, "command", sinope.message.messageAuthenticationKey.command) != None)
        self.assertTrue(sinope.classBrowser.getSubClassCommand(sinope.message.message, "command1", sinope.message.messageAuthenticationKey.command) == None)
        
