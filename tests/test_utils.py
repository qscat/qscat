# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import pytest
from qgis.core import QgsVectorLayer
from qgis.testing import start_app

from qscat.core.utils.date import (
    convert_to_decimal_year,
    extract_month_year,
    get_day_of_year,
)
from qscat.core.utils.layer import is_field_in_layer
from qscat.core.utils.number import locale_safe_float, locale_safe_int

start_app()


def test_utils_date():
    """Test utility date functions."""
    assert extract_month_year("01/2022") == (1, 2022)
    assert extract_month_year("12/1990") == (12, 1990)
    assert extract_month_year("2/1995") == (2, 1995)

    with pytest.raises(ValueError):
        extract_month_year("0/2022")
    with pytest.raises(ValueError):
        extract_month_year("13/2022")
    with pytest.raises(ValueError):
        extract_month_year("2022/03")

    with pytest.raises(TypeError):
        extract_month_year(2022)
        extract_month_year(2022.0)
        extract_month_year([2022])
        extract_month_year((2022,))
        extract_month_year(None)

    assert get_day_of_year(1, 2022) == 1
    assert get_day_of_year(2, 2022) == 32
    assert get_day_of_year(3, 2023) == 60
    assert get_day_of_year(3, 2024) == 61

    assert convert_to_decimal_year("01/2022") == 2022.0
    assert convert_to_decimal_year("2/2022") == 2022.09
    assert convert_to_decimal_year("3/2023") == 2023.16
    assert convert_to_decimal_year("3/2024") == 2024.17


def test_utils_is_field_in_layer():
    """Test if field is in the layer function."""
    layer = QgsVectorLayer(
        "LineString?crs=EPSG:4326&field=id:integer&field=name:string(20)",
        "test_layer",
        "memory",
    )

    assert is_field_in_layer("id", layer) is True
    assert is_field_in_layer("name", layer) is True
    assert is_field_in_layer("non_existent", layer) is False


def test_locale_safe_float():
    """Test locale-safe float conversion function."""
    # Test basic conversions
    assert locale_safe_float("95.00") == 95.0
    assert locale_safe_float("95,00") == 95.0
    assert locale_safe_float("95") == 95.0
    assert locale_safe_float("0") == 0.0
    assert locale_safe_float("0.0") == 0.0
    assert locale_safe_float("0,0") == 0.0
    
    # Test negative numbers
    assert locale_safe_float("-95.00") == -95.0
    assert locale_safe_float("-95,00") == -95.0
    
    # Test larger numbers with thousands separators
    assert locale_safe_float("1,234.56") == 1234.56  # US format
    assert locale_safe_float("1.234,56") == 1234.56  # European format
    assert locale_safe_float("1234.56") == 1234.56   # No thousands separator
    assert locale_safe_float("1234,56") == 1234.56   # European, no thousands separator
    
    # Test numbers that are already numeric
    assert locale_safe_float(95) == 95.0
    assert locale_safe_float(95.5) == 95.5
    
    # Test whitespace handling
    assert locale_safe_float(" 95.00 ") == 95.0
    assert locale_safe_float(" 95,00 ") == 95.0
    
    # Test scientific notation
    assert locale_safe_float("1.5e2") == 150.0
    
    # Test edge cases that should raise errors
    with pytest.raises(ValueError):
        locale_safe_float("")
    with pytest.raises(ValueError):
        locale_safe_float("   ")
    with pytest.raises(ValueError):
        locale_safe_float(None)
    with pytest.raises(ValueError):
        locale_safe_float("abc")
    with pytest.raises(ValueError):
        locale_safe_float("95.00.00")  # Multiple decimal points


def test_locale_safe_int():
    """Test locale-safe int conversion function."""
    # Test basic conversions
    assert locale_safe_int("95") == 95
    assert locale_safe_int("0") == 0
    
    # Test negative numbers
    assert locale_safe_int("-95") == -95
    
    # Test larger numbers with thousands separators
    assert locale_safe_int("1,234") == 1234  # US format thousands separator
    assert locale_safe_int("1.234") == 1234  # European format thousands separator
    assert locale_safe_int("1234") == 1234   # No separator
    
    # Test numbers with trailing zeros that should be considered integers
    assert locale_safe_int("95.00") == 95
    assert locale_safe_int("95,00") == 95
    
    # Test numbers that are already numeric
    assert locale_safe_int(95) == 95
    assert locale_safe_int(95.0) == 95
    
    # Test whitespace handling
    assert locale_safe_int(" 95 ") == 95
    
    # Test edge cases that should raise errors
    with pytest.raises(ValueError):
        locale_safe_int("")
    with pytest.raises(ValueError):
        locale_safe_int("   ")
    with pytest.raises(ValueError):
        locale_safe_int(None)
    with pytest.raises(ValueError):
        locale_safe_int("abc")
    with pytest.raises(ValueError):
        locale_safe_int("95.50")  # Non-zero decimal part
    with pytest.raises(ValueError):
        locale_safe_int("95,50")  # Non-zero decimal part
