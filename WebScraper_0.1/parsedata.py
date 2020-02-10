import json
json_data = open('twitterData.json')
jsonData = json.load(json_data)
for i in jsonData:
    if "obama" in i['tweet'].lower():
        print(i)
