import json

with open('user_data.txt', 'r') as jsonFile:
    jsonFileData = jsonFile.read()
jsonFile.close()

jsonFileData = json.loads(jsonFileData)
print(jsonFileData[0])