# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QComboBox, QLineEdit, QRadioButton
from qgis.core import Qgis, QgsProject
from qgis.gui import (
    QgsDoubleSpinBox,
    QgsFieldComboBox,
    QgsFileWidget,
    QgsMapLayerComboBox,
    QgsSpinBox,
)

from qscat.core.inputs import Inputs
from qscat.core.messages import display_message
from qscat.core.tabs.project_setting import load_current_projection


class Settings:
    """This refers to QGIS' project setting key-value saving. This is different
    from the Project Settings Tab. Although, Project Settings Tab uses this just
    for that section."""

    def __init__(self, qdw):
        self.qdw = qdw
        self.inputs = Inputs(qdw)

    @staticmethod
    def save(key, val):
        """Save project setting.

        Args:
            key (str): The key.
            val (str, int, float, bool): The value.
        """
        if val is not None:
            project = QgsProject.instance()
            val_type = type(val)
            if val_type is str or val_type is int:
                project.writeEntry("qscat", key, val)
            elif val_type is float:
                project.writeEntryDouble("qscat", key, val)
            elif val_type is bool:
                project.writeEntryBool("qscat", key, val)
            else:
                raise ValueError(
                    f"Invalid value type for saving settings: {val_type}. Only `str`, `int`, `float`, and `bool` are allowed."
                )

    @staticmethod
    def read(key, _type=str):
        """Read project setting.

        Args:
            key (str): The key.
            _type (str, int, float, bool): The value type.

        Returns:
            tuple: The value and result.
        """
        project = QgsProject.instance()
        if _type is str:
            val, res = project.readEntry("qscat", key)
        elif _type is int:
            val, res = project.readNumEntry("qscat", key)
        elif _type is float:
            val, res = project.readDoubleEntry("qscat", key)
        elif _type is bool:
            val, res = project.readBoolEntry("qscat", key)
        else:
            raise ValueError(
                f"Invalid value type for reading settings: {_type}. Only `str`, `int`, `float`, and `bool` are allowed."
            )
        return (val, res)

    def load(self, key, widget):
        """Populate the QT widget value given by a QT widget object and project
        setting `key`."""
        project = QgsProject.instance()
        _type = str
        if isinstance(
            widget,
            (
                QgsMapLayerComboBox,
                QLineEdit,
                QgsFieldComboBox,
                QgsSpinBox,
                QgsFileWidget,
                QgsDoubleSpinBox,
                QComboBox,
            ),
        ):
            _type = str
        elif isinstance(widget, (QRadioButton, QCheckBox)):
            _type = bool

        value, res = self.read(key, _type)

        if res:
            if isinstance(widget, (QRadioButton, QCheckBox)):
                widget.setChecked(value)
            elif isinstance(widget, QgsMapLayerComboBox):
                widget.setLayer(project.mapLayer(value))
            elif isinstance(widget, QLineEdit):
                widget.setText(value)
            elif isinstance(widget, QgsSpinBox):
                widget.setValue(int(value))
            elif isinstance(widget, QgsDoubleSpinBox):
                widget.setValue(float(value))
            elif isinstance(widget, QgsFieldComboBox):
                widget.setField(value)
            elif isinstance(widget, QComboBox):
                i = widget.findText(value, Qt.MatchExactly)
                widget.setCurrentIndex(i)
            elif isinstance(widget, QgsFileWidget):
                widget.setFilePath(value)
            else:
                raise ValueError(
                    "Changing saved settings is only for: `combo_box` and `line_edit`."
                )

    def load_project(self):
        """Load Project Settings Tab settings."""
        load_current_projection(self.qdw)
        self.qdw.qpsw_proj_selected_crs.setCrs(QgsProject.instance().crs())
        self.load("author_full_name", self.qdw.le_proj_author_full_name)
        self.load("author_affiliation", self.qdw.le_proj_author_affiliation)
        self.load("author_email", self.qdw.le_proj_author_email)

    def load_shorelines(self):
        """Load Shorelines Tab settings."""
        self.load("shorelines_layer_id", self.qdw.qmlcb_shorelines_layer)
        self.load("default_data_unc", self.qdw.le_shorelines_default_data_unc)
        self.load("date_field", self.qdw.qfcb_shorelines_date_field)
        self.load("unc_field", self.qdw.qfcb_shorelines_unc_field)

    def load_baseline(self):
        """Load Baseline Tab settings."""
        self.load("baseline_layer_id", self.qdw.qmlcb_baseline_layer)
        self.load("is_baseline_placement_sea", self.qdw.rb_baseline_placement_sea)
        self.load("is_baseline_placement_land", self.qdw.rb_baseline_placement_land)
        self.load(
            "is_baseline_orientation_land_right",
            self.qdw.rb_baseline_orientation_land_right,
        )
        self.load(
            "is_baseline_orientation_land_left",
            self.qdw.rb_baseline_orientation_land_left,
        )
        self.load("show_baseline_orientation", self.qdw.cb_baseline_show_orientation)
        self.load("placement_field", self.qdw.qfcb_baseline_placement_field)
        self.load("orientation_field", self.qdw.qfcb_baseline_orientation_field)
        self.load("transect_length_field", self.qdw.qfcb_baseline_length_field)
        self.load("smoothing_distance_field", self.qdw.qfcb_baseline_smoothing_field)

    def load_transects(self):
        """Load Transects Tab settings."""
        self.load("layer_output_name", self.qdw.le_transects_layer_output_name)
        self.load("is_by_transect_spacing", self.qdw.rb_transects_by_transect_spacing)
        self.load(
            "is_by_number_of_transects", self.qdw.rb_transects_by_number_of_transects
        )
        self.load("by_transect_spacing", self.qdw.qsb_transects_by_transect_spacing)
        self.load(
            "by_number_of_transects", self.qdw.qsb_transects_by_number_of_transects
        )
        self.load("length", self.qdw.qsb_transects_length)
        self.load("smoothing_distance", self.qdw.qsb_transects_smoothing_distance)

    def load_shoreline_change(self):
        """Load Shoreline Change Tab settings."""
        self.load("transects_layer_id", self.qdw.qmlcb_shoreline_change_transects_layer)
        self.load("is_clip_transects", self.qdw.cb_stats_clip_transects)
        self.load("is_choose_by_distance", self.qdw.rb_choose_by_distance)
        self.load(
            "is_choose_by_distance_farthest", self.qdw.rb_choose_by_distance_farthest
        )
        self.load(
            "is_choose_by_distance_closest", self.qdw.rb_choose_by_distance_closest
        )
        self.load("is_choose_by_placement", self.qdw.rb_choose_by_placement)
        self.load(
            "is_choose_by_placement_seaward", self.qdw.rb_choose_by_placement_seaward
        )
        self.load(
            "is_choose_by_placement_landward", self.qdw.rb_choose_by_placement_landward
        )
        self.load("is_stats_select_all", self.qdw.cb_stats_select_all)
        self.load("is_stats_SCE", self.qdw.cb_stats_SCE)
        self.load("is_stats_NSM", self.qdw.cb_stats_NSM)
        self.load("is_stats_EPR", self.qdw.cb_stats_EPR)
        self.load("is_stats_LRR", self.qdw.cb_stats_LRR)
        self.load("is_stats_WLR", self.qdw.cb_stats_WLR)
        self.load("newest_date", self.qdw.cb_shoreline_change_newest_date)
        self.load("oldest_date", self.qdw.cb_shoreline_change_oldest_date)
        self.load("confidence_interval", self.qdw.qdsb_stats_confidence_interval)

    def load_area_change(self):
        """Load Area Change Tab settings."""
        self.load("polygon_layer_id", self.qdw.qmlcb_area_change_polygon_layer)
        self.load("stat_layer_id", self.qdw.qmlcb_area_change_stat_layer)

    def load_forecasting(self):
        """Load Forecasting Tab settings."""
        self.load("transects_layer_id", self.qdw.qmlcb_forecasting_transects_layer)
        self.load("is_algorithm1", self.qdw.cb_forecasting_algorithm_1)
        self.load("is_time_10y", self.qdw.rb_forecasting_time_10y)
        self.load("is_time_20y", self.qdw.rb_forecasting_time_20y)

    def load_visualization(self):
        """Load Visualization Tab settings."""
        self.load("stat_layer_id", self.qdw.qmlcb_vis_stat_layer)
        self.load("stat_field", self.qdw.qfcb_vis_stat_field)
        self.load("unc_value", self.qdw.le_vis_unc_value)
        self.load("mode", self.qdw.cb_vis_mode)
        self.load("neg_classes", self.qdw.qsb_vis_neg_classes)
        self.load("pos_classes", self.qdw.qsb_vis_pos_classes)

    def load_summary_reports(self):
        """Load Summary Reports Tab settings."""
        self.load("is_report", self.qdw.cb_enable_report_generation)
        self.load(
            "is_shoreline_change_report",
            self.qdw.cb_enable_shoreline_change_report,
        )
        self.load("is_area_change_report", self.qdw.cb_enable_shoreline_change_report)
        self.load("is_forecasting_report", self.qdw.cb_enable_forecasting_report)
        self.load("save_location", self.qdw.qfw_report_save_location)

    def load_all(self):
        """Load all settings."""
        self.load_project()
        self.load_shorelines()
        self.load_baseline()
        self.load_transects()
        self.load_shoreline_change()
        self.load_area_change()
        self.load_forecasting()
        self.load_visualization()
        self.load_summary_reports()

    # -------------------------------------------------------------------------
    # Save project settings
    # -------------------------------------------------------------------------

    def save_project(self):
        """Save Project Settings Tab settings."""
        QgsProject.instance().setCrs(self.qdw.qpsw_proj_selected_crs.crs())
        load_current_projection(self.qdw)

        project = self.inputs.project()
        self.save("author_full_name", project["author_full_name"])
        self.save("author_affiliation", project["author_affiliation"])
        self.save("author_email", project["author_email"])

        display_message("Project settings inputs saved!", Qgis.Info)

    def save_shorelines(self):
        """Save Shorelines Tab settings."""
        shorelines = self.inputs.shorelines()
        self.save(
            "shorelines_layer_id",
            shorelines["shorelines_layer"].id()
            if shorelines["shorelines_layer"]
            else "",
        )
        self.save("default_data_unc", shorelines["default_data_unc"])
        self.save("date_field", shorelines["date_field"])
        self.save("unc_field", shorelines["unc_field"])

        display_message("Shorelines inputs saved!", Qgis.Info)

    def save_baseline(self):
        """Save Baseline Tab settings."""
        baseline = self.inputs.baseline()
        self.save(
            "baseline_layer_id",
            baseline["baseline_layer"].id() if baseline["baseline_layer"] else "",
        )
        self.save("is_baseline_placement_sea", baseline["is_baseline_placement_sea"])
        self.save("is_baseline_placement_land", baseline["is_baseline_placement_land"])
        self.save(
            "is_baseline_orientation_land_right",
            baseline["is_baseline_orientation_land_right"],
        )
        self.save(
            "is_baseline_orientation_land_left",
            baseline["is_baseline_orientation_land_left"],
        )
        self.save("show_baseline_orientation", baseline["show_baseline_orientation"])
        self.save("placement_field", baseline["placement_field"])
        self.save("orientation_field", baseline["orientation_field"])
        self.save("transect_length_field", baseline["transect_length_field"])
        self.save("smoothing_distance_field", baseline["smoothing_distance_field"])

        display_message("Baseline inputs saved!", Qgis.Info)

    def save_transects(self):
        """Save Transects Tab settings."""
        transects = self.inputs.transects()
        self.save("layer_output_name", transects["layer_output_name"])
        self.save("is_by_transect_spacing", transects["is_by_transect_spacing"])
        self.save("is_by_number_of_transects", transects["is_by_number_of_transects"])
        self.save("by_transect_spacing", transects["by_transect_spacing"])
        self.save("by_number_of_transects", transects["by_number_of_transects"])
        self.save("length", transects["length"])
        self.save("smoothing_distance", transects["smoothing_distance"])

        display_message("Transects inputs saved!", Qgis.Info)

    def save_shoreline_change(self):
        """Save Shoreline Change Tab settings."""
        shoreline_change = self.inputs.shoreline_change()
        self.save(
            "transects_layer_id",
            shoreline_change["transects_layer"].id()
            if shoreline_change["transects_layer"]
            else "",
        )
        self.save("is_clip_transects", shoreline_change["is_clip_transects"])
        self.save("is_choose_by_distance", shoreline_change["is_choose_by_distance"])
        self.save(
            "is_choose_by_distance_farthest",
            shoreline_change["is_choose_by_distance_farthest"],
        )
        self.save(
            "is_choose_by_distance_closest",
            shoreline_change["is_choose_by_distance_closest"],
        )
        self.save("is_choose_by_placement", shoreline_change["is_choose_by_placement"])
        self.save(
            "is_choose_by_placement_seaward",
            shoreline_change["is_choose_by_placement_seaward"],
        )
        self.save(
            "is_choose_by_placement_landward",
            shoreline_change["is_choose_by_placement_landward"],
        )
        self.save("is_stats_select_all", shoreline_change["is_stats_select_all"])
        self.save("is_stats_SCE", shoreline_change["is_stats_SCE"])
        self.save("is_stats_NSM", shoreline_change["is_stats_NSM"])
        self.save("is_stats_EPR", shoreline_change["is_stats_EPR"])
        self.save("is_stats_LRR", shoreline_change["is_stats_LRR"])
        self.save("is_stats_WLR", shoreline_change["is_stats_WLR"])
        self.save("newest_date", shoreline_change["newest_date"])
        self.save("oldest_date", shoreline_change["oldest_date"])
        self.save("confidence_interval", shoreline_change["confidence_interval"])

        display_message("Shoreline Change inputs saved!", Qgis.Info)

    def save_area_change(self):
        """Save Area Change Tab settings."""
        area_change = self.inputs.area_change()
        self.save(
            "polygon_layer_id",
            area_change["polygon_layer"].id() if area_change["polygon_layer"] else "",
        )
        self.save(
            "stat_layer_id",
            area_change["stat_layer"].id() if area_change["stat_layer"] else "",
        )

        display_message("Area Change inputs saved!", Qgis.Info)

    def save_forecasting(self):
        """Save Forecasting Tab settings."""
        forecasting = self.inputs.forecasting()
        self.save(
            "transects_layer_id",
            forecasting["transects_layer"].id()
            if forecasting["transects_layer"]
            else "",
        )
        self.save("is_algorithm1", forecasting["is_algorithm1"])
        self.save("is_time_10y", forecasting["is_time_10y"])
        self.save("is_time_20y", forecasting["is_time_20y"])

        display_message("Forecasting inputs saved!", Qgis.Info)

    def save_visualization(self):
        """Save Visualization Tab settings."""
        visualization = self.inputs.visualization()
        self.save(
            "stat_layer_id",
            visualization["stat_layer"].id() if visualization["stat_layer"] else "",
        )
        self.save("stat_field", visualization["stat_field"])
        self.save("unc_value", visualization["unc_value"])
        self.save("mode", visualization["mode"])
        self.save("neg_classes", visualization["neg_classes"])
        self.save("pos_classes", visualization["pos_classes"])

        display_message("Visualization inputs saved!", Qgis.Info)

    def save_summary_reports(self):
        """Save Summary Reports Tab settings."""
        summary_reports = self.inputs.summary_reports()
        self.save("is_report", summary_reports["is_report"])
        self.save(
            "is_shoreline_change_report", summary_reports["is_shoreline_change_report"]
        )
        self.save("is_area_change_report", summary_reports["is_area_change_report"])
        self.save("is_forecasting_report", summary_reports["is_forecasting_report"])
        self.save("save_location", summary_reports["save_location"])

        display_message("Summary Reports inputs saved!", Qgis.Info)
