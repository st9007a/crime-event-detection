#!/usr/bin/env python3
from datetime import datetime

import numpy as np

class Timeinfo():

    def __init__(self):

        self.time_slot = {
            'midnight': 0,
            'morning': 1,
            'afternoon': 2,
            'night': 3,
        }

        self.handler = {
            'is_holiday': self.get_is_holiday,
        }

    def get_is_holiday(self, time_stamp):
        if time_stamp.weekday() < 5:
            return 0
        return 1

    def query(self, time_stamp, input_form, time_slot, query_list=[]):
        ret = []
        time_stamp = datetime.strptime(time_stamp, input_form)

        for q in query_list:
            if q == 'time_slot':
                ret.append(self.time_slot[time_slot])
            else:
                ret.append(self.handler[q](time_stamp))

        return ret