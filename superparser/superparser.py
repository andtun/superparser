import json
import requests


def parse_mayak():
    #f = open("parsed.html", 'w', encoding="utf-8")
    a = requests.get("http://www.mayak-agent.ru/").text     # get page code
    #f.write(a)
    #f.close()

    # find var containing json with all models
    a = a[a.find("var publicModel = "):a.find("var googleAnalytics = ")]
    a = a[a.find("{"):a.rfind(";")]

    # getting info
    a = json.loads(a)
    a = a['pageList']['pages']

    returndic = {}

    # filling returndic
    for person in a:
        # get personInfo
        addr = "https://static.wixstatic.com/sites/" + person['pageJsonFileName'] + ".z?v=0"
        personInfo = json.loads(requests.get(addr).text)
        personInfo = personInfo['data']['document_data']
        k = person['title']
        returndic[k] = {"text": [], "imgurl": [], "vidurl": []} # init returndic for the person

        # filling info for the person
        for item in personInfo.values():
            if item['type'] == "StyledText":
                returndic[k]['text'].append(item['text'])
                #print("found text for", k)
                #print(returndic[k]['text'])
            elif item['type'] == "Image":
                returndic[k]['imgurl'].append("https://static.wixstatic.com/media/"+item['uri'])
            elif item['type'] == "Video":
                returndic[k]['vidurl'].append("https://www.youtube.com/watch?v="+item['videoId'])
            print("an item processed!", k)

    return returndic



#f = open('ans.json', 'w', encoding="utf-8")
#f.write(str(parse_mayak()))
#f.close()
        
