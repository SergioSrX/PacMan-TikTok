import pymongo
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams['figure.figsize'] = [12, 8] #Set the plot size
uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData

top5SongsSpotifySpain = ["Nunca Estoy","Favorito","PAM","Tusa","Amarillo"]
top5SongsSpotifyGermany = ["Fame","GOOBA","Nicht verdient","Emotions","ROCKSTAR"]
top5SongsSpotifyFrance = ["Lettre à une femme","Angela","Blinding Lights","Roses","6.3"]

def newSubPlot(top5SongsSpotify):
	numVideosUsingEachSong = []
	for topSong in top5SongsSpotify:
		contador = 0
		for user in list(collection.find({'mediaData.musicData.musicName': topSong}, {'_id': False,'mediaData.musicData.musicName':1})): 
			for video in user["mediaData"]:
				song = video['musicData']				
				if(song["musicName"] == topSong): 
					contador+=1
		numVideosUsingEachSong.append(contador)
	bar = plt.bar(top5SongsSpotify,numVideosUsingEachSong)
	autolabel(bar)
	plt.title('Number of videos in which the song appears')
	return numVideosUsingEachSong

def autolabel(rects):
    #Attach a text label above each bar in *rects*, displaying its height.
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{:,}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

print(newSubPlot(top5SongsSpotifySpain))
print(newSubPlot(top5SongsSpotifyGermany))
print(newSubPlot(top5SongsSpotifyFrance))
blue_patch = mpatches.Patch(color='blue', label='Top 5 Songs Spain')
orange_patch = mpatches.Patch(color='orange', label='Top 5 Songs Germany')
green_patch = mpatches.Patch(color='green', label='Top 5 Songs France')
plt.xticks(rotation=40)
fig = plt.legend(handles=[blue_patch,orange_patch,green_patch])
plt.xlabel("Songs")
plt.ylabel("Number of videos")
plt.show()
