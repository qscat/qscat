# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from __future__ import annotations

from qgis.core import QgsGeometry, QgsPointXY, QgsWkbTypes

_SEARCH_DISTANCE = 5000


def get_half_transect_intersection(
    shoreline: QgsGeometry,
    extended_half_transect: QgsGeometry,
    half_transect_center_pt: QgsGeometry,
) -> QgsGeometry | None:
    """Find the intersection between a shoreline and the extended
    non-final half transect.

    # TODO: illustration + link

    Args:
        shoreline: MultiLineString
        extended_half_transect: LineString
        half_transect_center_pt: Point
    """
    intersections = {}
    intersect = extended_half_transect.intersection(shoreline)
    if not intersect.isEmpty():
        if intersect.wkbType() == QgsWkbTypes.MultiPoint:
            for i in intersect.asMultiPoint():
                intersection = QgsGeometry.fromPointXY(i)
                intersections[intersection] = intersection.distance(
                    half_transect_center_pt
                )
        else:
            # intersection = QgsGeometry.fromPointXY(intersect)
            intersections[intersect] = intersect.distance(half_transect_center_pt)
    else:
        # print(shoreline)
        # print(extended_half_transect)
        # print(half_transect_center_pt)
        # raise Exception("No intersection found.")
        return None

    final_intersect = min(intersections, key=intersections.get)
    return final_intersect


def get_half_transect(
    newest_shorelines: QgsGeometry,
    oldest_shorelines: QgsGeometry,
    transect1: QgsGeometry,
    transect2: QgsGeometry,
) -> QgsGeometry | None:
    """Determine the (half) transect between two transects.

    # TODO: illustration + link

    Args:
        newest_shorelines: MultiLineString
        oldest_shorelines: MultiLineString
        transect1: LineString
        transect2: LineString

    Returns:
        LineString
    """
    half_baseline1 = QgsGeometry.fromPolylineXY(
        [
            QgsPointXY(transect1.vertexAt(0)),
            QgsPointXY(transect2.vertexAt(0)),
        ]
    )
    half_baseline2 = QgsGeometry.fromPolylineXY(
        [
            QgsPointXY(transect1.vertexAt(1)),
            QgsPointXY(transect2.vertexAt(1)),
        ]
    )

    half_baseline_pt1 = half_baseline1.interpolate(half_baseline1.length() / 2.0)
    half_baseline_pt2 = half_baseline2.interpolate(half_baseline2.length() / 2.0)
    half_transect = QgsGeometry.fromPolylineXY(
        [
            half_baseline_pt1.asPoint(),
            half_baseline_pt2.asPoint(),
        ]
    )

    half_transect_center_pt = half_transect.interpolate(half_transect.length() / 2.0)
    extend_distance = _SEARCH_DISTANCE / 2
    extended_half_transect = half_transect.extendLine(extend_distance, extend_distance)

    newest_shoreline_intersection = get_half_transect_intersection(
        newest_shorelines,
        extended_half_transect,
        half_transect_center_pt,
    )
    oldest_shoreline_intersection = get_half_transect_intersection(
        oldest_shorelines,
        extended_half_transect,
        half_transect_center_pt,
    )

    if newest_shoreline_intersection is None or oldest_shoreline_intersection is None:
        return None

    final_half_transect = QgsGeometry.fromPolylineXY(
        [
            newest_shoreline_intersection.asPoint(),
            oldest_shoreline_intersection.asPoint(),
        ]
    )
    return final_half_transect
