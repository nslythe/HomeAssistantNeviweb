def bytesToString(bytesVar):
    s = ""
    for b in bytesVar:
        s += "%02x" % b
    return s

