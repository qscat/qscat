# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import os

from qgis.core import QgsFieldProxyModel, QgsMapLayerProxyModel, QgsSettings

from qscat.core.utils.plugin import get_metadata_version


class WidgetProperties:
    """Set the widget properties for the QSCAT plugin."""
    def __init__(self, qdw):
        """
        Args:
            qdw (QscatDockWidget): QscatDockWidget instance.
        """
        self.qdw = qdw

    def set(self):
        """Set all widget properties for the QSCAT plugin."""
        self.set_automator()
        self.set_shorelines()
        self.set_baseline()
        self.set_transects()
        self.set_shoreline_change()
        self.set_area_change()
        self.set_forecasting()
        self.set_visualization()
        self.set_summary_reports()
        self.set_help()

    def set_automator(self):
        """Set the widget properties of the Automator Tab."""
        self.qdw.qmlcb_automator_field_shoreline_layer.setFilters(
            QgsMapLayerProxyModel.LineLayer
        )
        self.qdw.qmlcb_automator_field_shoreline_layer.showCrs()

        self.qdw.qmlcb_automator_field_baseline_layer.setFilters(
            QgsMapLayerProxyModel.LineLayer
        )
        self.qdw.qmlcb_automator_field_baseline_layer.showCrs()

        self.qdw.qmlcb_automator_baseline_shorelines_layer.setFilters(
            QgsMapLayerProxyModel.LineLayer
        )
        self.qdw.qmlcb_automator_baseline_shorelines_layer.showCrs()

    def set_shorelines(self):
        "Set the widget properties of the Shorelines Tab."
        self.qdw.qmlcb_shorelines_layer.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.qdw.qmlcb_shorelines_layer.showCrs()

        self.qdw.qfcb_shorelines_date_field.setLayer(
            self.qdw.qmlcb_shorelines_layer.currentLayer()
        )
        self.qdw.qfcb_shorelines_unc_field.setLayer(
            self.qdw.qmlcb_shorelines_layer.currentLayer()
        )

        self.qdw.qfcb_shorelines_date_field.setFilters(QgsFieldProxyModel.String)
        self.qdw.qfcb_shorelines_unc_field.setFilters(QgsFieldProxyModel.Double)

    def set_baseline(self):
        """Set the widget properties of the Baseline Tab."""
        self.qdw.qmlcb_baseline_layer.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.qdw.qmlcb_baseline_layer.showCrs()

        self.qdw.qfcb_baseline_placement_field.setLayer(
            self.qdw.qmlcb_baseline_layer.currentLayer()
        )
        self.qdw.qfcb_baseline_orientation_field.setLayer(
            self.qdw.qmlcb_baseline_layer.currentLayer()
        )
        self.qdw.qfcb_baseline_length_field.setLayer(
            self.qdw.qmlcb_baseline_layer.currentLayer()
        )
        self.qdw.qfcb_baseline_smoothing_field.setLayer(
            self.qdw.qmlcb_baseline_layer.currentLayer()
        )

        # Show only string fields for placement and orientation
        self.qdw.qfcb_baseline_placement_field.setFilters(QgsFieldProxyModel.String)
        self.qdw.qfcb_baseline_orientation_field.setFilters(QgsFieldProxyModel.String)

        # Show only integer fields for length and smoothing
        self.qdw.qfcb_baseline_length_field.setFilters(QgsFieldProxyModel.Int)
        self.qdw.qfcb_baseline_smoothing_field.setFilters(QgsFieldProxyModel.Int)

    def set_transects(self):
        """Set the widget properties of the Transects Tab."""
        self.qdw.qsb_transects_by_transect_spacing.setClearValue(50)
        self.qdw.qsb_transects_by_number_of_transects.setClearValue(100)
        self.qdw.qsb_transects_by_number_of_transects.setEnabled(False)
        self.qdw.qsb_transects_length.setClearValue(2000)
        self.qdw.qsb_transects_smoothing_distance.setClearValue(500)

    def set_shoreline_change(self):
        """Set the widget properties of the Shoreline Change Tab."""
        self.qdw.qmlcb_shoreline_change_transects_layer.setFilters(
            QgsMapLayerProxyModel.LineLayer
        )
        self.qdw.qmlcb_shoreline_change_transects_layer.showCrs()

    def set_area_change(self):
        """Set the widget properties of the Area Change Tab."""
        self.qdw.qmlcb_area_change_stat_layer.setFilters(
            QgsMapLayerProxyModel.LineLayer
        )
        self.qdw.qmlcb_area_change_polygon_layer.setFilters(
            QgsMapLayerProxyModel.PolygonLayer
        )
        self.qdw.qmlcb_area_change_stat_layer.showCrs()
        self.qdw.qmlcb_area_change_polygon_layer.showCrs()

    def set_forecasting(self):
        """Set the widget properties of the Forecasting Tab."""
        self.qdw.qmlcb_forecasting_transects_layer.setFilters(
            QgsMapLayerProxyModel.LineLayer
        )
        self.qdw.qmlcb_forecasting_transects_layer.showCrs()

    def set_visualization(self):
        """Set the widget properties of the Visualization Tab."""
        self.qdw.qmlcb_vis_stat_layer.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.qdw.qmlcb_vis_stat_layer.showCrs()

        self.qdw.qfcb_vis_stat_field.setLayer(
            self.qdw.qmlcb_vis_stat_layer.currentLayer()
        )
        self.qdw.qfcb_vis_stat_field.setFilters(QgsFieldProxyModel.Double)
        classification_methods = ["Quantile", "Equal Interval", "Jenks", "Pretty Break"]
        self.qdw.cb_vis_mode.addItems(classification_methods)

    def set_summary_reports(self):
        """Set the widget properties of the Summary Reports Tab."""
        # Create a directory for the summary reports in users home directory
        summary_reports_dir = os.path.join(
            os.path.expanduser("~"), "QSCATSummaryReports"
        )
        os.makedirs(summary_reports_dir, exist_ok=True)
        self.qdw.qfw_report_save_location.setFilePath(summary_reports_dir)

    def set_help(self):
        """Set the widget properties of the Help Tab."""
        s = QgsSettings()
        last_checked_datetime = s.value("qscat/last_checked_datetime", None)
        latest_version = s.value("qscat/latest_version", None)

        if last_checked_datetime is None:
            self.qdw.lbl_about_latest_version.setText("Update not yet checked.")
        else:
            self.qdw.lbl_about_latest_version.setText(
                f"Latest Version: {latest_version} (last checked {last_checked_datetime})"
            )

        self.qdw.lbl_about_current_version.setText(
            f"Current Version: v{get_metadata_version()}"
        )
