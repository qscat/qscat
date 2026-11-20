# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

"""Shapes of the dictionaries passed between QSCAT modules.

These are type hints only: at runtime every value is still a plain ``dict``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from PyQt5.QtCore import QVariant
    from qgis.core import QgsGeometry, QgsLineString


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
