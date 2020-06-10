import json
import math
from time import strftime
from time import gmtime
import statistics

def frequencyAlgo(vod_id):#a秒內有b個留言
    file_name = './ChatHistory/' + str(vod_id) + ".json"
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

    mean = chat_count / vod_length #平均
    sd = statistics.pstdev(freqCount)#標準差
    freq4 = math.floor(mean + 4 * sd) #99.7%
    freq3 = math.floor(mean + 3 * sd) #95%

    freq3Time = []
    for i in range(len(freqCount)):
        if freqCount[i] >= freq3:
            freq3Time.append(i)
    freq4Time=[]
    for i in range(len(freqCount)):
        if freqCount[i] >= freq4:
            freq4Time.append(i)

#標準差3 95%
    freq3Start=[]
    freq3End=[]
    i=0
    while i < len(freq3Time)-2:
        if freq3Time[i]+7 > freq3Time[i+1]:
            freq3Start.append(freq3Time[i]-5)
            for j in range(i+1,len(freq3Time)-2):
                if freq3Time[j] + 7 <= freq3Time[j + 1]:
                    break
            i = j + 1
            freq3End.append(freq3Time[j] + 2)
        else:
            freq3Start.append(freq3Time[i] - 5)
            freq3End.append(freq3Time[i] + 2)
            i += 1

#找尋精華片段 開始及時間點
    tempStart=[]
    tempEnd=[]

    for i in range(len(freq3Start)-1):
        for j in range(len(freq4Time)-1):
            if(freq4Time[j] >= freq3Start[i]) and (freq4Time[j] <= freq3End[i]):
                if len(tempStart) == 0:
                    tempStart.append(freq3Start[i])
                    tempEnd.append(freq3End[i])
                else:
                    if freq3Start[i] != tempStart[-1]:
                        tempStart.append(freq3Start[i])
                        tempEnd.append(freq3End[i])

    tempduration=[]
    for i in range(len(tempStart)):
         tempduration.append(tempEnd[i] - tempStart[i]+1)

    maxfreq = max(freqCount)

    totalClipLength = 0
    while totalClipLength < 600: #找大於 > 10分鐘
        topFreqTime = []  # top頻率所在秒數
        topFreqClipIndex = []  # 前N高的頻率在 標準差方法所成clip中的index
        f=0 #為找出top頻率
        for i in range(len(freqCount)):
            if freqCount[i] >= maxfreq:
                topFreqTime.append(i)

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

        nTopFreqClipIndex = list(set(topFreqClipIndex))#set出來是tuple 多個n轉成list
        nTopFreqClipIndex.sort()

         #如果精華不夠長，將最大頻率減1，找>=小1聊天聊天頻率的精華
        for i in range(len(nTopFreqClipIndex)):
            totalClipLength += tempduration[nTopFreqClipIndex[i]]
        # print('vod_id', vod_id, '最大頻率', maxfreq, '精華時間', strftime("%H:%M:%S", gmtime(totalClipLength)))
        maxfreq -= 1

    #最後輸出 開始時間 及 影片長度
    start=[]
    duration=[]
    for i in range(len(nTopFreqClipIndex)):
        start.append(tempStart[nTopFreqClipIndex[i]])
        duration.append(tempduration[nTopFreqClipIndex[i]])
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