# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from PyQt5.QtCore import QVariant

from qgis.core import Qgis
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsWkbTypes

from qscat.core.layer import create_add_layer
from qscat.core.messages import display_message
from qscat.core.utils.layer import is_field_in_layer


# On button clicks
def automate_shoreline_field_button_clicked(qscat):
    """Automate creation of shoreline field (on button clicked).

    Args:
        qscat (QscatPlugin): QscatPlugin instance.
    """
    layer = qscat.dockwidget.qmlcb_automator_field_shoreline_layer.currentLayer()
    date_field = qscat.dockwidget.le_automator_field_shoreline_date_field_name.text()
    unc_field = qscat.dockwidget.le_automator_field_shoreline_unc_field_name.text()

    is_date_field_checked = (
        qscat.dockwidget.chb_automator_field_shoreline_date_field.isChecked()
    )
    is_unc_field_checked = (
        qscat.dockwidget.chb_automator_field_shoreline_unc_field.isChecked()
    )

    automate_shoreline_field(
        layer,
        date_field,
        unc_field,
        is_date_field_checked,
        is_unc_field_checked,
    )


def automate_baseline_field_button_clicked(qscat):
    """Automate creation of baseline field (on button clicked).

    Args:
        qscat (QscatPlugin): QscatPlugin instance.
    """
    layer = qscat.dockwidget.qmlcb_automator_field_baseline_layer.currentLayer()
    placement_field = (
        qscat.dockwidget.le_automator_field_baseline_placement_field_name.text()
    )
    orientation_field = (
        qscat.dockwidget.le_automator_field_baseline_orientation_field_name.text()
    )
    length_field = qscat.dockwidget.le_automator_field_baseline_length_field_name.text()

    is_placement_field_checked = (
        qscat.dockwidget.chb_automator_field_baseline_placement_field.isChecked()
    )
    is_orientation_field_checked = (
        qscat.dockwidget.chb_automator_field_baseline_orientation_field.isChecked()
    )
    is_length_field_checked = (
        qscat.dockwidget.chb_automator_field_baseline_length_field.isChecked()
    )

    automate_baseline_field(
        layer,
        placement_field,
        orientation_field,
        length_field,
        is_placement_field_checked,
        is_orientation_field_checked,
        is_length_field_checked,
    )


def automate_baseline_buffer_button_clicked(qscat):
    """Automate creation of baseline buffer (on button clicked).

    Args:
        qscat (QscatPlugin): QscatPlugin instance.
    """
    layer = qscat.dockwidget.qmlcb_automator_baseline_shorelines_layer.currentLayer()
    distance = int(qscat.dockwidget.qsb_automator_baseline_buffer_distance.text())

    automate_baseline_buffer(layer, distance)


# Main functions
def automate_shoreline_field(
    layer,
    date_field,
    unc_field,
    is_date_field_checked,
    is_unc_field_checked,
):
    """Automate creation of shoreline field.

    Args:
        layer (QgsVectorLayer): Shorelines layer.
        date_field (str): Date field name.
        unc_field (str): Uncertainty field name.
        is_date_field_checked (bool): Date field checkbox.
        is_unc_field_checked (bool): Uncertainty field checkbox.
    """
    dp = layer.dataProvider()
    attributes = []

    if is_date_field_checked:
        if is_field_in_layer(date_field, layer):
            display_message(
                f"<b>{date_field}</b> already exist!",
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(date_field, QVariant.String))
            display_message(
                f"<b>{date_field}</b> added!",
                Qgis.Success,
            )
    if is_unc_field_checked:
        if is_field_in_layer(unc_field, layer):
            display_message(
                f"<b>{unc_field}</b> already exist!",
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(unc_field, QVariant.Double))
            display_message(
                f"<b>{unc_field}</b> added!",
                Qgis.Success,
            )

    dp.addAttributes(attributes)
    layer.updateFields()


def automate_baseline_field(
    layer,
    placement_field,
    orientation_field,
    length_field,
    is_placement_field_checked,
    is_orientation_field_checked,
    is_length_field_checked,
):
    """Automate creation of baseline field.

    Args:
        layer (QgsVectorLayer): Baseline layer.
        placement_field (str): Placement field name.
        orientation_field (str): Orientation field name.
        length_field (str): Length field name.
        is_placement_field_checked (bool): Placement field checkbox.
        is_orientation_field_checked (bool): Orientation field checkbox.
        is_length_field_checked (bool): Length field checkbox.
    """
    dp = layer.dataProvider()
    attributes = []

    if is_placement_field_checked:
        if is_field_in_layer(placement_field, layer):
            display_message(
                f"<b>{placement_field}</b> already exist!",
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(placement_field, QVariant.String))
            display_message(
                f"<b>{placement_field}</b> added!",
                Qgis.Success,
            )

    if is_orientation_field_checked:
        if is_field_in_layer(orientation_field, layer):
            display_message(
                f"<b>{orientation_field}</b> already exist!",
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(orientation_field, QVariant.String))
            display_message(
                f"<b>{orientation_field}</b> added!",
                Qgis.Success,
            )

    if is_length_field_checked:
        if is_field_in_layer(length_field, layer):
            display_message(
                f"<b>{length_field}</b> already exist!",
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(length_field, QVariant.Int))
            display_message(
                f"<b>{length_field}</b> added!",
                Qgis.Success,
            )

    dp.addAttributes(attributes)
    layer.updateFields()


def automate_baseline_buffer(layer, distance):
    """Automate creation of baseline buffer.

    Args:
        layer (QgsVectorLayer): Shorelines layer.
        distance (float): Distance in meters.

    Returns:
        QgsVectorLayer: Baseline buffer layer.
    """
    geoms = []
    for feat in layer.getFeatures():
        geom = feat.geometry()
        buffered_geometry = geom.buffer(
            distance, 5, QgsGeometry.CapRound, QgsGeometry.JoinStyleRound, 2.0
        )
        geoms.append(buffered_geometry)

    # Dissolve result
    unioned_geometry = QgsGeometry().unaryUnion(geoms)

    # Convert the geometry to linestring
    line_geometry = unioned_geometry.convertToType(
        destType=QgsWkbTypes.LineGeometry,
        destMultipart=True,
    )

    fields = [{"name": "distance", "type": QVariant.Int}]
    values = [[distance]]

    layer = create_add_layer(
        geometry="MultiLineString",
        geometries=[line_geometry],
        name=f"Baseline Buffer - {distance} meters",
        fields=fields,
        values=values,
    )

    return layer
