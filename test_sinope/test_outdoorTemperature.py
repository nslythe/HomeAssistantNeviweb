import unittest
import sinope.applicationData
import sinope.applicationDataCreator


class test_outDoorTemperature(unittest.TestCase):
    def test_create_1(self):
        appData = sinope.applicationData.outdoorTemperature()
        self.assertEqual(appData.getDataId(), b"\x00\x00\x02\x04")
        appData.setTemperature(10)
        print (sinope.str.bytesToString(appData.getDataRaw()))
        self.assertEqual(appData.getTemperature(), 10)
        appData.setTemperature(-10)
        self.assertEqual(appData.getTemperature(), -10)

    def test_create_2(self):
        tempData = sinope.applicationData.outdoorTemperature()
        appData = sinope.applicationDataCreator.create(tempData.getDataRaw())
        self.assertTrue(isinstance(appData, sinope.applicationData.outdoorTemperature))

    def test_send_1(self):
        message = sinope.message.messageDataRequestRead()
        appData = sinope.applicationData.outdoorTemperature()
        message.setApplicationData(appData)

