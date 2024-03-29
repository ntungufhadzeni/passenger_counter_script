from plyer import notification
import json
import requests
import pandas as pd
from passenger_counter import stops_routes, database, te5b_stops, runs
import os


def main():
    PATH = r'C:\Users\Administrator\Documents\Ntungufhadzeni\passenger_counter_script'
    routes = ('F1', 'F4B', 'TE4', 'TE5B')
    notification.notify(title="Passenger Counter Script",
                        message="The script is running",
                        timeout=10)
    with open(os.path.join(PATH, 'times.json'), 'r') as file:
        last_update = json.load(file)
        file.close()

    url = "http://192.168.5.100:5555/passenger-data"
    params = last_update
    res = requests.get(url, params=params)

    data = json.loads(res.text)

    df = pd.DataFrame(data)
    df = stops_routes.get_stops_routes(df)
    if df.shape[0] > 0:
        df = df.sort_values(by=['Alarm Time'])
        df.reset_index(inplace=True, drop=True)
        print('Getting stops for TE5B...')
        df = te5b_stops.get_te5b_stops(df)
        print('Getting runs...')
        for route in routes:
            df = runs.add_run(df, route)
        df['Alarm Time'] = df['Alarm Time'].apply(lambda x: x.strftime('%Y-%m-%d %X'))
        last_row = df.shape[0] - 1
        last_time = df['Alarm Time'][last_row]
        print('Exporting to database...')
        database.to_database(df)
        last_update['time'] = last_time
        with open(os.path.join(PATH, 'times.json'), 'w') as file:
            json.dump(last_update, file)
            file.close()

    notification.notify(title="Passenger Counter Script",
                        message="The script has successfully ended task",
                        timeout=10)


if __name__ == '__main__':
    main()
