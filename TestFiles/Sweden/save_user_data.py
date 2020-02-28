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
            "itemNum" : p["itemNum"],
            "userName": p["userName"],
            "userTag": p["userTag"],
            "userLink" : p["userLink"],
            "userDescription" : p["userDescription"],
            "userRegion" : p["userRegion"],
            "userImage" : p["userImg"],
            "userVerified" : p["userVerified"],
            "userFollowing": p["userFollowing"],
            "userFollowers": p["userFollowers"],
            "userLikes" : p["userLikes"],
            "userVideosCount" : p["userVideosCount"]
        }
        # Putting it in into MongoDB
        result = db.userDatas.insert_one(userData)
        # Just a print to see that everything has been put in the database
        print("Have written users")

