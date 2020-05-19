import pymongo
import pandas as pd
from pymongo import MongoClient

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData
top_ten_most_followed = []
european_countries = [ "Spain", "Germany","France"]
#Top 10 European TikTok users most followed in the database.
for user in list(collection.find({'userRegion': { "$in": european_countries}}, {'_id': False,'userName':1,'userRegion':1,"userStats": {"$slice": -1}}).sort("userStats.userFollowers",pymongo.DESCENDING).limit(10)):
	top_ten_most_followed.append(user)

data = pd.DataFrame(top_ten_most_followed,index=None)
print(data)