import logging
import time
import signal
import sys

import sinope.server
import sinope.message
import sinope.sessionManager
import sinope.applicationData



server = sinope.server.server("10.1.0.152", 4550)
server.connect()

sessionManager = sinope.sessionManager.sessionManager(server)
sessionManager.authenticate(sys.argv[1])
sessionManager.login()

message = sinope.message.messageDataRequestWrite()
appData = sinope.applicationData.outdoorTemperature()
appData.setTemperature(20)
message.setApplicationData(appData)

server.sendMessage(message)

server.wait()

