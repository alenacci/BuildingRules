__author__ = 'andreuke'
# !/usr/bin/env python
import numpy as np
# import matplotlib.pyplot as plt
import math
import json
from datetime import timedelta, datetime

STEP = 1



def timeToFloat(time):
    timeComponents = time.split(':')
    return float(timeComponents[0]) + float(timeComponents[1]) / 60.0


def model(t_min, t_max, h_rise, h_set, t_max_prev, h_set_prev, t_min_next, h_rise_next, x):
    # Times
    h_set = timeToFloat(h_set)
    h_rise = timeToFloat(h_rise)
    h_set_prev = timeToFloat(h_set_prev)
    h_rise_next = timeToFloat(h_rise_next)
    h_max = h_set - 4  # Max is reached 4 hours before sunset

    # Temp
    t_set = t_max - 0.39 * (t_max - t_min_next)
    t_set_prev = t_max_prev - 0.39 * (t_max_prev - t_min)

    if x <= h_rise:
        return t_set_prev + (t_min - t_set_prev) / math.sqrt(h_rise + 24 - h_set_prev) * math.sqrt(x + 24 - h_set_prev)
    elif x <= h_max:
        return t_min + (t_max - t_min) * math.sin((x - h_rise) / float(h_max - h_rise) * math.pi / 2.0)
    elif x <= h_set:
        return t_set + (t_max - t_set) * math.sin((math.pi / 2.0) + (x - h_max) / 4.0 * math.pi / 2.0)
    else:
        return t_set + (t_min_next - t_set) / math.sqrt(h_rise_next + 24 - h_set) * math.sqrt(x - h_set)


# filter_min:int, filter_max:int, start_date = %m-%d, end_date = %m-%d, start_time = int, end_time = int
def external_temperature_probability(filter_min, filter_max, start_date=None, end_date=None, start_time=None,
                                     end_time=None):
    print filter_min, filter_max, start_date, end_date, start_time, end_time
    with open('app/backend/controller/influenceManager/data/temp.json') as data_file:
        data = json.load(data_file)

    with open('app/backend/controller/influenceManager/data/sunset.json') as sunset_file:
        sunset_data = json.load(sunset_file)

    start_time = start_time or 0
    end_time = end_time or 24

    filtered_data = filter_by_date(data, start_date=start_date, end_date=end_date)
    aggregate = 0.0

    x = np.linspace(start_time, end_time, float(24) / STEP + 1)

    for date, d in filtered_data.iteritems():
        # print 'START'
        date = datetime.strptime(date, "%Y-%m-%d")
        t_min = int(d['min'])
        t_max = int(d['max'])
        if filter_max < t_min or filter_min > t_max:
            aggregate += 0.001
        else:
            if date > datetime(2006, 1, 1):
                day_before = date - timedelta(days=1)
            else:
                day_before = date

            if date < datetime(2015, 12, 31):
                day_after = date + timedelta(days=1)
            else:
                day_after = date

            h_rise = sunset_data[date.strftime("%m-%d")]['sunrise']
            h_set = sunset_data[date.strftime("%m-%d")]['sunset']
            t_max_prev = int(data[day_before.strftime("%Y-%-m-%-d")]['max'])
            h_set_prev = sunset_data[day_before.strftime("%m-%d")]['sunset']
            t_min_next = int(data[day_after.strftime("%Y-%-m-%-d")]['min'])
            h_rise_next = sunset_data[day_after.strftime("%m-%d")]['sunrise']

            # print t_min, t_max, h_rise, h_set, t_max_prev, h_set_prev, t_min_next, h_rise_next
            # print x

            data_points = model(t_min, t_max, h_rise, h_set, t_max_prev, h_set_prev, t_min_next, h_rise_next, x)
            # print data_points

            total = len(data_points)
            sat = len([p for p in data_points if filter_min <= p and p <= filter_max])

            aggregate += float(sat) / total

    return float(aggregate) / len(filtered_data)


# date to be passed in %m-%d format
def filter_by_date(data, format=None, start_date=None, end_date=None):
    if start_date == None and end_date == None:
        return data
    else:
        new_data = {}

        format = format or "%Y-%m-%d"

        for k, v in data.iteritems():
            date = datetime.strptime(k, format)
            year = str(date.year)
            start = datetime.strptime(year + "-" + start_date, "%Y-%m-%d")
            end = datetime.strptime(year + "-" + end_date, "%Y-%m-%d")

            if start <= date and date <= end:
                new_data[k] = v
        print 'new_data.len', len(new_data)
        return new_data


