# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import math
import time

import numpy as np
from PyQt5.QtCore import QVariant
from qgis.core import (
    Qgis,
    QgsGeometry,
    QgsLineString,
    QgsMessageLog,
    QgsPointXY,
    QgsProject,
)

from qscat.core.inputs import Inputs
from qscat.core.layer import create_add_layer, load_all_baselines
from qscat.core.messages import display_message


def cast_transects_button_clicked(qdw):
    """Cast transect (on button clicked).

    Args:
        qdw (QscatDockWidget): QscatDockWidget instance.
    """
    inputs = Inputs(qdw)
    baseline_inputs = inputs.baseline()
    shorelines_inputs = inputs.shorelines()
    transects_inputs = inputs.transects()

    project_crs = QgsProject.instance().crs()
    shoreline_change_transects_layer = qdw.qmlcb_shoreline_change_transects_layer

    start_time = time.perf_counter()

    cast_transects(
        baseline_inputs,
        shorelines_inputs,
        transects_inputs,
        project_crs,
        shoreline_change_transects_layer,
    )

    elapsed_time = round((time.perf_counter() - start_time) * 1000, 2)
    QgsMessageLog.logMessage(
        f'Transects cast of "{baseline_inputs["baseline_layer"].name()}" in {elapsed_time} ms',
        "Execution time",
        level=Qgis.Info,
    )


def cast_transects(
    baseline_inputs,
    shorelines_inputs,
    transects_inputs,
    project_crs,
    shoreline_change_transects_layer,
):
    """Start casting transects.

    Args:
        baseline_inputs (dict)
        shorelines_inputs (dict)
        transects_inputs (dict)
        project_crs (QgsCoordinateReferenceSystem)
        shoreline_change_transects_layer (QgsMapLayerComboBox)
    """
    # Checks CRS of the layers
    are_prechecks_passed = prechecks(
        shorelines_inputs["shorelines_layer"].crs(),
        baseline_inputs["baseline_layer"].crs(),
        project_crs,
        shorelines_inputs["shorelines_layer"].name(),
        baseline_inputs["baseline_layer"].name(),
    )

    if not are_prechecks_passed:
        return

    all_baselines = load_all_baselines(baseline_inputs)
    all_angles = []
    all_transects = []

    # Multi feature baseline
    for baselines in all_baselines:
        for baseline in baselines:
            # Get transect origin points
            distances = get_transect_points(baseline["line"], transects_inputs)
            points = [
                QgsPointXY(baseline["line"].interpolatePoint(distance))
                for distance in distances
            ]

            # Custom baseline fields
            baseline_params_copy = baseline_inputs.copy()

            # Baseline placement
            if baseline["placement"] == "sea":
                baseline_params_copy["is_baseline_placement_sea"] = True
                baseline_params_copy["is_baseline_placement_land"] = False
            elif baseline["placement"] == "land":
                baseline_params_copy["is_baseline_placement_sea"] = False
                baseline_params_copy["is_baseline_placement_land"] = True

            # Baseline orientation
            if baseline["orientation"] == "right":
                baseline_params_copy["is_baseline_orientation_land_right"] = True
                baseline_params_copy["is_baseline_orientation_land_left"] = False
            elif baseline["orientation"] == "left":
                baseline_params_copy["is_baseline_orientation_land_right"] = False
                baseline_params_copy["is_baseline_orientation_land_left"] = True

            # Transect length
            transect_length = (
                baseline["transect_length"]
                if baseline["transect_length"]
                else int(transects_inputs["length"])
            )

            # Smoothing distance
            smoothing_distance = (
                baseline["smoothing_distance"]
                if baseline["smoothing_distance"]
                else int(transects_inputs["smoothing_distance"])
            )

            # Smoothing distance angles
            angles = [
                get_smoothing_angle(
                    baseline["line"],
                    distance,
                    int(smoothing_distance),
                )
                for distance in distances
            ]

            # Get the smoothed transects
            transects = [
                cast_transect(point, angle, transect_length, baseline_params_copy)
                for (point, angle) in zip(points, angles)
            ]

            all_transects.append(transects)
            all_angles.append(angles)

    # Flatten
    transects = [t for transect in all_transects for t in transect]
    angles = [a for angles in all_angles for a in angles]

    # Add transects layer
    fields = [{"name": "angle", "type": QVariant.Double}]
    values = [[a] for a in angles]
    transects_layer = create_add_layer(
        geometry="LineString",
        geometries=transects,
        name=transects_inputs["layer_output_name"],
        fields=fields,
        values=values,
    )

    # Set shoreline change transects default layer
    # with the newly created transects layer
    shoreline_change_transects_layer.setLayer(transects_layer)

    # For tests only
    return (transects_layer, shoreline_change_transects_layer)


