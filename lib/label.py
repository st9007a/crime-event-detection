#!/usr/bin/env python3
import os

_file_dir = os.path.dirname(os.path.realpath(__file__))

_label_set = []

with open('%s/crime.txt' % _file_dir, 'r') as f:
    lines = f.readlines()

for line in lines:
    label = int(line[0])
    name = line.split(',')[0][2:-1]

    if name not in _label_set:
        _label_set.append(name)

print(_label_set)

NUM_LABELS = len(_label_set) + 1

def get_label(crime):

    if crime not in _label_set:
        return 0

    return _label_set.index(crime) + 1
