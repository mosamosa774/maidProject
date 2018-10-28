import re
import random
import voiceGenerator

async def hearVoice(onVoice,msg,pre_react,reactList,channel,client):
    passAllCond = True
    for react in reactList:
        if( (re.search(react[0],msg)) != None):
            sen = randomGet(react[1])
            await client.send_message(channel,sen)
            if(onVoice):
                voiceGenerator.callVoice(sen)
            passAllCond = False

    if(passAllCond):
        sen = randomGet(pre_react)
        await client.send_message(channel,randomGet(sen))
        if(onVoice):
            voiceGenerator.callVoice(sen)

def randomGet(reactList):
    reacts = reactList.split("|")
    return reacts[random.randrange(len(reacts))]    
