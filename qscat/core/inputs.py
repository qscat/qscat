# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from qgis.core import QgsProject

from qscat.core.constants import Statistic
from qscat.core.utils.date import convert_to_decimal_year

if TYPE_CHECKING:
    from qscat.qscat_dockwidget import QscatDockWidget


class Inputs:
    """A class that reads the inputs."""

    def __init__(self, qdw: QscatDockWidget):
        self.qdw = qdw

    def project(self) -> dict:
        """Read the inputs in Project Settings Tab."""
        return {
            "crs_id": QgsProject.instance().crs().authid(),
            "author_full_name": self.qdw.le_proj_author_full_name.text(),
            "author_affiliation": self.qdw.le_proj_author_affiliation.text(),
            "author_email": self.qdw.le_proj_author_email.text(),
        }

    def baseline(self) -> dict:
        """Read the inputs in Baseline Tab."""
        return {
            "baseline_layer": self.qdw.qmlcb_baseline_layer.currentLayer(),
            "is_baseline_placement_sea": self.qdw.rb_baseline_placement_sea.isChecked(),
            "is_baseline_placement_land": self.qdw.rb_baseline_placement_land.isChecked(),
            "is_baseline_orientation_land_right": self.qdw.rb_baseline_orientation_land_right.isChecked(),
            "is_baseline_orientation_land_left": self.qdw.rb_baseline_orientation_land_left.isChecked(),
            "show_baseline_orientation": self.qdw.cb_baseline_show_orientation.isChecked(),
            "placement_field": self.qdw.qfcb_baseline_placement_field.currentField(),
            "orientation_field": self.qdw.qfcb_baseline_orientation_field.currentField(),
            "transect_length_field": self.qdw.qfcb_baseline_length_field.currentField(),
            "smoothing_distance_field": self.qdw.qfcb_baseline_smoothing_field.currentField(),
        }

    def shorelines(self) -> dict:
        """Read the inputs in Shorelines Tab."""
        return {
            "shorelines_layer": self.qdw.qmlcb_shorelines_layer.currentLayer(),
            "default_data_unc": self.qdw.le_shorelines_default_data_unc.text(),
            "date_field": self.qdw.qfcb_shorelines_date_field.currentField(),
            "unc_field": self.qdw.qfcb_shorelines_unc_field.currentField(),
            "feats": self.qdw.qmlcb_shorelines_layer.currentLayer().getFeatures(),
        }

    def transects(self) -> dict:
        """Read the inputs in Transects Tab."""
        return {
            "layer_output_name": self.qdw.le_transects_layer_output_name.text(),
            "is_by_transect_spacing": self.qdw.rb_transects_by_transect_spacing.isChecked(),
            "is_by_number_of_transects": self.qdw.rb_transects_by_number_of_transects.isChecked(),
            "by_transect_spacing": self.qdw.qsb_transects_by_transect_spacing.text(),
            "by_number_of_transects": self.qdw.qsb_transects_by_number_of_transects.text(),
            "length": self.qdw.qsb_transects_length.text(),
            "smoothing_distance": self.qdw.qsb_transects_smoothing_distance.text(),
        }

    def shoreline_change(self) -> dict:
        """Read the inputs in Shoreline Change Tab."""
        return {
            "transects_layer_widget": self.qdw.qmlcb_shoreline_change_transects_layer,
            "transects_layer": self.qdw.qmlcb_shoreline_change_transects_layer.currentLayer(),
            "is_clip_transects": self.qdw.cb_stats_clip_transects.isChecked(),
            "is_choose_by_distance": self.qdw.rb_choose_by_distance.isChecked(),
            "is_choose_by_distance_farthest": self.qdw.rb_choose_by_distance_farthest.isChecked(),
            "is_choose_by_distance_closest": self.qdw.rb_choose_by_distance_closest.isChecked(),
            "is_choose_by_placement": self.qdw.rb_choose_by_placement.isChecked(),
            "is_choose_by_placement_seaward": self.qdw.rb_choose_by_placement_seaward.isChecked(),
            "is_choose_by_placement_landward": self.qdw.rb_choose_by_placement_landward.isChecked(),
            "selected_stats": self.selected_stats(),
            "is_stats_select_all": self.qdw.cb_stats_select_all.isChecked(),
            "is_stats_SCE": self.qdw.cb_stats_SCE.isChecked(),
            "is_stats_NSM": self.qdw.cb_stats_NSM.isChecked(),
            "is_stats_EPR": self.qdw.cb_stats_EPR.isChecked(),
            "is_stats_LRR": self.qdw.cb_stats_LRR.isChecked(),
            "is_stats_WLR": self.qdw.cb_stats_WLR.isChecked(),
            "oldest_date": self.qdw.cb_shoreline_change_oldest_date.currentText(),
            "newest_date": self.qdw.cb_shoreline_change_newest_date.currentText(),
            "oldest_year": convert_to_decimal_year(
                self.qdw.cb_shoreline_change_oldest_date.currentText()
            ),
            "newest_year": convert_to_decimal_year(
                self.qdw.cb_shoreline_change_newest_date.currentText()
            ),
            "confidence_interval": self.qdw.qdsb_stats_confidence_interval.value(),
            "epr_unc": self.epr_unc(),
            "highest_unc": self.highest_unc(),
            "years_uncs": self.shorelines_years_uncs(),
        }

    def selected_stats(self) -> list[str]:
        """Read the selected statistics in Shoreline Change Tab."""
        stats = []
        if self.qdw.cb_stats_SCE.isChecked():
            stats.append(Statistic.SCE)
        if self.qdw.cb_stats_NSM.isChecked():
            stats.append(Statistic.NSM)
        if self.qdw.cb_stats_EPR.isChecked():
            stats.append(Statistic.EPR)
        if self.qdw.cb_stats_LRR.isChecked():
            stats.append(Statistic.LRR)
        if self.qdw.cb_stats_WLR.isChecked():
            stats.append(Statistic.WLR)
        return stats

    def area_change(self) -> dict:
        """Read the inputs in Area Change Tab."""
        return {
            "polygon_layer": self.qdw.qmlcb_area_change_polygon_layer.currentLayer(),
            "stat_layer": self.qdw.qmlcb_area_change_stat_layer.currentLayer(),
        }

    def forecasting(self) -> dict:
        """Read the inputs in Forecasting Tab."""
        return {
            "transects_layer": self.qdw.qmlcb_forecasting_transects_layer.currentLayer(),
            "is_algorithm1": self.qdw.cb_forecasting_algorithm_1.isChecked(),
            "is_time_10y": self.qdw.rb_forecasting_time_10y.isChecked(),
            "is_time_20y": self.qdw.rb_forecasting_time_20y.isChecked(),
        }

    def visualization(self) -> dict:
        """Read the inputs in Visualization Tab."""
        return {
            "stat_layer": self.qdw.qmlcb_vis_stat_layer.currentLayer(),
            "stat_field": self.qdw.qfcb_vis_stat_field.currentField(),
            "unc_value": self.qdw.le_vis_unc_value.text(),
            "mode": int(self.qdw.cb_vis_mode.currentIndex()),
            "neg_classes": self.qdw.qsb_vis_neg_classes.text(),
            "pos_classes": self.qdw.qsb_vis_pos_classes.text(),
        }

    def summary_reports(self) -> dict:
        """Read the inputs in Summary Report Tab."""
        return {
            "is_report": self.qdw.cb_enable_report_generation.isChecked(),
            "is_shoreline_change_report": self.qdw.cb_enable_shoreline_change_report.isChecked(),
            "is_area_change_report": self.qdw.cb_enable_area_change_report.isChecked(),
            "is_forecasting_report": self.qdw.cb_enable_forecasting_report.isChecked(),
            "save_location": self.qdw.qfw_report_save_location.filePath(),
        }

    def shorelines_dates(self) -> list[str]:
        """Get the shoreline dates from the current selected shoreline layer
        and from the current selected date field.

        Returns:
            A list of shoreline dates in the format 'mm/yyyy'.
        """
        field = self.shorelines()["date_field"]
        feats = self.shorelines()["feats"]
        return [feat[field] for feat in feats]

    def shorelines_uncs(self) -> list[float | str]:
        """Get the shoreline uncertainties from the current selected shoreline layer
        and from the current selected uncertainty field.

        Returns:
            A list of shoreline uncertainties. Missing values fall back to the
            default uncertainty as entered in the text box (a str).
        """
        field = self.shorelines()["unc_field"]
        feats = self.shorelines()["feats"]
        default_unc = self.shorelines()["default_data_unc"]
        uncs = []
        for feat in feats:
            if self.is_no_unc_value(feat[field]):
                uncs.append(default_unc)
            else:
                uncs.append(feat[field])
        return uncs

    def shorelines_years_uncs(self) -> dict[float, float | str]:
        """Get the shoreline years and uncertainties from the current selected
        shoreline layer and from the current selected uncertainty field.

        Returns:
            A dictionary of {year: uncertainty}. Missing values fall back to the
            default uncertainty as entered in the text box (a str).
        """
        unc_field = self.shorelines()["unc_field"]
        date_field = self.shorelines()["date_field"]
        default_unc = self.shorelines()["default_data_unc"]
        feats = self.shorelines()["feats"]
        uncs = {}
        for feat in feats:
            decimal_year = convert_to_decimal_year(feat[date_field])
            if self.is_no_unc_value(feat[unc_field]):
                uncs[decimal_year] = default_unc
            else:
                uncs[decimal_year] = feat[unc_field]
        return uncs

    def highest_unc(self) -> float | str:
        """Get the highest uncertainty from the current selected shoreline layer."""
        return max(self.shorelines_uncs())

    def unc_by_date(self, date: str) -> float | None:
        """Get the uncertainty by date from the current selected shoreline layer.

        Args:
            date: The date in the format 'mm/yyyy'.

        Returns:
            The uncertainty value, or None if no shoreline has that date.
        """
        unc_field = self.shorelines()["unc_field"]
        date_field = self.shorelines()["date_field"]
        feats = self.shorelines()["feats"]
        for feat in feats:
            if date == feat[date_field]:
                return feat[unc_field]

    def epr_unc(self) -> float:
        """Calculate the EPR uncertainty from the current selected shoreline layer."""
        default_unc = self.shorelines()["default_data_unc"]
        oldest_year = self.qdw.cb_shoreline_change_oldest_date.currentText()
        newest_year = self.qdw.cb_shoreline_change_newest_date.currentText()

        newest_date_unc = self.unc_by_date(newest_year)
        oldest_date_unc = self.unc_by_date(oldest_year)

        if self.is_no_unc_value(newest_date_unc):
            newest_date_unc = default_unc
        if self.is_no_unc_value(oldest_date_unc):
            oldest_date_unc = default_unc

        EPR_unc_numerator = newest_date_unc**2 + oldest_date_unc**2
        EPR_unc = math.sqrt(EPR_unc_numerator) / (
            convert_to_decimal_year(newest_year) - convert_to_decimal_year(oldest_year)
        )

        return round(EPR_unc, 2)

    @staticmethod
    def is_no_unc_value(unc_val: float | None) -> bool:
        """Check if the uncertainty field value is None or not greater than 0.0.

        Args:
            unc_val: Uncertainty field value.
        """
        return bool(unc_val is None or not unc_val > 0.0)
