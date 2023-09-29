# coding=gbk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts
import datetime
import time
import sys

def day_get(d,n):
    oneday = datetime.timedelta(days=n)
    day = d - oneday
    date_from = datetime.datetime(day.year, day.month, day.day)
    return str(date_from).split(" ")[0]
print sys.argv[1]
i=4
d = datetime.datetime.now()
print day_get(d,i)
df = ts.get_tick_data(sys.argv[1],date=day_get(d,i),src='tt',pause=1)
i+=1
while i<30:
 print i   
 df=df.append(ts.get_tick_data(sys.argv[1],date=day_get(d,i),src='tt',pause=1))
 i+=1
df = df[::-1]
dict = {}
for item in df.values:
    if dict.has_key(item[1]):
        if item[5].decode("utf-8") == '买盘'.decode("utf-8"):
            dict[item[1]] = dict[item[1]] + item[3]
        else:
            dict[item[1]] = dict[item[1]] - item[3]
    else:
        if item[5].decode("utf-8") == '买盘'.decode("utf-8"):
            dict[item[1]] = item[3]
        else:
            dict[item[1]] = 0 - item[3]
listkey=[]     
listValue=[]
noNanDict={}
for key in dict.keys():
    if np.isnan(key):
        pass;
    else:
        noNanDict[key]=dict[key]
keys = noNanDict.keys();
keys.sort()
for key in keys:
    listkey.append(key)
    listValue.append(noNanDict[key])  
    print str(key)+","+str(noNanDict[key])      
plt.plot(listkey,listValue,color='r')	
plt.xticks(np.arange(listkey[0],listkey[len(listkey)-1],1))
plt.yticks(np.arange(-50,200,50))
plt.grid(True)
plt.show()	