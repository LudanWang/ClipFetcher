import requests
import json


class VOD():
    def __init__(self, vod_id, channel_id, game, cloud_id):
        self.vod_id=vod_id
        self.channel_id=channel_id
        self.game=game
        self.cloud_id=cloud_id

def getVodInformation(vod_id):
    url = "https://api.twitch.tv/kraken/videos/" + str(vod_id)
    headers = {
        "Accept": "application/vnd.twitchtv.v5+json",
        "Client-ID": "ildytfqanhzvdaprp96m5rkylap16k"
    }
    res = requests.get(url, headers=headers)
    vodInformation = res.json()
    streamerName=vodInformation['channel']['display_name']
    channel_id=vodInformation['channel']['_id']
    game=vodInformation['game']
    v=VOD(vod_id, channel_id, game, "http")

    url = "https://api.twitch.tv/kraken/videos/" + str(vod_id) + "/comments/?cursor"
    res = requests.get(url, headers=headers)
    commentJson=res.json()
    time=[]
    chat=[]
    for item in commentJson['comments']:
        time.append(item['content_offset_seconds'])
        chat.append(item['message']['body'])
    nextSection = url + "=" + commentJson['_next']

    while '_next' in commentJson:
        res = requests.get(nextSection, headers=headers)
        commentJson = res.json()
        for item in commentJson['comments']:
            time.append(item['content_offset_seconds'])
            chat.append(item['message']['body'])
        if '_next' in commentJson:
            nextSection = url + "=" + commentJson['_next']

    data={}
    data['comment']=[]
    for i in range(len(time)):
        data['comment'].append(
            {
                'time':time[i],
                'chat':chat[i]
            }
        )
    return

    fileName = vod_id + ".json"
    f = open(fileName, "w+", encoding="utf-8")
    f.write(json.dumps(data,ensure_ascii=False))
    f.close()

#554877888

#getVodInformation("569689535")
# t=BaseAlgorithm.frequencyAlgo("556617932",0)
# clipCount=len(t[0])
# ffmpegDownload("556617932",t)
# ffmpegCombine("556617932",clipCount)

#getDownloadURL("563696555")
#563696555 556617932 554877888 553397882 553337792 569689535
