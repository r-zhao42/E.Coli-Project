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
from typing import Dict, Set, Any, Tuple, List
import pandas as pd
import os
import math

# Variables containing the paths for the files and directories. Can be used for testing.
example_txt_file = 'Temperature Data/lerwickdata.txt'
hospital_data_with_locations = 'Monthly E.Coli 2012-2020 with Location.csv'
weather_stations_directory = 'Temperature Data'

EARTH_RADIUS = 6373.0  # km

# Using pandas to read the hospital data with locations csv file.
gf = pd.read_csv(hospital_data_with_locations)


def find_closest_weather_stations(hospitals: Any, directory: Any) -> Dict[str, List[str]]:
    """Returns a dictionary with keys being weather stations and the values being the hospitals that are closest to the
    weather station"""

    # Dictionary accumulator that has keys of weather location names and values of closest hospitals
    my_dict = {}

    sorted_hospitals = sort_hospitals(hospitals)
    sorted_stations = sort_weather_stations(directory)

    for hospital in sorted_hospitals:
        min_distance = min([calculate_distance(sorted_stations[x], hospital[1]) for x in sorted_stations])

        for x in sorted_stations:
            if calculate_distance(sorted_stations[x], hospital[1]) == min_distance:
                if x in my_dict:
                    my_dict[x].append(hospital[0])

                else:
                    my_dict[x] = [hospital[0]]

    return my_dict


# ------------------------------------------HELPER FUNCTIONS-----------------------------------------------------------
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


def sort_hospitals(hospitals: Any) -> List[Tuple[str, Tuple[float, float]]]:
    """Sorts hospitals with their name and location in a tuple of latitude and longitude

    Preconditions:
        - len([x for x in hosp['Location']]) == len([x for x in hosp['Trust Code']])
    """
    # List accumulator that collects tuples of names and locations of individual hospitals
    my_list = []

    hosp = pd.read_csv(hospitals)
    locations = [transform_string_coords(x) for x in hosp['Location']]
    names = [x for x in hosp['Trust Code']]

    for i in range(len(locations)):
        my_list.append((names[i], locations[i]))

    return my_list


# Here we are opening an example .txt file and converting it into a list of lists, where each line is a list.
with open(example_txt_file, 'r') as fl:
    data = fl.readlines()

    listed_example_file = [x.split() for x in data]


def get_monthly_average(year: int, month: int, my_data: list) -> float:
    """Returns the average from min_temp and max_temp of the given data set from a specified year and month.

    Preconditions:
        - self.year >= 1978
        - 1 <= self.month <= 12
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
    """ A helper function that removes any unneccessary characters besides numbers, especially commas and brackets

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


def calculate_distance(location1: Tuple[float, float],
                       location2: Tuple[float, float]) -> float:
    """Return the distance between location1 and location 2 given in (latitude, longitude) pairs.

    This function was reused from Tutorial Week 12!
    """

    delta_lat = math.radians(abs(location1[0] - location2[0]))
    delta_long = math.radians(abs(location1[1] - location2[1]))

    theta = 2 * math.asin(math.sqrt(math.sin(delta_lat / 2) ** 2) +
                          math.cos(location1[0]) * math.cos(location2[0]) * (math.sin(delta_long) / 2) ** 2)

    return theta * EARTH_RADIUS


def transform_string_coords(coords: str) -> Tuple[float, float]:
    """Returns the Tuple[float, float] version of the coordinates that were in a string.


    Preconditions:
        - type(coords) == str

    The format of the string coords must be in the following: '(x, y)'. There must be a space inbetween the
    variables.
 -
    >>> transform_string_coords('(15.235, -56.1265)')
    (15.235, -56.1265)

    """

    no_brackets_version = remove_chars(coords)

    splits = no_brackets_version.split(' ')

    return float(splits[0]), float(splits[-1])


def check_space(string: str) -> bool:
    """Return if there is a space after a comma. This is a helper function to check if the dataset in question
    has proper formatting of string coords.

    Usage:
    >>> check_space('(52.123, -455.256)')
    True
    >>> check_space('(18.295,-97.356)')
    False

    """

    for i in range(len(string)):
        if string[i] == ',':
            return string[i+1] == ' '

        else:
            return False


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import pytest
    pytest.main(['misc1.py'])
