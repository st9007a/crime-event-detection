#!/usr/bin/env python3
import numpy as np
import pandas as pd
from tqdm import tqdm

from lib.querylib.location import Location

l = Location()

def update(csv_file):

    data = pd.read_csv(csv_file, delimiter=',')
    new_data = []
    columns = ['second type', 'root type']

    for idx, row in tqdm(data.iterrows()):
        lat = row['lat']
        lon = row['lon']

        second, root = l.get_parent_category(lat, lon)
        new_data.append([second, root])

    df = pd.DataFrame(new_data, columns=columns)
    data = pd.concat([data, df], axis=1)

    data.to_csv(csv_file, index=False)

if __name__ == '__main__':

    update('../data/positive_samples.csv')
    update('../data/negative1_samples.csv')
    update('../data/negative2_samples.csv')

