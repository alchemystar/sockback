#coding=utf-8
#caculate shares
import pymongo
import numpy as np
# import matplotlib.pyplot as plt
import datetime
import tushare as ts

def day_get_start_end(d):
    a_month_ago = datetime.timedelta(days=d)
    one_day_ago = datetime.timedelta(days=0)
    today = datetime.datetime.now()
    one_day_ago_day=today-one_day_ago
    a_month_ago_day=today-a_month_ago
    start_date = datetime.datetime(a_month_ago_day.year, a_month_ago_day.month, a_month_ago_day.day)
    end_date= datetime.datetime(one_day_ago_day.year, one_day_ago_day.month, one_day_ago_day.day)
    return (str(start_date).split(" ")[0],str(end_date).split(" ")[0])

client = pymongo.MongoClient()
sc = client.shares.sock_classify
cursor = sc.find({'c_name':'电子信息'})
#cursor = sc.find({'c_name':'医疗器械'})
electronic=[]
electronicDict={}
for key in cursor:
	# here if for only electric
	#if key['code'].find('600') == 0 or key['code'].find('601') == 0:
	electronic.append(key['code'])
	electronicDict[key['code']]=key['name']		
print ('now we has %d electronic socks')%len(electronic)

#cacualte the least eps
pd = client.shares.profit_data_2019_03
startend=day_get_start_end(128)
print startend[0],startend[1]
cursor = pd.find({})
espElecDict={}
for key in cursor:
	if electronicDict.has_key(key['code']):
		df=ts.get_hist_data(key['code'],startend[0],pause=0.5)
		row=df['close']
		if len(row.index) >= 1:
			espElecDict[key['code']]=key['eps']/(row[0]*row[0])
espElecDict=sorted(espElecDict.items(), key=lambda d: d[1],reverse=True)
espElecRangeDict={}
for i in range(len(espElecDict)):
	espElecRangeDict[espElecDict[i][0]]=i;
print "=================================201903 here the eps/(row*row) follow at=============================================="	
for i in range(len(espElecDict)):
	print str(espElecDict[i])+","+electronicDict[espElecDict[i][0]]
#caculate the range inc and dec	
pd = client.shares.profit_data_2019_02
startend=day_get_start_end(128)
print startend[0],startend[1]
cursor = pd.find({})
espElecDict2={}
for key in cursor:
	if electronicDict.has_key(key['code']):
		df=ts.get_hist_data(key['code'],startend[0],pause=0.5)
		row=df['close']
		if len(row.index) >= 1:
			espElecDict2[key['code']]=key['eps']/(row[0]*row[0])
espElecDict2=sorted(espElecDict2.items(), key=lambda d: d[1],reverse=True)
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>201902 here the eps/(row*row) follow at>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"	
for i in range(len(espElecDict2)):
	print str(espElecDict2[i])+","+electronicDict[espElecDict2[i][0]]
espElecRangeDict2={}
for i in range(len(espElecDict2)):
	espElecRangeDict2[espElecDict2[i][0]]=i;
espGapElecRangeDict={}
for i in range(len(espElecDict2)):
	key = espElecDict2[i][0]
	if espElecRangeDict.has_key(key):
			a = espElecRangeDict[espElecDict2[i][0]]
			b = espElecRangeDict2[espElecDict2[i][0]]
			espGapElecRangeDict[espElecDict2[i][0]]=a-b;
print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"			
print espGapElecRangeDict
# for i in range(len(espElecDict2)):
#	print str(espElecDict2[i])+","+electronicDict[espElecDict2[i][0]]+","+str(espGapElecRangeDict[espElecDict2[i][0]]);
#sockCode=espElecDict[0][0]
#df=ts.get_hist_data(sockCode,startend[0],startend[1])
#dfclose=df['close']
#dfclose=dfclose.reindex(index=df.index[::-1])
#dfclose.plot()
#plt.show()




