from plyer import notification
import json
import requests
import pandas as pd
from passenger_counter import stops_routes, database


def main():
    notification.notify(title="Passenger Counter Script",
                        message="The script is running",
                        timeout=10)
    with open('times.json', 'r') as file:
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
        last_row = df.shape[0] - 1
        last_time = df['Alarm Time'][last_row]
        database.to_database(df)
        last_update['time'] = last_time
        with open('times.json', 'w') as file:
            json.dump(last_update, file)
            file.close()

    notification.notify(title="Passenger Counter Script",
                        message="The script has successfully ended task",
                        timeout=10)


if __name__ == '__main__':
    main()
