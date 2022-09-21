import time

import pandas as pd
import numpy as np
import requests
import warnings
import json

from urllib3.exceptions import NewConnectionError, ConnectTimeoutError

from . import location
from .dates import add_date, add_week


def get_stops_routes(arg_df):
    warnings.filterwarnings('ignore')
    arg_df['Stop Name'] = np.NaN
    arg_df['Route'] = np.NaN
    stops_dict = {
        'F1 - Flora Park': ['316', '300', '301', '302', '303', '304', '305', '306', '307', '308', '309',
                            '310', '311', '312', '313', '314', '315'],
        'TE4 - Seshego - Madiba Park': ['500', '200', '202', '204', '206', '207', '208', '209', '205', '203',
                                        '201', '501', '503', '505', '507', '508', '509'],
        'TE5B - Seshego': ['506', '504', '502', '101', '102', '103', '104', '105'],
        'F4B - Westernburg': ['409', '400', '401', '402', '403', '404', '405', '407', '408']
    }
    print('Getting stop names and routes...')
    for index in arg_df.index:
        v = arg_df.loc[index, 'GNSS']

        if not str(v).startswith('-'):
            continue

        try:
            cords = v.split(',')
        except AttributeError:
            continue

        cords_lat = cords[0]
        cords_lon = cords[1]
        if cords_lat.find('.') != -1:
            lat = cords_lat
            lon = cords_lon
        else:
            lat = cords_lat[:3] + '.' + cords_lat[3:]
            lon = cords_lon[:2] + '.' + cords_lon[2:]

        if location.is_layover(lat, lon):
            arg_df.loc[index, 'Stop Name'] = 'LayOver'
            continue
        elif location.is_fuel_wise(lat, lon):
            arg_df.loc[index, 'Stop Name'] = 'Fuel Wise'
            continue

        url = 'http://46.101.72.176:8080/otp/routers/default/index/stops'
        params = {'lat': lat, 'lon': lon, 'radius': 300}

        try:
            response = requests.get(url, params=params)
        except:
            time.sleep(10)
            response = requests.get(url, params=params)

        if response.status_code == 200:
            data_res = json.loads(response.text)
            if len(data_res) > 1:
                dist_list = []
                for i in range(len(data_res)):
                    dist_list.append(data_res[i]['dist'])
                min_dist = min(dist_list)
                min_index = dist_list.index(min_dist)
                stop_name = data_res[min_index]['name']
            elif len(data_res) == 1:
                stop_name = data_res[0]['name']
            else:
                continue
        else:
            continue

        church = {'410': "F4B - Westernburg", '316': "F1 - Flora Park", '409': "F4B - Westernburg",
                  '509': "TE4 - Seshego - Madiba Park"}
        stop = stop_name

        if stop in church.keys():
            stop_name = 'Church Street'
            route = church[stop]
            arg_df.loc[index, 'Stop Name'] = stop_name
            arg_df.loc[index, 'Route'] = route
        else:
            for key in stops_dict.keys():
                if stop_name in stops_dict[key]:
                    route = key
                    arg_df.loc[index, 'Stop Name'] = stop_name
                    arg_df.loc[index, 'Route'] = route
                    break

    arg_df = add_date(arg_df)
    arg_df['Week'] = arg_df['DOW'].apply(add_week)
    arg_df = arg_df[arg_df['Route'].notna() & arg_df['Alarm Time'].notna()]
    arg_df = arg_df[
        ['Bus No', 'IN', 'Out', 'Number of people', 'Alarm Time', 'GNSS', 'Stop Name', 'Route', 'Date', 'DOW', 'MY',
         'Week']]
    arg_df['Alarm Time'] = pd.to_datetime(arg_df['Alarm Time'])
    arg_df['Run'] = np.NaN
    arg_df['Run_id'] = np.NaN

    return arg_df
