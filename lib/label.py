#!/usr/bin/env python3
import os

_file_dir = os.path.dirname(os.path.realpath(__file__))

_label_dict = {}

with open('%s/crime.txt' % _file_dir, 'r') as f:
    lines = f.readlines()

for line in lines:
    label = int(line[0])
    name = line.split(',')[0][2:-1]
    _label_dict[name] = label

NUM_LABELS = len(_label_dict)

def get_label(crime):

    if crime not in _label_dict:
        return NUM_LABELS

    return _label_dict[crime]
