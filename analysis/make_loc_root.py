import csv
import json

def findRoot(data, childName):
    if (data.get('categories', None) is None):
        return
    for category in data['categories']:
        if category['name'] == childName or findRoot(category, childName):
            return category['name']
    return None

with open('loc.json') as json_file:
    loc = json.load(json_file)
    locations = csv.DictReader(open('../data/locCategory.csv', newline=''))

    fieldnames = ['Latitude', 'Longitude', 'Type', 'Second Type', 'Root Type']
    writer = csv.DictWriter(open('./loc.csv', 'w'), fieldnames=fieldnames)
    writer.writeheader()
    
    for location in locations:
        location['Root Type'] = findRoot(loc, location['Type'])
        for l in loc["categories"]:
            if findRoot(l, location['Type']) != None:
                location['Second Type'] = findRoot(l, location['Type'])
                break
        writer.writerow(location)
