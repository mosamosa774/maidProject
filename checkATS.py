#coding:utf-8
import urllib.request, urllib.error,sys
from urllib.parse import quote
import xmltodict #install xmltodict
import json

url = "http://yapi.ta2o.net/maseli/index.rss"

def get_info_ATS():
    try:
        html = urllib.request.urlopen(url)
        xml = html.read().decode('utf-8')
        dict = xmltodict.parse(xml)
        res = json.loads(json.dumps(dict))
        items = []
        try:
            res['rdf:RDF']['@xmlns']
            items = readRSS_ver1_0(res,items)
        except:
            items = readRSS_ver2_0(res,items)
        return items
    except Exception as e:
        print ("Exception Error: ", e)
        return None

def analyze_Description(items):
    if items == None:
        return
    body = []
    for i in items:
        tmp = i[1].split("<li>")
        for j in tmp[1:len(tmp)]:
            _tmp = j.split(": ")
            category = _tmp[0]
            _tmp = _tmp[1].split(" href=\"")[1].split("\">")
            link = _tmp[0]
            name = _tmp[1].split("</a>")[0]
            body.append( (i[0],category,name,link) )
    return body        

def readRSS_ver1_0(rss_json,items):
    rss = rss_json['rdf:RDF']['item']
    for i in rss:
        items.append( (i['title'],i['description']) )
    return items

def readRSS_ver2_0(rss_json,items):
    rss = rss_json['rss']['channel']['item']
    for i in rss:
        items.append( (i['title'],i['description']) )
    return items