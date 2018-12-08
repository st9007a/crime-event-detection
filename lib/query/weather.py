#!/usr/bin/env python3
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

class Weather():

    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, csvfile):
        self.table = pd.read_csv(csvfile, delimiter=',')
        self.table = self.table.set_index('datetime')

        self.handler = {
            'humidity': self.get_humidity,
            'pressure': self.get_pressure,
            'temperature': self.get_temperature,
            'wind_direction': self.get_wind_direction,
            'wind_speed': self.get_wind_speed,
        }

    def datetime_format_transform(self, datetime_str, input_form):
        date_obj = datetime.strptime(datetime_str, input_form)

        if date_obj.minute > 30 and (date_obj.month != 12 and date_obj.day != 31) or (date_obj.month == 1 and date_obj.day == 1):
            date_obj = date_obj + timedelta(hours=1)

        return date_obj.replace(minute=0, second=0).strftime(Weather.DATE_FORMAT)

    def get_humidity(self, df):
        return df['humidity']

    def get_pressure(self, df):
        return df['pressure']

    def get_temperature(self, df):
        return df['temperature']

    def get_wind_direction(self, df):
        return df['wind_direction']

    def get_wind_speed(self, df):
        return df['wind_speed']

    def query(self, date_str, input_form, query_list=[]):
        date = self.datetime_format_transform(date_str, input_form)
        df = self.table.loc[date]

        return [self.handler[el](df) for el in query_list]

if __name__ == '__main__':

    w = Weather('../../data/Weather.csv')
