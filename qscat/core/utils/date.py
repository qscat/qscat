from datetime import datetime


def extract_month_year(month_year_string):
    """Extract the month and year from a string.

    Args:
        month_year_string (str): Format 'mm/yyyy'

    Returns:
        tuple[int, int]: month and year
        
    Raises:
        ValueError: if month_year_string is not in the format 'mm/yyyy'

    Note:
        May change in the future if we consider input MM/DD/YYYY.
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
    """Get the day of a year given a month and year. Since we only have the 
    month and year, we set the day to 1.

    Args:
        month (int): 1-12
        year (int): YYYY

    Returns:
        int: day of year

    Note:
        May change in the future if we consider input MM/DD/YYYY.
    """
    date = datetime(year, month, 1) # 1 = default day 1 every month
    day_of_year = date.timetuple().tm_yday
    return day_of_year


def convert_to_decimal_year(month_year_string):
    """Convert a month and year string to a decimal year.

    Args:
        month_year_string (str): Format 'mm/yyyy'

    Returns:
        float: decimal year
    """
    month, year = extract_month_year(month_year_string)
    day_of_year = get_day_of_year(month, year)

    # Credit for the idea: https://code.usgs.gov/cch/dsas/-/blob/master/src/DSASv5Addin/DSASUtility.vb
    decimal_year = round(year + (day_of_year / 365.242199), 2)
    return decimal_year


def datetime_now():
    return datetime.now().strftime("%m-%d-%y %H-%M-%S")


def get_duration_ms(end, start):
    #return int(round((end-start) * 1000))
    return round(end-start, 10)
