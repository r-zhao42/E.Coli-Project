from typing import Optional
import e_coli_data as ECOLI_DATA
import projection
import location_data
from plotly_graph import plot_graph, plot_individual
from plotly_map import plot_map

HOSPITAL_DATA_WITH_LOCATIONS = 'Monthly E.Coli 2012-2020 with Location.csv'
WEATHER_STATIONS_DIRECTORY = 'Temperature Data'

# Copyright: Hayk Nazaryan, Ryan Zhao, Joanne Pan, Cliff Zhang


def run_all_stations(end_year: int) -> None:
    """This function is responsible for running the entirety our project:

    It should first run a modelled graph of the all the UK E.Coli infections until the specified year
    in the argument end_year

    And second, overlay of data on a map using MapBox. The data is the percent of
    increase of E.Coli cases from 2020 until the given end_year in the argument of
    run_all_stations.

    """

    plot_graph(end_year)
    plot_map(end_year)


def run_individual_station(name: str, start_year: int, end_year: int) -> None:
    """Returns the individual plotly graph of individual weather stations.

    Usage:
    >>> run_individual_station('waddington', 2010, 2100)

    """
    identifier = name.lower().replace(' ', '').replace('-', '')
    projections = projection.get_data_station(identifier, start_year, end_year)

    data = location_data.find_closest_weather_stations(HOSPITAL_DATA_WITH_LOCATIONS,
                                                       WEATHER_STATIONS_DIRECTORY)

    history = ECOLI_DATA.total_infections_by_codes(data[identifier])
    history_frame = history.to_frame().reset_index()
    history_frame.columns = ['x', 'y']

    plot_individual(name, history_frame, projections)

    print(projection)
    print(history_frame)


if __name__ == '__main__':
    print('This is main')

