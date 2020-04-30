import pymongo
import pandas as pd
from pymongo import MongoClient

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData
hashtags = ["europe","heritage"]
europeans_countries = [ "Spain", "Germany","United Kingdom","United Kingdom",'Russian Federation' ]
#Most followed European TikTok user using each hashtag
for hashtag in hashtags:
	user = collection.find({'userRegion': { "$in": europeans_countries},"mediaData.hashtagsData.title":hashtag}, {'_id': False,'userName':1,'userRegion':1,"userStats":1,"mediaData.$":1}).sort("userStats.userFollowers",pymongo.DESCENDING).limit(1)	
	data = pd.DataFrame(user,index=None)
	print("Most followed european TikTok user using #"+hashtag+":")
	print(data)