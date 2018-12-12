import csv

with open('../data/Crimes2016.csv', newline='') as crimeFile:
    rows = csv.DictReader(crimeFile)

    fieldnames = ['Date', 'Primary Type', 'Latitude', 'Longitude', 'Time slot']

    primary_type = {
        'ARSON': 514,
        'ASSAULT': 18670,
        'BATTERY': 50129,
        'BURGLARY': 14247,
        'CONCEALED CARRY LICENSE VIOLATION': 35,
        'CRIM SEXUAL ASSAULT': 1483,
        'CRIMINAL DAMAGE': 30856,
        'CRIMINAL TRESPASS': 6287,
        'DECEPTIVE PRACTICE': 18111,
        'GAMBLING': 189,
        'HOMICIDE': 786,
        'HUMAN TRAFFICKING': 11,
        'INTERFERENCE WITH PUBLIC OFFICER': 931,
        'INTIMIDATION': 134,
        'KIDNAPPING': 202,
        'LIQUOR LAW VIOLATION': 227,
        'MOTOR VEHICLE THEFT': 11250,
        'NARCOTICS': 13225,
        'NON - CRIMINAL': 5,
        'NON-CRIMINAL': 48,
        'NON-CRIMINAL (SUBJECT SPECIFIED)': 1,
        'OBSCENITY': 53,
        'OFFENSE INVOLVING CHILDREN': 2253,
        'OTHER NARCOTIC VIOLATION': 4,
        'OTHER OFFENSE': 17148,
        'PROSTITUTION': 800,
        'PUBLIC INDECENCY': 10,
        'PUBLIC PEACE VIOLATION': 1594,
        'ROBBERY': 11939,
        'SEX OFFENSE': 941,
        'STALKING': 173,
        'THEFT': 60889,
        'WEAPONS VIOLATION': 3439
    }

    writer = csv.DictWriter(open('../data/positive.csv', 'w'), fieldnames=fieldnames)
    writer.writeheader()
    count = 0
    for row in rows:
        if primary_type[row['Primary Type']] <= 100:
            continue
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
        count += 1
    print('Positive data: ' + str(count))
    