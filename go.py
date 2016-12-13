import logging
import time
import signal
import sys

import sinope.server
import sinope.message
import sinope.sessionManager
import sinope.deviceManager
import sinope.dataManager
import sinope.applicationData
import sinope.applicationObjectManager

server = sinope.server.server("10.1.0.152", 4550)
server.connect()

dataManager = sinope.dataManager.dataManager()
print (dataManager.getData())

sessionManager = sinope.sessionManager.sessionManager(server, dataManager)
appObjManager = sinope.applicationObjectManager.applicationObjectManager(server)
deviceManager = sinope.deviceManager.deviceManager(server, dataManager)

if len(sys.argv) >= 2:
    sessionManager.authenticate(sys.argv[1])
else:
    sessionManager.authenticate()
    
sessionManager.login()

appData = sinope.applicationData.roomTemperature()
answer = appObjManager.read(appData, deviceManager.serverDevice)

server.wait()

