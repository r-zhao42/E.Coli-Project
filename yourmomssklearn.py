"""DOCSTRING TODO"""

from typing import Dict
import sys
import numpy
import pandas as pd
from sklearn import linear_model
from misc1 import find_closest_weather_stations
from e_coli_data import total_infections_by_codes
import misc1
import e_coli_data

sys.setrecursionlimit(10**6)


ECOLI_FILE = 'Monthly E.Coli 2012-2020 with Location.csv'
TEMPERATURE_DIR = 'Temperature Data'
WEATHER_STATIONS = find_closest_weather_stations(ECOLI_FILE, TEMPERATURE_DIR)


def get_model_station(station: str) -> tuple:
    """Take a station name and returns a tuple containing a time-temperature and
    temperature-E.Coli model.

    Preconditions:
        - station in weather_stations
    """
    path = station + 'data.txt'
    with open('Temperature Data/' + path, 'r') as txt:
        temperature_data = txt.readlines()
        temperature_data = [row.split() for row in temperature_data]
        temperature_data = temperature_data[7:]

    if len(temperature_data[-1]) <= 2:
        temperature_data.pop()
    for entry in temperature_data:
        try:
            float(entry[0])
        except ValueError:
            temperature_data.remove(entry)
        if entry[2][-1] == "*":
            entry[2] = entry[2][:-1]
        if entry[3][-1] == "*":
            entry[3] = entry[3][:-1]

    temperature_to_ecoli_model = temp_ecoli_model(temperature_data, station)

    time_to_temperature_model = time_temp_model(temperature_data)

    return (time_to_temperature_model, temperature_to_ecoli_model)


def temp_ecoli_model(temperature_data: any, station: str) -> any:
    """Returns a linear regression model for temperature to E.Coli infections
    at the given station"""

    ecoli = total_infections_by_codes(WEATHER_STATIONS[station]).to_frame()
    ecoli_time = ecoli.index.tolist()
    ecoli_time = [date[:7] for date in ecoli_time]
    ecoli_value = ecoli.values.tolist()
    temperature_x = []
    ecoli_y = []
    for entry in temperature_data:
        year = entry[0]
        month = entry[1]
        if len(month) == 1:
            month = '0' + month
        time = "{}-{}".format(year, month)
        if time in ecoli_time:
            mean_temperature = (float(entry[2]) + float(entry[3])) / 2
            ecoli_index = ecoli_time.index(time)
            ecoli = ecoli_value[ecoli_index][0]
            temperature_x.append([mean_temperature])
            ecoli_y.append(ecoli)

    temperature_x, ecoli_y = numpy.array(temperature_x), numpy.array(ecoli_y)
    temperature_to_ecoli_model = linear_model.LinearRegression()

    temperature_to_ecoli_model.fit(temperature_x, ecoli_y)
    return temperature_to_ecoli_model


def time_temp_model(temperature_data: any) -> any:
    """Returns a sklearn linear regression model for time and temperature for the station
    specified in temperature_data"""

    time_x = []
    temperature_y = []

    for entry in temperature_data:
        if entry[2] != '---' and entry[3] != '---':
            year = float(entry[0])
            month = float(entry[1])
            time = year + (month - 1) / 12
            mean_temperature = (float(entry[2]) + float(entry[3])) / 2
            time_x.append([time])
            temperature_y.append(mean_temperature)

    time_x, temperature_y = numpy.array(time_x), numpy.array(temperature_y)
    time_to_temperature_model = linear_model.LinearRegression()
    time_to_temperature_model.fit(time_x, temperature_y)
    return time_to_temperature_model


def get_temp_prediction(station: str, end_year: int) -> float:
    """Returns the predicted temperature at the given station at the given year"""
    path = station + 'data.txt'
    with open('Temperature Data/' + path, 'r') as txt:
        temperature_data = txt.readlines()
        temperature_data = [row.split() for row in temperature_data]
        temperature_data = temperature_data[7:]

    if len(temperature_data[-1]) <= 2:
        temperature_data.pop()
    for entry in temperature_data:
        try:
            float(entry[0])
        except ValueError:
            temperature_data.remove(entry)
        if entry[2][-1] == "*":
            entry[2] = entry[2][:-1]
        if entry[3][-1] == "*":
            entry[3] = entry[3][:-1]

    time_temp = time_temp_model(temperature_data)
    return time_temp.predict([[end_year]])


