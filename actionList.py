import voiceGenerator
import translateImg2Txt
import weather
import readRSS
import fileRead
from time import sleep
import asyncio
import random
import wiki
import qiita
import manageRSS
import capRoom
import re

sleepHour = 6
city_code = "070030" # 会津若松の都市コード

def massage_init():
    return 0,""

def randomGet(List):
    return List[random.randrange(len(List))]

async def Greeting(onVoice,hour,channel,client): # #1
    if(hour >= 5 and hour <= 10):
        sen = "おはようございます。"
    elif(hour >= 11 and hour <= 17):
        sen = "こんにちは。"
    else:
        sen = "こんばんは。"
    await client.send_message(channel,sen)
    if(onVoice):
        voiceGenerator.callVoice(sen)

async def CheckWheather(onVoice,channel,client): # #2
    date, fore_weather, min_temperature, max_temperature = weather.set_weather_info(weather.get_weather_info(city_code),0)
    sen = "今日の天気予報は"+str(fore_weather)+"となっています。"
    if(max_temperature != None):
        sen+= "最高気温は"+str(max_temperature)+"度ですね。"
    if(min_temperature != None):
        sen+= "最低気温は"+str(min_temperature)+"度ですね。"
    await client.send_message(channel,sen)
    if(onVoice):
        voiceGenerator.callVoice(sen)

async def CheckTemp(onVoice): # #3
    print("test3")

async def CheckTime(onVoice,day,time,channel,client): # #4
    sen = "今日は"+str(day.month)+"月"+str(day.day)+"日です。"
    if(time.hour >= 12):
        hour = "午後"+str(time.hour - 12)
    else:
        hour = "午前"+str(time.hour)
    sen += "今は、"+hour+"時、"+str(time.minute)+"分です。"
    await client.send_message(channel,sen)
    if(onVoice):
        voiceGenerator.callVoice(sen)

async def soliloquy(onVoice,channel,client): # #5
    List = fileRead.readSoliloquy()
    word = randomGet(List)
    print(word)
    await client.send_message(channel,word)
    if(onVoice):
        voiceGenerator.callVoice(word)
    
async def checkWiki(onVoice,word,channel,client):
    res = wiki.set_wiki_info(wiki.get_wiki_info(word))
    if(res != None):
        foundURL,body,nearArticle = res[0],res[2],res[3]
        sen = "wikiで記事を見つけました！URLは"+foundURL+"です。"
        await client.send_message(channel,sen)
        sen = "本文はこちらです。"+body
        await client.send_message(channel,sen)
        if(len(nearArticle) > 0):
            sen = "似ている記事も見つけてきました。\n"
            count=0
            for i in nearArticle:
                sen += "タイトル: "+i[0]+"、 url:"+i[1]+"\n"
                count+=1
                if(count == 15):
                    await client.send_message(channel,sen)
                    await asyncio.sleep(1)
                    count,sen = massage_init()
            if(count != 0):
                await client.send_message(channel,sen)
    else:
        await client.send_message(channel,"見つかりませんでした...")

async def checkQiita(onVoice,word,channel,client,num=10):
    if(num > 100):
        await client.send_message(channel,"数が多すぎです。少なくしてください。")
    else:
        res = qiita.set_qiita_info(qiita.get_qiita_info(num,word))
        if(res != None):
            if(len(res) > 0):
                sen = "Qiitaで記事を見つけました！\n"
                count=0
                for i in res:
                    sen+= "タイトル:"+i[0]+"\nURL:"+i[1]+"　　最終更新日:"+i[2]+"\n"
                    count+=1
                    if(count == 15):
                        await client.send_message(channel,sen)
                        await asyncio.sleep(1)
                        count,sen = massage_init()
                if(count != 0):
                    await client.send_message(channel,sen)
        else:
            await client.send_message(channel,"見つかりませんでした...")

async def checkNews(onVoice,channel,client): # 6
    import manageRSS
    await checkQiitaTrend(onVoice,channel,client)
    for i in manageRSS.readBookmarkedRSS():
        sen = i["Title"]+"から記事を集めてきました。\n"
        articles = readRSS.set_rss_info(readRSS.get_rss_info(i["RSS_URL"]))
        count=0
        for article in articles:
            sen += "タイトル:"+article[0]+"\nURL:"+article[1]+"\n"
            count+=1
            if(count == 15):
                await client.send_message(channel,sen)
                await asyncio.sleep(1)
                count,sen = massage_init()
        if(count != 0):
            await client.send_message(channel,sen)

async def checkQiitaTrend(onVoice,channel,client):
    res = qiita.get_TrendURL()
    if(res != None):
        sen = "Qiitaの三か月間のトレンドっぽい記事をいくつか報告します！\n"
        count=0
        for i in res:
            sen+= "タイトル:"+i[0]+"\nURL:"+i[1]+"　　最終更新日:"+i[2]+"\n"
            count+=1
            if(count == 15):
                await client.send_message(channel,sen)
                await asyncio.sleep(1)
                count,sen = massage_init()
        if(count != 0):
            await client.send_message(channel,sen)

async def help(onVoice,channel,client):
    sen = "コマンドの一覧は以下のようになってます\n"
    for i in fileRead.readCommand():
        sen += "説明: "+i[0]+"         コマンド: "+i[1]+"\n"
    await client.send_message(channel, sen)

async def cleanLog(onVoice,channel,client):
    clean_flag = True
    while (clean_flag):
        msgs = []
        async for msg in client.logs_from(channel, limit=98): #can only remove range[2-100]
            msgs.append(msg) 
        if len(msgs) > 1:
            await client.delete_messages(msgs)
            msgs.clear()
        else:
            clean_flag = False
            await client.send_message(channel, 'ログのお掃除が完了しました！疲れた...')
            if(onVoice):
                voiceGenerator.callVoice('ログのお掃除が完了しました！疲れた...')

async def addRSS(onVoice,msg,channel,client):
    sen = ""
    try:
        title,url = msg.split("\"")[1],msg.split("\"")[3]
        manageRSS.addBookmarkedRSS(manageRSS.readBookmarkedRSS(),title,url)
        sen = title+":"+url+" のRSSを追加しましたよ。"
    except:
        if((re.search("リスト", msg)) != None):
            sen = "ブックマークしたRSSの一覧は以下のようになってます\n"
            for i in manageRSS.readBookmarkedRSS():
                sen += "説明:" +i["Title"]+"　、URL: "+i["RSS_URL"]+"\n"
        else:
            sen = '入力ミスですね、おそらく。'
    await client.send_message(channel, sen)

async def searchWord(onVoice,msg,channel,client): 
    if (re.search("(w|W)iki", msg) != None):
        await checkWiki(onVoice,msg.split("\"")[1],channel,client)
    elif (re.search("(q|Q)iita", msg) != None):
        num = re.search(r'([0-9]+\.?[0-9]*)', msg)
        if(num != None):
            num = int(num.group())
        else:
            num = 50
        await checkQiita(onVoice,msg.split("\"")[1],channel,client,num)
    else:
        await checkWiki(onVoice,msg.split("\"")[1],channel,client)
        await checkQiita(onVoice,msg.split("\"")[1],channel,client)

async def CaptureRoom(onVoice,channel,client): 
    await client.send_message(channel, "ちょっと待ってね！")
    await client.send_file(channel, capRoom.takeCapture(),content="今はこんな感じです")

async def TranslateImg2Txt(onVoice,url,channel,client):
    await client.send_message(channel, "ちょっと待ってね！")
    filePlace = translateImg2Txt.translate(url)
    await client.send_file(channel, filePlace, content="やってみたよ！")