def get_transect_points(baseline, transects_params):
    """Get the transect points along the baseline.

    Args:
        baseline (QgsLineString)
        transects_params (dict)

    Returns:
        list[float]
    """
    if transects_params["is_by_transect_spacing"]:
        distances = np.arange(
            0, baseline.length(), int(transects_params["by_transect_spacing"])
        )
    elif transects_params["is_by_number_of_transects"]:
        distances = np.linspace(
            0, baseline.length(), int(transects_params["by_number_of_transects"])
        )

    return distances


def get_arctan_angle(line):
    """Calculate the arctangent of the slope of a line.

    Args:
        line (QgsLineString): A LineString object representing a line.

    Returns:
        float: The arctangent of the slope of the line in radians.

    """
    return math.atan2(
        line.pointN(-1).y() - line.pointN(0).y(),
        line.pointN(-1).x() - line.pointN(0).x(),
    )


def cast_transect(origin, angle, distance, baseline):
    """Cast a single transect from a given origin point, angle, and distance.

    Args:
        origin (QgsPointXY)
        angle (float)
        distance (float)
        baseline (dict)

    Returns:
        list[QgsLineString]
    """
    # Find the second point of the transect extended from
    # the origin using the angle and distance
    x = origin.x() + distance * math.cos(angle)
    y = origin.y() + distance * math.sin(angle)

    transect = QgsLineString([origin, QgsPointXY(x, y)])
    transect_geom = QgsGeometry.fromPolyline(transect)

    ROTATE_RIGHT = 90
    ROTATE_LEFT = -90

    if baseline["is_baseline_placement_sea"]:
        if baseline["is_baseline_orientation_land_right"]:
            rotate = ROTATE_RIGHT
        elif baseline["is_baseline_orientation_land_left"]:
            rotate = ROTATE_LEFT
    elif baseline["is_baseline_placement_land"]:
        if baseline["is_baseline_orientation_land_right"]:
            rotate = ROTATE_LEFT
        elif baseline["is_baseline_orientation_land_left"]:
            rotate = ROTATE_RIGHT

    transect_geom.rotate(rotate, origin)
    return QgsLineString(QgsGeometry(transect_geom).asPolyline())


def get_smoothing_angle(baseline, distance, smoothing_val):
    """Get the angle, in radians, that will serve as the new orientation of the transect.
       This adjustment is performed by the smoothing distance feature.

    Args:
        baseline (QgsLineString)
        distance (float): Current transect point distance along the baseline.
        smoothing_val (int): Smoothing distance in meters.

    Returns:
        float: The angle in radians.
    """
    _len = baseline.length()

    left_distance = distance - (smoothing_val / 2)
    right_distance = distance + (smoothing_val / 2)

    left_pt = baseline.interpolatePoint(0 if left_distance < 0 else left_distance)
    right_pt = baseline.interpolatePoint(
        _len if right_distance > _len else right_distance
    )

    return get_arctan_angle(QgsLineString([left_pt, right_pt]))


def prechecks(
    shorelines_layer_crs,
    baseline_layer_crs,
    project_crs,
    shorelines_layer_name,
    baseline_layer_name,
):
    """Prechecks for casting transects.

    Note:
        Currently checks layers CRS if they match the project CRS.
        May add more prechecks in the future.

    Args:
        shorelines_layer_crs (QgsCoordinateReferenceSystem)
        baseline_layer_crs (QgsCoordinateReferenceSystem)
        project_crs (QgsCoordinateReferenceSystem)
        shorelines_layer_name (str)
        baseline_layer_name (str)

    Returns:
        bool: True if prechecks passed, otherwise False.
    """
    if shorelines_layer_crs != project_crs:
        display_message(
            f"The selected shorelines layer ({shorelines_layer_name}) CRS ({shorelines_layer_crs.authid()}) doesn't match the project CRS ({project_crs.authid()}).",
            Qgis.Critical,
        )
        return False

    if baseline_layer_crs != project_crs:
        display_message(
            f"The selected baseline layer ({baseline_layer_name}) CRS ({baseline_layer_crs.authid()}) doesn't match the project CRS ({project_crs.authid()}).",
            Qgis.Critical,
        )
        return False

    return True
