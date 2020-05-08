import pymongo
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData

countries = ['Spain','United Kingdom','Germany','Russian Federation','France']

def autolabel(rects):
    #Attach a text label above each bar in *rects*, displaying its height.
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{:,}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

for country in countries:
	usersNames = []
	followers = []
	#Top 10 most followed TikTok users by country in the database.
	for user in list(collection.find({'userRegion': country}, {'_id': False,'userName':1,'userStats':1}).sort("userStats.0.userFollowers",pymongo.DESCENDING).limit(10)):
		usersNames.append(user['userName'])
		followers.append(user['userStats'][0]['userFollowers'])
	#bar graph for each country	
	bar = plt.bar(usersNames,followers,color='green')
	autolabel(bar)
	plt.title("Top 10 most followed from "+country)
	plt.xlabel("Users")
	plt.ylabel("Followers")
	plt.ylim(0, 20000000) 
	plt.show()