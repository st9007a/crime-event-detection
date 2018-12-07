#!/usr/bin/env python3
import re
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm

time_slot = {
    'midnight': 0,
    'morning': 1,
    'afternoon': 2,
    'night': 3,
}

selected_columns = ['Date', 'Time slot']
weather = pd.read_csv('../data/Weather.csv', delimiter=',')

def datetime_format_transform(datetime_str, input_form, output_form):
    date_obj = datetime.strptime(datetime_str, input_form)

    if date_obj.minute > 30 and (date_obj.month != 12 and date_obj.day != 31) or (date_obj.month == 1 and date_obj.day == 1):
        date_obj = date_obj + timedelta(hours=1)

    date_obj = date_obj.replace(minute=0, second=0)

    return date_obj.strftime(output_form)

def build_numpy_data(csv_file, random_sample=None):

    data = pd.read_csv(csv_file, delimiter=',')

    if random_sample is not None:
        data = data.sample(frac=random_sample, random_state=0)

    array = []

    for idx, row in data[selected_columns].iterrows():
        date = row.iloc[0]
        date = datetime_format_transform(date, input_form='%m/%d/%Y %H:%M:%S', output_form='%Y-%m-%d %H:%M:%S')

        time = row.iloc[1]
        time = time_slot[time]

        weather_info = weather.loc[weather['datetime'] == date].values
        weather_info = np.reshape(weather_info, [-1])

        if weather_info.shape[0] != 7:
            print('Date not found:', date)
            exit()

        array.append(np.append(weather_info, time))

    array = np.array(array)
    array = np.delete(array, [0, 4], axis=1)

    return array

if __name__ == '__main__':

    pos_data = build_numpy_data('../data/positive.csv', random_sample=1)
    pos_label = np.array([1] * pos_data.shape[0])

    print('Build positive data')

    neg1_data = build_numpy_data('../data/negative1.csv', random_sample=0.6)
    neg1_label = np.array([0] * neg1_data.shape[0])

    print('Build negative 1 data')

    neg2_data = build_numpy_data('../data/negative1.csv', random_sample=0.06)
    neg2_label = np.array([0] * neg2_data.shape[0])

    print('Build negative 2 data')

    data = np.concatenate([pos_data, neg1_data, neg2_data], axis=0)
    label = np.concatenate([pos_label, neg1_label, neg2_label], axis=0)

    print(data.shape, label.shape)

    np.save('../data/x.npy', data)
    np.save('../data/y.npy', label)
