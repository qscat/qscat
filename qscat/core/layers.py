import os

from PyQt5.QtCore import QVariant

from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsFeature
from qgis.core import QgsField
from qgis.core import QgsLayerTreeGroup
from qgis.core import QgsLayerTreeLayer
from qgis.core import QgsLineString
from qgis.core import QgsGeometry
from qgis.core import QgsMapLayerType
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import QgsVectorFileWriter

from qscat.core.utils import datetime_now
from qscat.core.utils import convert_to_decimal_year


def add_layer(
    geometry_type: str,
    geometries: list[QgsGeometry],
    name: str,
    fields=None, # list[dict]
    values=None, # list[list[float,str]]
    datetime=None,
    #save_location=None,
    layer_group=None,
):
    crs = QgsProject.instance().crs().authid()

    # TODO: add line color
    # TODO: add specific crs (as argument)
    if datetime is None:
        layer = QgsVectorLayer(
            geometry_type, 
            f'{name} [{datetime_now()}]', 
            'memory'
        )
    else: 
        # for summary report use, want to make sure it has same datetime
        # outside the add_layer function
        layer = QgsVectorLayer(
            geometry_type, 
            f'{name} [{datetime}]', 
            'memory'
        )
    layer.setCrs(QgsCoordinateReferenceSystem(crs))
    
    # Add attributes / fields
    dp = layer.dataProvider()
    attributes = []
    attributes.append(QgsField('id', QVariant.Int)) # Fixed id field

    for f in fields:
        attributes.append(QgsField(f['name'], f['type']))
    dp.addAttributes(attributes)
    
    layer.updateFields()

    for i, (g, v) in enumerate(zip(geometries, values)):
        feat = QgsFeature(layer.fields())
        
        # Add geometries
        feat.setGeometry(g)
        """
         feature[field_name] = 'your_value'
         layer.updateFeature(feature)
        """
        attributes = []
        attributes.append(i+1) # Fixed id field

        # Add values
        for vd in v:
            attributes.append(vd)
        feat.setAttributes(attributes)
        dp.addFeature(feat)

    layer.updateExtents()
    
    """
    # Write to an ESRI Shapefile format dataset using UTF-8 text encoding
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "ESRI Shapefile"
    save_options.fileEncoding = "UTF-8"

    transform_context = QgsProject.instance().transformContext()
    layer_name = f"{name}_{datetime_now()}"

    error = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer,
        f"{save_location}/{layer_name}",
        #f"{save_location}/{name}",
        transform_context,
        save_options
    )
    
    if error[0] == QgsVectorFileWriter.NoError:
        print("success again!")
    else:
        print(error)

    layer = QgsVectorLayer(
        f"{save_location}/{layer_name}.shp", 
        f"{layer_name}", 
        "ogr"
    )
    """
    root = QgsProject.instance().layerTreeRoot()
    if layer_group == "area_change":
        layer_group_name = 'Area Change Results'
        area_layer_group = get_layer_tree_group_by_name(layer_group_name)

        if area_layer_group is None:
            area_layer_group = QgsLayerTreeGroup(layer_group_name)
            area_layer_group.insertChildNode(0, QgsLayerTreeLayer(layer))
            root.addChildNode(area_layer_group)
        else:
            area_layer_group.insertChildNode(0, QgsLayerTreeLayer(layer))
    else:
        QgsProject.instance().addMapLayers([layer])

    return layer


def get_layer_tree_group_by_name(group_name):
    root = QgsProject.instance().layerTreeRoot()
    for child_node in root.children():
        if isinstance(child_node, QgsLayerTreeGroup) and child_node.name() == group_name:
            return child_node
    return None


def is_layer_group_exist(layer_group_name):
    root = QgsProject.instance().layerTreeRoot()
    for childNode in root.children():
        if isinstance(childNode, QgsLayerTreeGroup) and childNode.name() == layer_group_name:
            return True
    else:
        return False


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
    features = shorelines_params['shorelines_layer'].getFeatures()
    
    for feat in features:
        shoreline = {}
        decimal_year = convert_to_decimal_year(feat[shorelines_params['date_field']])
        shoreline['year'] = decimal_year
        #shoreline['year'] = convert_to_decimal_year(feat[shorelines_params['date_field']])
        shoreline['geoms'] = [QgsGeometry.fromPolylineXY(l) for l in feat.geometry().asMultiPolyline()]
        if feat[shorelines_params['uncertainty_field']] is None or not feat[shorelines_params['uncertainty_field']] > 0.0:
            shoreline['unc'] = float(shorelines_params['default_data_uncertainty'])
        else:
            shoreline['unc'] = float(feat[shorelines_params['uncertainty_field']])
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


def load_baseline(baseline_params):
    """Load QGIS baseline layer as a list of multi line strings.
    
    Args:
        layer (QgsVectorLayer)
        
    Returns:
        list[QgsLineString]
    """
    multi_baselines = []
    features = baseline_params['baseline_layer'].getFeatures()

    # Since fields are optional, first check if they are selected
    placement_field = baseline_params['placement_field'] if baseline_params['placement_field'] else None
    orientation_field = baseline_params['orientation_field'] if baseline_params['orientation_field'] else None
    transect_length_field = baseline_params['transect_length_field'] if baseline_params['transect_length_field'] else None 

    for feat in features:
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
            transect_length = feat[transect_length_field] if feat[transect_length_field] else None
        else:
            transect_length = None

        multi_baseline = []
        geom = feat.geometry()
        multi_line_string = geom.asMultiPolyline()
        
        for line_string in multi_line_string:
            multi_baseline.append({
                'line': QgsLineString(line_string),
                'placement': placement,
                'orientation': orientation,
                'transect_length': transect_length,
            })

        multi_baselines.append(multi_baseline)

    return multi_baselines


def load_polygons(layer):
    # layer = layer.getFeatures()
    # for feat in layer:
    #     polygon_geom = feat.geometry()
    #     polygons = polygon_geom.asMultiPolygon()
    #     polygons_geom = [QgsGeometry.fromPolygonXY(polygon) for polygon in polygons]

    # return polygons_geom
    multi_polygons = []
    for feat in layer.getFeatures():
        name = feat['name'] if 'name' in feat.fields().names() else None
        multi_polygon = feat.geometry()
        multi_polygons.append({
            'geom': multi_polygon,
            'name': name,
        })

    return multi_polygons