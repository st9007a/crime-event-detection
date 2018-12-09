#!/usr/bin/env python3
from pprint import pprint

import pandas as pd

if __name__ == '__main__':

    raw_data = pd.read_csv('../data/Crimes2016.csv', delimiter=',')
    crime_type = raw_data['Primary Type'].values.tolist()
    crime_type = set(crime_type)
    pprint(crime_type)
    print(len(crime_type))

