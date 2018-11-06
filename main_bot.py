# coding UTF-8
# ssh -R 52698:127.0.0.1:52698 pi@192.168.1.2

import asyncio
import voiceGenerator
import analyzeSentence
import fileRead
import datetime
import json
from time import sleep
import re
import os
import workInterface
os.chdir("/home/pi/maidProj/")
import fileinput
txt = ""
for line in fileinput.input():
    txt += line
tokens = json.loads(txt)

date = ["mon","tue","wed","thu","fri","sat","sun"]

BOT_TOKEN = tokens['AccountToken']

voiceGenerator.callVoice("起動しました。初期化を始めます...")

import discord
client = discord.Client()
    
def timeInit():
    d_today = datetime.date.today()
    return datetime.datetime.now().time(),d_today,date[(datetime.datetime.strptime(str(d_today),'%Y-%m-%d')).weekday()]

async def my_background_task():
    global now,d_today,c_date
    await client.wait_until_ready()
    now,d_today,c_date = timeInit()
    schedule_date = c_date
    task_sch,time_sch = fileRead.readSchedule(schedule_date)

    await asyncio.sleep(20)
    voiceGenerator.callVoice("初期化完了しました。よろしくお願いします！")

    while(1):
        if(schedule_date != c_date):
            schedule_date = c_date
            task_sch,time_sch = fileRead.readSchedule(schedule_date)            
        if(len(task_sch)!=0): 
            print(task_sch,time_sch)
            try:
                next_time = time_sch[0].split(":")
                if(int(next_time[0]) <= now.hour and int(next_time[1]) <= now.minute ):
                    task = task_sch.pop(0)
                    time_sch.pop(0)
                    if( (now.hour - int(next_time[0])) >= 3):
                    	continue
                    for act in task:
                    	print(act)
                    	await workInterface.callAction(True,act,None,d_today,now,tokens,None,client)
                    	await asyncio.sleep(1) 
            except:
            	import traceback
            	traceback.print_exc()
        await asyncio.sleep(60*10)
        now,d_today,c_date =timeInit()

@client.event
async def on_ready():
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')
    await client.send_message(discord.Object(id=tokens['General']),"ディスコードにログインしましたよ！")
    voiceGenerator.callVoice("ディスコードにログインしましたよ！")

@client.event
async def on_message(message):
    global now,d_today,c_date
    # BOTとメッセージの送り主が同じ人なら処理しない
    if client.user == message.author:
        return
    
    onVoice,cmdNO = analyzeSentence.analyze(message.content,commandList)
    await workInterface.callAction(onVoice,cmdNO,message.content,d_today,now,tokens,message.channel,client)
     
commandList = fileRead.readCommand()

now,d_today,c_date = timeInit()
client.loop.create_task(my_background_task())
client.run(BOT_TOKEN)
