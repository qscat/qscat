# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from qscat.core.utils.layer import is_field_in_layer


def get_newest_oldest_date_from_layer(layer, date_field):
    pass


def get_interest_transects_within_polygon(layer, polygon, polygon_name):
    """Get transects within polygon.

    # TODO: illustration + link

    Args:
        layer (QgsVectorLayer): Stat layer (NSM, EPR)
        polygon (QgsGeometry): Polygon (user-drawn)
        polygon_name (str): Polygon name (user-defined: e.g. 'Area 1')

    Returns:
        list[dict[QgsGeometry, str, str]]: List of transects
        list[int]: List of transects' id
    """
    interest_transects = []
    interest_transects_ids = []

    features = layer.getFeatures()

    if is_field_in_layer("NSM_trend", layer):
        trend_field = "NSM_trend"
    elif is_field_in_layer("EPR_trend", layer):
        trend_field = "EPR_trend"

    for fi, feat in enumerate(features):
        line = feat.geometry()
        if line.within(polygon):
            interest_transects.append(
                {
                    "geom": line,
                    "trend": feat[trend_field],
                    "name": polygon_name,
                }
            )
            interest_transects_ids.append(fi)

    return (interest_transects, interest_transects_ids)


def group_dict_by_key(dict, key):
    """Create a list of groups of dicts based on a key.
    Convert list of dicts to list of lists of dicts.

    Example:
        [
            {'geom': xxx, group: 1},
            {'geom': xxx, group: 1},
            {'geom': xxx, group: 2}
        ]
        ->
        [
            [{'geom': xxx, group: 1}, {'geom': xxx, group: 1}],
            [{'geom': xxx, group: 2}]
        ]

    Args:
        dict (list[dict]): List of dicts
        key (str): Key to group by

    Returns:
        list[list[dict]]: List of groups of dicts
    """
    groups = []
    current_group = [dict[0]]
    for i in range(1, len(dict)):
        if dict[i][key] == dict[i - 1][key]:
            current_group.append(dict[i])
        else:
            groups.append(current_group)
            current_group = [dict[i]]
    groups.append(current_group)
    return groups


def load_shorelines_by_date(layer, date, date_field):
    """Load a multi line string shoreline geometry given by field `date`.

    Args:
        layer (QgsVectorLayer): Vector layer of shorelines.
        date (str): Date of the shoreline (MM/YYYY).
        date_field (str): The current `date` field.

    Returns:
        QgsGeometry: MultiLineString
    """
    feats = layer.getFeatures()

    for feat in feats:
        if feat[date_field] == date:
            return feat.geometry()
