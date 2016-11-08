import sinope.server
import sinope.message

message = sinope.message.messagePing()

server = sinope.server.server("10.1.0.152", 4550)
server.connect()
server.sendMessage(message)
#server.close()
