#coding:utf-8
import urllib.request, urllib.error,sys
from urllib.parse import quote
#install xmltodict
import xmltodict
import json

def get_rss_info(URL):
    try:
        html = urllib.request.urlopen(URL)
        xml = html.read().decode('utf-8')
        dict = xmltodict.parse(xml)
        res = json.loads(json.dumps(dict))
        return res
    except Exception as e:
        print ("Exception Error: ", e)
        return None

def set_rss_info(rss_json):
    if(rss_json == None):
        return None
    try:
        articles = []
        try:
            rss_json['rdf:RDF']['@xmlns']
            articles = readRSS_ver1_0(rss_json,articles)
        except:
            articles = readRSS_ver2_0(rss_json,articles)
    except TypeError as e:
        print ("TypeError: ", e)
        pass
    return articles

def readRSS_ver1_0(rss_json,articles):
    rss = rss_json['rdf:RDF']['item']
    for i in rss:
        articles.append( (i['title'],i['link']) )
    return articles

def readRSS_ver2_0(rss_json,articles):
    rss = rss_json['rss']['channel']['item']
    for i in rss:
        articles.append( (i['title'],i['link']) )
    return articles
