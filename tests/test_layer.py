from PyQt5.QtCore import QVariant
from qgis.core import QgsGeometry, QgsPointXY, QgsProject, QgsWkbTypes
from qgis.testing import start_app

from qscat.core.layer import create_add_layer
from qscat.core.utils.geometry import as_polylines

start_app()


def test_create_add_layer():
    """Test creating and adding of layer utility function."""

    project = QgsProject.instance()
    initial_layer_count = len(project.mapLayers())

    geometry_type = "LineString"
    geometries = [
        QgsGeometry.fromPolylineXY(
            [
                QgsPointXY(0, 0),
                QgsPointXY(1, 1),
            ]
        ),
        QgsGeometry.fromPolylineXY(
            [
                QgsPointXY(2, 2),
                QgsPointXY(3, 3),
            ]
        ),
    ]
    name = "test_layer"
    fields = [
        {"name": "field1", "type": QVariant.Double},
        {"name": "field2", "type": QVariant.Double},
    ]
    values = [
        [1.0, 2.0],
        [3.0, 4.0],
    ]

    extra_values = {"newest_date": "09/2002", "oldest_date": "09/1996"}

    layer = create_add_layer(
        geometry_type,
        geometries,
        name,
        fields,
        values,
        extra_values,
    )

    # Project layer count
    assert len(project.mapLayers()) == initial_layer_count + 1

    # Layer properties
    assert layer.isValid()
    assert layer.featureCount() == 2
    assert layer.geometryType() == QgsWkbTypes.LineGeometry
    assert "test_layer" in layer.name()
    assert [field.name() for field in layer.fields()] == ["id", "field1", "field2"]

    # Layer features
    for feat, geometry, value in zip(layer.getFeatures(), geometries, values):
        assert feat.geometry().asPolyline() == geometry.asPolyline()
        assert feat["field1"] == value[0]
        assert feat["field2"] == value[1]

    # Custom properties
    for key, value in extra_values.items():
        assert layer.customProperty(key) == value


def test_as_polylines():
    """Test getting line parts of single and multipart line geometries."""
    single = QgsGeometry.fromWkt("LineString (0 0, 1 1)")
    single_z = QgsGeometry.fromWkt("LineString Z (0 0 5, 1 1 5)")
    multi = QgsGeometry.fromWkt("MultiLineString ((0 0, 1 1), (2 2, 3 3))")

    assert as_polylines(single) == [[QgsPointXY(0, 0), QgsPointXY(1, 1)]]
    assert as_polylines(single_z) == [[QgsPointXY(0, 0), QgsPointXY(1, 1)]]
    assert as_polylines(multi) == [
        [QgsPointXY(0, 0), QgsPointXY(1, 1)],
        [QgsPointXY(2, 2), QgsPointXY(3, 3)],
    ]
