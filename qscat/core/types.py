# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

"""Shapes of the dictionaries passed between QSCAT modules.

These are type hints only: at runtime every value is still a plain ``dict``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from PyQt5.QtCore import QVariant
    from qgis.core import (
        QgsFeatureIterator,
        QgsGeometry,
        QgsLineString,
        QgsVectorLayer,
    )
    from qgis.gui import QgsMapLayerComboBox


class QscatShoreline(TypedDict):
    """A shoreline feature, as loaded by ``load_shorelines``."""

    year: float  # decimal year, e.g. 1990.5
    geoms: list[QgsGeometry]  # LineString parts of the shoreline
    unc: float  # uncertainty; the default is used if missing or <= 0


class QscatBaseline(TypedDict):
    """A baseline part, as loaded by ``load_all_baselines``.

    The optional per-feature values are None when the field is unset or empty.
    """

    line: QgsLineString
    placement: str | None  # "sea" or "land" (from the placement field)
    orientation: str | None  # "right" or "left" (from the orientation field)
    transect_length: float | None  # from the transect length field
    smoothing_distance: float | None  # from the smoothing distance field


class QscatTransectIntersection(TypedDict):
    """One transect-shoreline intersection, as computed per transect."""

    transect_origin: QgsGeometry  # Point at the transect's baseline end
    geom: QgsGeometry  # Point of the chosen intersection
    id: int
    transect_id: int  # 1-based
    shoreline_id: int  # 1-based
    shoreline_year: float  # decimal year
    shoreline_unc: float
    distance: float  # from the baseline; negative if the baseline is on the sea side
    intersect_x: float
    intersect_y: float
    orig_transect_geom: QgsGeometry  # LineString of the transect


class QscatYearIntersection(TypedDict):
    """A transect's intersection with the shoreline of one year."""

    transect_origin: QgsGeometry  # Point at the transect's baseline end
    unc: float  # shoreline uncertainty
    distance: float  # from the baseline; negative if the baseline is on the sea side
    intersect_x: float
    intersect_y: float
    orig_transect_geom: QgsGeometry  # LineString of the transect


# A single transect's intersections, keyed by shoreline decimal year.
QscatYearsIntersections = dict[float, QscatYearIntersection]


class _QscatInterestTransectBase(TypedDict):
    geom: QgsGeometry  # LineString of the transect
    trend: str  # NSM or EPR trend (stable, accreting, eroding)
    name: (
        str | None
    )  # area polygon name (e.g. 'Area 1'); None if the layer has no name field


class QscatInterestTransect(_QscatInterestTransectBase, total=False):
    """A transect within an area change polygon."""

    group: str  # added by cluster_interest_transects


class QscatLayerField(TypedDict):
    """A field definition for ``create_add_layer``."""

    name: str
    type: QVariant.Type  # e.g. QVariant.Double


class QscatForecastResult(TypedDict):
    """Forecasted shoreline position for a single transect."""

    year: float  # forecasted decimal year
    point_geom: QgsGeometry  # Point of the forecasted shoreline
    distance: float  # forecasted distance from the baseline
    point_unc_neg_geom: QgsGeometry  # Point at the negative uncertainty bound
    unc1: float  # negative uncertainty bound (distance)
    point_unc_pos_geom: QgsGeometry  # Point at the positive uncertainty bound
    unc2: float  # positive uncertainty bound (distance)


class _QscatReleaseInfoBase(TypedDict):
    status: str  # SUCCESS, TIMEOUT, BAD_URL or UNKNOWN_ERROR


class QscatReleaseInfo(_QscatReleaseInfoBase, total=False):
    """Latest GitHub release info; the other keys are set only on SUCCESS."""

    tag_name: str  # e.g. v1.0.0
    body: str  # release notes
    zipball_url: str


# Tab inputs, as read from the dock widget by ``Inputs`` (qscat/core/inputs.py).
# Values from text boxes and spin boxes are read with ``.text()``, so they are
# strings; convert them with int() or float() before doing math.


