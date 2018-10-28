# coding UTF-8
# ssh -R 52698:127.0.0.1:52698 pi@192.168.1.7

import asyncio
import voiceGenerator
import actionList
import reaction
import datetime
import json
from time import sleep
import re
import os
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
mainChannel = discord.Object(id=tokens['General'])
newsChannel = discord.Object(id=tokens['News'])
def readSchedule(date):
    task_list = []
    time_list = []
    with open("schedule/schedule"+date+".txt", "r") as f:
        data = f.read()
    data = data.split("\n") 
    for i in data:
        try:
            task,time = i.split(";")
            task = task.split(",")
            task_list.append(task)
            time_list.append(time)
        except:
            continue
    return task_list,time_list

def readCommand():
    commandName = []
    commandList = []
    with open("dataset/command.txt", "r") as f:
        data = f.read()
    data = data.split("\n") 
    for i in data:
        description,command = i.split(",")
        commandName.append(description)
        commandList.append( (description,command) )
    return commandName,commandList

def readReaction():
    reactList = []
    with open("dataset/reaction.txt", "r") as f:
        data = f.read()
    data = data.split("\n") 
    for i in data:
        cond,sentence = i.split(",")
        if(cond == '0'):
            pre_react = sentence
        else:
            reactList.append( (cond,sentence) )
    return pre_react,reactList

def readSoliloquy():
    with open("dataset/soliloquy.txt", "r") as f:
        data = f.read()
    data = data.split("\n") 
    return data

def readBookmarkedRSS():
    f = open('dataset/bookmarkRSS.json', 'r')
    rss_dict = json.load(f)
    return rss_dict
    
def addBookmarkedRSS(rss_dict,description,URL):
    for i in rss_dict:
        if(i["RSS_URL"] == URL):
            print(i["Title"])
            return
    f = open("dataset/bookmarkRSS.json", "w")
    rss_dict.append({"Title":description,"RSS_URL":URL})
    f.write(json.dumps(rss_dict, ensure_ascii=False, indent=2))


async def callAction(act,d_today,now,mainChannel,newsChannel,client):
    if(act == "#1"):
        await actionList.Greeting(True,now.hour,mainChannel,client)
    elif(act == "#2"):
        await actionList.Sleep(True,now.hour,mainChannel,client)
    elif(act == "#3"):
        await actionList.CheckWheather(True,mainChannel,client)
    elif(act == "#4"):
        await actionList.CheckTemp(True)
    elif(act == "#5"):
        await actionList.CheckTime(True,d_today,now,mainChannel,client)
    elif(act == "#6"):
        await actionList.EatMeal(True,now.hour,mainChannel,client)
    elif(act == "#7"):
        await actionList.soliloquy(True,soliloquy,mainChannel,client)
    elif(act == "#8"):
        await actionList.checkNews(True,newsChannel,client,bookmarkedRSS)

def initDataFile():
    global soliloquy
    global pre_react,reactList
    global bookmarkedRSS
    soliloquy = readSoliloquy()
    pre_react,reactList = readReaction()
    bookmarkedRSS = readBookmarkedRSS()
    
def timeInit():
    d_today = datetime.date.today()
    return datetime.datetime.now().time(),d_today,date[(datetime.datetime.strptime(str(d_today),'%Y-%m-%d')).weekday()]

async def my_background_task(mainChannel,newsChannel):
    global now,d_today,c_date
    await client.wait_until_ready()
    now,d_today,c_date =timeInit()
    schedule_date = c_date
    task_sch,time_sch = readSchedule(schedule_date)

    await asyncio.sleep(20)
    voiceGenerator.callVoice("初期化完了しました。よろしくお願いします！")

    while(1):
        if(schedule_date != c_date):
            schedule_date = c_date
            initDataFile()
            task_sch,time_sch = readSchedule(schedule_date)            
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
                    await callAction(act,d_today,now,mainChannel,newsChannel,client)
                    await asyncio.sleep(1) 
        except:
            import traceback
            traceback.print_exc()
        await asyncio.sleep(60*10)
        now,d_today,c_date =timeInit()
    
