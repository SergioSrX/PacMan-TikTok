from pymongo import MongoClient
import json
uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(uri)
db = client.userDatas

# Opens the .txt file and reads it as an json file
with open("user_data.txt") as json_file:
    user = json.load(json_file)
    # Making a loop to put in every user into json format
    for p in user:
        userData = {
            "userName": p["userName"],
            "userTag": p["userTag"],
            "userFollowing": p["userFollowing"],
            "userFollowers": p["userFollowers"]
        }
        # Putting it in into MongoDB
        result = db.userDatas.insert_one(userData)
        # Just a print to see that everything has been written into the database
        print("Har skrivit users")
