#!/usr/bin/env python3
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

if __name__ == '__main__':

    x = np.load('data/x.npy')
    y = np.load('data/y.npy')
    print(x.shape)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)
    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2, random_state=1)

    clf = XGBClassifier(
        max_depth=5,
        learning_rate=1,
        objective='binary:logistic',
        n_estimators=500,
    )

    clf.fit(
        x_train, y_train,
        eval_set=[(x_valid, y_valid)],
        eval_metric='error',
        early_stopping_rounds=10
    )

    pred = clf.predict(x_test, ntree_limit=clf.best_ntree_limit)
    print(pred.shape)
    print(pred)

    print(classification_report(y_test, pred))