def find_Command(str):
    for i in commandList:
        if (i[0] == str):
            return i[1]

@client.event
async def on_ready():
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')
    await client.send_message(mainChannel,"ディスコードにログインしましたよ！")
    voiceGenerator.callVoice("ディスコードにログインしましたよ！")

@client.event
async def on_message(message):
    global now,d_today,c_date
    # BOTとメッセージの送り主が同じ人なら処理しない
    if client.user == message.author:
        return

    if message.content.find('＄') > -1:
        onVoice = True
    else:
        onVoice = False
    
    if (re.search(find_Command(commandName[0]), message.content) != None):
        if (re.search("(w|W)iki", message.content) != None):
            await actionList.checkWiki(onVoice,message.content.split("\"")[1],message.channel,client)
        elif (re.search("(q|Q)iita", message.content) != None):
            num = re.search(r'([0-9]+\.?[0-9]*)', message.content)
            if(num != None):
                num = int(num.group())
            else:
                num = 50
            await actionList.checkQiita(onVoice,message.content.split("\"")[1],message.channel,client,num)
        else:
            await actionList.checkWiki(onVoice,message.content.split("\"")[1],message.channel,client)
            await actionList.checkQiita(onVoice,message.content.split("\"")[1],message.channel,client)
    elif (re.search(find_Command(commandName[1]), message.content) != None):
        sen = message.content
        try:
            title,url = sen.split("\"")[1],sen.split("\"")[3]
            addBookmarkedRSS(bookmarkedRSS,title,url)
            initDataFile()
            sen = title+":"+url+" のRSSを追加しましたよ。"
        except:
            if((re.search("リスト", sen)) != None):
                sen = "ブックマークしたRSSの一覧は以下のようになってます\n"
                for i in bookmarkedRSS:
                    sen += "説明:" +i["Title"]+"　、URL: "+i["RSS_URL"]+"\n"
            else:
                sen = '入力ミスですね、おそらく。'
        await client.send_message(message.channel, sen)
    elif (re.search(find_Command(commandName[2]), message.content) != None):
        await actionList.Greeting(onVoice,now.hour,message.channel,client)
    elif (re.search(find_Command(commandName[3]), message.content) != None):
        await client.send_message(message.channel, 'わかりました。')
        await actionList.Sleep(onVoice,now.hour,message.channel,client)
    elif (re.search(find_Command(commandName[4]), message.content) != None):
        await actionList.CheckWheather(onVoice,message.channel,client)
    elif (re.search(find_Command(commandName[5]), message.content) != None):
        await actionList.EatMeal(onVoice,now.hour,message.channel,client)
    elif (re.search(find_Command(commandName[6]), message.content) != None):
        await client.send_message(message.channel, '無理です...')
    elif (re.search(find_Command(commandName[7]), message.content) != None):
        sen = "コマンドの一覧は以下のようになってます\n"
        for i in commandList:
            sen += "説明: "+i[0]+"　、コマンド: "+i[1]+"\n"
        await client.send_message(message.channel, sen)
    elif (re.search(find_Command(commandName[8]), message.content) != None):
        await actionList.checkQiitaTrend(onVoice,message.channel,client)
    elif (re.search(find_Command(commandName[9]), message.content) != None):
        clean_flag = True
        while (clean_flag):
            msgs = []
            async for msg in client.logs_from(message.channel, limit=98): #can only remove range[2-100]
                msgs.append(msg) 
            if len(msgs) > 1:
                await client.delete_messages(msgs)
                msgs.clear()
            else:
                clean_flag = False
                await client.send_message(message.channel, 'ログのお掃除が完了しました！疲れた...')
                if(onVoice):
                    voiceGenerator.callVoice('ログのお掃除が完了しました！疲れた...')
    else:
        await reaction.hearVoice(onVoice,message.content,pre_react,reactList,message.channel,client)

commandName,commandList = readCommand()
pre_react,reactList = readReaction()
soliloquy = readSoliloquy()
bookmarkedRSS = readBookmarkedRSS()

now,d_today,c_date = timeInit()
client.loop.create_task(my_background_task(mainChannel,newsChannel))
client.run(BOT_TOKEN)
