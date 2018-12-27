#!/usr/bin/env python3
import os
from pprint import pprint
import pickle
import sys
from glob import glob

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from lib.query import FEATURE_COLUMNS, UPDATE_COLUMNS
from lib.label import NUM_LABELS

categorical_features = [
]

numerical_features = [
    'humidity',
    'pressure',
    'temperature',
    'wind_direction',
    'wind_speed',
    'population_density',
    'night_spot_density',
    'event_density',
    'residence_density',
    'art_enter_density',
    'college_density',
    'outdoors_density',
    'professional_density',
    'shop_density',
    'travel_density',
    'category',
    'time_slot',
    'weather_description',
    'lat',
    'lon',
    'hour',
]

def one_hot(arr):
    ret = np.zeros((arr.size, arr.max() + 1))
    ret[np.arange(arr.size), arr] = 1

    return ret

def build_features(df):

    numerical = df[numerical_features].values
    categorical = df[categorical_features].values

    for i in range(categorical.shape[1]):
        numerical = np.concatenate([numerical, one_hot(categorical[:, i])], axis=1)

    return numerical

if __name__ == '__main__':

    model_path = sys.argv[1]

    pos = pd.read_csv('./data/positive_samples.csv', delimiter=',')
    neg1 = pd.read_csv('./data/negative1_samples.csv', delimiter=',')
    neg2 = pd.read_csv('./data/negative2_samples.csv', delimiter=',')
    dataset = pd.concat([pos, neg1.sample(frac=0.4)])
    testset = dataset[dataset['set'] == 'test']

    x = build_features(testset)
    y = testset['label'].values
    y = np.where(y > 0, 1, 0)

    deval = xgb.DMatrix(x, feature_names=numerical_features)

    models = []

    for path in glob('%s/*.pkl' % model_path):
        with open(path, 'rb') as p:
            models.append(pickle.load(p))

    pred = sum([bst.predict(deval, ntree_limit=bst.best_ntree_limit) for bst in models]) / len(models)
    pred = np.where(pred > 0.5, 1, 0)

    print(classification_report(y, pred))
