#encoding:utf-8
import urllib.request, urllib.error,sys
from urllib.parse import quote
import json

URL="http://wikipedia.simpleapi.net/api?keyword=%s&output=json"

def get_wiki_info(KeyWord):
    try:
        url = URL % quote(KeyWord)
        html = urllib.request.urlopen(url)
        html_json = json.loads(html.read().decode('utf-8',errors='ignore'))
        return html_json
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)
        return None

def set_wiki_info(wiki_json):
    if(wiki_json == None):
        return None
    try:
        foundURL = wiki_json[0]['url']
        title = wiki_json[0]['title']
        body = wiki_json[0]['body']
        nearArticle = []
        for i in range(len(wiki_json)):
            if(wiki_json[i]['title'] == title):
                continue
            nearArticle.append( (wiki_json[i]['title'],wiki_json[i]['url']) )
    except TypeError:
        # temperature data is None etc...
        pass  
        print("error")
    return foundURL,title,body,nearArticle
