# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsVectorLayer,
)
from qgis.testing import start_app

from qscat.core.constants import AreaChangeField, Statistic, Trend
from qscat.core.tabs.visualization import apply_area_colors, apply_color_ramp

start_app()


def test_apply_area_colors():
    """Test if the layer is categorized based on the `AreaChangeField.TREND` field."""
    field_name = AreaChangeField.TREND
    field_values = ["accreting", "stable", "eroding"]
    layer = QgsVectorLayer("Polygon", "test_layer", "memory")

    # Add AreaChangeField.TREND field
    dp = layer.dataProvider()
    dp.addAttributes([QgsField(field_name, QVariant.String)])
    layer.updateFields()

    # Create features with different area trend values
    for value in field_values:
        feat = QgsFeature(layer.fields())
        feat.setGeometry(QgsGeometry.fromWkt("POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))"))
        feat.setAttribute(field_name, value)
        dp.addFeature(feat)

    layer.updateExtents()

    apply_area_colors(layer)

    assert layer.renderer().type() == "categorizedSymbol"
    assert len(layer.renderer().categories()) == 3

    assert layer.renderer().categories()[0].label() == Trend.ERODING
    assert layer.renderer().categories()[1].label() == Trend.STABLE
    assert layer.renderer().categories()[2].label() == Trend.ACCRETING


def test_apply_color_ramp():
    """Test apply color ramp visualization to the layer."""
    layer = QgsVectorLayer("LineString", "test_layer", "memory")
    layer.setCustomProperty("stat", Statistic.NSM)

    field_name = Statistic.NSM
    field_values = [-100, -50, 0, 50, 100]

    # Add Statistic.NSM field
    dp = layer.dataProvider()
    dp.addAttributes([QgsField(field_name, QVariant.Double)])
    layer.updateFields()

    # Create features with different NSM values
    for value in field_values:
        feat = QgsFeature(layer.fields())
        feat.setGeometry(QgsGeometry.fromWkt("LINESTRING (0 0, 1 1)"))
        feat.setAttribute(field_name, value)
        dp.addFeature(feat)

    layer.updateExtents()

    unc = 25
    apply_color_ramp(
        layer=layer,
        stat_field=field_name,
        mode=1,  # Equal Interval
        num_of_pos_classes=5,
        num_of_neg_classes=5,
        unc=unc,
    )

    assert layer.renderer().type() == "graduatedSymbol"
    assert layer.renderer().classAttribute() == field_name
    assert layer.renderer().classificationMethod().name() == "Custom"

    # Colors
    assert layer.renderer().sourceColorRamp().color1().getRgb() == (173, 29, 42, 255)
    assert layer.renderer().sourceColorRamp().color2().getRgb() == (34, 101, 188, 255)
    assert layer.renderer().sourceColorRamp().stops()[0].color.getRgb() == (
        229,
        228,
        218,
        255,
    )
    assert layer.renderer().sourceColorRamp().isDiscrete() is False

    # Values
    assert len(layer.renderer().ranges()) == 11  # 10 class + 1 unc
    assert layer.renderer().ranges()[0].lowerValue() == -100  # lowest
    assert layer.renderer().ranges()[0].upperValue() == -85
    assert layer.renderer().ranges()[5].lowerValue() == -unc  # stable
    assert layer.renderer().ranges()[5].upperValue() == unc
    assert layer.renderer().ranges()[10].lowerValue() == 85  # highest
    assert layer.renderer().ranges()[10].upperValue() == 100
