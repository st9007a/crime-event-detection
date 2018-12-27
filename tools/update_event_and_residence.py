#!/usr/bin/env python3
import numpy as np
import pandas as pd
from tqdm import tqdm

import lib.query as Q
from lib.querylib.location import Location

l = Location()

def update(csv_file):

    data = pd.read_csv(csv_file, delimiter=',')
    new_data = []
    columns = ['event_density', 'residence_density']

    for idx, row in tqdm(data.iterrows()):
        lat = row['lat']
        lon = row['lon']

        features = l.query(lat, lon, query_list=columns)
        new_data.append(features)

    df = pd.DataFrame(new_data, columns=columns)
    data = pd.concat([data, df], axis=1)

    data.to_csv(csv_file, index=False)

if __name__ == '__main__':

    update('../data/positive_samples.csv')
    update('../data/negative1_samples.csv')
    update('../data/negative2_samples.csv')
