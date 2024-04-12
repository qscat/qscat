# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import math
import numpy as np
import time

from PyQt5.QtCore import QVariant

from qgis.core import QgsApplication
from qgis.core import QgsGeometry
from qgis.core import QgsLineString
from qgis.core import QgsMessageLog
from qgis.core import QgsPointXY
from qgis.core import QgsProject
from qgis.core import QgsTask
from qgis.core import QgsWkbTypes
from qgis.core import Qgis

from qgis.utils import iface
from qgis.PyQt.QtWidgets import QMessageBox

from qscat.core.intersects import add_intersections_layer
from qscat.core.layers import add_layer
from qscat.core.layers import load_baseline
from qscat.core.layers import load_shorelines
from qscat.core.messages import display_message
from qscat.core.intersects import load_list_years_intersections
from qscat.core.utils.input import get_baseline_input_params
from qscat.core.utils.input import get_shorelines_input_params
from qscat.core.utils.input import get_transects_input_params


def add_transects_layer(
    transects: list[QgsGeometry],
    base_angles,
    baseline_layer_name,
    transect_layer_output_name,
    qmlcb_stats_transects_layer,
):
    fields = [{'name': 'angle', 'type': QVariant.Double}]
    values = [[a] for a in base_angles]
    transects_layer = add_layer(
        'LineString',
        transects,
        f'{baseline_layer_name}_{transect_layer_output_name}',
        fields,
        values,
    )
    qmlcb_stats_transects_layer.setLayer(transects_layer)


def cast_transects(self):
    start_time = time.perf_counter()
    
    baseline_params = get_baseline_input_params(self)
    shorelines_params = get_shorelines_input_params(self)
    transects_params = get_transects_input_params(self)

    cast_transects_pre_checks_result = cast_transects_pre_checks(
        self,
        transects_params,
        shorelines_params,
        baseline_params
    )

    # TODO: 2 for loop!
    if cast_transects_pre_checks_result:
        multi_baselines = load_baseline(baseline_params)

        multi_base_angles = []
        multi_transects = []

        for baselines in multi_baselines:
            for baseline in baselines:
                # Get points that will use to draw the transects
                if transects_params['is_by_transect_spacing']:
                    distances = np.arange(
                        0, baseline['line'].length(),
                        int(transects_params['by_transect_spacing'])
                    )
                elif transects_params['is_by_number_of_transects']:
                    distances = np.linspace(
                        0, baseline['line'].length(),
                        int(transects_params['by_number_of_transects'])
                    )

                transect_points = [
                    QgsPointXY(baseline['line'].interpolatePoint(distance)) 
                    for distance in distances
                ]

                # Get the reference of baseline angle per transect points
                base_angles = [
                    get_baseline_angle(
                        baseline['line'],
                        distance, 
                        int(transects_params['smoothing_distance'])
                    ) 
                    for distance in distances
                ]

                # Check if baseline layer has specific or custom values of:
                # placement, orientation, and transect length
                baseline_params_copy = baseline_params.copy()
                
                # Optional field baseline placement
                if baseline['placement'] == "sea":
                    baseline_params_copy['is_baseline_placement_sea'] = True
                    baseline_params_copy['is_baseline_placement_land'] = False
                elif baseline['placement'] == "land":
                    baseline_params_copy['is_baseline_placement_sea'] = False
                    baseline_params_copy['is_baseline_placement_land'] = True

                # Optional field baseline orientation
                if baseline['orientation'] == "right":
                    baseline_params_copy['is_baseline_orientation_land_right'] = True
                    baseline_params_copy['is_baseline_orientation_land_left'] = False
                elif baseline['orientation'] == "left":
                    baseline_params_copy['is_baseline_orientation_land_right'] = False
                    baseline_params_copy['is_baseline_orientation_land_left'] = True
                
                # Optional field baseline length
                transect_length = baseline['transect_length'] if baseline['transect_length'] else int(transects_params['length'])

                # Create normal line smooth
                transects = [
                    cast_transect(
                        transect_point,
                        base_angle,
                        transect_length,
                        baseline_params_copy
                    )
                    for (base_angle, transect_point) in zip(base_angles, transect_points)
                ]
                transects = [QgsGeometry.fromPolyline(t) for t in transects]

                multi_transects.append(transects)
                multi_base_angles.append(base_angles)

        # Flatten the lists
        transects = [t for transect in multi_transects for t in transect]
        base_angles = [a for angles in multi_base_angles for a in angles]

        # For intersection operations
        #shorelines = load_shorelines(shorelines_params)
        
        # TODO: Make loading shorelines as a task
        # For future if required for very big shorelines
        # Ask users to divide.
   

        add_transects_layer(
            transects,
            base_angles,
            baseline_params["baseline_layer"].name(),
            transects_params["layer_output_name"],
            self.dockwidget.qmlcb_stats_transects_layer,
        )
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000
        print(f"Elapsed time: {elapsed_time} ms")
        #show_message(self, 'Success', f'Transect cast in {get_duration_ms(end_transect, start_transect)} ms', 0)    


