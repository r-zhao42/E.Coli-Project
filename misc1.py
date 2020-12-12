"""CSC110 Fall 2020 Assignment 3, Part 2: Text Generation, One-Word Context Model

Instructions (READ THIS FIRST!)
===============================
Implement each of the functions in this file. As usual, do not change any function headers
or preconditions. You do NOT need to add doctests.

You may create some additional helper functions to help break up your code into smaller parts.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 David Liu and Mario Badr.
"""
import random
from typing import Dict, Set, Any, Tuple, List
import netCDF4 as nc
import urllib.request
import json
import mysql.connector
from datetime import date, datetime, timedelta
import sys
import codecs
import csv
import pandas as pd
import lxml
import html5lib
from urllib.request import Request, urlopen
import pprint
import io
import statistics
import os
import math
import random

# txt = 'C:/Users/Hayk/Desktop/yur2.txt'
txt2 = 'C:/Users/Hayk/Desktop/Project/Temperature/lerwickdata.txt'
txt3 = 'C:/Users/Hayk/Desktop/ecolilocations.csv'

# df = pd.read_csv(txt, delimiter='\t', names=['yyyy'])
gf = pd.read_csv(txt3)

# print(df.head(20))
locations_list = [x for x in gf['Location']]




with open(txt2, 'r') as ok:
    data = ok.readlines()

    reus = [x.split() for x in data]



def get_monthly_average(year: int, month: int, my_data: list) -> float:
    """Returns the average from min_temp and max_temp of the given data set

    Preconditions:
        - self.year >= 1978
    """

    for x in my_data[1:]:
        if x[0] == str(year):
            if x[1] == str(month):
                return (float(x[2]) + float(x[3])) / 2


def get_location(my_data: list) -> Tuple[float, float]:
    """"Returns the location of a specific weather station data"""

    latitude = ''
    longitude = ''

    for x in my_data:
        for i in range(len(x) - 1):
            if x[i] == 'Lat':
                latitude = latitude + x[i + 1]
            if x[i] == 'Lon':
                longitude = longitude + x[i + 1]

    lat_processed = remove_chars(latitude)
    long_processed = remove_chars(longitude)

    return float(lat_processed), float(long_processed)


def remove_chars(string: str) -> str:
    """ Removes any unneccessary characters besides numbers, especially commas

    Usage:

    >>> remove_chars('-1.835, ')
    '-1.835'
    """
    punctuation = {',', '(', ')'}

    if not string.isalnum():
        processed = [x for x in string if x not in punctuation]

        return ''.join(processed)

    else:
        return string


my_directory = 'C:/Users/Hayk/Desktop/Project/Temperature'


def sort_weather_stations(directory: Any) -> Dict[str, Tuple[float, float]]:
    """Returns all the weather stations in the directory, sorted in a dictionary. The keys are the names
    of the weather stations and the values are their locations."""

    my_dict = {}

    for file in os.listdir(directory):
        if file.endswith('.txt'):
            path = directory + '/' + file
            with open(path, 'r') as new:
                file_data = new.readlines()
                listed_data = [x.split() for x in file_data]

            location = get_location(listed_data)
            my_dict[listed_data[0][0]] = location

    return my_dict


# print(get_monthly_average(1995, 3, reus))




# This is the intro of the data. The actual data follows after this.
# intro = [x for x in data][:5]
#
# rest = [x for x in data[5:]]
#
#
# yum = io.StringIO(str(rest))
# br = pd.read_table(yum)

# print(br)

req = Request('https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/cambornedata.txt', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

uhuh = webpage.decode()

EARTH_RADIUS = 6373.0  # km
COURIER_SPEED = 20  # km/h


def calculate_distance(location1: Tuple[float, float],
                       location2: Tuple[float, float]) -> float:
    """Return the distance between location1 and location 2 given in (latitude, longitude) pairs.

    We illustrate using *spherical* distance rather than Euclidean (2-D) distance.
    It doesn't make a difference in our case because the points are very close together,
    but we wanted to illustrate yet another example of implementing a mathematical
    formula in Python!

    Further reading: https://en.wikipedia.org/wiki/Great-circle_distance

    NOTE: the locations are in degrees, but the math module functions expect radians.
    Use math.radians to convert from degrees to radians before computing the given formula.
    """

    delta_lat = math.radians(abs(location1[0] - location2[0]))
    delta_long = math.radians(abs(location1[1] - location2[1]))

    theta = 2 * math.asin(math.sqrt(math.sin(delta_lat / 2) ** 2) +
                          math.cos(location1[0]) * math.cos(location2[0]) * (math.sin(delta_long) / 2) ** 2)

    return theta * EARTH_RADIUS


def get_distances_between(directory: Any, hospitals: List[Tuple[float, float]]):
    """Returns the distance between each hospital and weather station in a tuple (hospital, weather station, distance)
    """
    my_list = []

    for file in os.listdir(directory):
        if file.endswith('.txt'):
            path = directory + '/' + file
            with open(path, 'r') as new:
                file_data = new.readlines()
                listed_data = [x.split() for x in file_data]

            location = get_location(listed_data)

    return my_list


def sort_hospitals(hospitals: Any):
    """Sorts hospitals with their name and location in a tuple of latitude and longitude

    Preconditions:
        - len([x for x in hosp['Location']]) == len([x for x in hosp['Trust Code']])
    """
    my_list = []

    hosp = pd.read_csv(hospitals)
    locations = [transform_string_coords(x) for x in hosp['Location']]
    names = [x for x in hosp['Trust Code']]

    for i in range(len(locations)):
        my_list.append((names[i], locations[i]))

    return my_list


def transform_string_coords(coords: str) -> Tuple[float, float]:
    """Returns the Tuple[float, float] version of the coordinates that were in a string.
 -
    >>> transform_string_coords('(15.235, -56.1265)')
    (15.235, -56.1265)

    """

    no_brackets_version = remove_chars(coords)

    splits = no_brackets_version.split(' ')

    return float(splits[0]), float(splits[-1])



def check_space(string: str):
    """Return if there is a space after a comma. """

    for i in range(len(string)):
        if string[i] == ',':
            return string[i+1] == ' '

