import re
from datetime import datetime

from qgis.core import Qgis

from qscat.core.inputs import Inputs
from qscat.core.messages import display_message


def validate_shorelines_layer(qdw):
    """Validate the selected shorelines layer.

    Args:
        qdw (QscatDockWidget): QscatDockWidget instance.

    Returns:
        bool: True if valid, False otherwise.
    """
    shorelines_layer = qdw.qmlcb_shorelines_layer.currentLayer().name()

    # Check features existence
    if qdw.qmlcb_shorelines_layer.currentLayer().featureCount() <= 0:
        display_message(
            f'The selected shorelines layer "{shorelines_layer}" has no features.',
            Qgis.Warning,
        )
        return False

    # Check fields existence
    if qdw.qfcb_shorelines_date_field.count() <= 0:
        display_message(
            f'The selected shorelines layer "{shorelines_layer}" has no fields.',
            Qgis.Warning,
        )
        return False

    # Check if dates are valid
    # Get selected date field values as list of strings
    inputs = Inputs(qdw)
    dates = inputs.shorelines_dates()
    invalid = get_invalid_date_inputs(dates)

    if invalid:
        # Show only 10 invalid date inputs
        if len(invalid) <= 10:
            invalid_str = ", ".join(invalid)
            message = f'The selected shorelines layer "{shorelines_layer}" has invalid date inputs: {invalid_str}.'
        elif len(invalid) > 10:
            invalid_str = ", ".join(invalid[:10])
            message = f'The selected shorelines layer "{shorelines_layer}" has invalid date inputs: {invalid_str}...'

        display_message(message, Qgis.Warning)
        return False

    return True


def is_valid_date_input(date):
    """Validate if date has the format mm/yyyy. Months should be in 1-12 and
    year should be in 1900-2100.

    Args:
        date (str): A date input value in selected shoreline date field.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Null/none values
    if not date:
        return False

    # Check if in mm/yyyy format
    pattern = r"^(0[1-9]|1[0-2])/(\d{4})$"
    match = re.match(pattern, date)

    # Check if month is 1-12 and year is 1900-2100
    if match:
        month = int(match.group(1))
        year = int(match.group(2))
        if 1 <= month <= 12 and 1900 <= year <= 2100:
            return True
        else:
            return False
    else:
        return False


def get_invalid_date_inputs(dates):
    """Get invalid date inputs using `is_valid_date_input()`.

    Args:
        dates (list[str]): A list of date input values in selected shoreline date field.

    Returns:
        list[str]: A list of invalid date inputs.
    """
    invalid = []
    for date in dates:
        if not is_valid_date_input(date):
            invalid.append(date)

    return invalid
