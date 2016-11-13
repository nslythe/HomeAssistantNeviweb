import sinope.message

CRC_SIZE = 1
HEADER55 = 0x55
HEADER00 = 0x00
HEADER_SIZE = 2
SIZE_SIZE = 2
COMMAND_SIZE = 2

def create(commandRaw):
    """
    Create sinope.message.message from commandRaw.
        
    Parameters
    ----------
    commandRaw : bytes
        The command has read from the srteam (in raw format), it must be of length COMMAND_SIZE
        
    Returns
    -------
    message
        The message created or None if creation failed
    """
    msg = sinope.message.message("UnknownCommand")
    msg.setCommandRaw(commandRaw)

    for c in sinope.message.message.__subclasses__():
        if c.command == msg.getCommand() and type(msg) != c:
            obj = c()
            obj.clone(msg)
            return obj
    return msg


def read(stream):
    """
    Read one message from the stream
        
    Parameters
    ----------
    stream : iostream
        A stream with a read function like file.read
        
    Returns
    -------
    message
        Return a valid new message, if any error ocured while parsing an exception is raised
        
    """
    message = None

    # read and validate header
    header = stream.read(HEADER_SIZE)
    if header == None or header == "" or header[0] != HEADER55 or header[1] != HEADER00:
        raise Exception("Header not valid")

    # read and validate size
    size = stream.read(SIZE_SIZE)
    if size==None or size == "":
        raise Exception("Unable to read size")

    # read and validate command
    command = stream.read(COMMAND_SIZE)
    if command == None or command == "":
        raise Exception("Unable to read command")

    # read data
    data = stream.read(sinope.message.message.getSizeFromRawData(size) - COMMAND_SIZE)

    # read crc
    crc = stream.read(CRC_SIZE)

    message = sinope.messageCreator.create(command)

    message.setDataRaw(data)

    if message.getCrc() != crc:
        raise Exception("Message CRC does not match")

    return message

