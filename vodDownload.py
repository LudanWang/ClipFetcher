import requests
import urllib.request
import subprocess
import os

def GetM3U8(vod_id):
    url = "https://api.twitch.tv/api/vods/"+vod_id+"/access_token"
    headers = {
         "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
    }
    response = requests.get(url, headers=headers).json()
    token = response['token']
    sig = response['sig']

    m3u8url = "https://usher.twitch.tv/vod/"+vod_id+"?nauthsig="+sig+"&nauth="+token
    # query = "https://usher.ttvnw.net/vod/"+vod_id+".m3u8?player=twitchweb&nauthsig="+sig+"&nauth="+token+"&allow_audio_only=true&allow_source=true&type=any&p=123"
    query = "https://usher.ttvnw.net/vod/"+vod_id+".m3u8?player=twitchweb&nauthsig="+sig+"&nauth="+token+"&allow_source=true&type=any&p=123"
    response3 = urllib.request.urlopen(query)
    data = response3.read()  # a `bytes` object
    text = data.decode('utf-8')
    download_url = []
    for item in text.split("\n"):
        if "https:" in item:
            download_url.append(item.strip())
    # for res in download_url:
    #     print(res.split('/')[-2])
    return download_url

def FFMPEGDownload(vod_id, start, duration, highlight_id):
    vod_folder = r'./' + vod_id  #新增vod_id資料夾
    print(vod_folder)
    if not os.path.exists(vod_folder):
        os.makedirs(vod_folder)
    download_url = GetM3U8(vod_id)
    for i in range(len(start)):
        cmd = '/app/vendor/ffmpeg/ffmpeg -protocol_whitelist "file,http,https,tcp,tls" -y -ss '+ start[i] +' -i '+download_url[-3]+' -c copy -t '+ duration[i] +' '+vod_folder+'/'+ highlight_id + '_' + str(i) +'.mp4'
        subprocess.run(cmd)

def FFMPEGCombine(vod_id, clip_count, highlight_id):
    vod_folder = './' + vod_id
    cmd = '/app/vendor/ffmpeg/ffmpeg'
    for i in range(0,clip_count):
        cmd = cmd + ' -i ' + vod_folder + '/' + highlight_id + '_' + str(i) + ".mp4"
    cmd = cmd +" -vsync 2 -filter_complex concat=n=" + str(clip_count) + ":v=1:a=1 -y " + vod_folder + "/" + highlight_id + ".mp4"
    subprocess.run(cmd)

def FFMPEGDownloadFull(vod_id):
    vod_folder = r'./' + vod_id
    if not os.path.exists(vod_folder):
        os.makedirs(vod_folder)
    download_url = GetM3U8(vod_id)
    vodPath = 'C:\\Users\\yan\\Desktop\\'+vod_id
    mp4name = vod_id
    cmd='ffmpeg -protocol_whitelist "file,http,https,tcp,tls" -y -i '+ download_url[-3]+' -c copy '+vodPath+'\\'+mp4name+'.mp4'
    subprocess.run(cmd)
