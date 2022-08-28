from sqlalchemy import create_engine

DBNAME = 'defaultdb'
USER = 'doadmin'
PASSWORD = 'AVNS_6dxIhC_uyPodpL_'
HOST = 'leeto-dashboard-db-do-user-9909499-0.b.db.ondigitalocean.com'
PORT = '25060'

engine = create_engine('postgresql://' + USER + ':' + PASSWORD + '@' + HOST + ':' + PORT + '/' + DBNAME)


def to_database(arg_df):
    arg_df = arg_df.reset_index(drop=True)
    # arg_df.to_sql('trips_v2', engine, if_exists='append', chunksize=1000)
    arg_df['Alarm Time'] = arg_df['Alarm Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    arg_df.to_sql('trips_development_v2', engine, if_exists='append', chunksize=1000)
    print('Done Exporting.')
