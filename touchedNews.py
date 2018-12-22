import json
from datetime import date

def checkThisNewsTouched(title,touchedNewsList,today,fileName):
    for i in touchedNewsList:
        if i['title'] == title:
            return True
    addTouchedNews(title,touchedNewsList,today,fileName)
    return False

def updateTouchedNewsList(touchedNewsList,today,fileName,days):
    found = False
    markList = []
    for i in touchedNewsList:
        old = i['date'].split("-")
        old = date(int(old[0]),int(old[1]),int(old[2]))
        diff = today - old
        if diff.days >= days:
            found = True
            markList.append(i['date'])
    if found:
        touchedNewsList = removeTouchedNews(touchedNewsList,markList,fileName)
    return touchedNewsList

def addTouchedNews(title,touchedNewsList,today,fileName):
    touchedNewsList.append({'title':title,'date':str(today)})
    writeTouchedNews(touchedNewsList,fileName)

def removeTouchedNews(touchedNewsList,markList,fileName):
    for i in markList:
        for j in touchedNewsList:
            if i == j['date']:
                touchedNewsList.remove(j)
                break
    writeTouchedNews(touchedNewsList,fileName)
    return touchedNewsList

def readTouchedNews(fileName):
    try:
        with open("dataset/"+fileName, "r") as f:
            data = f.read()
        touchedNewsList = json.loads(data)
    except:
        touchedNewsList = []
    return touchedNewsList

def writeTouchedNews(touchedNewsList,fileName):
    with open("dataset/"+fileName,mode='w') as f:
        f.write(json.dumps(touchedNewsList, ensure_ascii=False, indent=2))