# start_time:int, end_time:int, weekday:'Sunday...'
def occupancy_probability(start_time=None, end_time=None, weekday=None):
    start_time = start_time or 0
    end_time = end_time or 24

    weekday_probabilities = [0.02, 0.02, 0.035, 0.035, 0.055, 0.085, 0.195, 0.425, 0.61, 0.755, 0.81, 0.81, 0.755,
                             0.795, 0.82, 0.805, 0.65, 0.44, 0.22, 0.165, 0.095, 0.065, 0.035, 0.02]
    weekend_probability = 0.01

    probabilities = weekday_probabilities[start_time:end_time]
    if weekday in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        return float(sum(probabilities)) / len(probabilities)
    elif weekday in ['Saturday', 'Sunday']:
        return weekend_probability
    else:
        return (5 * float(sum(probabilities)) / len(probabilities) + 2 * weekend_probability) / 7.0


def date_probability(start_date, end_date):
    start = datetime.strptime(start_date, "%m-%d")
    end = datetime.strptime(end_date, "%m-%d")

    days = (end - start).days

    return (days + 1) / 365.0


def time_probability(start_time, end_time):
    return (end_time - start_time + 1) / 24.0


def day_probability():
    return 1 / 7.0


# Dummy implementation
def weather_probability():
    return 1 / 3.0


def room_temperature_probability(filter_min, filter_max, start_date=None, end_date=None, start_time=None,
                                 end_time=None):
    start_time = start_time or 0
    end_time = end_time or 24

    print filter_min, filter_max, start_date, end_date, start_time, end_time

    with open('app/backend/controller/influenceManager/data/room_temp.json') as data_file:
        data = json.load(data_file)

    data = filter_by_date(data, format='%m-%d', start_date=start_date, end_date=end_date)

    aggregate = 0.0
    count = 0
    for day, values in data.iteritems():
        for hour, distribution in values.iteritems():
            if start_time <= int(hour) and int(hour) <= end_time:
                if filter_max < distribution['min'] or filter_min > distribution['max']:
                    aggregate += 0.001
                else:
                    total_occurrencies = 0
                    for value, occurrencies in distribution['values'].iteritems():
                        if filter_min <= int(value) and int(value) <= filter_max:
                            # print day, hour, distribution, value, occurrencies, aggregate
                            total_occurrencies += occurrencies
                    aggregate += total_occurrencies / float(distribution['total'])
                count += 1

    return aggregate / float(count)


def probability(external_temp_min=None, external_temp_max=None, weather=None, occupancy=None, room_temp_min=None,
                room_temp_max=None, start_date=None, end_date=None, start_time=None, end_time=None, day=None, priority=None):
    probability = priority or 1
    print probability

    if external_temp_min and external_temp_max:
        ext_temp_prob = external_temperature_probability(external_temp_min, external_temp_max, start_date, end_date,
                                                         start_time, end_time)
        print 'ext', ext_temp_prob
        probability *= ext_temp_prob

    if weather:
        weather_prob = weather_probability()
        print 'weather', weather_prob
        probability *= weather_prob

    if occupancy != None:
        occupancy_prob = occupancy_probability(start_time, end_time, day)
        if occupancy == True:
            print 'occupancy', occupancy_prob
            probability *= occupancy_prob
        else:
            print 'occupancy', (1-occupancy_prob)
            probability *= (1 - occupancy_prob)

    if room_temp_min and room_temp_max:
        room_temp_prob = room_temperature_probability(room_temp_min, room_temp_max, start_date, end_date, start_time,
                                                      end_time)
        print 'room_temp_prob', room_temp_prob
        probability *= room_temp_prob

    if start_date and end_date:
        date_prob = date_probability(start_date, end_date)
        print 'date_prob', date_prob
        probability *= date_prob

    if start_time and end_time:
        time_prob = time_probability(start_time, end_time)
        print 'time_prob', time_prob
        probability *= time_prob

    if day:
        day_prob = day_probability()
        print 'day_prob', day_prob
        probability *= day_prob

    return probability

model = np.vectorize(model)