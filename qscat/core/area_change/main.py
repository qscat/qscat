# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from PyQt5.QtCore import QVariant

from qgis.core import QgsGeometry

from qscat.core.constants import AreaChangeField
from qscat.core.layer import create_add_layer
from qscat.core.layer import load_polygons
from qscat.core.reports import SummaryReport
from qscat.core.utils.date import datetime_now
from qscat.core.utils.input import get_area_change_input_params
from qscat.core.visualization import apply_area_colors

from qscat.core.area_change.extra_transect import insert_extra_transects
from qscat.core.area_change.half_transect import get_half_transect
from qscat.core.area_change.polygon import extract_area_polygon
from qscat.core.area_change.utils import group_dict_by_key
from qscat.core.area_change.utils import get_interest_transects_within_polygon
from qscat.core.area_change.utils import load_shorelines_by_date

from qscat.core.constants import Trend

# Use to extend a transect by a small value
_EXTEND_BY_SMALL_EPSILON = 1e-8


def compute_area_change_stats(qscat):
    """Compute area change statistics.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.
    """
    area_change_params = get_area_change_input_params(qscat)

    polygon_boundaries = load_polygons(area_change_params["polygon_layer"])

    # Store each area stats per feature of the polygon layer
    polygon_areas_stats = []

    for polygon_boundary in polygon_boundaries:
        # TODO: Add checks if all transects are inside of the polygon, no
        # transects must be outside of the polygon (even a small part)
        # otherwise let's ask user to
        # 1. Redraw the polygon
        # 2. Display an error message
        # 3. Maybe circle which part is outside of the polygon

        # Get transects inside polygon
        interest_transects, interest_transects_ids = (
            get_interest_transects_within_polygon(
                area_change_params["stat_layer"],
                polygon_boundary["geom"],
                polygon_boundary["name"],
            )
        )

        # TODO: If len(interest_transects) == 0, cant compute area change

        layer = qscat.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer()
        date_field = qscat.dockwidget.qfcb_shorelines_date_field.currentField()

        newest_shorelines = load_shorelines_by_date(
            layer,
            area_change_params["stat_layer"].customProperty("newest_date"),
            date_field,
        )

        oldest_shorelines = load_shorelines_by_date(
            layer,
            area_change_params["stat_layer"].customProperty("oldest_date"),
            date_field,
        )

        newest_shorelines_as_lines = [
            QgsGeometry.fromPolylineXY(line)
            for line in newest_shorelines.asMultiPolyline()
        ]  # -> list[QgsGeometry: LineString]

        oldest_shorelines_as_lines = [
            QgsGeometry.fromPolylineXY(line)
            for line in oldest_shorelines.asMultiPolyline()
        ]  # -> list[QgsGeometry: MultiLineString]

        # Add the `group` dict key
        partial_clustered_interest_transects = cluster_interest_transects(
            newest_shorelines_as_lines,
            oldest_shorelines_as_lines,
            interest_transects,
        )  # -> list[dict]

        # Group by list using the `group` key
        clustered_interest_transects = group_dict_by_key(
            partial_clustered_interest_transects, "group"
        )  # -> list[list[dict]]

        # For each clusters, group of same trend: erosion, accretion, stable
        grouped_clustered_interest_transects = []
        for cluster in clustered_interest_transects:
            final_cluster = group_dict_by_key(cluster, "trend")
            grouped_clustered_interest_transects.append(final_cluster)
        # -> list[list[list[dict]]]

        # Get the half transect boundary for each group
        for cluster in grouped_clustered_interest_transects:
            for i in range(len(cluster.copy()) - 1):
                half_transect = get_half_transect(
                    newest_shorelines,
                    oldest_shorelines,
                    cluster[i][-1]["geom"],
                    cluster[i + 1][0]["geom"],
                )
                # Do not insert if the boundary cuts by shoreline
                if half_transect is None:
                    continue

                # Insert new boundary to the groups
                # Insert to the last of the first group
                cluster[i].append(
                    {
                        "geom": half_transect,
                        "trend": cluster[i][0]["trend"],
                        "name": cluster[i][0]["name"],
                    }
                )

                # Insert to the first of the second group
                cluster[i + 1].insert(
                    0,
                    {
                        "geom": half_transect,
                        "trend": cluster[i + 1][0]["trend"],
                        "name": cluster[i][0]["name"],
                    },
                )
                # We insert them that way so that we can use them as both boundary
                # on different groups

        # Remove 1 element cluster that is from first and last
        if len(grouped_clustered_interest_transects[0][0]) == 1:
            grouped_clustered_interest_transects.pop(0)

        if len(grouped_clustered_interest_transects[-1][-1]) == 1:
            grouped_clustered_interest_transects.pop(-1)

        # Fix a cluster with only 1 transect by inserting extra transects
        grouped_clustered_interest_transects = insert_extra_transects(
            grouped_clustered_interest_transects,
            newest_shorelines_as_lines,
            oldest_shorelines_as_lines,
        )

        # Calculate the main result values for each clusters
        for cluster in grouped_clustered_interest_transects:
            polygons = []
            for grouped_by_trend in cluster:

                result = extract_area_polygon(
                    newest_shorelines,
                    oldest_shorelines,
                    grouped_by_trend[0]["geom"],
                    grouped_by_trend[-1]["geom"],
                )

                if result:
                    polygon = {}
                    extracted_polygon, new_newest_shoreline, new_oldest_shoreline = result

                    polygon["geom"] = extracted_polygon
                    polygon["area"] = extracted_polygon.area()
                    polygon["type"] = grouped_by_trend[0]["trend"]
                    polygon["newest_shoreline_length"] = new_newest_shoreline.length()
                    polygon["oldest_shoreline_length"] = new_oldest_shoreline.length()

                    polygon["avg_shoreline_length"] = (
                        polygon["newest_shoreline_length"]
                        + polygon["oldest_shoreline_length"]
                    ) / 2
                    polygon["shoreline_displacement"] = (
                        polygon["area"] / polygon["avg_shoreline_length"]
                    )

                    polygon["name"] = grouped_by_trend[0]["name"]  # Optional area name
                    polygons.append(polygon)

                    # add_layer(
                    #     'LineString',
                    #     [new_newest_shoreline],
                    #     'shoreline - parts by parts',
                    #     [{'name': 'type', 'type': QVariant.String}],
                    #     [['newest']]
                    # )
            polygon_areas_stats.append(polygons)

    # Start summary

    # Flatten polygon_areas_stats
    polygons = [item for sublist in polygon_areas_stats for item in sublist]
    total_area = sum(p["area"] for p in polygons)
    total_newest_length = sum(p["newest_shoreline_length"] for p in polygons)
    total_oldest_length = sum(p["oldest_shoreline_length"] for p in polygons)

    total_area_by_type = {
        Trend.ACCRETING: 0.0,
        Trend.ERODING: 0.0,
        Trend.STABLE: 0.0,
        "accretion_percent": 0.0,
        "erosion_percent": 0.0,
        "stable_percent": 0.0,
    }
    total_newest_length_by_type = {
        Trend.ACCRETING: 0.0,
        Trend.ERODING: 0.0,
        Trend.STABLE: 0.0,
        "accretion_percent": 0.0,
        "erosion_percent": 0.0,
        "stable_percent": 0.0,
    }
    total_oldest_length_by_type = {
        Trend.ACCRETING: 0.0,
        Trend.ERODING: 0.0,
        Trend.STABLE: 0.0,
        "accretion_percent": 0.0,
        "erosion_percent": 0.0,
        "stable_percent": 0.0,
    }

    # Sum area and length by type
    for polygon in polygons:
        if polygon["type"] == Trend.ACCRETING:
            total_area_by_type[Trend.ACCRETING] += polygon["area"]
            total_newest_length_by_type[Trend.ACCRETING] += polygon[
                "newest_shoreline_length"
            ]
            total_oldest_length_by_type[Trend.ACCRETING] += polygon[
                "oldest_shoreline_length"
            ]
        elif polygon["type"] == Trend.ERODING:
            total_area_by_type[Trend.ERODING] += polygon["area"]
            total_newest_length_by_type[Trend.ERODING] += polygon[
                "newest_shoreline_length"
            ]
            total_oldest_length_by_type[Trend.ERODING] += polygon[
                "oldest_shoreline_length"
            ]
        elif polygon["type"] == Trend.STABLE:
            total_area_by_type[Trend.STABLE] += polygon["area"]
            total_newest_length_by_type[Trend.STABLE] += polygon[
                "newest_shoreline_length"
            ]
            total_oldest_length_by_type[Trend.STABLE] += polygon[
                "oldest_shoreline_length"
            ]

    # Get total percentages by type
    total_area_by_type["accretion_percent"] = (
        total_area_by_type[Trend.ACCRETING] / total_area
    )
    total_area_by_type["erosion_percent"] = (
        total_area_by_type[Trend.ERODING] / total_area
    )
    total_area_by_type["stable_percent"] = total_area_by_type[Trend.STABLE] / total_area

    total_newest_length_by_type["accretion_percent"] = (
        total_newest_length_by_type[Trend.ACCRETING] / total_newest_length
    )
    total_newest_length_by_type["erosion_percent"] = (
        total_newest_length_by_type[Trend.ERODING] / total_newest_length
    )
    total_newest_length_by_type["stable_percent"] = (
        total_newest_length_by_type[Trend.STABLE] / total_newest_length
    )

    total_oldest_length_by_type["accretion_percent"] = (
        total_oldest_length_by_type[Trend.ACCRETING] / total_oldest_length
    )
    total_oldest_length_by_type["erosion_percent"] = (
        total_oldest_length_by_type[Trend.ERODING] / total_oldest_length
    )
    total_oldest_length_by_type["stable_percent"] = (
        total_oldest_length_by_type[Trend.STABLE] / total_oldest_length
    )

    layer_fields = [
        {"name": "area", "type": QVariant.Double},
        {"name": "area_percent", "type": QVariant.Double},
        {"name": AreaChangeField.TREND, "type": QVariant.String},
        {"name": "newest_shoreline_length", "type": QVariant.Double},
        {"name": "newest_shoreline_length_percent", "type": QVariant.Double},
        {"name": "oldest_shoreline_length", "type": QVariant.Double},
        {"name": "oldest_shoreline_length_percent", "type": QVariant.Double},
        {"name": "avg_shoreline_length", "type": QVariant.Double},
        {"name": "mean_shoreline_displacement", "type": QVariant.Double},
        {"name": "name", "type": QVariant.String},
    ]
    layer_values = []

    # Get field values per current single area (not total)
    for polygon in polygons:
        area_percentage = polygon["area"] / total_area
        newest_length_percentage = (
            polygon["newest_shoreline_length"] / total_newest_length
        )
        oldest_length_percentage = (
            polygon["oldest_shoreline_length"] / total_oldest_length
        )

        value = [
            round(polygon["area"], 2),
            round(area_percentage * 100, 2),
            polygon["type"],
            round(polygon["newest_shoreline_length"], 2),
            round(newest_length_percentage * 100, 2),
            round(polygon["oldest_shoreline_length"], 2),
            round(oldest_length_percentage * 100, 2),
            round(polygon["avg_shoreline_length"], 2),
            round(polygon["shoreline_displacement"], 2),
            polygon["name"],
        ]

        layer_values.append(value)

    # TODO: Add area change layer output to a group 'Area'
    # layer_group = QgsProject.instance().layerTreeRoot().addGroup('Area')

    current_datetime = datetime_now()

    polygon_geoms = [p["geom"] for p in polygons]
    polygon_layer = create_add_layer(
        geometry="Polygon",
        geometries=polygon_geoms,
        name=f'{area_change_params["polygon_layer"].name()}_area',
        fields=layer_fields,
        values=layer_values,
        datetime=current_datetime,
    )

    if (
        qscat.dockwidget.cb_enable_report_generation.isChecked()
        and qscat.dockwidget.cb_enable_area_change_report.isChecked()
    ):
        summary = {}

        # Base information
        summary["datetime"] = current_datetime

        # Summary of results
        # Area Change
        summary["total_area"] = round(total_area, 2)

        # Erosion
        erosion_count = len([p for p in polygons if p["type"] == Trend.ERODING])
        erosion_areas = [p["area"] for p in polygons if p["type"] == Trend.ERODING]
        summary["area_erosion_total_of_areas"] = round(
            total_area_by_type[Trend.ERODING], 2
        )
        summary["area_erosion_pct_of_areas"] = (
            f"{total_area_by_type['erosion_percent']*100:.2f}%"
        )
        summary["area_erosion_num_of_areas"] = erosion_count
        summary["area_erosion_pct_of_num_of_areas"] = (
            f"{(erosion_count / len(polygons)) * 100:.2f}%"
        )
        summary["area_erosion_avg"] = round(
            total_area_by_type[Trend.ERODING] / len(polygons), 2
        )
        summary["area_erosion_max"] = (
            round(max(erosion_areas), 2) if erosion_areas else 0
        )
        summary["area_erosion_min"] = (
            round(min(erosion_areas), 2) if erosion_areas else 0
        )

        # Accretion
        accretion_count = len([p for p in polygons if p["type"] == Trend.ACCRETING])
        accretion_areas = [p["area"] for p in polygons if p["type"] == Trend.ACCRETING]
        summary["area_accretion_total_of_areas"] = round(
            total_area_by_type[Trend.ACCRETING], 2
        )
        summary["area_accretion_pct_of_areas"] = (
            f"{total_area_by_type['accretion_percent']*100:.2f}%"
        )
        summary["area_accretion_num_of_areas"] = accretion_count
        summary["area_accretion_pct_of_num_of_areas"] = (
            f"{(accretion_count / len(polygons)) * 100:.2f}%"
        )
        summary["area_accretion_avg"] = round(
            total_area_by_type[Trend.ACCRETING] / len(polygons), 2
        )
        summary["area_accretion_max"] = (
            round(max(accretion_areas), 2) if accretion_areas else 0
        )
        summary["area_accretion_min"] = (
            round(min(accretion_areas), 2) if accretion_areas else 0
        )

        # Stable
        stable_count = len([p for p in polygons if p["type"] == Trend.STABLE])
        stable_areas = [p["area"] for p in polygons if p["type"] == Trend.STABLE]
        summary["area_stable_total_of_areas"] = round(
            total_area_by_type[Trend.STABLE], 2
        )
        summary["area_stable_pct_of_areas"] = (
            f"{total_area_by_type['stable_percent']*100:.2f}%"
        )
        summary["area_stable_num_of_areas"] = stable_count
        summary["area_stable_pct_of_num_of_areas"] = (
            f"{(stable_count / len(polygons)) * 100:.2f}%"
        )
        summary["area_stable_avg"] = round(
            total_area_by_type[Trend.STABLE] / len(polygons), 2
        )
        summary["area_stable_max"] = round(max(stable_areas), 2) if stable_areas else 0
        summary["area_stable_min"] = round(min(stable_areas), 2) if stable_areas else 0

        # Newest shoreline length
        summary["total_newest_length"] = round(total_newest_length, 2)

        # Erosion
        erosion_newest_lengths = [
            p["newest_shoreline_length"] for p in polygons if p["type"] == Trend.ERODING
        ]
        summary["newest_length_erosion_total_of_lengths"] = round(
            total_newest_length_by_type[Trend.ERODING], 2
        )
        summary["newest_length_erosion_pct_of_lengths"] = (
            f"{total_newest_length_by_type['erosion_percent']*100:.2f}%"
        )
        summary["newest_length_erosion_num_of_lengths"] = erosion_count
        summary["newest_length_erosion_pct_of_num_of_lengths"] = (
            f"{(erosion_count / len(polygons)) * 100:.2f}%"
        )
        summary["newest_length_erosion_avg"] = round(
            total_newest_length_by_type[Trend.ERODING] / len(polygons), 2
        )
        summary["newest_length_erosion_max"] = (
            round(max(erosion_newest_lengths), 2) if erosion_newest_lengths else 0
        )
        summary["newest_length_erosion_min"] = (
            round(min(erosion_newest_lengths), 2) if erosion_newest_lengths else 0
        )

        # Accretion
        accretion_newest_lengths = [
            p["newest_shoreline_length"]
            for p in polygons
            if p["type"] == Trend.ACCRETING
        ]
        summary["newest_length_accretion_total_of_lengths"] = round(
            total_newest_length_by_type[Trend.ACCRETING], 2
        )
        summary["newest_length_accretion_pct_of_lengths"] = (
            f"{total_newest_length_by_type['accretion_percent']*100:.2f}%"
        )
        summary["newest_length_accretion_num_of_lengths"] = accretion_count
        summary["newest_length_accretion_pct_of_num_of_lengths"] = (
            f"{(accretion_count / len(polygons)) * 100:.2f}%"
        )
        summary["newest_length_accretion_avg"] = round(
            total_newest_length_by_type[Trend.ACCRETING] / len(polygons), 2
        )
        summary["newest_length_accretion_max"] = (
            round(max(accretion_newest_lengths), 2) if accretion_newest_lengths else 0
        )
        summary["newest_length_accretion_min"] = (
            round(min(accretion_newest_lengths), 2) if accretion_newest_lengths else 0
        )

        # Stable
        stable_newest_lengths = [
            p["newest_shoreline_length"] for p in polygons if p["type"] == Trend.STABLE
        ]
        summary["newest_length_stable_total_of_lengths"] = round(
            total_newest_length_by_type[Trend.STABLE], 2
        )
        summary["newest_length_stable_pct_of_lengths"] = (
            f"{total_newest_length_by_type['stable_percent']*100:.2f}%"
        )
        summary["newest_length_stable_num_of_lengths"] = stable_count
        summary["newest_length_stable_pct_of_num_of_lengths"] = (
            f"{(stable_count / len(polygons)) * 100:.2f}%"
        )
        summary["newest_length_stable_avg"] = round(
            total_newest_length_by_type[Trend.STABLE] / len(polygons), 2
        )
        summary["newest_length_stable_max"] = (
            round(max(stable_newest_lengths), 2) if stable_newest_lengths else 0
        )
        summary["newest_length_stable_min"] = (
            round(min(stable_newest_lengths), 2) if stable_newest_lengths else 0
        )

        # Oldest shoreline length
        summary["total_oldest_length"] = round(total_oldest_length, 2)

        # Erosion
        erosion_oldest_lengths = [
            p["oldest_shoreline_length"] for p in polygons if p["type"] == Trend.ERODING
        ]
        summary["oldest_length_erosion_total_of_lengths"] = round(
            total_oldest_length_by_type[Trend.ERODING], 2
        )
        summary["oldest_length_erosion_pct_of_lengths"] = (
            f"{total_oldest_length_by_type['erosion_percent']*100:.2f}%"
        )
        summary["oldest_length_erosion_num_of_lengths"] = erosion_count
        summary["oldest_length_erosion_pct_of_num_of_lengths"] = (
            f"{(erosion_count / len(polygons)) * 100:.2f}%"
        )
        summary["oldest_length_erosion_avg"] = round(
            total_oldest_length_by_type[Trend.ERODING] / len(polygons), 2
        )
        summary["oldest_length_erosion_max"] = (
            round(max(erosion_oldest_lengths), 2) if erosion_oldest_lengths else 0
        )
        summary["oldest_length_erosion_min"] = (
            round(min(erosion_oldest_lengths), 2) if erosion_oldest_lengths else 0
        )

        # Accretion
        accretion_oldest_lengths = [
            p["oldest_shoreline_length"]
            for p in polygons
            if p["type"] == Trend.ACCRETING
        ]
        summary["oldest_length_accretion_total_of_lengths"] = round(
            total_oldest_length_by_type[Trend.ACCRETING], 2
        )
        summary["oldest_length_accretion_pct_of_lengths"] = (
            f"{total_oldest_length_by_type['accretion_percent']*100:.2f}%"
        )
        summary["oldest_length_accretion_num_of_lengths"] = accretion_count
        summary["oldest_length_accretion_pct_of_num_of_lengths"] = (
            f"{(accretion_count / len(polygons)) * 100:.2f}%"
        )
        summary["oldest_length_accretion_avg"] = round(
            total_oldest_length_by_type[Trend.ACCRETING] / len(polygons), 2
        )
        summary["oldest_length_accretion_max"] = (
            round(max(accretion_oldest_lengths), 2) if accretion_oldest_lengths else 0
        )
        summary["oldest_length_accretion_min"] = (
            round(min(accretion_oldest_lengths), 2) if accretion_oldest_lengths else 0
        )

        # Stable
        stable_oldest_lengths = [
            p["oldest_shoreline_length"] for p in polygons if p["type"] == Trend.STABLE
        ]
        summary["oldest_length_stable_total_of_lengths"] = round(
            total_oldest_length_by_type[Trend.STABLE], 2
        )
        summary["oldest_length_stable_pct_of_lengths"] = (
            f"{total_oldest_length_by_type['stable_percent']*100:.2f}%"
        )
        summary["oldest_length_stable_num_of_lengths"] = stable_count
        summary["oldest_length_stable_pct_of_num_of_lengths"] = (
            f"{(stable_count / len(polygons)) * 100:.2f}%"
        )
        summary["oldest_length_stable_avg"] = round(
            total_oldest_length_by_type[Trend.STABLE] / len(polygons), 2
        )
        summary["oldest_length_stable_max"] = (
            round(max(stable_oldest_lengths), 2) if stable_oldest_lengths else 0
        )
        summary["oldest_length_stable_min"] = (
            round(min(stable_oldest_lengths), 2) if stable_oldest_lengths else 0
        )

        # Mean shoreline displacement
        summary["mean_shoreline_displacement_avg"] = round(
            sum(p["shoreline_displacement"] for p in polygons) / len(polygons), 2
        )
        summary["mean_shoreline_displacement_max"] = round(
            max(p["shoreline_displacement"] for p in polygons), 2
        )
        summary["mean_shoreline_displacement_min"] = round(
            min(p["shoreline_displacement"] for p in polygons), 2
        )

        reports = SummaryReport(qscat, summary)
        reports.area_change()

    # Shoreline length geometry
    # interest_newest_shorelines = add_layer(
    #     'LineString',
    #     [interest_newest_shorelines],
    #     'Area - interest newest shorelines',
    #     [{'name': 'type', 'type': QVariant.String}],
    #     [['newest']]
    # )
    # interest_oldest_shorelines = add_layer(
    #     'LineString',
    #     [interest_oldest_shorelines],
    #     'Area - interest oldest shorelines',
    #     [{'name': 'type', 'type': QVariant.String}],
    #     [['oldest']]
    # )
    apply_area_colors(polygon_layer)


