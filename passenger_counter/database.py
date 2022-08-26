from sqlalchemy import create_engine
import numpy as np
from .te5b_stops import get_te5b_stops
from .runs import add_run

DBNAME = 'defaultdb'
USER = 'doadmin'
PASSWORD = 'AVNS_6dxIhC_uyPodpL_'
HOST = 'leeto-dashboard-db-do-user-9909499-0.b.db.ondigitalocean.com'
PORT = '25060'

engine = create_engine('postgresql://' + USER + ':' + PASSWORD + '@' + HOST + ':' + PORT + '/' + DBNAME)


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
