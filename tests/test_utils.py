# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import pytest

from qgis.core import QgsVectorLayer
from qgis.testing import start_app

from qscat.core.utils.date import convert_to_decimal_year
from qscat.core.utils.date import extract_month_year
from qscat.core.utils.date import get_day_of_year
from qscat.core.utils.layer import is_field_in_layer

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

    assert is_field_in_layer("id", layer) == True
    assert is_field_in_layer("name", layer) == True
    assert is_field_in_layer("non_existent", layer) == False
