#!/usr/bin/env python3
from pprint import pprint

import pandas as pd

if __name__ == '__main__':

    loc = pd.read_csv('../data/locCategory.csv')
    pprint(set(loc['Type'].values))
