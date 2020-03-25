import pymongo
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData

users_no_verified = collection.count_documents({'userVerified':False})
total_users_verified = collection.count_documents({'userVerified':True})

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Percentage of verified users', 'Percentage of NO verified users'
sizes = [total_users_verified, users_no_verified]
explode = (0, 0.1)
colors = ['gold', 'lightskyblue']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda p : '{:.2f}%  ({:,.0f})'.format(p,p * sum(sizes)/100),
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Percentage of Verified Users')
plt.show()
