import logging
import time
import signal
import sys

import sinope.server
import sinope.message



logger = logging.getLogger('sinope.server')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

server = sinope.server.server("10.1.0.152", 4550)
message = sinope.message.messageAuthenticationKey(sys.argv[1])
server.connect()
server.sendMessage(message)

time.sleep(350)

server.close()
server.wait()