class QscatProjectInputs(TypedDict):
    """Project Settings Tab inputs."""

    crs_id: str  # e.g. "EPSG:32651"
    author_full_name: str
    author_affiliation: str
    author_email: str


class QscatBaselineInputs(TypedDict):
    """Baseline Tab inputs."""

    baseline_layer: QgsVectorLayer  # selected layer (None if nothing is selected)
    is_baseline_placement_sea: bool
    is_baseline_placement_land: bool
    is_baseline_orientation_land_right: bool
    is_baseline_orientation_land_left: bool
    show_baseline_orientation: bool
    placement_field: str  # "" if no field is selected
    orientation_field: str  # "" if no field is selected
    transect_length_field: str  # "" if no field is selected
    smoothing_distance_field: str  # "" if no field is selected


class QscatShorelinesInputs(TypedDict):
    """Shorelines Tab inputs."""

    shorelines_layer: QgsVectorLayer  # selected layer (None if nothing is selected)
    default_data_unc: str  # number as text
    date_field: str  # "" if no field is selected
    unc_field: str  # "" if no field is selected
    feats: QgsFeatureIterator  # can only be iterated once


class QscatTransectsInputs(TypedDict):
    """Transects Tab inputs."""

    layer_output_name: str
    is_by_transect_spacing: bool
    is_by_number_of_transects: bool
    by_transect_spacing: str  # number as text (meters)
    by_number_of_transects: str  # number as text
    length: str  # number as text (meters)
    smoothing_distance: str  # number as text (meters)


class QscatShorelineChangeInputs(TypedDict):
    """Shoreline Change Tab inputs."""

    transects_layer_widget: QgsMapLayerComboBox  # the widget itself
    transects_layer: QgsVectorLayer  # selected layer (None if nothing is selected)
    is_clip_transects: bool
    is_choose_by_distance: bool
    is_choose_by_distance_farthest: bool
    is_choose_by_distance_closest: bool
    is_choose_by_placement: bool
    is_choose_by_placement_seaward: bool
    is_choose_by_placement_landward: bool
    selected_stats: list[str]  # Statistic values, e.g. ["SCE", "NSM"]
    is_stats_select_all: bool
    is_stats_SCE: bool
    is_stats_NSM: bool
    is_stats_EPR: bool
    is_stats_LRR: bool
    is_stats_WLR: bool
    oldest_date: str  # mm/yyyy
    newest_date: str  # mm/yyyy
    oldest_year: float  # decimal year
    newest_year: float  # decimal year
    confidence_interval: float
    epr_unc: float
    highest_unc: float | str  # str if it is the default uncertainty text
    years_uncs: dict[float, float | str]  # {decimal year: uncertainty}


class QscatAreaChangeInputs(TypedDict):
    """Area Change Tab inputs."""

    polygon_layer: QgsVectorLayer  # selected layer (None if nothing is selected)
    stat_layer: QgsVectorLayer  # selected layer (None if nothing is selected)


class QscatForecastingInputs(TypedDict):
    """Forecasting Tab inputs."""

    transects_layer: QgsVectorLayer  # selected layer (None if nothing is selected)
    is_algorithm1: bool
    is_time_10y: bool
    is_time_20y: bool


class QscatVisualizationInputs(TypedDict):
    """Visualization Tab inputs."""

    stat_layer: QgsVectorLayer  # selected layer (None if nothing is selected)
    stat_field: str  # "" if no field is selected
    unc_value: str  # number as text
    mode: int  # classification mode (combo box index)
    neg_classes: str  # number as text
    pos_classes: str  # number as text


class QscatSummaryReportsInputs(TypedDict):
    """Summary Reports Tab inputs."""

    is_report: bool
    is_shoreline_change_report: bool
    is_area_change_report: bool
    is_forecasting_report: bool
    save_location: str  # directory path
