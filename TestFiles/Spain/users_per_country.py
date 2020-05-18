import pymongo
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData

countries = ['Spain','Germany','France']
users = []
total_users = collection.count_documents({})
for country in countries:
	users.append(collection.count_documents({'userRegion': country}))

bar = plt.bar(countries,users,color='blue')

def autolabel(rects):
    #Attach a text label above each bar in *rects*, displaying its height.
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(bar)
plt.title("Number of users per country (Total Users: "+ str(total_users)+")")
plt.xlabel("Countries")
plt.ylabel("Users")
plt.ylim(0, 120) 
plt.show()