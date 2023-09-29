#mongo insert
import pymongo
import json
import tushare as ts
client = pymongo.MongoClient()
dp_collection=client.shares.profit_data_2019_02
dp=ts.get_report_data(2019,2)
dp_collection.insert(json.loads(dp.to_json(orient='records')))