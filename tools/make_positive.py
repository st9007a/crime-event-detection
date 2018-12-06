import csv

with open('../data/Crimes2016.csv', newline='') as crimeFile:
    rows = csv.DictReader(crimeFile)

    fieldnames = ['Date', 'Primary Type', 'Latitude', 'Longitude', 'Time slot']
    writer = csv.DictWriter(open('../data/positive.csv', 'w'), fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        hour = int(row['Date'][-11:-9])
        if 'PM' in row['Date']:
            if hour != 12:
                hour = hour + 12
                row['Date'] = row['Date'][:-11] + str(hour) + row['Date'][-9:]
        else:
            if hour == 12:
                row['Date'] = row['Date'][:-11] + '00' + row['Date'][-9:]
        row['Date'] = row['Date'][:-3]
        time_slot = ['midnight', 'morning', 'afternoon', 'night']
        row['Time slot'] = time_slot[int(hour/6)]
        writer.writerow(row)
    