import os
import configparser
import math

from datetime import datetime
from pathlib import Path

from qgis.core import QgsProject
from qgis.core import QgsApplication


def extract_month_year(month_year_string):
    """Extract the month and year from a string.

    Args:
        month_year_string (str): string in the format 'mm/yyyy'

    Returns:
        tuple: (month, year)

    Raises:
        ValueError: if month_year_string is not in the format 'mm/yyyy'
        TypeError: if month_year_string is not a string
    """
    try:
        date = datetime.strptime(month_year_string, '%m/%Y')
    except ValueError:
        raise ValueError("Month and year must be in the format 'mm/yyyy'.")
    except TypeError:
        raise TypeError("Month and year must be a string.")
    else:
        return date.month, date.year
    
def get_day_of_year(month, year):
    """get day of year from month and year, 
    with default of day 01 for every month"""
    date = datetime(year, month, 1) # 1 = default day 1 every month
    day_of_year = date.timetuple().tm_yday
    return day_of_year


def convert_to_decimal_year(month_year_string):
    month, year = extract_month_year(month_year_string)
    if not isinstance(month, int) or not isinstance(year, int):
        raise TypeError("Month and year must be integers.")

    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12.")

    if year < 0:
        raise ValueError("Year must be positive.")
    
    day_of_year = get_day_of_year(month, year)
    decimal_year = round(year + (day_of_year / 365.242199), 2)
    return decimal_year


def datetime_now():
    return datetime.now().strftime("%m-%d-%y %H-%M-%S")


def get_duration_ms(end, start):
    #return int(round((end-start) * 1000))
    return round(end-start, 10)
