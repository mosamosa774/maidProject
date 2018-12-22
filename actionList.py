import voiceGenerator
import translateImg2Txt
import weather
import readRSS
import fileRead
import checkATS
from time import sleep
from datetime import date
import asyncio
import random
import wiki
import qiita
import manageRSS
import capRoom
import touchedNews
import re

sleepHour = 6
city_code = "070030" # 会津若松の都市コード

def massage_init():
    return 0,""

def randomGet(List):
    return List[random.randrange(len(List))]

async def sendMassage(onVoice,sen,channel,client):
    try:
        await client.send_message(channel,sen)
        if(onVoice):
            voiceGenerator.callVoice(sen)
    except:
        pass

async def sendFile(address,sen,channel,client):
    try:
        await client.send_file(channel, address, content=sen)
    except:
        pass

async def Greeting(onVoice,hour,channel,client): # #1
    if(hour >= 5 and hour <= 10):
        sen = "おはようございます。"
    elif(hour >= 11 and hour <= 17):
        sen = "こんにちは。"
    else:
        sen = "こんばんは。"
    await sendMassage(onVoice,sen,channel,client)

async def CheckWheather(onVoice,channel,client): # #2
    date, fore_weather, min_temperature, max_temperature = weather.set_weather_info(weather.get_weather_info(city_code),0)
    sen = "今日の天気予報は"+str(fore_weather)+"となっています。"
    if(max_temperature != None):
        sen+= "最高気温は"+str(max_temperature)+"度ですね。"
    if(min_temperature != None):
        sen+= "最低気温は"+str(min_temperature)+"度ですね。"
    await sendMassage(onVoice,sen,channel,client)

async def CheckTemp(onVoice): # #3
    print("test3")

async def CheckTime(onVoice,day,time,channel,client): # #4
    sen = "今日は"+str(day.month)+"月"+str(day.day)+"日です。"
    if(time.hour >= 12):
        hour = "午後"+str(time.hour - 12)
    else:
        hour = "午前"+str(time.hour)
    sen += "今は、"+hour+"時、"+str(time.minute)+"分です。"
    await sendMassage(onVoice,sen,channel,client)

async def soliloquy(onVoice,channel,client): # #5
    List = fileRead.readSoliloquy()
    word = randomGet(List)
    await sendMassage(onVoice,word,channel,client)
    
async def checkWiki(onVoice,word,channel,client):
    res = wiki.set_wiki_info(wiki.get_wiki_info(word))
    if(res != None):
        foundURL,body,nearArticle = res[0],res[2],res[3]
        sen = "wikiで記事を見つけました！URLは"+foundURL+"です。\n"
        sen = "本文はこちらです。"+body+"\n"
        await sendMassage(onVoice,sen,channel,client)
        if(len(nearArticle) > 0):
            sen = "似ている記事も見つけてきました。\n"
            count=0
            for i in nearArticle:
                sen += "タイトル: "+i[0]+"、 url:"+i[1]+"\n"
                count+=1
                if(count == 15):
                    await sendMassage(onVoice,sen,channel,client)
                    await asyncio.sleep(1)
                    count,sen = massage_init()
            if(count != 0):
                await sendMassage(onVoice,sen,channel,client)
    else:
        await sendMassage(onVoice,"見つかりませんでした...",channel,client)

async def checkQiita(onVoice,word,channel,client,num=10):
    if(num > 100):
        await sendMassage(onVoice,"数が多すぎです。少なくしてください。",channel,client)
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
                        await sendMassage(onVoice,sen,channel,client)
                        await asyncio.sleep(1)
                        count,sen = massage_init()
                if(count != 0):
                    await sendMassage(onVoice,sen,channel,client)
        else:
            await sendMassage(onVoice,"見つかりませんでした...",channel,client)

async def checkNews(onVoice,channel,client): # 6
    import manageRSS
    await checkQiitaTrend(onVoice,channel,client)
    tNL = touchedNews.readTouchedNews("touchedNewsList.json")
    for i in manageRSS.readBookmarkedRSS():
        sen = i["Title"]+"から記事を集めてきました。\n"
        articles = readRSS.set_rss_info(readRSS.get_rss_info(i["RSS_URL"]))
        count=0
        for article in articles:
            if(not touchedNews.checkThisNewsTouched(article[0],tNL,date.today(),"touchedNewsList.json")):
                sen += "タイトル:"+article[0]+"\nURL:"+article[1]+"\n"
                count+=1
                if(count == 15):
                    await sendMassage(onVoice,sen,channel,client)
                    await asyncio.sleep(1)
                    count,sen = massage_init()
        if(count != 0):
            await sendMassage(onVoice,sen,channel,client)

async def checkQiitaTrend(onVoice,channel,client):
    res = qiita.get_TrendURL()
    if(res != None):
        sen = "Qiitaの三か月間のトレンドっぽい記事をいくつか報告します！\n"
        count=0
        tNL = touchedNews.readTouchedNews("touchedNewsList.json")
        tNL = touchedNews.updateTouchedNewsList(tNL,date.today(),"touchedNewsList.json",7)
        for i in res:
            if(not touchedNews.checkThisNewsTouched(i[0],tNL,date.today(),"touchedNewsList.json")):
                sen+= "タイトル:"+i[0]+"\nURL:"+i[1]+"　　最終更新日:"+i[2]+"\n"
                count+=1
                if(count == 15):
                    await sendMassage(onVoice,sen,channel,client)
                    await asyncio.sleep(1)
                    count,sen = massage_init()
        if(count != 0):
            await sendMassage(onVoice,sen,channel,client)

async def checkAmazonTimeSale(onVoice,mainChannel,saleChannel,client): # 7
    res = checkATS.analyze_Description(checkATS.get_info_ATS())
    if res == None:
        return        
    tNL = touchedNews.readTouchedNews("touchedSaleList.json")
    tNL = touchedNews.updateTouchedNewsList(tNL,date.today(),"touchedSaleList.json",30)
    count,sen = massage_init()
    current_category = ""
    for i in res:
        if(not touchedNews.checkThisNewsTouched(i[2],tNL,date.today(),"touchedSaleList.json")):
            if not current_category == i[1]:
                sen += "日時: "+i[0]+"\nカテゴリー: "+i[1]+"\n商品: "+i[2]+"\nリンク: "+i[3]+"\n"
            else:
                sen += "商品: "+i[2]+"\nリンク: "+i[3]+"\n"
            current_category = i[1]
            count+=1
            if(count == 10):
                await sendMassage(onVoice,sen,saleChannel,client)
                await asyncio.sleep(1)
                count,sen = massage_init()
    if count > 0:
        await sendMassage(onVoice,sen,saleChannel,client)
    await sendMassage(onVoice,"終わったよ！",mainChannel,client)

async def help(onVoice,channel,client):
    sen = "コマンドの一覧は以下のようになってます\n"
    for i in fileRead.readCommand():
        sen += "説明: "+i[0]+"         コマンド: "+i[1]+"\n"
    await sendMassage(onVoice,sen,channel,client)

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
            await sendMassage(onVoice,'ログのお掃除が完了しました！疲れた...',channel,client)

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
    await sendMassage(onVoice,sen,channel,client)

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
    await sendMassage(onVoice,"ちょっと待ってね！",channel,client)
    await sendFile(capRoom.takeCapture(),"今はこんな感じです",channel,client)

async def TranslateImg2Txt(onVoice,url,channel,client):
    await sendMassage(onVoice,"ちょっと待ってね！",channel,client)
    filePlace = translateImg2Txt.translate(url)
    await sendFile(filePlace,"やってみたよ！",channel,client)

