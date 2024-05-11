# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import os

from qgis.core import QgsFieldProxyModel, QgsMapLayerProxyModel, QgsSettings

from qscat.core.utils.plugin import get_metadata_version


def set_automator_tab_widget_properties(qscat):
    qscat.dockwidget.qmlcb_automator_field_shoreline_layer.setFilters(
        QgsMapLayerProxyModel.LineLayer
    )
    qscat.dockwidget.qmlcb_automator_field_shoreline_layer.showCrs()

    qscat.dockwidget.qmlcb_automator_field_baseline_layer.setFilters(
        QgsMapLayerProxyModel.LineLayer
    )
    qscat.dockwidget.qmlcb_automator_field_baseline_layer.showCrs()

    qscat.dockwidget.qmlcb_automator_baseline_shorelines_layer.setFilters(
        QgsMapLayerProxyModel.LineLayer
    )
    qscat.dockwidget.qmlcb_automator_baseline_shorelines_layer.showCrs()


def set_shorelines_tab_widget_properties(qscat):
    qscat.dockwidget.qmlcb_shorelines_layer.setFilters(QgsMapLayerProxyModel.LineLayer)
    qscat.dockwidget.qmlcb_shorelines_layer.showCrs()

    qscat.dockwidget.qfcb_shorelines_date_field.setLayer(
        qscat.dockwidget.qmlcb_shorelines_layer.currentLayer()
    )
    qscat.dockwidget.qfcb_shorelines_unc_field.setLayer(
        qscat.dockwidget.qmlcb_shorelines_layer.currentLayer()
    )

    qscat.dockwidget.qfcb_shorelines_date_field.setFilters(QgsFieldProxyModel.String)
    qscat.dockwidget.qfcb_shorelines_unc_field.setFilters(QgsFieldProxyModel.Double)


def set_baseline_tab_widget_properties(qscat):
    qscat.dockwidget.qmlcb_baseline_layer.setFilters(QgsMapLayerProxyModel.LineLayer)
    qscat.dockwidget.qmlcb_baseline_layer.showCrs()

    qscat.dockwidget.qfcb_baseline_placement_field.setLayer(
        qscat.dockwidget.qmlcb_baseline_layer.currentLayer()
    )
    qscat.dockwidget.qfcb_baseline_orientation_field.setLayer(
        qscat.dockwidget.qmlcb_baseline_layer.currentLayer()
    )
    qscat.dockwidget.qfcb_baseline_length_field.setLayer(
        qscat.dockwidget.qmlcb_baseline_layer.currentLayer()
    )
    qscat.dockwidget.qfcb_baseline_smoothing_field.setLayer(
        qscat.dockwidget.qmlcb_baseline_layer.currentLayer()
    )

    # Show only string fields for placement and orientation
    qscat.dockwidget.qfcb_baseline_placement_field.setFilters(QgsFieldProxyModel.String)
    qscat.dockwidget.qfcb_baseline_orientation_field.setFilters(
        QgsFieldProxyModel.String
    )

    # Show only integer fields for length and smoothing
    qscat.dockwidget.qfcb_baseline_length_field.setFilters(QgsFieldProxyModel.Int)
    qscat.dockwidget.qfcb_baseline_smoothing_field.setFilters(QgsFieldProxyModel.Int)


def set_transects_tab_widget_properties(qscat):
    qscat.dockwidget.qsb_transects_by_transect_spacing.setClearValue(50)
    qscat.dockwidget.qsb_transects_by_number_of_transects.setClearValue(100)
    qscat.dockwidget.qsb_transects_by_number_of_transects.setEnabled(False)
    qscat.dockwidget.qsb_transects_length.setClearValue(2000)
    qscat.dockwidget.qsb_transects_smoothing_distance.setClearValue(500)


def set_shoreline_change_tab_widget_properties(qscat):
    qscat.dockwidget.qmlcb_shoreline_change_transects_layer.setFilters(
        QgsMapLayerProxyModel.LineLayer
    )
    qscat.dockwidget.qmlcb_shoreline_change_transects_layer.showCrs()


def set_area_change_tab_widget_properties(qscat):
    qscat.dockwidget.qmlcb_area_change_stat_layer.setFilters(
        QgsMapLayerProxyModel.LineLayer
    )
    qscat.dockwidget.qmlcb_area_change_polygon_layer.setFilters(
        QgsMapLayerProxyModel.PolygonLayer
    )
    qscat.dockwidget.qmlcb_area_change_stat_layer.showCrs()
    qscat.dockwidget.qmlcb_area_change_polygon_layer.showCrs()


def set_forecasting_tab_widget_properties(qscat):
    qscat.dockwidget.qmlcb_forecasting_transects_layer.setFilters(
        QgsMapLayerProxyModel.LineLayer
    )
    qscat.dockwidget.qmlcb_forecasting_transects_layer.showCrs()


def set_visualization_tab_widget_properties(qscat):
    qscat.dockwidget.qmlcb_vis_stat_layer.setFilters(QgsMapLayerProxyModel.LineLayer)
    qscat.dockwidget.qmlcb_vis_stat_layer.showCrs()

    qscat.dockwidget.qfcb_vis_stat_field.setLayer(
        qscat.dockwidget.qmlcb_vis_stat_layer.currentLayer()
    )
    qscat.dockwidget.qfcb_vis_stat_field.setFilters(QgsFieldProxyModel.Double)
    classification_methods = ["Quantile", "Equal Interval", "Jenks", "Pretty Break"]
    qscat.dockwidget.cb_vis_mode.addItems(classification_methods)


def set_summary_reports_tab_widget_properties(qscat):
    """
    Args:
        qscat (QscatPlugin): QscatPlugin instance.
    """
    # Create a directory for the summary reports in users home directory
    summary_reports_dir = os.path.join(os.path.expanduser("~"), "QSCATSummaryReports")
    os.makedirs(summary_reports_dir, exist_ok=True)
    qscat.dockwidget.qfw_report_save_location.setFilePath(summary_reports_dir)


def set_about_tab_widget_properties(qscat):
    s = QgsSettings()
    last_checked_datetime = s.value("qscat/last_checked_datetime", None)
    latest_version = s.value("qscat/latest_version", None)

    if last_checked_datetime is None:
        qscat.dockwidget.lbl_about_latest_version.setText("Update not yet checked.")
    else:
        qscat.dockwidget.lbl_about_latest_version.setText(
            f"Latest Version: {latest_version} (last checked {last_checked_datetime})"
        )

    qscat.dockwidget.lbl_about_current_version.setText(
        f"Current Version: v{get_metadata_version()}"
    )


def set_plugin_widget_properties(qscat):
    set_automator_tab_widget_properties(qscat)
    set_shorelines_tab_widget_properties(qscat)
    set_baseline_tab_widget_properties(qscat)
    set_transects_tab_widget_properties(qscat)
    set_shoreline_change_tab_widget_properties(qscat)
    set_area_change_tab_widget_properties(qscat)
    set_forecasting_tab_widget_properties(qscat)
    set_visualization_tab_widget_properties(qscat)
    set_summary_reports_tab_widget_properties(qscat)
    set_about_tab_widget_properties(qscat)
