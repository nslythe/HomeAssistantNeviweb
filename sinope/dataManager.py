import pickle
import os

class dataManager(object):
    def __init__(self):
        self.__filePath = ".sinope.dat"
        self.__data = None
        self.__load()

    def __save(self):
        f = open(self.__filePath, 'wb')
        pickle.dump(self.__data, f, 0)
        f.close()

    def __load(self):
        if os.path.exists(self.__filePath):
            f = open(self.__filePath, 'rb')
            self.__data = pickle.load(f)
            f.close()

        if self.__data == None:
            self.__data = {}

    def newValue(self, owner, name):
        key = self.__getKey(owner, name)
        if not key in self.__data:
            self.__data[key] = None
            self.__save()

    def removeValue(self, owner, name):
        key = self.__getKey(owner, name)
        self.__data.pop(key)
        self.__save()

    def setValue(self, owner, name, value):
        key = self.__getKey(owner, name)
        if not key in self.__data:
            raise Exception("Key not in values")
        self.__data[key] = value
        self.__save()

    def getValue(self, owner, name):
        key = self.__getKey(owner, name)
        if not key in self.__data:
            raise Exception("Key not in values")
        return self.__data[key]

    def getData(self):
        return self.__data

    def __getKey(self, owner, name):
        return type(owner).__name__ + "/" + name
