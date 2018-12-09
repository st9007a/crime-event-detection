#!/usr/bin/env python3
import pickle

import numpy as np
import pandas as pd
import xgboost as xgb
from xgboost.callback import reset_learning_rate
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from lib.query import FEATURE_COLUMNS
from lib.label import NUM_LABELS

feature_names = FEATURE_COLUMNS + ['lat', 'lon']

def get_all_features():

    pos = pd.read_csv('./data/positive_samples.csv', delimiter=',')
    neg1 = pd.read_csv('./data/negative1_samples.csv', delimiter=',')
    neg2 = pd.read_csv('./data/negative2_samples.csv', delimiter=',')

    res = pd.concat([pos, neg1, neg2])

    train = res[res['set'] == 'train']
    test = res[res['set'] == 'test']

    return train[feature_names].values, test[feature_names].values, train['label'].values, test['label'].values

if __name__ == '__main__':

    x_train, x_test, y_train, y_test = get_all_features()

    y_train = np.where(y_train > 0, 1, 0)
    y_test = np.where(y_test > 0, 1, 0)

    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2, random_state=1)

    dtrain = xgb.DMatrix(x_train, label=y_train, feature_names=feature_names)
    dvalid = xgb.DMatrix(x_valid, label=y_valid, feature_names=feature_names)
    dtest = xgb.DMatrix(x_test, label=y_test, feature_names=feature_names)

    params = {
        'max_depth': 8,
        'eta': 1,
        'objective': 'binary:logistic',
        'eval_metric': 'error',
        'silent': 1,
    }

    evallist = [(dvalid, 'eval')]

    bst = xgb.train(params, dtrain, num_boost_round=500, evals=evallist, early_stopping_rounds=20)

    pred = bst.predict(dtest, ntree_limit=bst.best_ntree_limit)
    pred = np.where(pred > 0.5, 1, 0)
    print(pred.shape)
    print(bst.get_score())
    print(classification_report(y_test, pred))

    bst.save_model('model.xgb')
