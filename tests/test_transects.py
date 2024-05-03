# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from unittest.mock import patch

from qgis.testing import start_app

from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer

from qgis.gui import QgsMapLayerComboBox

from qscat.core.transects import cast_transects
from qscat.core.transects import prechecks

start_app()


def test_cast_transects():
    """Test main cast transects function."""
    project = QgsProject.instance()
    initial_layer_count = len(project.mapLayers())

    crs = QgsCoordinateReferenceSystem("EPSG:4326")

    # Input layers
    baseline_layer = QgsVectorLayer("MultiLineString?epsg:4326", "test", "memory")
    shoreline_layer = baseline_layer = QgsVectorLayer(
        "MultiLineString?epsg:4326", "test", "memory"
    )

    # Input params
    baseline_params = {
        "baseline_layer": baseline_layer,
        "is_baseline_placement_sea": True,
        "is_baseline_placement_land": False,
        "is_baseline_orientation_land_right": True,
        "is_baseline_orientation_land_left": False,
        "placement_field": None,  #'qs_place',
        "orientation_field": None,  #'qs_orient',
        "transect_length_field": None,  #'qs_length',
    }
    shorelines_params = {
        "shorelines_layer": shoreline_layer,
    }
    transects_params = {
        "smoothing_distance": "1",
        "length": "1",
        "layer_output_name": "test_transects",
    }

    result = cast_transects(
        baseline_params, shorelines_params, transects_params, crs, QgsMapLayerComboBox()
    )

    assert len(project.mapLayers()) == initial_layer_count + 1
    assert "test_transects" in result[0].name()
    assert result[1].currentLayer() is result[0]

    # Exclude display_message() function (requires iface messageBar())
    with patch("qscat.core.transects.display_message", return_value=None):
        crs = QgsCoordinateReferenceSystem("EPSG:32651")

        result = cast_transects(
            baseline_params,
            shorelines_params,
            transects_params,
            crs,  # Different project CRS
            QgsMapLayerComboBox(),
        )
        assert result is None


def test_prechecks():
    """Test CRS prechecks function."""
    # Exclude display_message() function (requires iface messageBar())
    with patch("qscat.core.transects.display_message", return_value=None):
        crs1 = QgsCoordinateReferenceSystem("EPSG:4326")
        crs2 = QgsCoordinateReferenceSystem("EPSG:3857")
        crs3 = QgsCoordinateReferenceSystem("EPSG:32651")

        assert prechecks(crs1, crs1, crs1) == True
        assert prechecks(crs1, crs2, crs3) == False
        assert prechecks(crs2, crs1, crs1) == False
        assert prechecks(crs1, crs2, crs1) == False
