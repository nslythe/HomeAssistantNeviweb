

class applicationData(object):
    def __init__(self, name):
        self.__name = name
        self.size = 0
        self.data = bytearray(self.size)
        pass

class outdoorTemperature(applicationData):
    name = "OutdoorTemperature"

    def __init__(self):
        super(outdoorTemperature, self).__init__(outdoorTemperature.name)

