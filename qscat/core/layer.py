# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import json

from PyQt5.QtCore import QVariant

from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsLineString
from qgis.core import QgsGeometry
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer

from qscat.core.utils.date import datetime_now
from qscat.core.utils.date import convert_to_decimal_year


def create_add_layer(
    geometry,
    geometries,
    name,
    fields=None,
    values=None,
    extra_values=None,
    datetime=None,
):
    """Create and add vector layer in memory (temporary).

    Args:
        geometry (str): 'LineString', 'Polygon', etc.
        geometries (list[QgsGeometry]): List of geometries.
        name (str): Name used as part of the layer name.
        fields (list[dict]): List of fields.
        values (list[list[float,str]]): List of values.
        extra_values (dict): A dict to be stored in the layer's custom properties.
        datetime (str): Date and time value to append to the layer name.

    Returns:
        QgsVectorLayer

    Example:
        layer = create_layer(
            'LineString',
            [QgsGeometry.fromPolylineXY([QgsPointXY(0, 0), QgsPointXY(1, 1)]),
             QgsGeometry.fromPolylineXY([QgsPointXY(2, 2), QgsPointXY(3, 3)]),
            ],
            'test_layer',
            'EPSG:4326',
            [
                {'name': 'field1', 'type':  QVariant.Double},
                {'name': 'field2', 'type':  QVariant.Double},
            ],
            [
                [1.0, 2.0],
                [3.0, 4.0],
            ],
            '2022-08-01 12:00:00',
        )
    """
    if datetime is None:
        datetime = datetime_now()

    layer = QgsVectorLayer(geometry, f"{name} [{datetime}]", "memory")
    layer.setCrs(QgsProject.instance().crs())

    # Add attributes / fields
    dp = layer.dataProvider()
    fields_with_id = []

    # Add fix id field
    fields_with_id.append(QgsField("id", QVariant.Int))

    ## Add custom fields
    for field in fields:
        fields_with_id.append(QgsField(field["name"], field["type"]))
    dp.addAttributes(fields_with_id)

    layer.updateFields()

    # Add geometries and values
    for i, (geometry, value) in enumerate(zip(geometries, values)):
        feat = QgsFeature(layer.fields())
        # Add geometry
        feat.setGeometry(geometry)
        # Add values: id + field1, field2, ...
        feat.setAttributes([i + 1] + value)
        dp.addFeature(feat)

    # Add custom properties
    if extra_values:
        for key, value in extra_values.items():
            layer.setCustomProperty(key, value)

    layer.updateExtents()
    QgsProject.instance().addMapLayers([layer])

    return layer


def load_shorelines(shorelines_params):
    """Read merged shoreline QGIS's vector layer object.

    Example dictionary:
        shorelines = [
            {'year': 1990.xx, 'geoms': [list of QgsGeometry], 'unc': 143},
            {'year': 1998, 'geoms': [list of QgsGeometry], 'unc': 143},
            .
            .
            .
        ]

    Args:
        layer (QgsVectorLayer)

    Returns:
        list[dict(year:int, geoms:list[QgsGeometry.LineString])]
    """
    shorelines = []
    features = shorelines_params["shorelines_layer"].getFeatures()

    for feat in features:
        shoreline = {}
        decimal_year = convert_to_decimal_year(feat[shorelines_params["date_field"]])
        shoreline["year"] = decimal_year
        # shoreline['year'] = convert_to_decimal_year(feat[shorelines_params['date_field']])
        shoreline["geoms"] = [
            QgsGeometry.fromPolylineXY(l) for l in feat.geometry().asMultiPolyline()
        ]
        if (
            feat[shorelines_params["uncertainty_field"]] is None
            or not feat[shorelines_params["uncertainty_field"]] > 0.0
        ):
            shoreline["unc"] = float(shorelines_params["default_data_uncertainty"])
        else:
            shoreline["unc"] = float(feat[shorelines_params["uncertainty_field"]])
        shorelines.append(shoreline)

    return shorelines


def load_shorelines_geoms(layer):
    """Load shorelines geoms only

    Args:
        layer (QgsVectorLayer)

    Returns:
        list[list[QgsGeometry.LineString]]]
    """
    shorelines = []
    features = layer.getFeatures()

    for feat in features:
        shoreline = []
        geom = feat.geometry()
        multi_line_string = geom.asMultiPolyline()
        for line_string in multi_line_string:
            shoreline.append(QgsGeometry.fromPolylineXY(line_string))
        shorelines.append(shoreline)
    return shorelines


def load_transects(layer):
    """
    Args:
        layer (QgsVectorLayer)

    Returns:
        list[QgsGeometry.LineString]
    """
    return [f.geometry() for f in layer.getFeatures()]


# def load_baseline(layer):
#     """Load QGIS baseline layer as a line string.

#     Args:
#         layer (QgsVectorLayer)

#     Returns:
#         QgsLineString
#     """
#     features = layer.getFeatures()
#     for feature in features:
#         geom = feature.geometry()
#         multi_line_string = geom.asMultiPolyline()

#         for line_string in multi_line_string:
#             baseline = line_string

#     return QgsLineString(baseline) # consider just the first line string for now


def load_all_baselines(baseline_params):
    """Load QGIS baseline layer as a list of multi line strings.

    Args:
        layer (QgsVectorLayer)

    Returns:
        list[QgsLineString]
    """
    all_baselines = []
    feats = baseline_params["baseline_layer"].getFeatures()

    # Since fields are optional, first check if they are selected
    placement_field = (
        baseline_params["placement_field"]
        if baseline_params["placement_field"]
        else None
    )
    orientation_field = (
        baseline_params["orientation_field"]
        if baseline_params["orientation_field"]
        else None
    )
    transect_length_field = (
        baseline_params["transect_length_field"]
        if baseline_params["transect_length_field"]
        else None
    )

    for feat in feats:
        # Access the value for each feature
        # If null, set to None
        if placement_field:
            placement = feat[placement_field] if feat[placement_field] else None
        else:
            placement = None

        if orientation_field:
            orientation = feat[orientation_field] if feat[orientation_field] else None
        else:
            orientation = None

        if transect_length_field:
            transect_length = (
                feat[transect_length_field] if feat[transect_length_field] else None
            )
        else:
            transect_length = None

        baselines = []
        geom = feat.geometry()
        multi_line_string = geom.asMultiPolyline()

        for line_string in multi_line_string:
            baselines.append(
                {
                    "line": QgsLineString(line_string),
                    "placement": placement,
                    "orientation": orientation,
                    "transect_length": transect_length,
                }
            )

        all_baselines.append(baselines)

    return all_baselines


def load_polygons(layer):
    # layer = layer.getFeatures()
    # for feat in layer:
    #     polygon_geom = feat.geometry()
    #     polygons = polygon_geom.asMultiPolygon()
    #     polygons_geom = [QgsGeometry.fromPolygonXY(polygon) for polygon in polygons]

    # return polygons_geom
    multi_polygons = []
    for feat in layer.getFeatures():
        name = feat["name"] if "name" in feat.fields().names() else None
        multi_polygon = feat.geometry()
        multi_polygons.append(
            {
                "geom": multi_polygon,
                "name": name,
            }
        )

    return multi_polygons
