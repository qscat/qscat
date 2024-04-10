# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import pytest

from qscat.core.utils import extract_month_year


def test_extract_month_year():
    assert extract_month_year("01/2022") == (1, 2022)
    assert extract_month_year("12/1990") == (12, 1990)
    assert extract_month_year("2/1995") == (2, 1995)

    with pytest.raises(ValueError):
        extract_month_year("0/2022")
    with pytest.raises(ValueError):
        extract_month_year("13/2022")
    with pytest.raises(ValueError):
        extract_month_year("2022/03")
    with pytest.raises(ValueError):
        extract_month_year("/2023")
    with pytest.raises(ValueError):
        extract_month_year("10/")


def test_invalid_month_year_format():
    with pytest.raises(TypeError):
        extract_month_year(None)
    with pytest.raises(TypeError):
        extract_month_year(12)
    with pytest.raises(TypeError):
        extract_month_year(1.2)
    with pytest.raises(TypeError):
        extract_month_year([1, 2])
    with pytest.raises(TypeError):
        extract_month_year((1, 2))