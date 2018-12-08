#!/usr/bin/env python3
import math

import numpy as np
import pandas as pd

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

    def get_nearest_poi(self, lat, lon, k=1):

        candidate = [(distance(lat, lon, el[0], el[1]), el[2]) for el in self.poi]
        candidate.sort(key=lambda x: x[0])

        return candidate[:k]

class Location():

    def __init__(self, csvfile, grid_size=1000):

        self.handler = {
            'category': self.get_category,
            # 'population_density': self.get_population_density,
            # 'police_station_density': self.get_population_density,
        }

        self.grid_size = grid_size
        self.build_grid_map(csvfile)

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

    def build_grid_map(self, csvfile):
        self.table = pd.read_csv(csvfile, delimiter=',')
        self.max_lat = -math.inf
        self.max_lon = -math.inf
        self.min_lat = math.inf
        self.min_lon = math.inf
        self.grids = []
        self.categories = set()

        for idx, row in self.table.iterrows():
            lat = row.loc['Latitude']
            lon = row.loc['Longitude']
            self.categories.add(row.loc['Type'])

            if lat > self.max_lat:
                self.max_lat = lat
            elif lat < self.min_lat:
                self.min_lat = lat

            if lon > self.max_lon:
                self.max_lon = lon
            elif lon < self.min_lon:
                self.min_lon = lon

        self.categories = list(self.categories)

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

        pois.extend(grid.get_nearest_poi(lat, lon, k=1))

        for g in near_grids:
            pois.extend(g.get_nearest_poi(lat, lon, k=1))

        if len(pois) == 0:
            return len(self.categories)

        pois.sort(key=lambda x: x[0])

        return self.categories.index(pois[0][1])

    def query(self, lat, lon, query_list=[]):
        return [self.handler[el](lat, lon) for el in query_list]

if __name__ == '__main__':

    loc = Location('../../data/locCategory.csv')
