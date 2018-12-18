#!/usr/bin/env python3
from datetime import datetime
import pickle

import numpy as np
import pandas as  pd
from xgboost import Booster, DMatrix

import lib.query as Q

numerical_features = [
    'humidity',
    'pressure',
    'temperature',
    'wind_direction',
    'wind_speed',
    'population_density',
    'night_spot_density',
    'category',
    'time_slot',
    'weather_description',
    'lat',
    'lon',
    'hour',
]

time_slot = {'midnight': range(0, 6), 'morning': range(6, 12), 'afternoon': range(12, 18), 'night': range(18, 24)}

if __name__ == '__main__':

    with open('data/questionNode_2017.csv', 'r') as f:
        lines = f.readlines()

    models = []

    for i in range(9):
        with open('models/model.%d.pkl' % i, 'rb') as p:
            bst = pickle.load(p)
        models.append(bst)

    samples = []

    for line in lines[1:]:
        lat, lon, date, ts, _ = line.split(',')
        lat = float(lat)
        lon = float(lon)

        score = []

        for hour in time_slot[ts]:
            new_date = date + ' ' + str(hour) + ':00:00'
            new_date = datetime.strptime(new_date, '%Y/%m/%d %H:%M:%S')

            if new_date.month == 12:
                continue

            features = Q.get(['humidity',
                              'pressure',
                              'temperature',
                              'wind_direction',
                              'wind_speed',
                              'population_density',
                              'night_spot_density',
                              'category',
                              'time_slot',
                              'weather_description',
                              ], new_date, ts, lat, lon)
            features.extend([lat, lon, hour])

            samples.append(features)

    samples = np.array(samples)
    print(samples[0])
    deval = DMatrix(samples, feature_names=numerical_features)
    pred_proba = sum([bst.predict(deval, ntree_limit=bst.best_ntree_limit) for bst in models]) / len(models)
    print(pred_proba)

    prediction = []

    for i in range(0, samples.shape[0], 6):
        p = 0
        c = 0
        for j in range(6):
            if pred_proba[i + j] > 0.5:
                c += 1
        if c >= 1:
            p = 1
        prediction.append(p)

    print(prediction)

    ptr = 0

    for i in range(len(lines)):
        if i == 0:
            continue

        lat, lon, date, ts, _ = lines[i].split(',')
        date = datetime.strptime(date, '%Y/%m/%d')

        if date.month == 12:
            continue

        lines[i] = lines[i].rstrip('\n') + str(prediction[ptr]) + '\n'
        ptr += 1

    with open('result2.csv', 'w') as f:
        for line in lines:
            f.write(line)
