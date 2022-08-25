from sqlalchemy import create_engine
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests
import warnings
import json
import time
from plyer import notification

DBNAME = 'defaultdb'
USER = 'doadmin'
PASSWORD = 'AVNS_6dxIhC_uyPodpL_'
HOST = 'leeto-dashboard-db-do-user-9909499-0.b.db.ondigitalocean.com'
PORT = '25060'

engine = create_engine('postgresql://' + USER + ':' + PASSWORD + '@' + HOST + ':' + PORT + '/' + DBNAME)


def get_te5b_stops(arg_df):
    df_s = pd.read_excel('schedule.xlsx', 'TE5B_Timetable')
    indexes = list(arg_df.index)
    dt_s = arg_df.loc[indexes[0], 'Date']
    routes = ['TE4 - Seshego - Madiba Park', 'TE5B - Seshego']
    stops = ['101', '102', '103', '104', '105']

    for index in df_s.index:
        start_time_str = df_s.loc[index, 509].strftime('%H:%M')
        start_str = dt_s + ' ' + start_time_str
        end_time_str = df_s.loc[index, '509.1'].strftime('%H:%M')
        end_str = dt_s + ' ' + end_time_str
        start = datetime.strptime(start_str, '%d %B %Y %H:%M') - timedelta(minutes=15)
        end = datetime.strptime(end_str, '%d %B %Y %H:%M') + timedelta(minutes=15)

        b_start_time_str = df_s.loc[index, 500].strftime('%H:%M')
        b_start_str = dt_s + ' ' + b_start_time_str
        b_end_time_str = df_s.loc[index, 501].strftime('%H:%M')
        b_end_str = dt_s + ' ' + b_end_time_str
        b_start = datetime.strptime(b_start_str, '%d %B %Y %H:%M') - timedelta(minutes=10)
        b_end = datetime.strptime(b_end_str, '%d %B %Y %H:%M') + timedelta(minutes=10)
        bus = ''

        for i in arg_df.index:
            route = arg_df.loc[i, 'Route']
            alarm = arg_df.loc[i, 'Alarm Time']
            stop = arg_df.loc[i, 'Stop Name']
            if b_start < alarm < b_end and route == 'TE5B - Seshego' and stop in stops:
                bus = arg_df.loc[i, 'Bus No']
                break

        if bus == '':
            continue

        for j in arg_df.index:
            b = arg_df.loc[j, 'Bus No']
            t = arg_df.loc[j, 'Alarm Time']
            r = arg_df.loc[j, 'Route']
            if start < t < end and r in routes and b == bus:
                arg_df.loc[j, 'Route'] = 'TE5B - Seshego'
    return arg_df


def add_run(arg_df, sheet):
    stations = {'F1 Timetable': {
        'start': 316,
        'end': '316.1',
        'b_start': 315,
        'b_end': 312,
        'stops': ['306', '307', '308', '310', '311', '312'],
        'route': 'F1 - Flora Park'
    },
        'TE4_Timetable': {
            'start': 509,
            'end': '509.1',
            'b_start': 500,
            'b_end': 501,
            'stops': ['200', '201', '202', '203', '204', '205', '206', '207', '208', '209'],
            'route': 'TE4 - Seshego - Madiba Park'

        },
        'F4B_TimeTable': {
            'start': 409,
            'end': '409.1',
            'b_start': 401,
            'b_end': 407,
            'stops': ['402', '403', '404', '405', '406'],
            'route': 'F4B - Westernburg'
        },
        'TE5B_Timetable': {
            'start': 509,
            'end': '509.1',
            'b_start': 500,
            'b_end': 501,
            'stops': ['101', '102', '103', '104', '105'],
            'route': 'TE5B - Seshego'
        }
    }

    data = stations[sheet]
    df_s = pd.read_excel('schedule.xlsx', sheet)
    indexes = list(arg_df.index)
    dt_s = arg_df.loc[indexes[0], 'Date']
    stops = data['stops']
    for index in df_s.index:
        start_time_str = df_s.loc[index, data['start']].strftime('%H:%M')
        start_str = dt_s + ' ' + start_time_str
        end_time_str = df_s.loc[index, data['end']].strftime('%H:%M')
        end_str = dt_s + ' ' + end_time_str
        start = datetime.strptime(start_str, '%d %B %Y %H:%M') - timedelta(minutes=15)
        end = datetime.strptime(end_str, '%d %B %Y %H:%M') + timedelta(minutes=15)

        b_start_time_str = df_s.loc[index, data['b_start']].strftime('%H:%M')
        b_start_str = dt_s + ' ' + b_start_time_str
        b_end_time_str = df_s.loc[index, data['b_end']].strftime('%H:%M')
        b_end_str = dt_s + ' ' + b_end_time_str
        b_start = datetime.strptime(b_start_str, '%d %B %Y %H:%M') - timedelta(minutes=10)
        b_end = datetime.strptime(b_end_str, '%d %B %Y %H:%M') + timedelta(minutes=10)
        run = df_s.loc[index, 'Run']
        bus = ''

        for i in arg_df.index:
            route = arg_df.loc[i, 'Route']
            tm = arg_df.loc[i, 'Alarm Time']
            stop = arg_df.loc[i, 'Stop Name']
            if b_start < tm < b_end and route == data['route'] and stop in stops:
                bus = arg_df.loc[i, 'Bus No']
                break

        if bus == '':
            continue

        for j in arg_df.index:
            b = arg_df.loc[j, 'Bus No']
            t = arg_df.loc[j, 'Alarm Time']
            if start < t < end and b == bus:
                arg_df.loc[j, 'Route'] = data['route']
                arg_df.loc[j, 'Run'] = run
    return arg_df


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

        if is_lay_over(lat, lon):
            arg_df.loc[index, 'Stop Name'] = 'LayOver'
            continue
        elif is_fuel_wise(lat, lon):
            arg_df.loc[index, 'Stop Name'] = 'Fuel Wise'

        url = 'http://46.101.72.176:8080/otp/routers/default/index/stops'
        params = {'lat': lat, 'lon': lon, 'radius': 300}

        try:
            response = requests.get(url, params=params)
        except:
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

    return arg_df


