# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from PyQt5.QtCore import QVariant

from qgis.core import Qgis
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsWkbTypes

from qscat.core.layers import create_add_layer
from qscat.core.messages import display_message
from qscat.core.utils.layer import is_field_in_layer


def automate_shoreline_field(self):
    layer = self.dockwidget.qmlcb_automator_field_shoreline_layer.currentLayer()
    date_field = self.dockwidget.le_automator_field_shoreline_date_field_name.text()
    unc_field = self.dockwidget.le_automator_field_shoreline_unc_field_name.text()

    dp = layer.dataProvider()
    attributes = []

    if self.dockwidget.chb_automator_field_shoreline_date_field.isChecked():
        if is_field_in_layer(date_field, layer):
            display_message(
                f'<b>{date_field}</b> already exist!', 
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(date_field, QVariant.String))
            display_message(
                f'<b>{date_field}</b> added!', 
                Qgis.Success,
            )
    if self.dockwidget.chb_automator_field_shoreline_unc_field.isChecked():
        if is_field_in_layer(unc_field, layer):
            display_message(
                f'<b>{unc_field}</b> already exist!', 
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(unc_field, QVariant.Double))
            display_message(
                f'<b>{unc_field}</b> added!', 
                Qgis.Success,
            )

    dp.addAttributes(attributes)
    layer.updateFields()


def automate_baseline_field(self):
    layer = self.dockwidget.qmlcb_automator_field_baseline_layer.currentLayer()
    placement_field = self.dockwidget.le_automator_field_baseline_placement_field_name.text()
    orientation_field = self.dockwidget.le_automator_field_baseline_orientation_field_name.text()
    length_field = self.dockwidget.le_automator_field_baseline_length_field_name.text()

    dp = layer.dataProvider()
    attributes = []

    # TODO: show a list of message
    if self.dockwidget.chb_automator_field_baseline_placement_field.isChecked():
        if is_field_in_layer(placement_field, layer):
            display_message(
                f'<b>{placement_field}</b> already exist!', 
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(placement_field, QVariant.String))
            display_message(
                f'<b>{placement_field}</b> added!', 
                Qgis.Success,
            )

    if self.dockwidget.chb_automator_field_baseline_orientation_field.isChecked():
        if is_field_in_layer(orientation_field, layer):
            display_message(
                f'<b>{orientation_field}</b> already exist!', 
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(orientation_field, QVariant.String))
            display_message(
                f'<b>{orientation_field}</b> added!', 
                Qgis.Success,
            )

    if self.dockwidget.chb_automator_field_baseline_length_field.isChecked():
        if is_field_in_layer(length_field, layer):
            display_message(
                f'<b>{length_field}</b> already exist!', 
                Qgis.Critical,
            )
        else:
            attributes.append(QgsField(length_field, QVariant.Int))
            display_message(
                f'<b>{length_field}</b> added!', 
                Qgis.Success,
            )

    dp.addAttributes(attributes)
    layer.updateFields()


def automate_baseline_buffer(self):
    layer = self.dockwidget.qmlcb_automator_baseline_shorelines_layer.currentLayer()
    distance = int(self.dockwidget.qsb_automator_baseline_buffer_distance.text())

    geoms = []
    for feat in layer.getFeatures():
        geom = feat.geometry()
        buffered_geometry = geom.buffer(
            distance, 
            5,
            QgsGeometry.CapRound,
            QgsGeometry.JoinStyleRound,
            2.0
        )
        geoms.append(buffered_geometry)

    # dissolve result
    unioned_geometry = QgsGeometry().unaryUnion(geoms)
    #print(unioned_geometry)

    # convert to the geometry to linestring
    line_geometry = unioned_geometry.convertToType(
        destType=QgsWkbTypes.LineGeometry,
        destMultipart=True,
    )
    #print(line_geometry)
    fields = [{'name': 'distance', 'type': QVariant.Int}]
    values = [[distance]]
    
    create_add_layer(
        'MultiLineString',
        [line_geometry],
        f'Baseline Buffer - {distance} meters',
        fields,
        values
    )
