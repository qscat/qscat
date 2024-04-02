# QSCAT by Louis Facun – louisfacun@gmail.com
# License – GPL v3

import math

from qgis.core import QgsGeometry
from qgis.core import QgsPoint
from qgis.core import QgsWkbTypes

_EXTEND_BY_SMALL_EPSILON = 1e-8


def insert_extra_transects(grouped_clustered_interest_transects,
                           newest_shorelines_as_lines,
                           oldest_shorelines_as_lines):
    """Insert extra transects to the grouped clustered interest transects.

    TODO: illustration + link

    Args:
        grouped_clustered_interest_transects (list[list[list[dict]]]): List of
            grouped clustered interest transects
        newest_shorelines_as_lines (list[QgsGeometry]): List of newest shorelines
            as lines
        oldest_shorelines_as_lines (list[QgsGeometry]): List of oldest shorelines
            as lines

    Returns:
        list[list[list[dict]]]: List of grouped clustered interest transects
            with extra transects
    """
    for ci, cluster in enumerate(grouped_clustered_interest_transects):
        # If group on that cluster is 1 and element of that group is 1
        # Then we have lone transect, add extra transect both sides
        if len(cluster) == 1 and len(cluster[0]) == 1:
            transect = cluster[0][0]['geom']
            
            # Determine which shoreline does a transect intersects
            newest_shoreline_base = which_shoreline_transect_intersects(
                transect, newest_shorelines_as_lines)
            oldest_shoreline_base = which_shoreline_transect_intersects(
                transect, oldest_shorelines_as_lines)
            
            if (newest_shoreline_base is not None and 
                oldest_shoreline_base is not None):
                # Check which is shorter in .length()
                # Maybe that's the side of shoreline we need to extend
                if newest_shoreline_base.length() < oldest_shoreline_base.length():
                    shoreline_base = newest_shoreline_base
                    longer_shoreline = oldest_shoreline_base
                else:
                    shoreline_base = oldest_shoreline_base
                    longer_shoreline = newest_shoreline_base
                
                # Determine which transect is closer
                shoreline_start_point1 = shoreline_base.asPolyline()[0]
                shoreline_start_point2 = shoreline_base.asPolyline()[-1]

                # TODO: to support more than 1 group
                # let have different transects choices per shoreline start point
                # Take note of that element:
                # shoreline start poitn1 transect
                # shoreline start poitn2 transect
                transect_choices1 = []
                transect_choices2 = []

                transects_choices = [
                    grouped_clustered_interest_transects[ci-1][-1][-1]['geom'], # top
                    grouped_clustered_interest_transects[ci+1][0][0]['geom'], # bottom
                    cluster[0][0]['geom'], # middle # TODO: edit
                ]

                # track shoreline point distances to both transect point
                # we dont know what transect point (side) we will use
                # lets just get distances then lets pick the avg distances
                # with lowest value
                # TODO: add figure for developers

                # Apply differnet transects start point 1 and 2
                transects1a = {}
                transects1b = {}
                transects2a = {}
                transects2b = {}

                # Apply differnet transects start point 1 and 2
                for transect in transects_choices:
                    transects1a[transect] = shoreline_start_point1.distance(
                        transect.asPolyline()[0]
                    )
                    transects1b[transect] = shoreline_start_point1.distance(
                        transect.asPolyline()[-1]
                    )
                for transect in transects_choices:
                    transects2a[transect] = shoreline_start_point2.distance(
                        transect.asPolyline()[0]
                    )
                    transects2b[transect] = shoreline_start_point2.distance(
                        transect.asPolyline()[-1]
                    )

                # check which average key' value is lower between
                # dictionary transects1a and transect1b
                # just a hack, to know which transect point is closer
                if sum(transects1a.values()) / len(transects1a) < sum(transects1b.values()) / len(transects1b):
                    closest_transect1 = min(transects1a, key=transects1a.get)
                else:    
                    closest_transect1 = min(transects1b, key=transects1b.get)

                if sum(transects2a.values()) / len(transects2a) < sum(transects2b.values()) / len(transects2b):
                    closest_transect2 = min(transects2a, key=transects2a.get)
                else:
                    closest_transect2 = min(transects2b, key=transects2b.get)

                points1 = closest_transect1.asPolyline()
                points2 = closest_transect2.asPolyline()

                angle_rad1 = math.atan2(
                    points1[1].y() - points1[0].y(), 
                    points1[1].x() - points1[0].x()
                )
                angle_rad2 = math.atan2(
                    points2[1].y() - points2[0].y(), 
                    points2[1].x() - points2[0].x()
                )

                EXTEND_LENGTH_METERS = 2000

                # End point 1
                shoreline_point1_end_point1_x = shoreline_start_point1.x() + EXTEND_LENGTH_METERS * math.cos(angle_rad1)
                shoreline_point1_end_point1_y = shoreline_start_point1.y() + EXTEND_LENGTH_METERS * math.sin(angle_rad1)
                shoreline_point1_end_point1 = QgsPoint(shoreline_point1_end_point1_x, shoreline_point1_end_point1_y)

                shoreline_point2_end_point1_x = shoreline_start_point2.x() + EXTEND_LENGTH_METERS * math.cos(angle_rad2)
                shoreline_point2_end_point1_y = shoreline_start_point2.y() + EXTEND_LENGTH_METERS * math.sin(angle_rad2)
                shoreline_point2_end_point1 = QgsPoint(shoreline_point2_end_point1_x, shoreline_point2_end_point1_y)

                # End point 2
                angle_rad1 += math.pi
                shoreline_point1_end_point2_x = shoreline_start_point1.x() + EXTEND_LENGTH_METERS * math.cos(angle_rad1)
                shoreline_point1_end_point2_y = shoreline_start_point1.y() + EXTEND_LENGTH_METERS * math.sin(angle_rad1)
                shoreline_point1_end_point2 = QgsPoint(shoreline_point1_end_point2_x, shoreline_point1_end_point2_y)

                angle_rad2 += math.pi
                shoreline_point2_end_point2_x = shoreline_start_point2.x() + EXTEND_LENGTH_METERS * math.cos(angle_rad2)
                shoreline_point2_end_point2_y = shoreline_start_point2.y() + EXTEND_LENGTH_METERS * math.sin(angle_rad2)
                shoreline_point2_end_point2 = QgsPoint(shoreline_point2_end_point2_x, shoreline_point2_end_point2_y)

                # Create the line
                shoreline_point1_line = QgsGeometry.fromPolyline([shoreline_point1_end_point1, shoreline_point1_end_point2])
                shoreline_point2_line = QgsGeometry.fromPolyline([shoreline_point2_end_point1, shoreline_point2_end_point2])

                intersect1 = shoreline_point1_line.intersection(longer_shoreline)
                intersect2 = shoreline_point2_line.intersection(longer_shoreline)

                intersection1 = None
                intersection2 = None
                intersections1 = {}
                intersections2 = {}

                if not intersect1.isEmpty():
                    if intersect1.wkbType() == QgsWkbTypes.MultiPoint:
                        for i in intersect1.asMultiPoint():
                            i = QgsGeometry.fromPointXY(i)
                            intersections1[i] = i.distance(
                                QgsGeometry.fromPointXY(
                                    shoreline_start_point1
                                )
                            ) 
                    else:
                        intersections1[intersect1] = intersect1.distance(
                            QgsGeometry.fromPointXY(
                                shoreline_start_point1
                            )
                        )
                    intersection1 = min(intersections1, key=intersections1.get)

                if not intersect2.isEmpty():
                    if intersect2.wkbType() == QgsWkbTypes.MultiPoint:
                        for i in intersect2.asMultiPoint():
                            i = QgsGeometry.fromPointXY(i)
                            intersections2[i] = i.distance(
                                QgsGeometry.fromPointXY(
                                    shoreline_start_point2
                                )
                            ) 
                    else:
                        intersections2[intersect2] = intersect2.distance(
                            QgsGeometry.fromPointXY(
                                shoreline_start_point2
                            )
                        )
                    intersection2 = min(intersections2, key=intersections2.get)

                # TODO: support not just 1 transect
                # But we neeed to make sure if append or insert
                # if shoreline_start_point1 is closer to 
                # cluster[0][0]['geom'].asPolyline()[0] then append

                # if shoreline_start_point1 is closer to 
                # cluster[0][-1]['geom'].asPolyline()[0] then insert

                # TODO: Apply differnet transects start point 1 and 2
                # based on previous assignment / reference
                # for trend, name, group

                if intersection1 is not None:
                    cluster[0].append(
                        {
                            'geom': QgsGeometry.fromPolylineXY([
                                shoreline_start_point1, 
                                intersection1.asPoint()
                            ]),
                            'trend': cluster[0][0]['trend'],
                            'name': cluster[0][0]['name'],
                            'group': cluster[0][0]['group']
                        }
                    )
                
                if intersection2 is not None:
                    # Insert to the first position of the second group
                    cluster[0].insert(0, 
                        {
                            'geom': QgsGeometry.fromPolylineXY([
                                shoreline_start_point2, 
                                intersection2.asPoint()
                            ]),
                            'trend': cluster[0][0]['trend'],
                            'name': cluster[0][0]['name'],
                            'group': cluster[0][0]['group']
                        }
                    )

    return grouped_clustered_interest_transects


def which_shoreline_transect_intersects(transect, shorelines):
    """Determine which shoreline in list of line string shorelines does
    a transects intersects.
    
    Args:
        transect (QgsGeometry): LineString
        shorelines (list[QgsGeometry]): MultiLineString

    Returns:
        QgsGeometry: LineString
    """
    extended_transect = transect.extendLine(
        _EXTEND_BY_SMALL_EPSILON, 
        _EXTEND_BY_SMALL_EPSILON)
    
    for line in shorelines:
        intersect = extended_transect.intersection(line)
        if not intersect.isEmpty():
            ## NOTE: Temporary skip multi intersections
            #if intersect.wkbType() == QgsWkbTypes.MultiPoint:
            return line
    return None