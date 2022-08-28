import pandas as pd
from datetime import datetime, timedelta
from passenger_counter import schedule


def get_te5b_stops(arg_df):
    df_s = pd.DataFrame(schedule.te5b)
    dt_s = arg_df.loc[0, 'Date']
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
