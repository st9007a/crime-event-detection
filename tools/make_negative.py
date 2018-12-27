import csv
import random
from datetime import datetime
from dateutil import rrule

with open('../data/positive.csv', newline='') as crimeFile:
    rows = csv.DictReader(crimeFile)

    fieldnames = ['Date', 'Latitude', 'Longitude', 'Time slot']
    writer = csv.DictWriter(open('../data/negative1.csv', 'w'), fieldnames=fieldnames)
    writer.writeheader()

    has_crime = {}
    loc_has_crime = set()
    for row in rows:
        time_has_crime = {
            'location': {'Latitude': 0.0, 'Longitude': 0.0},
            'time_slot': {'midnight': False, 'morning': False, 'afternoon': False, 'night': False}
        }
        row['Latitude'] = '%.6f' % (float(row['Latitude']))
        row['Longitude'] = '%.6f' % (float(row['Longitude']))
        date_location = row['Date'][:5] + row['Latitude'][:6] + row['Longitude'][:7]
        if date_location not in has_crime:
            has_crime[date_location] = time_has_crime
            has_crime[date_location]['location']['Latitude'] = row['Latitude']
            has_crime[date_location]['location']['Longitude'] = row['Longitude']
            has_crime[date_location]['time_slot'][row['Time slot']] = True
            loc_has_crime.add(row['Latitude'][:6] + row['Longitude'][:7])
        else:
            has_crime[date_location]['time_slot'][row['Time slot']] = True
    count = 0

    # print(has_crime['01/0141.918-87.729'])

    for key, crime in has_crime.items():
        arr = range(-3, 4)
        for i in arr:
            for j in arr:
                date_location = key[:5] + str(float(crime['location']['Latitude']) + i * 0.001)[:6] + str(float(crime['location']['Longitude']) + j * 0.001)[:7]
                if date_location in has_crime:
                    for ts in crime['time_slot']:
                        if crime['time_slot'][ts]:
                            has_crime[date_location]['time_slot'][ts] = True
    # print(has_crime['01/0141.918-87.729'])

    time_slot = {'midnight': range(0, 6), 'morning': range(6, 12), 'afternoon': range(12, 18), 'night': range(18, 24)}
    for h in has_crime:
        for ts in has_crime[h]['time_slot']:
            if not has_crime[h]['time_slot'][ts]:
                count += 1
                writer.writerow({
                    'Date': h[:5] + '/2016 ' + '%02d' % random.choice(time_slot[ts]) + ':00:00',
                    'Latitude': has_crime[h]['location']['Latitude'],
                    'Longitude': has_crime[h]['location']['Longitude'],
                    'Time slot': ts
                })
    print('Negative 1 data: ' + str(count))

    ran_time_slot = ['midnight', 'morning', 'afternoon', 'night']
    loc_not_crime = set()
    locations = csv.DictReader(open('../data/locCategory.csv', newline=''))

    writer2 = csv.DictWriter(open('../data/negative2.csv', 'w'), fieldnames=fieldnames)
    writer2.writeheader()

    for location in locations:
        location['Latitude'] = '%.6f' % (float(location['Latitude']))
        location['Longitude'] = '%.6f' % (float(location['Longitude']))
        if (location['Latitude'][:6] + location['Longitude'][:7]) in loc_has_crime:
            continue
        loc_not_crime.add(location['Latitude'] + location['Longitude'])

    count = 0
    for dt in rrule.rrule(rrule.DAILY,
                          dtstart=datetime.strptime('01/01/2016', '%m/%d/%Y'),
                          until=datetime.strptime('12/31/2016', '%m/%d/%Y')):
        date = dt.strftime('%m/%d/%Y')
        for location in loc_not_crime:
            ran = random.randint(0, 3)
            writer2.writerow({
                'Date': date + ' ' + '%02d' % random.choice(time_slot[ran_time_slot[ran]]) + ':00:00',
                'Latitude': location[:9],
                'Longitude': location[9:19],
                'Time slot': ran_time_slot[ran]
            })
            count += 1
    print('Negative 2 data: ' + str(count))
