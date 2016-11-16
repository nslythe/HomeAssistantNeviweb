import sinope.applicationData

def create(data):
    """
    """
    appData = sinope.applicationData.applicationData("UnknownApplicationData")
    appData.setDataRaw(0, data)

    for c in sinope.applicationData.applicationData.__subclasses__():
        if c.dataId == appData.getDataId():
            obj = c()
            obj.clone(appData)
            return obj
    return appData
