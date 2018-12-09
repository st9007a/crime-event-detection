#!/usr/bin/env python3
from .querylib.weather import Weather
from .querylib.timeinfo import Timeinfo
from .querylib.location import Location

_w = Weather()
_t = Timeinfo()
_l = Location()

def reset_grid_size(grid_size):
    global _l
    _l = Location(grid_size)

def get(query_list, date, time_slot, lat, lon):
    w_query = []
    t_query = []
    l_query = []

    res = {}

    for q in query_list:
        if q in _w.handler:
            w_query.append(q)
        elif q in _t.handler:
            t_query.append(q)
        elif q in _l.handler:
            l_query.append(q)
        else:
            print('Unknown query:', q)
            exit()

    w_res = _w.query(date, w_query)
    t_res = _t.query(date, time_slot, t_query)
    l_res = _l.query(lat, lon, l_query)

    res = {**res, **{k: v for k, v in zip(w_query, w_res)}}
    res = {**res, **{k: v for k, v in zip(t_query, t_res)}}
    res = {**res, **{k: v for k, v in zip(l_query, l_res)}}

    ret = [None] * len(query_list)

    for k in res:
        ret[query_list.index(k)] = res[k]

    return ret
