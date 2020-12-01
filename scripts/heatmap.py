import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import datetime
from enum import Enum
from functools import reduce
import os


class Week(Enum):
    U45 = 0
    U46 = 1
    U47 = 2


def parse(month, day, hour, minute, second):
    return '2020' + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second


def generate_time_intervals(starttime, endtime, step_per_hour):
    times = []
    for t in range(starttime,endtime + 1):
        for step in range(step_per_hour):
            min = step * 60 / step_per_hour
            time = f'{t:02d}:{int(min):02d}:00'
            times.append(time)
            if t == endtime:
                break
    return times


def create_discretized_activations(dates, time_slots):
    discretized_activations = {}

    week_index = 0
    day_index = 0
    time_index = 0

    timestamp_before = pd.Timestamp(f'{dates[week_index][day_index]} {time_slots[time_index]}')
    timestamp_after = pd.Timestamp(f'{dates[week_index][day_index]} {time_slots[time_index + 1]}')

    for el in [df.iloc[x] for x in range(0, df.size)]:
        print("Checking:", el['month_day_hour_minute_second'])
        if timestamp_before <= el['month_day_hour_minute_second'] < timestamp_after:
            date_key = f'{el["month_day_hour_minute_second"].date()}'
            time_key = f'{time_slots[time_index][:2]} {time_slots[time_index + 1][:2]}'
            if discretized_activations.get(date_key) is None:
                discretized_activations[date_key] = {}

            discretized_activations[date_key][time_key] = discretized_activations[date_key].get(time_key, 0) + 1

        elif timestamp_after <= el['month_day_hour_minute_second']:
            time_index += 1
            if time_index == len(time_slots) - 1:
                time_index = 0
                day_index += 1
            if day_index == len(dates[week_index]):
                day_index = 0
                week_index += 1
            if week_index == len(dates.keys()):
                break
            timestamp_before = pd.Timestamp(f'{dates[week_index][day_index]} {time_slots[time_index]}')
            timestamp_after = pd.Timestamp(f'{dates[week_index][day_index]} {time_slots[time_index + 1]}')
    return discretized_activations


def dict_to_ndarray(dict, days, times):
    arr = np.zeros((len(days), len(times)))

    for i, day in enumerate(days):
        for j, time in enumerate(times):
            if j == len(times) - 1:
                break
            day_dict = dict.get(day, {})
            time_key = f'{time[:2]} {times[j + 1][:2]}'
            actvns = day_dict.get(time_key, 0)
            arr[i][j] = actvns
    return arr


include_dates = {
    Week.U45.value: ['2020-11-02', '2020-11-03', '2020-11-04', '2020-11-05', '2020-11-06'],
    Week.U46.value: ['2020-11-09', '2020-11-10', '2020-11-11', '2020-11-12', '2020-11-13'],
    Week.U47.value: ['2020-11-16', '2020-11-17', '2020-11-18', '2020-11-19', '2020-11-20'],
}
time_intervals = generate_time_intervals(7, 16, 1)

df = pd.read_csv(os.path.join(os.pardir, 'activations', 'activations_all_corrected.csv'),
                 names=['month', 'day', 'hour', 'minute', 'second'],
                 parse_dates=[[0, 1, 2, 3, 4]],
                 date_parser=parse,
                 )
discretized_activations = create_discretized_activations(include_dates, time_intervals)

# Heatmap
ndf = pd.DataFrame(discretized_activations)
ax = sb.heatmap(ndf.transpose(), cmap="Blues", linewidths=0.2, cbar_kws={"shrink": .8})
ws_index = 0
for key in include_dates.keys():
    ws = len(include_dates[key])
    ws_index += ws
    ax.axhline(ws_index, color='white', lw=10)
ax.set(xlabel='Time Interval', ylabel='Dates')
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
plt.show()


'''
        6   7   8   9   10  11  12  13  14  15  16  17  18  19  20
    Mon
    Tue
U45 Wed
    Thu
    Fri
    
    Mon
    Tue
U46 Wed
    Thu
    Fri

    Mon
    Tue
U47 Wed
    Thu
    Fri
'''



