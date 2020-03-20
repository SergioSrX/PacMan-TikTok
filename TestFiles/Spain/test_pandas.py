import pymongo
import pandas as pd
from pymongo import MongoClient

uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userData
collection = db.userData
data = pd.DataFrame(list(collection.find()))
print(data)