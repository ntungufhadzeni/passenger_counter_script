import pandas as pd
from datetime import datetime, timedelta
from passenger_counter import schedule


def add_run(arg_df, route):
    stations = {'F1': {
        'start': 316,
        'end': '316.1',
        'b_start': 315,
        'b_end': 312,
        'stops': ['306', '307', '308', '310', '311', '312'],
        'route': 'F1 - Flora Park'
    },
        'TE4': {
            'start': 509,
            'end': '509.1',
            'b_start': 500,
            'b_end': 501,
            'stops': ['200', '201', '202', '203', '204', '205', '206', '207', '208', '209'],
            'route': 'TE4 - Seshego - Madiba Park'

        },
        'F4B': {
            'start': 409,
            'end': '409.1',
            'b_start': 401,
            'b_end': 407,
            'stops': ['402', '403', '404', '405', '406'],
            'route': 'F4B - Westernburg'
        },
        'TE5B': {
            'start': 509,
            'end': '509.1',
            'b_start': 500,
            'b_end': 501,
            'stops': ['101', '102', '103', '104', '105'],
            'route': 'TE5B - Seshego'
        }
    }

    data = stations[route]
    if route == 'F1':
        df_s = pd.DataFrame(schedule.f1)
    elif route == 'F4B':
        df_s = pd.DataFrame(schedule.f4)
    elif route == 'TE4':
        df_s = pd.DataFrame(schedule.te4)
    else:
        df_s = pd.DataFrame(schedule.te5b)

    dt_s = arg_df.loc[0, 'Date']
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
