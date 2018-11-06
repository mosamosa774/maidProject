import json

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