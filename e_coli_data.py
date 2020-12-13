import pandas as pd
from typing import List
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


def infections_by_code(code: str) -> pd.DataFrame:
    """Returns a panda dataframe containing all the infection data for the
    hospital specified by the code"""
    tp = ECOLI_DATA.transpose()
    new_header = tp.iloc[0]
    tp.columns = new_header
    return tp[code]


def infections_by_codes(codes: List[str]) -> pd.DataFrame:
    """Return a data set containing infections for all the hospitals specified
    in the codes"""
    dfs = []
    for code in codes:
        dfs.append(infections_by_code(code))
    result = dfs[0]
    for i in range(len(dfs) - 1):
        result = pd.merge(result, dfs[i + 1], right_index=True, left_index=True)
    return result


def total_infections_by_codes(codes: List[str]) -> pd.Series:
    """Returns a series of the total infections in the hospitals specified
    in codes"""
    df = infections_by_codes(codes)
    if type(df) == pd.Series:
        df = df.to_frame()
    result = df.sum(axis=1)
    result = result.drop('Trust Code')
    return result

def get_str_date(date: datetime.date) -> str:
    """Turns a datetime.date object into a string with form yyyy-mm-dd"""
    return date.strftime("20%y-%m-%d")
