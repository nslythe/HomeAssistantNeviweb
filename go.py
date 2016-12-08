import logging
import time
import signal
import sys

import sinope.server
import sinope.message
import sinope.sessionManager
import sinope.applicationData
import sinope.applicationObjectManager


server = sinope.server.server("10.1.0.152", 4550)
server.connect()


sessionManager = sinope.sessionManager.sessionManager(server)
sessionManager.authenticate(sys.argv[1])
sessionManager.login()

appObjManager = sinope.applicationObjectManager.applicationObjectManager(server)

message = sinope.message.messageDataRequestWrite()
message.setDeviceId(b"\x00\x00\x21\xb5")
appData = sinope.applicationData.outdoorTemperature()
appData.setTemperature(22.2)
message.setApplicationData(appData)
server.sendMessage(message)

message = sinope.message.messageDataRequestRead()
message.setDeviceId(b"\x00\x00\x21\xb5")
appData = sinope.applicationData.outdoorTemperature()
message.setApplicationData(appData)
server.sendMessage(message)

server.wait()

