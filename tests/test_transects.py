# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from unittest.mock import patch

from qgis.core import QgsCoordinateReferenceSystem, QgsProject, QgsVectorLayer
from qgis.gui import QgsMapLayerComboBox
from qgis.testing import start_app

from qscat.core.tabs.transects import cast_transects, prechecks

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
    baseline_inputs = {
        "baseline_layer": baseline_layer,
        "is_baseline_placement_sea": True,
        "is_baseline_placement_land": False,
        "is_baseline_orientation_land_right": True,
        "is_baseline_orientation_land_left": False,
        "placement_field": None,  #'qs_place',
        "orientation_field": None,  #'qs_orient',
        "transect_length_field": None,  #'qs_length',
        "smoothing_distance_field": None,  #'qs_smooth',
    }
    shorelines_inputs = {
        "shorelines_layer": shoreline_layer,
    }
    transects_inputs = {
        "smoothing_distance": "1",
        "length": "1",
        "layer_output_name": "test_transects",
    }

    result = cast_transects(
        baseline_inputs, shorelines_inputs, transects_inputs, crs, QgsMapLayerComboBox()
    )

    assert len(project.mapLayers()) == initial_layer_count + 1
    assert "test_transects" in result[0].name()
    assert result[1].currentLayer() is result[0]

    # Exclude display_message() function (requires iface messageBar())
    with patch("qscat.core.tabs.transects.display_message", return_value=None):
        crs = QgsCoordinateReferenceSystem("EPSG:32651")

        result = cast_transects(
            baseline_inputs,
            shorelines_inputs,
            transects_inputs,
            crs,  # Different project CRS
            QgsMapLayerComboBox(),
        )
        assert result is None


def test_prechecks():
    """Test CRS prechecks function."""
    # Exclude display_message() function (requires iface messageBar())
    with patch("qscat.core.tabs.transects.display_message", return_value=None):
        crs1 = QgsCoordinateReferenceSystem("EPSG:4326")
        crs2 = QgsCoordinateReferenceSystem("EPSG:3857")
        crs3 = QgsCoordinateReferenceSystem("EPSG:32651")
        name1 = "name1"
        name2 = "name2"
        assert prechecks(crs1, crs1, crs1, name1, name2) is True
        assert prechecks(crs1, crs2, crs3, name1, name2) is False
        assert prechecks(crs2, crs1, crs1, name1, name2) is False
        assert prechecks(crs1, crs2, crs1, name1, name2) is False
