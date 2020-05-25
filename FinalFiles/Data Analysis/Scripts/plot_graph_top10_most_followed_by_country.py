import pymongo
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData

europeanUnionCountries= ["Spain","France","Germany"]

for country in europeanUnionCountries:
	plt.figure(figsize=(20, 35))
	contUsers = 1
	for user in list(collection.find({'userRegion': country}, {'_id': False,'userTag':1,'userStats.userFollowers':1,'userStats.datetime':1}).sort("userStats.1.userFollowers",pymongo.DESCENDING).limit(10)):
		followersList = []
		datetimeList = []
		contDataTime = 0
		for datetime in user['userStats']:
			contDataTime += 1
			if(contDataTime < 5): 
				followersList.append(datetime['userFollowers'])
				datetimeList.append(datetime['datetime'])	
			else: 
				break
		ax = plt.subplot(5,2,contUsers)
		ax.title.set_text(user['userTag'])
		ax.set_ylabel('Followers')
		ax.set_xlabel('Dates')
		plt.subplots_adjust(hspace=0.5, wspace=0.5)
		plt.plot(datetimeList, followersList)
		contUsers += 1
	plt.suptitle('Gain of followers of the four most followed influencers in '+country)
	plt.show()