def cluster_interest_transects(
    newest_shorelines_as_lines, oldest_shorelines_as_lines, interest_transects
):
    """Add a new `group` key to the list of interest transects.
    Grouping is based on the transect's intersection to the
    multi newest and oldest shorelines.

    - TODO: Add illustration + link
    - TODO: Group by whole shorelines
        - Currently groups (hardcoded) by stat NSM and EPR (newest and oldest)

    Args:
        newest_shorelines_as_lines (list[QgsGeometry]): MultiLineString
        oldest_shorelines_as_lines (list[QgsGeometry]): MultiLineString
        interest_transects (list[dict[QgsGeometry, str, str]]): List of transects

    Returns:
        list[dict[QgsGeometry, str, str, str]]: List of transects
    """
    # TODO: check if interest transects num = transects num
    interest_transects_clustered = []

    for ti, transect in enumerate(interest_transects):
        new_group = ""
        old_group = ""

        transect = transect["geom"]
        transect = transect.extendLine(
            _EXTEND_BY_SMALL_EPSILON, _EXTEND_BY_SMALL_EPSILON
        )

        # newest shorelines
        for i, shoreline in enumerate(newest_shorelines_as_lines):
            # Get the intersection nearest to the transect point
            # Handles two or more intersections
            if transect.intersects(shoreline):
                new_group = str(i)

        for i, shoreline in enumerate(oldest_shorelines_as_lines):
            # Get the intersection nearest to the transect point
            # Handles two or more intersections
            if transect.intersects(shoreline):
                old_group = str(i)

        interest_transects[ti]["group"] = new_group + old_group
        interest_transects_clustered.append(interest_transects[ti])

    return interest_transects_clustered
