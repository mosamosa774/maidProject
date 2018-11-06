import re

def analyze(msg,commandList):
    if(re.search("\$|＄", msg) != None):
        onVoice = True
    else:
        onVoice = False

    for i in commandList:
        if(re.search(i[1], msg) != None):
            return onVoice,i[2]
    return onVoice,"#4000"