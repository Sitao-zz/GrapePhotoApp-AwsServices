def getResultSingle(obj):
    array = []
    array.append(obj)
    result = {
        "success":True,
        "result":array,
        "error":None
    }
    return result

def getResultMultiple():
    result = {
        "success":True,
        "result":obj,
        "error":None
    }
    return result

def getResultError(msg):
    result = {
      "success":False,
      "result":None,
      "error":msg
    }
    return result
