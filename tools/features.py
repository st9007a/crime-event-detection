#!/usr/bin/env python3
import re
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder

time_slot = {
    'midnight': 0,
    'morning': 1,
    'afternoon': 2,
    'night': 3,
}

selected_columns = ['Date', 'Time slot', 'Latitude', 'Longitude']
weather = pd.read_csv('../data/Weather.csv', delimiter=',')
weather = weather.set_index('datetime')

def datetime_format_transform(datetime_str, input_form, output_form):
    date_obj = datetime.strptime(datetime_str, input_form)

    if date_obj.minute > 30 and (date_obj.month != 12 and date_obj.day != 31) or (date_obj.month == 1 and date_obj.day == 1):
        date_obj = date_obj + timedelta(hours=1)

    date_obj = date_obj.replace(minute=0, second=0)

    return date_obj.strftime(output_form)

def dataset_select(datetime_str, input_form):
    date_obj = datetime.strptime(datetime_str, input_form)

    return date_obj.day % 2

def build_numpy_data(csv_file, random_sample=None):

    train = []
    test = []

    data = pd.read_csv(csv_file, delimiter=',')

    if random_sample is not None:
        data = data.sample(frac=random_sample, random_state=0)

    for idx, row in tqdm(data[selected_columns].iterrows()):
        date = row.iloc[0]
        date = datetime_format_transform(date, input_form='%m/%d/%Y %H:%M:%S', output_form='%Y-%m-%d %H:%M:%S')

        time = row.iloc[1]
        time = time_slot[time]

        weather_info = weather.loc[date].values
        weather_info = np.reshape(weather_info, [-1])

        if weather_info.shape[0] != 6:
            print('Date not found:', date)
            exit()

        # Time slot as feature
        features = np.append(weather_info, time)

        # geolocation as feature
        features = np.append(features, [row.iloc[2], row.iloc[3]])

        # odd day or even day: for train test split
        dataset_id = dataset_select(date, '%Y-%m-%d %H:%M:%S')

        if dataset_id == 0:
            train.append(features)
        else:
            test.append(features)

    train = np.array(train)
    train = np.delete(train, [3], axis=1)

    test = np.array(test)
    test = np.delete(test, [3], axis=1)

    return train, test

if __name__ == '__main__':

    pos_train, pos_test = build_numpy_data('../data/positive.csv', random_sample=1)
    pos_train_label = np.array([1] * pos_train.shape[0])
    pos_test_label = np.array([1] * pos_test.shape[0])

    neg1_train, neg1_test = build_numpy_data('../data/negative1.csv', random_sample=0.6)
    neg1_train_label = np.array([0] * neg1_train.shape[0])
    neg1_test_label = np.array([0] * neg1_test.shape[0])

    neg2_train, neg2_test = build_numpy_data('../data/negative2.csv', random_sample=0.06)
    neg2_train_label = np.array([0] * neg2_train.shape[0])
    neg2_test_label = np.array([0] * neg2_test.shape[0])

    train_data = np.concatenate([pos_train, neg1_train, neg2_train], axis=0)
    test_data = np.concatenate([pos_test, neg1_test, neg2_test], axis=0)

    train_label = np.concatenate([pos_train_label, neg1_train_label, neg2_train_label], axis=0)
    test_label = np.concatenate([pos_test_label, neg1_test_label, neg2_test_label], axis=0)

    print(train_data.shape, train_label.shape)
    print(test_data.shape, test_label.shape)

    np.save('../data/x_train.npy', train_data)
    np.save('../data/y_train.npy', train_label)
    np.save('../data/x_test.npy', test_data)
    np.save('../data/y_test.npy', test_label)