def temp_prediction_all(end_year: int) -> pd.DataFrame:
    """Returns a dataframe matching station name to predicted temperature
    at end_year"""
    temp_df = pd.DataFrame(columns=['location', 'temp'])
    for station in WEATHER_STATIONS:
        df2 = pd.DataFrame([[station, get_temp_prediction(station, end_year)]], columns=['location', 'temp'])
        temp_df = temp_df.append(df2)
    return temp_df


def get_data_station(station: str, start_year: int, end_year: int) -> pd.DataFrame:
    """Returns a dataframe containing the projected average monthly E.Coli infections
    from the start_year to the end_year

    Preconditions:
        - stations in weather_stations
    """
    model = get_model_station(station)
    df = pd.DataFrame(columns=['years', 'ecoli'])

    time_to_temp_model = model[0]
    temp_to_ecoli_model = model[1]

    for year in range(start_year, end_year + 1):
        temperature_prediction = time_to_temp_model.predict([[year]])[0]
        ecoli_prediction = temp_to_ecoli_model.predict([[temperature_prediction]])
        df2 = pd.DataFrame([[year, ecoli_prediction]], columns=['years', 'ecoli'])
        df = df.append(df2)
    return df


def get_data_all_stations(start_year: int, end_year: int) -> Dict[str, pd.DataFrame]:
    """Returns a dictionary that matches the string of the station name to a dataframe
    containing the projected average monthly E.Coli infections between start_year
    and end_year
    """
    result_so_far = {}
    for station in WEATHER_STATIONS:
        result_so_far[station] = get_data_station(station, start_year, end_year)
    return result_so_far


def get_percentage_increase(end_year: int) -> Dict[str, float]:
    """Returns a dictionary matching the string of a station name to a float
     representing the percentage increase in average monthly E.Coli incidence at end_year"""
    projection = get_data_all_stations(2020, end_year)
    hospital_data = misc1.HOSPITAL_DATA_WITH_LOCATIONS
    weather_data = misc1.WEATHER_STATIONS_DIRECTORY
    station_codes = misc1.find_closest_weather_stations(hospital_data, weather_data)
    result_so_far = {}
    for station in projection:
        past_data = e_coli_data.total_infections_by_codes(station_codes[station])
        total = past_data.sum(axis=0)
        average = total / len(past_data.index)
        df = projection[station]
        for i in range(len(df.index)):
            df.iat[i, 1] = ((df.iat[i, 1] / average) - 1) * 100
        result_so_far[station] = float(df.iloc[-1, -1])

    return result_so_far


def get_total_data(start_year: int, end_year: int) -> pd.DataFrame:
    """Returns a dataframe containing the projected years and average monthly E.Coli infections
    in that year between the start_year and end_year"""
    dfs = []
    for station in WEATHER_STATIONS:
        dfs.append(get_data_station(station, start_year, end_year))
    df = dfs[0]
    for i in range(len(dfs) - 1):
        df = df.merge(dfs[i + 1], on='years')
    sums = df.iloc[:, 1:].sum(axis=1)
    sums.name = 'ecoli'
    years = df.iloc[:, 0]
    years.name = 'years'
    result = pd.concat([years, sums], axis=1)
    return result


# if __name__ == '__main__':
#     import python_ta
#
#     python_ta.check_all(config={
#         'extra-imports': ['python_ta.contracts', 'numpy', 'pandas',
#                           'misc1', 'e_coli_data', 'sklearn', 'sys'],
#         'allowed-io': ['get_model_station'],
#         'max-line-length': 100,
#         'disable': ['R1705', 'C0200']
#     })
#
#     import python_ta.contracts
#
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
#
#     import pytest
#
#     pytest.main(['yourmomssklearn.py'])
