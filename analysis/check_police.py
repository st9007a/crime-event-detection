import csv

locs = csv.DictReader(open('../data/locCategory.csv', newline=''))
polices = []

for loc in locs:
    if loc['Type'] == 'Police Station':
        loc['Amount'] = 0
        polices.append(loc)

def nearby(police, loc):
    if (abs(float(police['Latitude']) - float(loc['Latitude'])) <= 0.001 and abs(float(police['Longitude']) - float(loc['Longitude'])) <= 0.001):
        police['Amount'] += 1

crimes = csv.DictReader(open('../data/Crimes2016.csv', newline=''))

fieldnames = ['Latitude', 'Longitude', 'Type', 'Amount']
writer = csv.DictWriter(open('./police_amount.csv', 'w'), fieldnames=fieldnames)
writer.writeheader()

for crime in crimes:
    for police in polices:
        nearby(police, crime)

for police in polices:
    writer.writerow(police)
