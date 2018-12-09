#!/usr/bin/env python3
import os

import pandas as pd

_file_dir = os.path.dirname(os.path.realpath(__file__))

_specific_cluster = [
    set(['NON - CRIMINAL', 'NON-CRIMINAL', 'NON-CRIMINAL (SUBJECT SPECIFIED)']),
    set(['OTHER NARCOTIC VIOLATION', 'OTHER OFFENSE']),
    set(['SEX OFFENSE', 'CRIM SEXUAL ASSAULT']),
]

_raw_data = pd.read_csv('%s/Crimes2016.csv' % _file_dir, delimiter=',')
_crime_type = _raw_data['Primary Type'].values
_crime_type = list(set(_crime_type))

for cluster in _specific_cluster:
    for crime in cluster:
        _crime_type.remove(crime)

NUM_LABELS = len(_crime_type) + len(_specific_cluster) + 1

def get_label(crime):

    for i, cluster in enumerate(_specific_cluster):
        if crime in cluster:
            return i + 1

    return _crime_type.index(crime) + len(_specific_cluster) + 1
