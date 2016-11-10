import logging
import time
import signal
import sys

import sinope.server
import sinope.message
import sinope.sessionManager



logger = logging.getLogger('sinope.server')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

server = sinope.server.server("10.1.0.152", 4550)

server.addMessageHandler(sinope.sessionManager.sessionManager(), sinope.message.messageAuthenticationKeyAnswer.command)

message = sinope.message.messageAuthenticationKey()
message.setKey(sys.argv[1])
server.connect()
server.sendMessage(message)
server.wait()


