import e_coli_data as ECOLI_DATA
import yourmomssklearn
import plotly
import misc1
from plotly_graph import plot_your_mom, yourmomsweatherstation
import pandas as pd
from plotly_map import plot_map

HOSPITAL_DATA_WITH_LOCATIONS = 'Monthly E.Coli 2012-2020 with Location.csv'
WEATHER_STATIONS_DIRECTORY = 'Temperature Data'


def run_all_weather_stations():
    """This function is responsible for running our project:

    It should first run a modelled graph

    And second, an overlayed data on an image of a map.

    """

    plot_your_mom()
    plot_map(2100)


def run_individual_weather_station(name: str, start_year: int, end_year):
    """Returns the individual plotly graph of individual weather stations."""

    projection = yourmomssklearn.get_data_station(name, start_year, end_year)

    data = misc1.find_closest_weather_stations(HOSPITAL_DATA_WITH_LOCATIONS, WEATHER_STATIONS_DIRECTORY)

    history = ECOLI_DATA.total_infections_by_codes(data[name])
    history_frame = history.to_frame().reset_index()
    history_frame.columns = ['x', 'y']

    # yourmomsweatherstation(name, history_frame, projection)

    print(history_frame)


if __name__ == '__main__':
    print('This is main')
