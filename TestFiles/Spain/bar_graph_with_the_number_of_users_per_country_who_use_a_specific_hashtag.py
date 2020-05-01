import pymongo
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData
hashtag ="stayathome"
european_countries = ["Spain", "Germany","United Kingdom","France",'Russian Federation']
users = []
#Get the number of users who use a specific hashtag per country
for country in european_countries:
	users.append(collection.count_documents({'userRegion': country,"mediaData.hashtagsData.title":hashtag}))

bar = plt.bar(european_countries,users,color='orange')

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
plt.title("Number of users who use the hashtag #"+hashtag)
plt.xlabel("Countries")
plt.ylabel("Users")
plt.ylim(0, 60) 
plt.show()	