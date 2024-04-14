# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from unittest.mock import patch

from qgis.testing import start_app

from qgis.core import QgsCoordinateReferenceSystem

from qscat.core.transects import prechecks

start_app()


def test_prechecks():
    """Test CRS prechecks function."""
    # Do not test the display_message function (requires iface messageBar())
    with patch('qscat.core.transects.display_message', return_value=None):
        crs1 = QgsCoordinateReferenceSystem('EPSG:4326')
        crs2 = QgsCoordinateReferenceSystem('EPSG:3857')
        crs3 = QgsCoordinateReferenceSystem('EPSG:32651')

        assert prechecks(crs1, crs1, crs1) == True
        assert prechecks(crs1, crs2, crs3) == False
        assert prechecks(crs2, crs1, crs1) == False
        assert prechecks(crs1, crs2, crs1) == False