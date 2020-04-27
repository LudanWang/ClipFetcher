import json
from time import strftime
from time import gmtime
import statistics

def frequencyAlgo(vod_id):#a秒內有b個留言
    filename=vod_id+".json"
    f = open(filename, "r", encoding="utf-8")  # filename
    y = json.loads(f.read())

    # 計算每一個時間點的留言頻率
    freqCount=[0]*int(y['comment'][-1]['time']+1)
    print(y['comment'][-1]['time'])
    print(freqCount)
    for i in range(len(y['comment'])):
        freqCount[int(y['comment'][i]['time'])]+=1

    mean=statistics.mean(freqCount)#平均
    sd=statistics.pstdev(freqCount)#標準差
    freq997=mean+3*sd #99.7%
    freq95=mean+2*sd #95%

    maxfreq=[]
    for i in range(len(freqCount)):
        if freqCount[i] == max(freqCount):
            maxfreq.append(i)
    print(',',maxfreq)
    print(len(maxfreq))

    maxStart=[]
    maxEnd=[]
    i=0
    while i < len(maxfreq)-2: #數到倒數第三個
        if maxfreq[i] + 15 > maxfreq[i+1]:
            maxStart.append(maxfreq[i]-10)
            for j in range(i+1,len(maxfreq)-1):
                if maxfreq[j]+15<=maxfreq[j+1]:
                    break
            maxEnd.append(maxfreq[j] + 5)
            i = j +1
        else:
            maxStart.append(maxfreq[i]-10)
            maxEnd.append(maxfreq[i]+5)
            i+=1
    print('maxS',maxStart)
    print('maxE',maxEnd)
    print(len(maxStart))

    durationMax=[]
    for i in range(len(maxStart)):
        durationMax.append(maxEnd[i]-maxStart[i]+1)
    print('d,',durationMax)
    s=0
    for i in durationMax:
        s+=i
    print(s)


    #各頻率符合的秒數
    #常態分佈大於兩個標準差的時間點
    freq95Time=[]
    for i in range(len(freqCount)):
        if freqCount[i]>=freq95:
            freq95Time.append(i)
    # 常態分佈大於三個標準差的時間點
    freq997Time=[]
    for i in range(len(freqCount)):
        if freqCount[i]>=freq997:
            freq997Time.append(i)

    freq997Start=[]
    freq997End=[]
    i=0
    while i <= len(freq997Time)-2: #數到倒數第三個
        if freq997Time[i]  > freq997Time[i+1]:
            freq997Start.append(freq997Time[i]-7)
            for j in range(i+1,len(freq997Time)-1):
                if freq997Time[j]<=freq997Time[j+1]:
                    break
            freq997End.append(freq997Time[j]  - 7)
            i = j +1
        else:
            freq997Start.append(freq997Time[i] - 7)
            freq997End.append(freq997Time[i]  - 7)
            i+=1
    print(freq997Start)
    print(freq997End)

    freq95Start=[]
    freq95End=[]
    i=0
    while i<len(freq95Time)-2:
        if freq95Time[i]+15>freq95Time[i+1]:
            freq95Start.append(freq95Time[i]-10)
            for j in range(i+1,len(freq95Time)-2):
                if freq95Time[j]+15<=freq95Time[j+1]:
                    break
            i = j + 1
            freq95End.append(freq95Time[j] + 5)
        else:
            freq95Start.append(freq95Time[i]-10)
            freq95End.append(freq95Time[i]+5)
            i+=1
    print('95start',freq95Start)
    print(freq95End)

    Start=[]
    End=[]
    for i in range(len(freq95Start)-1):#外 有在裡面就記下來
        for j in range(len(freq997Start)-1):
            if ( freq997Start[j]>=freq95Start[i] ) and ( freq997End[j]<=freq95End[i] ):
                if len(Start)==0:
                    Start.append(freq95Start[i])
                    End.append(freq95End[i])
                else:
                    if freq95Start[i]!=Start[-1]:
                        Start.append(freq95Start[i])
                        End.append(freq95End[i])
    print(Start)
    print(End)
    duration=[]

    if len(Start)==0:
        Start = freq95Start
        for i in range(len(Start)):
            duration.append(freq95End[i] - freq95Start[i] + 1)
    else:
        for i in range(len(Start)):
            duration.append(End[i]-Start[i]+1)
    sum=0
    for i in duration:
        sum+=i
    print(sum)
    print(strftime("%H:%M:%S", gmtime(sum)))
    print(len(Start))
    print(End)
    timestamp=[Start,duration]
    for i in range(len(timestamp[0])):
        timestamp[0][i]=strftime("%H:%M:%S", gmtime(timestamp[0][i]))
        timestamp[1][i]=strftime("%H:%M:%S", gmtime(timestamp[1][i]))
    print(timestamp[0])
    print(timestamp[1])
    Start=strftime("%H:%M:%S", gmtime(timestamp[0][i]))
    duration=strftime("%H:%M:%S", gmtime(timestamp[1][i]))
    return Start,duration#回傳list list[0]為開始時間 list[1]為結束時間 以hh:mm:ss字串


