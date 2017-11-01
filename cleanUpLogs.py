import json

with open('testLog.json') as json_data:
    data = json.load(json_data)
    data.pop('coverageMap', None)

with open('testLog.json', 'w') as json_data:
    data = json.dump(data, json_data)