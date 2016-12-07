

class StreamMoc:
    def __init__(self, data):
        self.data = data
        self.pt = 0

    def read(self, size):
        if self.pt + size > len(self.data):
            return ""
        returnValue = self.data[self.pt : self.pt + size]
        self.pt += size
        return bytes(returnValue)

