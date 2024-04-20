# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from qgis.testing import start_app

from PyQt5.QtCore import QVariant

from qgis.core import QgsGeometry
from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsVectorLayer

from qscat.core.visualization import apply_area_colors

from qscat.core.constants import AreaChangeField
from qscat.core.constants import Trend

start_app()


def test_apply_area_colors():
    """Test if the layer is categorized based on the `AreaChangeField.TREND` field."""
    field_name = AreaChangeField.TREND
    field_values = ['accreting', 'stable', 'eroding']
    layer = QgsVectorLayer('Polygon', 'test_layer', 'memory')

    # Add AreaChangeField.TREND field 
    dp = layer.dataProvider()
    dp.addAttributes([QgsField(field_name, QVariant.String)])
    layer.updateFields()
    
    # Create features with different area trend values
    for value in field_values:
        feat = QgsFeature(layer.fields())
        feat.setGeometry(
            QgsGeometry.fromWkt(f'POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))')
        )
        feat.setAttribute(field_name, value)
        dp.addFeature(feat)

    layer.updateExtents()

    apply_area_colors(layer)

    assert layer.renderer().type() == 'categorizedSymbol'
    assert len(layer.renderer().categories()) == 3

    assert layer.renderer().categories()[0].label() == Trend.ERODING
    assert layer.renderer().categories()[1].label() == Trend.STABLE
    assert layer.renderer().categories()[2].label() == Trend.ACCRETING