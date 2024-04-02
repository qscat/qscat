# QSCAT by Louis Facun – louisfacun@gmail.com
# License – GPL v3

from qgis.core import QgsGeometry
from qgis.core import QgsWkbTypes


def extract_area_polygon(shoreline1, shoreline2, transect1, transect2):
    """Extract the area's polygon(s) between two shorelines and two transects.
    
    # TODO: illustration + link

    Args:
        shoreline1 (QgsGeometry): MultiLineString
        shoreline2 (QgsGeometry): MultiLineString
        transect1 (QgsGeometry): LineString
        transect2 (QgsGeometry): LineString

    Returns:
        QgsGeometry: Polygon, TODO: MultiPolygon
    """
    EPSILON = 1e-8
    extended_transect1 = transect1.extendLine(EPSILON, EPSILON)
    extended_transect2 = transect2.extendLine(EPSILON, EPSILON)

    transect1_shoreline1_intersections = get_transect_shoreline_intersections(
        extended_transect1, shoreline1)
    transect1_shoreline2_intersections = get_transect_shoreline_intersections(
        extended_transect1, shoreline2)
    transect2_shoreline1_intersections = get_transect_shoreline_intersections(
        extended_transect2, shoreline1)
    transect2_shoreline2_intersections = get_transect_shoreline_intersections(
        extended_transect2, shoreline2)

    # Determine which transect end points touches which shoreline
    if transect1.asPolyline()[0] in transect1_shoreline1_intersections:
        shoreline1_transect1_point = transect1.asPolyline()[0]
        shoreline2_transect1_point = transect1.asPolyline()[-1]
    else:
        shoreline1_transect1_point = transect1.asPolyline()[-1]
        shoreline2_transect1_point = transect1.asPolyline()[0]

    if transect2.asPolyline()[0] in transect2_shoreline1_intersections:
        shoreline1_transect2_point = transect2.asPolyline()[0]
        shoreline2_transect2_point = transect2.asPolyline()[-1]
    else:
        shoreline1_transect2_point = transect2.asPolyline()[-1]
        shoreline2_transect2_point = transect2.asPolyline()[0] 

    """
    if we have origin on middle of transect, we can say that
    shoreline1_transect1_point is the farthest point from shoreline1 intersections
    shoreline2_transect1_point is the farthest point from shoreline2 intersections
    """

    # apply filter, if len(intersections) is even, remove farthest point
    # otherwise do nothing
    # TODO: fixes what? show diagram
    if len(transect1_shoreline1_intersections) % 2 == 0:
        if shoreline1_transect1_point == transect1_shoreline1_intersections[-1]:
            transect1_shoreline1_intersections.pop()
        else:
            transect1_shoreline1_intersections.reverse()
            transect1_shoreline1_intersections.pop()
    if len(transect1_shoreline2_intersections) % 2 == 0:
        if shoreline2_transect1_point == transect1_shoreline2_intersections[-1]:
            transect1_shoreline2_intersections.pop()
        else:
            transect1_shoreline2_intersections.reverse()
            transect1_shoreline2_intersections.pop()

    if len(transect2_shoreline1_intersections) % 2 == 0:
        if shoreline1_transect2_point == transect2_shoreline1_intersections[-1]:
            transect2_shoreline1_intersections.pop()
        else:
            transect2_shoreline1_intersections.reverse()
            transect2_shoreline1_intersections.pop()
    if len(transect2_shoreline2_intersections) % 2 == 0:
        if shoreline2_transect2_point == transect2_shoreline2_intersections[-1]:
            transect2_shoreline2_intersections.pop()
        else:
            transect2_shoreline2_intersections.reverse()
            transect2_shoreline2_intersections.pop()

    # Assembling sub transects
    # transect1_middle_sub_transect = (
    #     transect1_shoreline1_intersections[0],
    #     transect1_shoreline2_intersections[0],
    # )
    transect1_left_sub_transects = [
        (
            transect1_shoreline1_intersections[i],
            transect1_shoreline1_intersections[i+1],
        ) for i in range(1, len(transect1_shoreline1_intersections), 2)
    ]
    transect1_right_sub_transects = [
        (
            transect1_shoreline2_intersections[i],
            transect1_shoreline2_intersections[i+1],
        ) for i in range(1, len(transect1_shoreline2_intersections), 2)
    ]

    # transect2_middle_sub_transect = (
    #     transect2_shoreline1_intersections[0],
    #     transect2_shoreline2_intersections[0],
    # )
    transect2_left_sub_transects = [
        (
            transect2_shoreline1_intersections[i],
            transect2_shoreline1_intersections[i+1],
        ) for i in range(1, len(transect2_shoreline1_intersections), 2)
    ]
    transect2_right_sub_transects = [
        (
            transect2_shoreline2_intersections[i],
            transect2_shoreline2_intersections[i+1],
        ) for i in range(1, len(transect2_shoreline2_intersections), 2)
    ]

    # Determine which side we will compare
    # TODO: compare to what?
    both_left_sub_transects_empty = (
        len(transect1_left_sub_transects) == 0 and
        len(transect2_left_sub_transects) == 0
    )
    both_right_sub_transects_empty = (
        len(transect1_right_sub_transects) == 0 and
        len(transect2_right_sub_transects) == 0
    )
    one_of_left_sub_transects_not_empty = (
        len(transect1_left_sub_transects) != 0 or
        len(transect2_left_sub_transects) != 0
    ) 
    one_of_right_sub_transects_not_empty = (
        len(transect1_right_sub_transects) != 0 or
        len(transect2_right_sub_transects) != 0
    )

    if both_left_sub_transects_empty and both_right_sub_transects_empty:
        shoreline1_transect1_intersection = transect1_shoreline1_intersections[0]
        shoreline2_transect1_intersection = transect1_shoreline2_intersections[0]
        
        combined_transects = extended_transect1.combine(extended_transect2)
        
        # fix the problem of perfectly place shoreline point and transect point
        # not fidning intersection
        # for 1 element on a cluster fix
        EPSILON = 1e-8
        for shoreline in shoreline1.asMultiPolyline():
            shoreline_geom = QgsGeometry.fromPolylineXY(shoreline)
            shoreline_geom = shoreline_geom.extendLine(EPSILON, EPSILON)
            if shoreline_geom.intersects(extended_transect1):
                divided_shoreline1 = shoreline_geom.difference(
                    combined_transects)#.asMultiPolyline()[1] 
                
        for shoreline in shoreline2.asMultiPolyline():
            shoreline_geom = QgsGeometry.fromPolylineXY(shoreline)
            shoreline_geom = shoreline_geom.extendLine(EPSILON, EPSILON)
            if shoreline_geom.intersects(extended_transect1):
                divided_shoreline2 = shoreline_geom.difference(
                    combined_transects)#.asMultiPolyline()[1] 
       
        # get second part of divided shoreline
        interest_shoreline1 = divided_shoreline1.asMultiPolyline()[1]
        interest_shoreline2 = divided_shoreline2.asMultiPolyline()[1]

        # reverse if needed
        if shoreline1_transect1_intersection != interest_shoreline1[-1]:
            interest_shoreline1.reverse()
        if shoreline2_transect1_intersection != interest_shoreline2[0]:
            interest_shoreline2.reverse()
        # Connect line strings as one line string
        poly_points = interest_shoreline1 \
            + interest_shoreline2 \
            + [interest_shoreline1[0]]

        # Finally, create the polygon out of that line string
        polygon = QgsGeometry.fromPolygonXY([poly_points])
        
        # For stat
        new_newest_shoreline = QgsGeometry.fromPolylineXY(interest_shoreline1)
        # print("===========================================")
        return polygon, new_newest_shoreline
    
    elif both_left_sub_transects_empty and one_of_right_sub_transects_not_empty:
        print("both_left_sub_transects_empty and one_of_right_sub_transects_not_empty")
    elif both_right_sub_transects_empty and one_of_left_sub_transects_not_empty:
        print("both_right_sub_transects_empty and one_of_left_sub_transects_not_empty")
    elif one_of_left_sub_transects_not_empty and one_of_right_sub_transects_not_empty:
        print("one_of_left_sub_transects_not_empty and one_of_right_sub_transects_not_empty")


def get_transect_shoreline_intersections(transect, shoreline):
    """Get the intersection points of a transects to a shorelines.

    Args:
        transect (QgsGeometry): LineString
        shoreline (QgsGeometry): MultiLineString

    Returns:
        list[QgsPointXY]
    """
    intersections = []
    for line in shoreline.asMultiPolyline():
        line = QgsGeometry.fromPolylineXY(line)
        # Fix not finding an intersection by extending the transect line by small
        extended_line = line.extendLine(1e-8, 1e-8)
        intersect = transect.intersection(extended_line)
        if not intersect.isEmpty():
            if intersect.wkbType() == QgsWkbTypes.MultiPoint:
                for i in intersect.asMultiPoint():
                    intersections.append(i)
            else:
                intersections.append(intersect.asPoint())
                
    return intersections