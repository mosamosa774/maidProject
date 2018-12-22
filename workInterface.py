# coding UTF-8
import actionList
import manageRSS
import reaction
import discord

async def callAction(onVoice,actNo,msg,today,now,tokens,channel,client):
    DocomoAPIKey = tokens['DocomoAPIKey']
    if(channel != None):
        mainChannel = channel
    else:
        mainChannel = discord.Object(id=tokens['General'])
    newsChannel = discord.Object(id=tokens['News'])
    saleChannel = discord.Object(id=tokens['Sale'])
    if(actNo == "#1"):
        await actionList.Greeting(onVoice,now.hour,mainChannel,client)
    elif(actNo == "#2"):
        await actionList.CheckWheather(onVoice,mainChannel,client)
    elif(actNo == "#3"):
        await actionList.CheckTemp(onVoice)
    elif(actNo == "#4"):
        await actionList.CheckTime(onVoice,today,now,mainChannel,client)
    elif(actNo == "#5"):
        await actionList.soliloquy(onVoice,mainChannel,client)
    elif(actNo == "#6"):
        await actionList.checkNews(False,newsChannel,client)
    elif(actNo == "#7"):
        await actionList.checkAmazonTimeSale(False,mainChannel,saleChannel,client)
    elif(actNo == "#1000"):
        await actionList.searchWord(False,msg,channel,client)
    elif(actNo == "#1001"):
        await actionList.addRSS(onVoice,msg,channel,client)
    elif(actNo == "#1002"):
        await actionList.help(onVoice,channel,client)
    elif(actNo == "#1003"):
        await actionList.checkQiitaTrend(False,channel,client)
    elif(actNo == "#1004"):
        await actionList.cleanLog(onVoice,channel,client)
    elif(actNo == "#1005"):
        await actionList.CaptureRoom(onVoice,channel,client)
    elif(actNo == "#1006"):
        await actionList.TranslateImg2Txt(onVoice,msg,channel,client)
    elif(actNo == "#4000"):
        await reaction.talk(onVoice,msg,DocomoAPIKey,channel,client)