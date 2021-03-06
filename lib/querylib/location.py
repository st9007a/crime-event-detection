#!/usr/bin/env python3
import math
import os

import numpy as np
import pandas as pd

_file_dir = os.path.dirname(os.path.realpath(__file__))

def distance(lat1, lon1, lat2, lon2):

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return c * 6371e3

class Grid():

    def __init__(self):

        self.poi = []

    def add(self, lat, lon, category):
        self.poi.append((lat, lon, category))

    def get_nearest_poi(self, lat, lon, max_distance=1000, filter_fn=None):

        candidate = [(distance(lat, lon, el[0], el[1]), el[2]) for el in self.poi]
        candidate = list(filter(lambda x: x[0] <= max_distance, candidate))

        if filter_fn is not None:
            candidate = filter(filter_fn, candidate)

        return candidate

    def get_nearest_police_station(self, lat, lon, max_distance=1000):
        candidate = [(distance(lat, lon, el[0], el[1]), el[2]) for el in self.poi]
        candidate = list(filter(lambda x: x[1] == 'Police Station' and x[0] <= max_distance, candidate))

        return len(candidate)

class Location():

    def __init__(self, grid_size=1000):

        self.handler = {
            'category': self.get_category,
            'population_density': self.get_population_density,
            'police_station_density': self.get_police_station_density,
            'night_spot_density': self.get_night_spot_density,
            'event_density': self.get_event_density,
            'residence_density': self.get_residence_density,
            'art_enter_density': self.get_art_enter_density,
            'college_density': self.get_college_density,
            'outdoors_density': self.get_outdoors_density,
            'professional_density': self.get_professional_density,
            'shop_density': self.get_shop_density,
            'travel_density': self.get_travel_density,
        }

        self.grid_size = grid_size
        self.build_grid_map()

    def get_grid(self, lat, lon, return_near_grids=False):
        i_h = distance(lat, lon, self.min_lat, lon) // self.grid_size
        i_w = distance(lat, lon, lat, self.min_lon) // self.grid_size

        if i_h >= self.h:
            i_h = self.h - 1

        if i_w >= self.w:
            i_w = self.w - 1

        idx = int(i_h * self.w + i_w)

        if not return_near_grids:
            return self.grids[idx]

        near_grids = []

        if idx + 1 < self.num_grids:
            near_grids.append(self.grids[idx + 1])

            if idx + 1 + self.w < self.num_grids:
                near_grids.append(self.grids[idx + 1 + self.w])

            if idx + 1 - self.w >= 0:
                near_grids.append(self.grids[idx + 1 - self.w])

        if idx - 1 >= 0:
            near_grids.append(self.grids[idx - 1])

            if idx - 1 + self.w < self.num_grids:
                near_grids.append(self.grids[idx - 1 + self.w])

            if idx - 1 - self.w >= 0:
                near_grids.append(self.grids[idx - 1 - self.w])

        if idx + self.w < self.num_grids:
            near_grids.append(self.grids[idx + self.w])

        if idx - self.w >= 0:
            near_grids.append(self.grids[idx - self.w])

        return self.grids[idx], near_grids

    def build_grid_map(self):
        self.table = pd.read_csv('%s/loc.csv' % _file_dir, delimiter=',')
        self.max_lat = -math.inf
        self.max_lon = -math.inf
        self.min_lat = math.inf
        self.min_lon = math.inf
        self.grids = []
        self.categories = []
        self.second_categories = []
        self.root_categories = []
        self.category_map = {}

        for idx, row in self.table.iterrows():
            lat = row.loc['Latitude']
            lon = row.loc['Longitude']

            if row.loc['Type'] not in self.categories:
                self.categories.append(row.loc['Type'])

            if row.loc['Second Type'] not in self.second_categories:
                self.second_categories.append(row.loc['Second Type'])

            if row.loc['Root Type'] not in self.root_categories:
                self.root_categories.append(row.loc['Root Type'])

            self.category_map[row.loc['Type']] = {
                'second': row.loc['Second Type'],
                'root': row.loc['Root Type'],
            }

            if lat > self.max_lat:
                self.max_lat = lat
            elif lat < self.min_lat:
                self.min_lat = lat

            if lon > self.max_lon:
                self.max_lon = lon
            elif lon < self.min_lon:
                self.min_lon = lon

        self.h = distance(self.max_lat, self.min_lon, self.min_lat, self.min_lon) // self.grid_size + 1
        self.h = int(self.h)
        self.w = distance(self.min_lat, self.max_lon, self.min_lat, self.min_lon) // self.grid_size + 1
        self.w = int(self.w)

        self.num_grids = int(self.h * self.w)

        for _ in range(self.num_grids):
            self.grids.append(Grid())

        for idx, row in self.table.iterrows():
            lat = row.loc['Latitude']
            lon = row.loc['Longitude']
            category = row.loc['Type']

            self.get_grid(lat, lon).add(lat, lon, category)

    def get_category(self, lat, lon):

        grid, near_grids = self.get_grid(lat, lon, return_near_grids=True)
        pois = []

        pois.extend(grid.get_nearest_poi(lat, lon, max_distance=100))

        for g in near_grids:
            pois.extend(g.get_nearest_poi(lat, lon, max_distance=100))

        if len(pois) == 0:
            return len(self.categories)

        pois.sort(key=lambda x: x[0])

        return self.categories.index(pois[0][1])

    def get_parent_category(self, lat, lon):
        num = self.get_category(lat, lon)

        if num == len(self.categories):
            return len(self.second_categories), len(self.root_categories)

        c = self.categories[num]

        return self.second_categories.index(self.category_map[c]['second']), self.root_categories.index(self.category_map[c]['root'])

    def get_police_station_density(self, lat, lon):
        grid, near_grids = self.get_grid(lat, lon, return_near_grids=True)

        num = grid.get_nearest_police_station(lat, lon, max_distance=1000)

        for g in near_grids:
            num += g.get_nearest_police_station(lat, lon, max_distance=1000)

        return num

    def get_density(self, lat, lon, category):

        def filter_fn(el):
            return self.category_map[el[1]]['root'] == category

        grid, near_grids = self.get_grid(lat, lon, return_near_grids=True)
        pois = []

        pois.extend(grid.get_nearest_poi(lat, lon, max_distance=500, filter_fn=filter_fn))

        for g in near_grids:
            pois.extend(g.get_nearest_poi(lat, lon, max_distance=500, filter_fn=filter_fn))

        return len(pois)

    def get_night_spot_density(self, lat, lon):
        return self.get_density(lat, lon, 'Nightlife Spot')

    def get_event_density(self, lat, lon):
        return self.get_density(lat, lon, 'Event')

    def get_residence_density(self, lat, lon):
        return self.get_density(lat, lon, 'Residence')

    def get_art_enter_density(self, lat, lon):
        return self.get_density(lat, lon, 'Arts & Entertainment')

    def get_college_density(self, lat, lon):
        return self.get_density(lat, lon, 'College & University')

    def get_outdoors_density(self, lat, lon):
        return self.get_density(lat, lon, 'Outdoors & Recreation')

    def get_professional_density(self, lat, lon):
        return self.get_density(lat, lon, 'Professional & Other Places')

    def get_shop_density(self, lat, lon):
        return self.get_density(lat, lon, 'Shop & Service')

    def get_travel_density(self, lat, lon):
        return self.get_density(lat, lon, 'Travel & Transport')

    def get_population_density(self, lat, lon):
        grid, near_grids = self.get_grid(lat, lon, return_near_grids=True)
        pois = []

        pois.extend(grid.get_nearest_poi(lat, lon, max_distance=500))

        for g in near_grids:
            pois.extend(g.get_nearest_poi(lat, lon, max_distance=500))

        return len(pois)

    def query(self, lat, lon, query_list=[]):
        return [self.handler[el](lat, lon) for el in query_list]

if __name__ == '__main__':

    # print(distance(41.941562, -87.664011, 41.942562, -87.664011))
    # print(distance(41.941562, -87.664011, 41.941562, -87.665011))
    l = Location()
    print(l.categories)
