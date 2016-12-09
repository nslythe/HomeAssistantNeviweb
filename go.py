import logging
import time
import signal
import sys

import sinope.server
import sinope.message
import sinope.sessionManager
import sinope.deviceManager
import sinope.applicationData
import sinope.applicationObjectManager

server = sinope.server.server("10.1.0.152", 4550)
server.connect()

sessionManager = sinope.sessionManager.sessionManager(server)
appObjManager = sinope.applicationObjectManager.applicationObjectManager(server)
deviceManager = sinope.deviceManager.deviceManager(server)

sessionManager.authenticate(sys.argv[1])
sessionManager.login()

appData = sinope.applicationData.outdoorTemperature()
appData.setTemperature(22.2)
answer = appObjManager.report(appData, deviceManager.serverDevice)

server.wait()

