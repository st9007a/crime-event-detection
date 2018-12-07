#!/usr/bin/env python3
import pickle

import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

if __name__ == '__main__':

    x_train = np.load('data/x_train.npy')
    y_train = np.load('data/y_train.npy')

    x_test = np.load('data/x_test.npy')
    y_test = np.load('data/y_test.npy')

    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2, random_state=1)

    clf = XGBClassifier(
        max_depth=5,
        learning_rate=0.1,
        objective='binary:logistic',
        n_estimators=100,
    )

    clf.fit(
        x_train, y_train,
        eval_set=[(x_valid, y_valid)],
        eval_metric='error',
        early_stopping_rounds=10
    )

    print(clf.feature_importances_)

    pred = clf.predict(x_test, ntree_limit=clf.best_ntree_limit)
    print(pred.shape)
    print(pred)

    print(classification_report(y_test, pred))

    with open('model.pkl', 'wb') as p:
        pickle.dump(clf, p, pickle.HIGHEST_PROTOCOL)
