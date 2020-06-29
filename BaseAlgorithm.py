from vodDownload import FFMPEGDownload,FFMPEGCombine
from YouTubeUpload import start_upload
from time import strftime
from time import gmtime
import modules.HighLight
import json
import statistics
import math


def frequencyAlgo(vod_id):#a秒內有b個留言
    file_name = './ChatHistory/' + vod_id + ".json"
    f = open(file_name, "r", encoding="utf-8")  # filename
    file_content_json = json.loads(f.read())
    title = file_content_json['title']
    channel_id = file_content_json['channel_id']
    vod_length = file_content_json['vod_length']
    streamerName = file_content_json['streamerName']
    game = file_content_json['game']

    chat_count = len(file_content_json['comment'])

    freqCount = [0] * int(file_content_json['comment'][-1]['time']+1)  #計算每一個時間點的時間頻率
    for i in range(len(file_content_json['comment'])):
        freqCount[int(file_content_json['comment'][i]['time'])] += 1
    # print(freqCount)
    mean = chat_count / vod_length  #平均
    sd = statistics.pstdev(freqCount) #標準差
    maxfreq = max(freqCount)
    freq3 = math.floor(mean + 3 * sd) #99.7%
    freq2 = math.floor(mean + 2 * sd) #95%
    # print('vod_id:',vod_id,'留言平均:',round(mean,2),'留言標準差:',round(sd,2),'3個留言標準差:',round(freq2,2),'4個留言標準差:',round(freq2+sd,2),'5個留言標準差:',round(freq2+2*sd,2),'max',max(freqCount))
    #聊天頻率大於等於2,3標準差符合秒數
    freq2Time = []
    for i in range(len(freqCount)):
        if freqCount[i] >= freq2:
            freq2Time.append(i)
    freq3Time=[]
    for i in range(len(freqCount)):
        if freqCount[i] >= freq3:
            freq3Time.append(i)

    #標準差2 95%
    freq2Start=[]
    freq2End=[]
    i=0
    while i < len(freq2Time)-2:
        if freq2Time[i]+7 > freq2Time[i+1]:
            freq2Start.append(freq2Time[i] - 7)
            for j in range(i+1,len(freq2Time)-2):
                if freq2Time[j] + 7 <= freq2Time[j + 1]:
                    break
            i = j + 1
            freq2End.append(freq2Time[j] + 2)
        else:
            freq2Start.append(freq2Time[i] - 7)
            freq2End.append(freq2Time[i] + 2)
            i += 1
    #找尋精華片段 開始及時間點
    tempStart=[]
    tempEnd=[]

    for i in range(len(freq2Start)-1):
        for j in range(len(freq3Time)-1):
            if(freq3Time[j] >= freq2Start[i]) and (freq3Time[j] <= freq2End[i]):
                if len(tempStart) == 0:
                    tempStart.append(freq2Start[i])
                    tempEnd.append(freq2End[i])
                else:
                    if freq2Start[i] != tempStart[-1]:
                        tempStart.append(freq2Start[i])
                        tempEnd.append(freq2End[i])

    tempduration=[]
    for i in range(len(tempStart)):
         tempduration.append(tempEnd[i] - tempStart[i]+1)

    totalClipLength = 0
    while totalClipLength < 600: #找大於 > 10分鐘
        totalClipLength = 0
        topFreqTime = []  # top頻率所在秒數
        topFreqClipIndex = []  # 前N高的頻率在 標準差方法所成clip中的index
        f = 0 #為找出top頻率
        for i in range(len(freqCount)):
            if freqCount[i] >= maxfreq:
                topFreqTime.append(i)
        # print('maxfreqcount',len(topFreqTime)) # >= max聊天頻率
        j=0
        while j < len(tempStart):
            if tempStart[j] <= topFreqTime[f] and tempEnd[j] >= topFreqTime[f]: #要找的最大頻率時間在標準差95%的精華片段中間
                topFreqClipIndex.append(j)
                f += 1
                j = 0
                if f == len(topFreqTime):
                    break
            else:
                j += 1
        # print('精華數:', len(tempStart),'選取包含最大頻率的片段數:',len(topFreqClipIndex))
        nTopFreqClipIndex = list(set(topFreqClipIndex))#set出來是tuple 多個n轉成list
        nTopFreqClipIndex.sort()

        #如果精華不夠長，將最大頻率減1，找>=小1聊天聊天頻率的精華
        for i in range(len(nTopFreqClipIndex)):
            totalClipLength += tempduration[nTopFreqClipIndex[i]]
        # print(totalClipLength)
        # print('vod_id', vod_id, '最大頻率', maxfreq, '精華時間', strftime("%H:%M:%S", gmtime(totalClipLength)))
        maxfreq -= 1
    #最後輸出 開始時間 及 影片長度
    start=[tempStart[nTopFreqClipIndex[i]] for i in range(len(nTopFreqClipIndex))]
    duration=[tempduration[nTopFreqClipIndex[i]] for i in range(len(nTopFreqClipIndex))]
    # print('top',nTopFreqClipIndex)

    for i in range(len(start)):
        start[i]=strftime("%H:%M:%S", gmtime(start[i]))
        duration[i]=strftime("%H:%M:%S", gmtime(duration[i]))

    data = {}
    data['title'] = title
    data['channel_id'] = channel_id
    data['streamerName'] = streamerName
    data['game'] = game
    data['start'] = start
    data['duration'] = duration
    return data

def run_ClipFetcher(data, vod_id, highlight_id):
    print('status: 4')
    FFMPEGDownload(str(vod_id), data['start'], data['duration'], str(highlight_id))
    print('status: 5')
    FFMPEGCombine(str(vod_id), len(data['start']), str(highlight_id))
    clip_file = './Vod/' + highlight_id + '.mp4'
    yt_title = highlight_id
    print('status: 6')
    modules.HighLight.update_highlight_youtube(highlight_id, start_upload(clip_file, yt_title))
    print('status: 11')