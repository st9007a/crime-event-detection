#!/usr/bin/env python3
from datetime import datetime

import pandas as pd
from tqdm import tqdm

import lib.query as Q
from lib.label import get_label

def get_set_name(date):
    if date.day % 4 == 0:
        return 'test'
    elif date.day % 4 == 2:
        return 'valid'
    return 'train'


def create_feature_csv(in_file, out_file, random_sample=None, selected_features=[]):
    columns = ['date', 'set', 'lat', 'lon', 'label'] + selected_features
    raw_data = pd.read_csv(in_file, delimiter=',')
    out_data = []

    if random_sample is not None:
        raw_data = raw_data.sample(frac=random_sample, random_state=0)

    for idx, row in tqdm(raw_data.iterrows()):
        date, lat, lon, time_slot = row['Date'], row['Latitude'], row['Longitude'], row['Time slot']
        date = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')

        row_data = [
            date,
            get_set_name(date),
            lat,
            lon,
            get_label(row['Primary Type']) if 'Primary Type' in row else 0
        ]

        features = Q.get(selected_features, date, time_slot, lat, lon)

        row_data.extend(features)
        out_data.append(row_data)

    df = pd.DataFrame(out_data, columns=columns)
    df.to_csv(out_file, index=False)

if __name__ == '__main__':

    create_feature_csv('../data/positive.csv',
                       '../data/positive_samples.csv',
                       random_sample=1,
                       selected_features=Q.FEATURE_COLUMNS)

    create_feature_csv('../data/negative1.csv',
                       '../data/negative1_samples.csv',
                       random_sample=1,
                       selected_features=Q.FEATURE_COLUMNS)

    create_feature_csv('../data/negative2.csv',
                       '../data/negative2_samples.csv',
                       random_sample=0.25,
                       selected_features=Q.FEATURE_COLUMNS)
