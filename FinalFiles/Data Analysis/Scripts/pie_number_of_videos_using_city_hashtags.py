import pymongo
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData

europeanCapitals= ["madrid","berlin","paris"]
numVideosUsingHashtag=[]
for capital in europeanCapitals:
	contador = 0
	for user in list(collection.find({"mediaData.hashtagsData.title":capital}, {'_id': False,"mediaData.hashtagsData.title":1})):
		videos = user['mediaData']
		for video in videos:
			hashtag = video["hashtagsData"]
			for title in hashtag:
				if(title['title']==capital): 
					contador+=1
	numVideosUsingHashtag.append(contador)

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = '#madrid', '#berlin', '#paris'
explode = (0, 0, 0)
colors = ['gold', 'lightskyblue','red']
fig1, ax1 = plt.subplots()
ax1.pie(numVideosUsingHashtag, explode=explode, labels=labels, colors=colors, autopct=lambda p : '{:,.0f} videos'.format(p * sum(numVideosUsingHashtag)/100),
        shadow=False, startangle=90)
ax1.axis('equal')# Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Number of videos using the hashtags:')
plt.show()