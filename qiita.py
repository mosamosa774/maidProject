#encoding:utf-8
import urllib.request, urllib.error,sys
from urllib.parse import quote
import json
import datetime

URL="https://qiita.com/api/v2/items?page=1&per_page={0}&query=tags={1}%20HTTP/1.1"
TrendURL="https://qiita.com/api/v2/items?page=1&per_page=50&query=created%3A%3E{0}+stocks%3A%3E10%20HTTP/1.1"

#url = test_URL.format('2018-10-15')
#print(url)
#html = urllib.request.urlopen(url)
#html_json = json.loads(html.read().decode('utf-8',errors='ignore'))
#articles = []
#for i in html_json:
#    print(i['title'],i['likes_count'],i['created_at'])

def get_qiita_info(Num,KeyWord):
    try:
        url = URL.format(Num,quote(KeyWord))
        html = urllib.request.urlopen(url)
        html_json = json.loads(html.read().decode('utf-8',errors='ignore'))
        return html_json
    except Exception as e:
        print ("Exception Error: ", e)
        return None

def set_qiita_info(html_json):
    if(html_json == None):
        return None
    try:
        articles = []
        for i in html_json:
            articles.append( (i['title'],i['url'],i['updated_at'].split("T")[0]))
        return articles
    except TypeError:
        # temperature data is None etc...
        return None

def get_TrendURL():
    duration = str(datetime.date.today())
    duration = duration.split("-")
    duration = duration[0]+"-"+str(int(duration[1])-3)+"-"+duration[2]
    try:
        url = TrendURL.format(duration)
        html = urllib.request.urlopen(url)
        html_json = json.loads(html.read().decode('utf-8',errors='ignore'))
        articles = []
        for i in html_json:
            articles.append( (i['title'],i['url'],i['updated_at'].split("T")[0]) ) 
        return articles
    except Exception as e:
        print ("Exception Error: ", e)
        return None
