import requests
import json
import urllib.request
import BaseAlgorithm
import subprocess
import os

def getM3U8(vod_id):
    url = "https://api.twitch.tv/api/vods/"+vod_id+"/access_token"
    headers = {
         "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
    }
    response = requests.get(url, headers=headers).json()
    print(response)
    token=response['token']
    sig=response['sig']
    print(token)
    print(sig)
    m3u8url="https://usher.twitch.tv/vod/"+vod_id+"?nauthsig="+sig+"&nauth="+token
    u="https://usher.ttvnw.net/vod/"+vod_id+".m3u8?player=twitchweb&nauthsig="+sig+"&nauth="+token+"&allow_audio_only=true&allow_source=true&type=any&p=123"
    print(u)
    response3 = urllib.request.urlopen(u)
    data = response3.read()  # a `bytes` object
    text = data.decode('utf-8')
    output = []
    for item in text.split("\n"):
        if "https:" in item:
            output.append(item.strip())
    print(output)#url list
    print(type(output))
    return output

def ffmpegDownload(vod_id,timeStamp):
    newpath = r'C:\Users\yan\Desktop\\' + vod_id  #新增vod_id資料夾
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    downloadURL=getM3U8(vod_id)
    print(downloadURL[0])
    vodPath='C:\\Users\\yan\\Desktop\\'+vod_id
    mp4name=vod_id
    for i in range(len(timeStamp[0])):#len(timeStamp[0])
        cmd='ffmpeg -protocol_whitelist "file,http,https,tcp,tls" -y -ss '+ timeStamp[0][i]+' -i '+downloadURL[2]+' -c copy -t '+timeStamp[1][i]+' '+vodPath+'\\'+mp4name+'_'+ str(i) +'.mp4'
        print(cmd)
        subprocess.run(cmd)

def ffmpegCombine(vod_id,clipCount):
    vodPath = 'C:\\Users\\yan\\Desktop\\' + vod_id
    cmd = 'ffmpeg'
    for i in range(0,clipCount):
        cmd=cmd+' -i '+vodPath+'\\'+vod_id+'_'+str(i)+".mp4"
        print(cmd)
    cmd = cmd +" -filter_complex concat=n="+str(clipCount)+":v=1:a=1 -y "+vodPath+"\\"+vod_id+".mp4"
    subprocess.run(cmd)