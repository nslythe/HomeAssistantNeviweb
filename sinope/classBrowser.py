

def getSubClassCommand(c, attrname, command):
    returnClass = None
    for subc in c.__subclasses__():
        if hasattr(subc, attrname) and getattr(subc, attrname) == command:
            returnClass = subc
            break
        else:
            returnClass = getSubClassCommand(subc, attrname, command)
            if returnClass != None:
                break
    return returnClass

