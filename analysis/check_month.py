import csv
import pprint

locs = csv.DictReader(open('../data/Crimes2016.csv', newline=''))

months = {
    '01': {},
    '02': {},
    '03': {},
    '04': {},
    '05': {},
    '06': {},
    '07': {},
    '08': {},
    '09': {},
    '10': {},
    '11': {},
    '12': {}
}

for month in months:
    months[month] = {
        'ARSON': 0,
        'ASSAULT': 0,
        'BATTERY': 0,
        'BURGLARY': 0,
        'CONCEALED CARRY LICENSE VIOLATION': 0,
        'CRIM SEXUAL ASSAULT': 0,
        'CRIMINAL DAMAGE': 0,
        'CRIMINAL TRESPASS': 0,
        'DECEPTIVE PRACTICE': 0,
        'GAMBLING': 0,
        'HOMICIDE': 0,
        'HUMAN TRAFFICKING': 0,
        'INTERFERENCE WITH PUBLIC OFFICER': 0,
        'INTIMIDATION': 0,
        'KIDNAPPING': 0,
        'LIQUOR LAW VIOLATION': 0,
        'MOTOR VEHICLE THEFT': 0,
        'NARCOTICS': 0,
        'NON - CRIMINAL': 0,
        'NON-CRIMINAL': 0,
        'NON-CRIMINAL (SUBJECT SPECIFIED)': 0,
        'OBSCENITY': 0,
        'OFFENSE INVOLVING CHILDREN': 0,
        'OTHER NARCOTIC VIOLATION': 0,
        'OTHER OFFENSE': 0,
        'PROSTITUTION': 0,
        'PUBLIC INDECENCY': 0,
        'PUBLIC PEACE VIOLATION': 0,
        'ROBBERY': 0,
        'SEX OFFENSE': 0,
        'STALKING': 0,
        'THEFT': 0,
        'WEAPONS VIOLATION': 0
    }

total = {
    'ARSON': 0,
    'ASSAULT': 0,
    'BATTERY': 0,
    'BURGLARY': 0,
    'CONCEALED CARRY LICENSE VIOLATION': 0,
    'CRIM SEXUAL ASSAULT': 0,
    'CRIMINAL DAMAGE': 0,
    'CRIMINAL TRESPASS': 0,
    'DECEPTIVE PRACTICE': 0,
    'GAMBLING': 0,
    'HOMICIDE': 0,
    'HUMAN TRAFFICKING': 0,
    'INTERFERENCE WITH PUBLIC OFFICER': 0,
    'INTIMIDATION': 0,
    'KIDNAPPING': 0,
    'LIQUOR LAW VIOLATION': 0,
    'MOTOR VEHICLE THEFT': 0,
    'NARCOTICS': 0,
    'NON - CRIMINAL': 0,
    'NON-CRIMINAL': 0,
    'NON-CRIMINAL (SUBJECT SPECIFIED)': 0,
    'OBSCENITY': 0,
    'OFFENSE INVOLVING CHILDREN': 0,
    'OTHER NARCOTIC VIOLATION': 0,
    'OTHER OFFENSE': 0,
    'PROSTITUTION': 0,
    'PUBLIC INDECENCY': 0,
    'PUBLIC PEACE VIOLATION': 0,
    'ROBBERY': 0,
    'SEX OFFENSE': 0,
    'STALKING': 0,
    'THEFT': 0,
    'WEAPONS VIOLATION': 0
}

for loc in locs:
    months[loc['Date'][:2]][loc['Primary Type']] += 1
    total[loc['Primary Type']] += 1

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(months)
pp.pprint(total)