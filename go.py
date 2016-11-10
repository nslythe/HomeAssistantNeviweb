import logging
import time
import signal
import sys

import sinope.server
import sinope.message
import sinope.sessionManager



# sinope.sessionManager.sessionManager()
# message = sinope.message.messageAuthenticationKey()
# message.setKey(sys.argv[1])


server = sinope.server.server("10.1.0.152", 4550)
# server.addMessageHandler(sinope.sessionManager.sessionManager(), sinope.message.messageAuthenticationKeyAnswer.command)
server.connect()
server.wait()