def get_orig_baseline_transect_points(baseline, by, n):
    """Get the transect points of the original baseline line string.

    Args:
        baseline (QgsLineString)
        by (int): Either by 0-distance between or 1-number of transects.
        n (float): Either by distance or number of transects value.

    Returns:
        list[QgsPointXY]
    """
    if by == 0:
        distances = np.arange(0, baseline.length(), n)[:-1]
    elif by == 1:
        distances = np.linspace(0, baseline.length(), n) 

    return [QgsPointXY(baseline.interpolatePoint(distance)) for distance in distances]


def get_arctan2(line):
    """
    Args:
        line (QgsLineString)

    Returns:
        float
    """
    #y = line.pointN(-1).y() - line.pointN(0).y()
    #x = line.pointN(-1).x() - line.pointN(0).x()
    return math.atan2(
        line.pointN(-1).y() - line.pointN(0).y(), 
        line.pointN(-1).x() - line.pointN(0).x()
    )


def contains(line, point):
    """
    Args:
        line (QgsLineString)
        point (QgsPointXY)
    
    Returns:
        bool
    """
    geom_line = QgsGeometry.fromPolyline(line)
    geom_point = QgsGeometry.fromPointXY(point)

    # solves floating imprecision problem
    return True if geom_line.distance(geom_point) < 1e-8 else False


def cast_transect(origin, angle, distance, baseline):
    """
    Args:
        origin (QgsPointXY)
        angle (float)
        distance (float)
        baseline (dict) : Contains the values in baseline tab

    Returns:
        list[QgsLineString]: length of 2 (origin of transect and second point).
    """
    # Find the second point of the transect extended from 
    # the origin using the angle and distance
    x = origin.x() + distance * math.cos(angle)
    y = origin.y() + distance * math.sin(angle)
    
    transect = QgsLineString([origin, QgsPointXY(x, y)])
    transect_geom = QgsGeometry.fromPolyline(transect)

    ROTATE_RIGHT = 90
    ROTATE_LEFT = -90

    if baseline['is_baseline_placement_sea']:
        if baseline['is_baseline_orientation_land_right']:
            rotate = ROTATE_RIGHT
        elif baseline['is_baseline_orientation_land_left']:
            rotate = ROTATE_LEFT
    elif baseline['is_baseline_placement_land']:
        if baseline['is_baseline_orientation_land_right']:
            rotate = ROTATE_LEFT
        elif baseline['is_baseline_orientation_land_left']:
            rotate = ROTATE_RIGHT

    transect_geom.rotate(rotate, origin)
    return QgsLineString(QgsGeometry(transect_geom).asPolyline())


def get_baseline_angle(baseline, distance, smoothing_val):
    """Get transection orientation (angle) of a smoothed transect.

    Args:
        baseline (QgsLineString)
        distance (float)
        smoothing_val (int)
    """
    d_left = distance - (smoothing_val/2)
    d_right = distance + (smoothing_val/2)
    len = baseline.length()
    pt_left = baseline.interpolatePoint(0 if d_left < 0 else d_left)
    pt_right = baseline.interpolatePoint(len if d_right > len else d_right)
    return get_arctan2(QgsLineString([pt_left, pt_right]))


def cast_transects_pre_checks(self, transects_params, shorelines_params, baseline_params):
    proj_crs_authid = QgsProject.instance().crs().authid()

    if not QgsProject.instance().fileName():
        display_message(
            'The QGIS project has not been saved yet. Save first to continue', 
            Qgis.Critical,
        )
        return False
    
    if shorelines_params['shorelines_layer'].crs().authid() != proj_crs_authid:
        display_message(
            'The CRS of the selected shoreline layer does not match the project CRS.', 
            Qgis.Critical,
        )
        return False

    if baseline_params['baseline_layer'].crs().authid() != proj_crs_authid:
        display_message(
            'The CRS of the baseline shoreline layer does not match the project CRS.', 
            Qgis.Critical,
        )
        return False

    return True