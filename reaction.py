import re
import random
import voiceGenerator
import _request

async def talk(onVoice,msg,APIkey,channel,client):
    sen = _request.send_message(msg,APIkey)
    await client.send_message(channel,sen)
    if(onVoice):
        voiceGenerator.callVoice(sen)
