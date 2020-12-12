import pandas as pd
import math
import datetime

ECOLI_DATA = pd.read_csv('Monthly E.Coli 2012-2020.csv')

def get_total_year(year: int) -> int:
    """Returns to the total number of E.Coli cases in a given year.
    Since the data for 2012 and 2020 is not complete, the total number is only
    for a months of the year

    Preconditions:
        - 2012 <= year <= 2020
    """
    start_month = 1
    end_month = 12
    total_so_far = 0

    if year == 2012:
        start_month = 4
    elif year == 2020:
        end_month = 2

    for month in range(start_month, end_month + 1):
        total_so_far += get_total_month(year, month)

    return total_so_far


def get_monthly_average(year: int) -> float:
    """Get average monthly E.Coli Infections for the given year

    Preconditions:
        - 2012 <= year <= 2020
    """
    total_months = 12

    if year == 2012:
        total_months = 9
    elif year == 2020:
        total_months = 2

    return get_total_year(year) / total_months

def get_total_month(year: int, month: int):
    """Get total number of cases in a given month

    Preconditions:
        - 2012 <= year <= 2020
        - 1 <= month <= 12
    """
    date = datetime.date(year=year, month=month, day=1)
    date = get_str_date(date)
    return ECOLI_DATA[date].sum()

def get_str_date(date: datetime.date) -> str:
    return date.strftime("20%y-%m-%d")
