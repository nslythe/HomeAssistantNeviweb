import sinope.applicationData

def create(rawData):
    """
    """
    appData = sinope.applicationData.applicationData("UnknownApplicationData")
    appData.setDataRaw(0, rawData)

    for c in sinope.applicationData.applicationData.__subclasses__():
        if c.dataId == appData.getDataId():
            obj = c()
            obj.clone(appData)
            return obj
    return appData
