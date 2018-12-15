#!/usr/bin/env python3
from pprint import pprint

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
    'lat', 'lon',
    'category',
    'second_type',
    # 'root_type',
    'time_slot',
    'weather_description',
    # 'month',
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

def get_features():

    pos = pd.read_csv('./data/positive_samples.csv', delimiter=',')
    neg1 = pd.read_csv('./data/negative1_samples.csv', delimiter=',')
    neg2 = pd.read_csv('./data/negative2_samples.csv', delimiter=',')

    # neg1 = neg1.sample(frac=0.6, random_state=0)

    res = pd.concat([pos, neg1, neg2])
    train_set = res[res['set'] == 'train']
    valid_set = res[res['set'] == 'valid']
    test_set = res[res['set'] == 'test']

    return build_features(train_set), build_features(valid_set), build_features(test_set), train_set['label'].values, valid_set['label'].values, test_set['label'].values

if __name__ == '__main__':

    x_train, x_valid, x_test, y_train, y_valid, y_test = get_features()

    y_train = np.where(y_train > 0, 1, 0)
    y_valid = np.where(y_valid > 0, 1, 0)
    y_test = np.where(y_test > 0, 1, 0)

    dtrain = xgb.DMatrix(x_train, label=y_train, feature_names=numerical_features)
    dvalid = xgb.DMatrix(x_valid, label=y_valid, feature_names=numerical_features)
    dtest = xgb.DMatrix(x_test, label=y_test, feature_names=numerical_features)

    params = {
        'max_depth': 5,
        'eta': 0.1,
        'objective': 'binary:logistic',
        'eval_metric': 'error',
        'silent': 1,
    }

    evallist = [(dvalid, 'eval')]

    bst = xgb.train(params, dtrain, num_boost_round=1000, evals=evallist, early_stopping_rounds=10)

    pred = bst.predict(dtest, ntree_limit=bst.best_ntree_limit)
    pred = np.where(pred > 0.5, 1, 0)
    pprint(bst.get_score())
    print(classification_report(y_test, pred))

    bst.save_model('model.xgb')
