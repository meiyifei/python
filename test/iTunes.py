#!/usr/bin/python
# -*- coding:utf-8 -*-
#Author:Mei
#plistlib提供load和dump函数解析和生成xml文件
import plistlib
import numpy as np
import matplotlib.pyplot as plt

#找到重复的音轨
def find_duplicate(filename):
    print("find duplicate tracks in %s......"%(filename))
    with open(filename,'rb') as fp:
        p1=plistlib.load(fp)
    tracks=p1["Tracks"]
    trackNames={}
    for trackId,track in tracks.items():
        try:
            name=track['Name']
            duration=track['Total Time']
            if name in trackNames:
                if duration//1000 == trackNames[name][0]//1000:
                    count=trackNames[name][1]
                    trackNames[name]=(duration,count+1)
            else:
                trackNames[name]=(duration,1)
        except:
            pass
    return trackNames

 #存储重复的音轨
def store_duplicate(trackNames,filename):
    print("find store duplicate tracks in %s......" % (filename))
    with open(filename, 'w+') as f:
        for trackname in trackNames:
            if trackNames[trackname][1]>1:

              f.write("%s %d\n"%(trackname,trackNames[trackname][1]))
    f.close()

def findcommonTracks(filenames,file):
    tracknameSet=[]
    for filename in filenames:
        trackname=set()
        with open(filename,'rb') as fp:
            p=plistlib.load(fp)
        tracks=p["Tracks"]
        for trackId, track in tracks.items():
            try:
                 trackname.add(track['Name'])
            except:
                pass
        tracknameSet.append(trackname)
    #set.intersection找到多个集合中公共的元素
    commonTracks=set.intersection(*tracknameSet)

    if len(commonTracks)>0:
        with open(file,'w+') as f:
            for name in commonTracks:
                f.write("%s\n"%name)
    else:
        print("no common Tracks!")


def plotStats(filename,file):
    with open(filename,'rb') as fp:
        plist=plistlib.load(fp)
    tracks=plist["Tracks"]
    rating = []
    durations = []
    for tackId,track in tracks.items():
        try:
            with open(file,'a+') as f:
                f.write("%d %d\n"%(track["Album Rating"],track["Total Time"]))
        except:
            pass

    with open(file,'rb') as ff:
        for line in ff.readlines():
            rating.append(line.split()[0])
            durations.append(line.split()[1])



    x=np.array(durations,np.int32)
    x=x/60000
    y=np.array(rating,np.int32)
    plt.subplot(2,1,1)
    plt.plot(x,y,'o')
    plt.axis([0,1.05*np.max(x),-1,110])
    plt.xlabel('Track duration')
    plt.ylabel('Track rating')

    //直方图
    plt.subplot(2, 1, 2)
    plt.hist(x,bins=20)
    plt.xlabel('Track duration')
    plt.ylabel('Duration Count')
    plt.show()




if __name__ == '__main__':

    #找到重复的Track并存储
    filename="C:\\Users\\admin\\PycharmProjects\\ex_one\\test_data\\pl1.xml"
    tracknames=find_duplicate(filename)
    store_file="C:\\Users\\admin\\PycharmProjects\\ex_one\\test_data\\a.txt"
    store_duplicate(tracknames,store_file)

    #找到多个播放列表的公共Track
    filenames=["C:\\Users\\admin\\PycharmProjects\\ex_one\\test_data\\pl1.xml",
               "C:\\Users\\admin\\PycharmProjects\\ex_one\\test_data\\pl2.xml"
               ]
    file="C:\\Users\\admin\\PycharmProjects\\ex_one\\test_data\\b.txt"
    findcommonTracks(filenames,file)

    #统计时长与评分之间的信息，并画图展示
    fn="C:\\Users\\admin\\PycharmProjects\\ex_one\\test_data\\rating.xml"
    f="C:\\Users\\admin\\PycharmProjects\\ex_one\\test_data\\c.txt"
    plotStats(fn,f)