def add_week(name):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekends = ['Sunday', 'Saturday']
    if name in weekends:
        return 'Weekend'
    elif name in weekdays:
        return 'Weekday'


def is_fuel_wise(arg_lat, arg_lon):
    arg_lat = float(arg_lat)
    arg_lon = float(arg_lon)

    min_lat = -23.89453
    max_lat = -23.89581
    min_lon = 29.44261
    max_lon = 29.44393

    if max_lat < arg_lat < min_lat:
        if min_lon < arg_lon < max_lon:
            return True
        else:
            return False

    else:
        return False


def is_lay_over(arg_lat, arg_lon):
    arg_lat = float(arg_lat)
    arg_lon = float(arg_lon)

    min_lat = -23.89813
    max_lat = -23.89937
    min_lon = 29.44261
    max_lon = 29.44507

    if max_lat < arg_lat < min_lat:
        if min_lon < arg_lon < max_lon:
            return True
        else:
            return False

    else:
        return False


def to_database(arg_df):
    sheets = ['F1 Timetable', 'TE4_Timetable', 'F4B_TimeTable', 'TE5B_Timetable']
    arg_df['Run'] = np.NaN
    arg_df['Run_id'] = np.NaN
    dff = get_te5b_stops(arg_df)

    print('[Adding] runs')
    for sheet in sheets:
        dff = add_run(dff, sheet)

    dff = dff.reset_index(drop=True)
    # dff.to_sql('trips_v2', engine, if_exists='append', chunksize=1000)
    dff['Alarm Time'] = dff['Alarm Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    dff.to_sql('trips_development_v2', engine, if_exists='append', chunksize=1000)
    print('Done Exporting.')


def add_date(df):
    df['Date'] = pd.to_datetime(df['Alarm Time'])
    df['Year'] = df.Date.dt.year
    df['Year'] = df['Year'].astype(str)
    df['Month'] = df.Date.dt.month_name()
    df['Day'] = df.Date.dt.day
    df['Day'] = df['Day'].astype(str)
    df['DOW'] = df.Date.dt.day_name()
    df['MY'] = df.Month + ' ' + df.Year
    df['Date'] = df.Day + ' ' + df.Month + ' ' + df.Year

    return df


def main():
    notification.notify(title="Passenger Counter Script",
                        message="The script is running",
                        timeout=10)
    with open('times.json', 'r') as file:
        last = json.load(file)
        file.close()

    url = "http://192.168.5.100:8000/passenger-data"
    params = last
    res = requests.get(url, params=params)

    data = json.loads(res.text)

    df = pd.DataFrame(data)
    df = get_stops_routes(df)
    if df.shape[0] > 0:
        df = df.sort_values(by=['Alarm Time'])
        df.reset_index(inplace=True, drop=True)
        last_row = df.shape[0] - 1
        last_time = df['Alarm Time'][last_row]
        to_database(df)
        last['time'] = last_time
        with open('times.json', 'w') as file:
            json.dump(last, file)
            file.close()
    notification.notify(title="Passenger Counter Script",
                        message="The script has successfully ended task",
                        timeout=10)


if __name__ == '__main__':
    main()
