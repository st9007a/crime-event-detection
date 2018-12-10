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
    time_slot = {'midnight': '01:00:00', 'morning': '07:00:00', 'afternoon': '13:00:00', 'night': '19:00:00'}
    for row in rows:
        time_has_crime = {'midnight': False, 'morning': False, 'afternoon': False, 'night': False}
        row['Latitude'] = '%.6f' % (float(row['Latitude']))
        row['Longitude'] = '%.6f' % (float(row['Longitude']))
        date_location = row['Date'][:5] + row['Latitude'][:9] + row['Longitude'][:10]
        if date_location not in has_crime:
            has_crime[date_location] = time_has_crime
            has_crime[date_location][row['Time slot']] = True
            loc_has_crime.add(row['Latitude'][:6] + row['Longitude'][:7])
        else:
            has_crime[date_location][row['Time slot']] = True
    count = 0
    for h in has_crime:
        for ts in has_crime[h]:
            if has_crime[h][ts] == False:
                count += 1
                writer.writerow({
                    'Date': h[:5] + '/2016 ' + time_slot[ts],
                    'Latitude': h[5:14],
                    'Longitude': h[14:24],
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
                'Date': date + ' ' + time_slot[ran_time_slot[ran]],
                'Latitude': location[:9],
                'Longitude': location[9:19],
                'Time slot': ran_time_slot[ran]
            })
            count += 1
    print('Negative 2 data: ' + str(count))
