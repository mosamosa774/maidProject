import urllib.request, json
from datetime import date
import time as ctime

def readJSON():
    f = open('dataset/user.json', 'r')
    user = json.load(f)
    return user

def updateJSON(JSON):
    f = open('dataset/user.json', 'w')
    f.write(json.dumps(JSON, ensure_ascii=False, indent=2))
 
def send_message(msg,APIKey):
    url = "https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY="
    url += APIKey
    method = "POST"
    user = readJSON()
    time = date.today().isoformat()+" "+ctime.ctime(ctime.time()).split(' ')[4]
    obj = {
        "language": "ja-JP",
        "botId": "Chatting",
        "appId": user['appid'],
        "voiceText": msg,
        "clientData":{
            "option":{
                "nickname":user['user']['name'],
                "nicknameY":user['user']['yomi']
            }
        },
        "appRecvTime" : user['last_time'],
        "appSendTime" : time
    }
    json_data = json.dumps(obj).encode("utf-8")
    headers = {"Content-Type" : "application/json;charset=UTF-8"}

    request = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
    res = json.loads(response_body)
    user['last_time'] = time
    updateJSON(user)
    return res['systemText']['utterance']
