#!/usr/bin/env python3
from datetime import datetime

import numpy as np
import pandas as pd
from tqdm import tqdm

def update(csv_file):
    new_data = []
    data = pd.read_csv(csv_file, delimiter=',')

    for idx, row in tqdm(data.iterrows()):
        date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')

        if date.month == 12:
            data.at[idx, 'set'] = 'test'
        elif date.month == 11:
            data.at[idx, 'set'] = 'valid'
        else:
            data.at[idx, 'set'] = 'train'

    data.to_csv(csv_file, index=False)

if __name__ == '__main__':

    update('../data/positive_samples.csv')
    update('../data/negative1_samples.csv')
    update('../data/negative2_samples.csv')
