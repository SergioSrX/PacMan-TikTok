import pymongo
import pandas as pd
from pymongo import MongoClient

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData

countries = ['Spain','Germany','France']

for country in countries:
	top_ten_most_followed = []
	#Top 10 most followed TikTok users by country in the database.
	for user in list(collection.find({'userRegion': country}, {'_id': False,'userName':1,'userStats':1,'userRegion':1}).sort("userStats.userFollowers",pymongo.DESCENDING).limit(10)):
		top_ten_most_followed.append(user)

	data = pd.DataFrame(top_ten_most_followed,index=None)
	print(data)