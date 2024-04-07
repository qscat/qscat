# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from PyQt5.QtCore import QVariant

from qgis.core import QgsGeometry
from qgis.core import QgsWkbTypes

from qscat.core.layers import add_layer


def load_list_years_intersections(transects_intersects):
    """Convert list of list of transect intersections to list of list of shoreline intersections where the year will be the dictionary key, and the values will 
    be the dictionary values.
    
    (from) Original:
        transect_intersects = [
            [
                { # intersection 1
                    'transect_origin': <(no more wkt) transect origin from QgsPointXY>
                    'geom': <no more wkt of determined intersection based from params>
                    'id': <intersection id>
                    'transect_id': <transect id>
                    'shoreline_id': <shoreline id>
                    'shoreline_year: <shoreline id>
                    'shoreline_unc: <shoreline id>
                    'distance: <shoreline id>
                    'intersect)x: <shoreline id>
                    'intersect_y: <shoreline id>
                },
                {intersection2}, 
                {intersection3},
                {intersection4},
                ...
            ],
            [transect2],
            [transect3],
            ...
        ]

    (to) New:
        shoreline_intersections = [
            {
                1990.00 : {
                    'unc': xxx,
                    'distance': xxx,
                    'intersect_x': xxx,
                    'intersect_y': xxx,   
                },
                year2: { ... },
                year3: { ... },
                ...
                
            },
            { transect2 intersections },
            { transect3 intersections },
            ... 
        ]
        
    Args:
        transects_intersects (list[list[dict]]): List of list of transect intersections (see above for details)

    Returns:
        list[dict]: List of list of shoreline intersections (see above for details)
    """
    shoreline_intersections = []
    
    for transects_intersect in transects_intersects:
        shorelines = {}

        for shoreline_intersect in transects_intersect:
            shoreline = {}
            # #shoreline['transect_origin'] = QgsGeometry.fromWkt(
            #     shoreline_intersect['transect_origin']
            # )
            shoreline['transect_origin'] = shoreline_intersect['transect_origin']
            shoreline['unc'] = shoreline_intersect['shoreline_unc']
            shoreline['distance'] = shoreline_intersect['distance']
            shoreline['intersect_x'] = shoreline_intersect['intersect_x']
            shoreline['intersect_y'] = shoreline_intersect['intersect_y']
            shorelines[shoreline_intersect['shoreline_year']] = shoreline

            shoreline['orig_transect_geom'] = shoreline_intersect['orig_transect_geom']

        shoreline_intersections.append(shorelines)
    return shoreline_intersections


def add_intersections_layer(transects_intersects, baseline_params):
    fields = [
        {'name': 'transect_id', 'type': QVariant.Int},
        {'name': 'shoreline_id', 'type': QVariant.Int},
        {'name': 'shoreline_year', 'type': QVariant.Double},
        {'name': 'shoreline_unc', 'type': QVariant.Double},
        {'name': 'distance', 'type': QVariant.Double},
        {'name': 'intersect_x', 'type': QVariant.Double},
        {'name': 'intersect_y', 'type': QVariant.Double},
    ]
    geometries = []
    values = []

    for transects_intersect in transects_intersects:
        for individual_transect_intersect in transects_intersect:
            geometries.append(QgsGeometry.fromWkt(individual_transect_intersect['geom']))
            #geometries.append(individual_transect_intersect['geom']) pickled xD
            intersects = [individual_transect_intersect[f['name']] for f in fields]
            values.append(intersects)
    
    baseline_layer_name = baseline_params["baseline_layer"].name()
    
    add_layer(
        'Point', 
        geometries, 
        f'{baseline_layer_name}_intersections', 
        fields, values
    )


def get_intersections(transect, shoreline):
    """Get the intersections between a transect and a shoreline.

    Parameters:
        transect (QgsGeometry): The transect geometry.
        shoreline (QgsGeometry): The shoreline geometry.

    Returns:
        list[QgsPointXY]: A list of intersection points between the transect and shoreline.
    """

    intersections = []
    intersect = transect.intersection(shoreline)

    if not intersect.isEmpty():
        if intersect.wkbType() == QgsWkbTypes.MultiPoint:
            for i in intersect.asMultiPoint():
                intersections.append(i)
        else:
            intersections.append(intersect.asPoint())

    return intersections
