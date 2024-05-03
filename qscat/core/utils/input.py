# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import math

from qgis.core import QgsProject

from qscat.core.utils.date import convert_to_decimal_year
from qscat.core.constants import Statistic


def get_project_settings_input_params(qscat):
    """Returns a dictionary containing the input parameters in Project Settings Tab.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Returns:
        dict: A dictionary containing the input parameters in Project Settings Tab.
    """
    return {
        "crs_id": QgsProject.instance().crs().authid(),
        "author_full_name": qscat.dockwidget.le_proj_author_full_name.text(),
        "author_affiliation": qscat.dockwidget.le_proj_author_affiliation.text(),
        "author_email": qscat.dockwidget.le_proj_author_email.text(),
    }


def get_baseline_input_params(qscat):
    """Returns a dictionary containing the input parameters in Baseline Tab.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Returns:
        dict: A dictionary containing the input parameters in Baseline Tab.
    """
    return {
        "baseline_layer": qscat.dockwidget.qmlcb_baseline_baseline_layer.currentLayer(),
        "is_baseline_placement_sea": qscat.dockwidget.rb_baseline_placement_sea.isChecked(),
        "is_baseline_placement_land": qscat.dockwidget.rb_baseline_placement_land.isChecked(),
        "is_baseline_orientation_land_right": qscat.dockwidget.rb_baseline_orientation_land_right.isChecked(),
        "is_baseline_orientation_land_left": qscat.dockwidget.rb_baseline_orientation_land_left.isChecked(),
        "placement_field": qscat.dockwidget.qfcb_baseline_placement_field.currentField(),
        "orientation_field": qscat.dockwidget.qfcb_baseline_orientation_field.currentField(),
        "transect_length_field": qscat.dockwidget.qfcb_baseline_length_field.currentField(),
    }


def get_shorelines_input_params(qscat):
    """Returns a dictionary containing the input parameters in Shorelines Tab.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Returns:
        dict: A dictionary containing the input parameters in Shorelines Tab.
    """
    return {
        "shorelines_layer": qscat.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer(),
        "default_data_uncertainty": qscat.dockwidget.le_shorelines_default_data_unc.text(),
        "date_field": qscat.dockwidget.qfcb_shorelines_date_field.currentField(),
        "uncertainty_field": qscat.dockwidget.qfcb_shorelines_uncertainty_field.currentField(),
    }


def get_transects_input_params(qscat):
    """Returns a dictionary containing the input parameters in Transects Tab.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Returns:
        dict: A dictionary containing the input parameters in Transects Tab.
    """
    return {
        "layer_output_name": qscat.dockwidget.le_transects_layer_output_name.text(),
        "is_by_transect_spacing": qscat.dockwidget.rb_transects_by_transect_spacing.isChecked(),
        "is_by_number_of_transects": qscat.dockwidget.rb_transects_by_number_of_transects.isChecked(),
        "by_transect_spacing": qscat.dockwidget.qsb_transects_by_transect_spacing.text(),
        "by_number_of_transects": qscat.dockwidget.qsb_transects_by_number_of_transects.text(),
        "length": qscat.dockwidget.qsb_transects_length.text(),
        "smoothing_distance": qscat.dockwidget.qsb_transects_smoothing_distance.text(),
    }


def get_shoreline_change_input_params(qscat):
    """Returns a dictionary containing the input parameters in Shoreline Change Tab.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Returns:
        dict: A dictionary containing the input parameters in Shoreline Change Tab.
    """
    return {
        "transects_layer": qscat.dockwidget.qmlcb_shoreline_change_transects_layer.currentLayer(),
        "transects_layer_widget": qscat.dockwidget.qmlcb_shoreline_change_transects_layer,
        "is_clip_transects": qscat.dockwidget.cb_stats_clip_transects.isChecked(),
        "is_choose_by_distance": qscat.dockwidget.rb_choose_by_distance.isChecked(),
        "is_choose_by_distance_farthest": qscat.dockwidget.rb_choose_by_distance_farthest.isChecked(),
        "is_choose_by_distance_closest": qscat.dockwidget.rb_choose_by_distance_closest.isChecked(),
        "is_choose_by_placement": qscat.dockwidget.rb_choose_by_placement.isChecked(),
        "is_choose_by_placement_seaward": qscat.dockwidget.rb_choose_by_placement_seaward.isChecked(),
        "is_choose_by_placement_landward": qscat.dockwidget.rb_choose_by_placement_landward.isChecked(),
        "selected_stats": get_shoreline_change_stat_selected(qscat),
        "oldest_date": qscat.dockwidget.cb_shoreline_change_oldest_date.currentText(),
        "newest_date": qscat.dockwidget.cb_shoreline_change_newest_date.currentText(),
        "oldest_year": convert_to_decimal_year(
            qscat.dockwidget.cb_shoreline_change_oldest_date.currentText()
        ),
        "newest_year": convert_to_decimal_year(
            qscat.dockwidget.cb_shoreline_change_newest_date.currentText()
        ),
        "confidence_interval": float(
            qscat.dockwidget.qdsb_stats_confidence_interval.text()
        ),
        "epr_unc": get_epr_unc_from_input(qscat),
        "highest_unc": get_highest_unc_from_input(qscat),
        "years_uncs": get_shorelines_years_uncs_from_input(qscat),
    }


