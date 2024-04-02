import unittest

from qscat.core.utils import convert_to_decimal_year
from qscat.core.utils import extract_month_year


class TestUtils(unittest.TestCase):
    # extract_month_year()
    def test_extract_month_year(self):
        self.assertEqual(extract_month_year("01/2022"), (1, 2022))
        self.assertEqual(extract_month_year("12/1990"), (12, 1990))
        self.assertEqual(extract_month_year("2/1995"), (2, 1995))

    def test_invalid_month_year_format(self):
        with self.assertRaises(ValueError):
            extract_month_year("0/2022")
        with self.assertRaises(ValueError):
            extract_month_year("13/2022")
        with self.assertRaises(ValueError):
            extract_month_year("2022/03")
        with self.assertRaises(ValueError):
            extract_month_year("/2023")
        with self.assertRaises(ValueError):
            extract_month_year("10/")

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            extract_month_year(None)
        with self.assertRaises(TypeError):
            extract_month_year(12)
        with self.assertRaises(TypeError):
            extract_month_year(1.2)
        with self.assertRaises(TypeError):
            extract_month_year([1, 2])
        with self.assertRaises(TypeError):
            extract_month_year((1, 2))

    # convert_to_decimal_year()
    def test_convert_to_decimal_year(self):
        self.assertEqual(convert_to_decimal_year(1, 2022), 2022.08)
        self.assertEqual(convert_to_decimal_year(9, 1996), 1996.75)
        self.assertEqual(convert_to_decimal_year(2, 1995), 1995.17)

    def test_invalid_month_year_value(self):
        with self.assertRaises(ValueError):
            convert_to_decimal_year(0, 2022)
        with self.assertRaises(ValueError):
            convert_to_decimal_year(13, 2022)
        with self.assertRaises(ValueError):
            convert_to_decimal_year(12, -2022)
        with self.assertRaises(ValueError):
            convert_to_decimal_year(12, -2022)

    def test_wrong_type_month_year_value(self):
        with self.assertRaises(TypeError):
            convert_to_decimal_year(None, 2022)
        with self.assertRaises(TypeError):
            convert_to_decimal_year(12.2, 2022)
        with self.assertRaises(TypeError):
            convert_to_decimal_year([1, 2], 2022)
        with self.assertRaises(TypeError):
            convert_to_decimal_year((1, 2), 2022)
        with self.assertRaises(TypeError):
            convert_to_decimal_year("1", 2022)
        with self.assertRaises(TypeError):
            convert_to_decimal_year(1, None)
        with self.assertRaises(TypeError):
            convert_to_decimal_year(1, 2022.2)
        with self.assertRaises(TypeError):
            convert_to_decimal_year(1, [1, 2])
        with self.assertRaises(TypeError):
            convert_to_decimal_year(1, (1, 2))
        with self.assertRaises(TypeError):
            convert_to_decimal_year(1, "1")
            