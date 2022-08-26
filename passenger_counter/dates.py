import pandas as pd


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


def add_week(name):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekends = ['Sunday', 'Saturday']
    if name in weekends:
        return 'Weekend'
    elif name in weekdays:
        return 'Weekday'