def get_shoreline_change_stat_selected(qscat):
    """Returns a list of selected statistics in Shoreline Change Tab.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Returns:
        list[Statistic]: A list of selected statistics.
    """
    stats = []
    if qscat.dockwidget.cb_stats_SCE.isChecked():
        stats.append(Statistic.SCE)
    if qscat.dockwidget.cb_stats_NSM.isChecked():
        stats.append(Statistic.NSM)
    if qscat.dockwidget.cb_stats_EPR.isChecked():
        stats.append(Statistic.EPR)
    if qscat.dockwidget.cb_stats_LRR.isChecked():
        stats.append(Statistic.LRR)
    if qscat.dockwidget.cb_stats_WLR.isChecked():
        stats.append(Statistic.WLR)
    return stats


def get_area_change_input_params(qscat):
    """Returns a dictionary containing the input parameters in Area Change Tab.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Returns:
        dict: A dictionary containing the input parameters in Area Change Tab.
    """
    return {
        "polygon_layer": qscat.dockwidget.qmlcb_area_change_polygon_layer.currentLayer(),
        "stat_layer": qscat.dockwidget.qmlcb_area_change_stat_layer.currentLayer(),
    }


def get_summary_report_input_params(qscat):
    """Returns a dictionary containing the input parameters in Summary Report Tab.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Returns:
        dict: A dictionary containing the input parameters in Summary Report Tab.
    """
    return {
        "is_report": qscat.dockwidget.cb_enable_report_generation.isChecked(),
        "is_shoreline_change_report": qscat.dockwidget.cb_enable_shoreline_change_report.isChecked(),
        "is_area_change_report": qscat.dockwidget.cb_enable_area_change_report.isChecked(),
        "is_forecasting_report": qscat.dockwidget.cb_enable_forecasting_report.isChecked(),
    }


def get_shorelines_dates(qscat):
    """Get the shoreline dates from the current selected shoreline layer
    and from the current selected date field.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Returns:
        list[str]: A list of shoreline dates in the format 'mm/yyyy'.
    """
    layer = qscat.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer()
    field = qscat.dockwidget.qfcb_shorelines_date_field.currentField()
    feats = layer.getFeatures()
    return [feat[field] for feat in feats]


def get_shorelines_uncs(self):
    layer = self.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer()
    feats = layer.getFeatures()
    unc_field = self.dockwidget.qfcb_shorelines_uncertainty_field.currentField()
    default_unc = float(self.dockwidget.le_shorelines_default_data_unc.text())
    uncs = []
    for f in feats:
        if is_no_unc_value(f[unc_field]):
            uncs.append(default_unc)
        else:
            uncs.append(f[unc_field])
    return uncs


def get_shorelines_years_uncs_from_input(self):
    """Returns a dict of {year: unc}"""
    layer = self.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer()
    feats = layer.getFeatures()

    unc_field = self.dockwidget.qfcb_shorelines_uncertainty_field.currentField()
    date_field = self.dockwidget.qfcb_shorelines_date_field.currentField()

    default_unc = float(self.dockwidget.le_shorelines_default_data_unc.text())
    uncs = {}

    for f in feats:
        decimal_year = convert_to_decimal_year(f[date_field])
        if is_no_unc_value(f[unc_field]):
            uncs[decimal_year] = default_unc
        else:
            uncs[decimal_year] = f[unc_field]

    return uncs


def get_highest_unc_from_input(self):
    return max(get_shorelines_uncs(self))


def get_unc_by_date(self, date):
    layer = self.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer()
    feats = layer.getFeatures()

    unc_field = self.dockwidget.qfcb_shorelines_uncertainty_field.currentField()
    date_field = self.dockwidget.qfcb_shorelines_date_field.currentField()

    for f in feats:
        if date == f[date_field]:
            return f[unc_field]


def is_no_unc_value(unc_field_value):
    if unc_field_value is None or not unc_field_value > 0.0:
        return True
    else:
        return False


def get_epr_unc_from_input(self):
    default_unc = float(self.dockwidget.le_shorelines_default_data_unc.text())
    oldest_year_txt = self.dockwidget.cb_shoreline_change_oldest_date.currentText()
    newest_year_txt = self.dockwidget.cb_shoreline_change_newest_date.currentText()

    newest_date_unc = get_unc_by_date(self, newest_year_txt)
    oldest_date_unc = get_unc_by_date(self, oldest_year_txt)

    if is_no_unc_value(newest_date_unc):
        newest_date_unc = default_unc
    if is_no_unc_value(oldest_date_unc):
        oldest_date_unc = default_unc

    EPR_unc_numerator = newest_date_unc**2 + oldest_date_unc**2
    EPR_unc = math.sqrt(EPR_unc_numerator) / (
        convert_to_decimal_year(newest_year_txt)
        - convert_to_decimal_year(oldest_year_txt)
    )

    return round(EPR_unc, 2)
