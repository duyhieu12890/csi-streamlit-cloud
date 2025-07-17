import time
from datetime import datetime


def get_today_str():
    today = datetime.today()
    return str(today.year), f"{today.month:02d}", f"{today.day:02d}"

def get_value(data, year, month, day):
    return data.get(year, {}).get(month, {}).get(day)

def update_value(data, year, month, day, value):
    if year not in data:
        data[year] = {}
    if month not in data[year]:
        data[year][month] = {}
    data[year][month][day] = value