import voiceGenerator
import weather
import readRSS
from time import sleep
import asyncio
import random
import wiki
import qiita

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

async def Sleep(onVoice,hour,channel,client): # #2
    hour2 = hour + sleepHour
    if(hour2 > 24):
        hour2-=24
    sen = "今は"+str(hour)+"時ですね。私は寝ます。おやすみなさい。私は"+str(hour2)+"時に起きます。"
    await client.send_message(channel,sen)
    if(onVoice):
        voiceGenerator.callVoice(sen)
    await asyncio.sleep(60*60*sleepHour)
    sen = "目が覚めました。今..."+str(hour2)+"時ですね。"
    await client.send_message(channel,sen)
    if(onVoice):
        voiceGenerator.callVoice(sen)

async def CheckWheather(onVoice,channel,client): # #3
    date, fore_weather, min_temperature, max_temperature = weather.set_weather_info(weather.get_weather_info(city_code),0)
    sen = "今日の天気予報は"+str(fore_weather)+"となっています。"
    if(max_temperature != None):
        sen+= "最高気温は"+str(max_temperature)+"度ですね。"
    if(min_temperature != None):
        sen+= "最低気温は"+str(min_temperature)+"度ですね。"
    await client.send_message(channel,sen)
    if(onVoice):
        voiceGenerator.callVoice(sen)

async def CheckTemp(onVoice): # #4
    print("test3")

async def CheckTime(onVoice,day,time,channel,client): # #5
    sen = "今日は"+str(day.month)+"月"+str(day.day)+"日です。"
    if(time.hour >= 12):
        hour = "午後"+str(time.hour - 12)
    else:
        hour = "午前"+str(time.hour)
    sen += "今は、"+hour+"時、"+str(time.minute)+"分です。"
    if(onVoice):
        voiceGenerator.callVoice(sen)

async def EatMeal(onVoice,hour,channel,client): # #6
    if(hour >= 5 and hour <= 10):
        sen = "朝ごはんですね！いただきます！"
    elif(hour >= 11 and hour <= 17):
        sen = "ランチタイムですね！いただきます!"
    else:
        sen = "晩ご飯ですよ。厳かに食べます。"
    await client.send_message(channel,sen)
    if(onVoice):
        voiceGenerator.callVoice(sen)

async def soliloquy(onVoice,List,channel,client): # #7
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
                    sen+= "タイトル:"+i[0]+", URL:"+i[1]+", 最終更新日:"+i[2]+"\n"
                    count+=1
                    if(count == 15):
                        await client.send_message(channel,sen)
                        await asyncio.sleep(1)
                        count,sen = massage_init()
                if(count != 0):
                    await client.send_message(channel,sen)
        else:
            await client.send_message(channel,"見つかりませんでした...")

async def checkNews(onVoice,channel,client,RSSDetails): # 8
    await checkQiitaTrend(onVoice,channel,client)
    for i in RSSDetails:
        sen = i["Title"]+"から記事を集めてきました。\n"
        articles = readRSS.set_rss_info(readRSS.get_rss_info(i["RSS_URL"]))
        count=0
        for article in articles:
            sen += "タイトル:"+article[0]+", URL:"+article[1]+"\n"
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
            sen+= "タイトル:"+i[0]+", URL:"+i[1]+", 最終更新日:"+i[2]+"\n"
            count+=1
            if(count == 15):
                await client.send_message(channel,sen)
                await asyncio.sleep(1)
                count,sen = massage_init()
        if(count != 0):
            await client.send_message(channel,sen)
