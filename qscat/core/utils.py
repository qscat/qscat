# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import os
import configparser
import math

from datetime import datetime
from pathlib import Path

from qgis.core import QgsProject
from qgis.core import QgsApplication


def extract_month_year(month_year_string):
    """Extract the month and year from string.

    Args:
        month_year_string (str): string in the format 'mm/yyyy'

    Returns:
        tuple: (month, year)

    Raises:
        ValueError: if month_year_string is not in the format 'mm/yyyy'
        TypeError: if month_year_string is not a string
    """
    try:
        date = datetime.strptime(month_year_string, '%m/%Y')
    except ValueError:
        raise ValueError("Month and year must be in the format 'mm/yyyy'.")
    except TypeError:
        raise TypeError("Month and year must be a string.")
    else:
        return date.month, date.year


def convert_to_decimal_year(month_year_string):
    month, year = extract_month_year(month_year_string)
    if not isinstance(month, int) or not isinstance(year, int):
        raise TypeError("Month and year must be integers.")

    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12.")

    if year < 0:
        raise ValueError("Year must be positive.")
    
    day_of_year = get_day_of_year(month, year)
    decimal_year = round(year + (day_of_year / 365.242199), 2)
    return decimal_year


def get_day_of_year(month, year):
    """get day of year from month and year, 
    with default of day 01 for every month"""
    date = datetime(year, month, 1) # 1 = default day 1 every month
    day_of_year = date.timetuple().tm_yday
    return day_of_year


def datetime_now():
    return datetime.now().strftime("%m-%d-%y %H-%M-%S")


def get_duration_ms(end, start):
    #return int(round((end-start) * 1000))
    return round(end-start, 10)


def is_field_in_layer(field, layer):
    if layer.fields().indexFromName(field) == -1:
        return False
    return True


"""def get_current_project_crs():
    project = QgsProject.instance()    
    return project.crs().authid()"""


def get_project_input_params(self):
    project = {
        'crs_id':             QgsProject.instance().crs().authid(),
        'author_full_name':   self.dockwidget.le_proj_author_full_name.text(),
        'author_affiliation': self.dockwidget.le_proj_author_affiliation.text(),
        'author_email':       self.dockwidget.le_proj_author_email.text(),
    }
    return project


def get_baseline_input_params(self):
    baseline = {
        'baseline_layer':                     self.dockwidget.qmlcb_baseline_baseline_layer.currentLayer(),
        'is_baseline_placement_sea':          self.dockwidget.rb_baseline_placement_sea.isChecked(),
        'is_baseline_placement_land':         self.dockwidget.rb_baseline_placement_land.isChecked(),
        'is_baseline_orientation_land_right': self.dockwidget.rb_baseline_orientation_land_right.isChecked(),
        'is_baseline_orientation_land_left':  self.dockwidget.rb_baseline_orientation_land_left.isChecked(),
        'placement_field':                    self.dockwidget.qfcb_baseline_placement_field.currentField(),
        'orientation_field':                  self.dockwidget.qfcb_baseline_orientation_field.currentField(),
        'transect_length_field':              self.dockwidget.qfcb_baseline_length_field.currentField(),
    }
    return baseline


def get_shorelines_input_params(self):
    shorelines = {
        'shorelines_layer':                self.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer(),
        'default_data_uncertainty':        self.dockwidget.le_shorelines_default_data_unc.text(),
        'date_field':                      self.dockwidget.qfcb_shorelines_date_field.currentField(),
        'uncertainty_field':               self.dockwidget.qfcb_shorelines_uncertainty_field.currentField(),
    }
    return shorelines


def get_transects_input_params(self):
    transects = {
        'layer_output_name':         self.dockwidget.le_transects_layer_output_name.text(),
        'is_by_transect_spacing':    self.dockwidget.rb_transects_by_transect_spacing.isChecked(),
        'is_by_number_of_transects': self.dockwidget.rb_transects_by_number_of_transects.isChecked(),
        'by_transect_spacing':       self.dockwidget.qsb_transects_by_transect_spacing.text(),
        'by_number_of_transects':    self.dockwidget.qsb_transects_by_number_of_transects.text(),
        'length':                    self.dockwidget.qsb_transects_length.text(),
        'smoothing_distance':        self.dockwidget.qsb_transects_smoothing_distance.text(),
    }
    return transects


def get_shoreline_change_input_params(qscat):
    """
    Args:
        qscat (QscatPlugin): QscatPlugin instance.
    """
    shoreline_change = {
        'transect_layer':                  qscat.dockwidget.qmlcb_stats_transects_layer.currentLayer(),
        'is_clip_transects':               qscat.dockwidget.cb_stats_clip_transects.isChecked(),
        'is_choose_by_distance':           qscat.dockwidget.rb_choose_by_distance.isChecked(),
        'is_choose_by_distance_farthest':  qscat.dockwidget.rb_choose_by_distance_farthest.isChecked(),
        'is_choose_by_distance_closest':   qscat.dockwidget.rb_choose_by_distance_closest.isChecked(),
        'is_choose_by_placement':          qscat.dockwidget.rb_choose_by_placement.isChecked(),
        'is_choose_by_placement_seaward':  qscat.dockwidget.rb_choose_by_placement_seaward.isChecked(),
        'is_choose_by_placement_landward': qscat.dockwidget.rb_choose_by_placement_landward.isChecked(),
        'selected_stats':                  get_statistics_selected(qscat),
        'oldest_year':                     convert_to_decimal_year(qscat.dockwidget.cb_stats_oldest_year.currentText()),
        'newest_year':                     convert_to_decimal_year(qscat.dockwidget.cb_stats_newest_year.currentText()),
        'highest_unc':                     get_highest_unc_from_input(qscat),
    }
    return shoreline_change


def get_area_change_input_params(qscat):
    """Returns a dictionary containing the input parameters in Area Change Tab.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.
        
    Returns:
        dict: A dictionary containing the following keys:
            - 'NSM_layer': The current layer selected in the NSM layer combo box.
            - 'polygon_layer': The current layer selected in the polygon layer combo box.
    """
    area_change = {
        'polygon_layer': qscat.dockwidget.qmlcb_stats_polygon_layer.currentLayer(),
        'NSM_layer':  qscat.dockwidget.qmlcb_stats_NSM_layer.currentLayer(),
    }
    return area_change


def get_statistics_selected(self):
    stats = []
    if self.dockwidget.cb_stats_SCE.isChecked():
        stats.append('SCE')
    if self.dockwidget.cb_stats_NSM.isChecked():
        stats.append('NSM')
    if self.dockwidget.cb_stats_EPR.isChecked():
        stats.append('EPR')
    if self.dockwidget.cb_stats_LRR.isChecked():
        stats.append('LRR')
    if self.dockwidget.cb_stats_WLR.isChecked():
        stats.append('WLR')
    return stats


def get_project_dir():
    project_path = QgsProject.instance().absoluteFilePath()
    project_dir = os.path.dirname(project_path)
    return project_dir


def get_plugin_dir():
    profiles_default_dir = QgsApplication.qgisSettingsDirPath()
    plugin_dir = os.path.join(
        profiles_default_dir,
        'python', 
        'plugins', 
        'qscat',
    )
    return plugin_dir


def get_plugins_dir():
    profiles_default_dir = QgsApplication.qgisSettingsDirPath()
    plugins_dir = os.path.join(
        profiles_default_dir,
        'python', 
        'plugins',
    )
    return plugins_dir


def get_metadata_version():
    """Get the version from local QGIS plugin metadata.txt.
    Returns:
        str: The string version from local metadata.txt
    """
    plugin_dir = get_plugin_dir()
    config = configparser.ConfigParser()
    config.read(Path(plugin_dir) / "metadata.txt")
    version = config.get('general', 'version')
    return version


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
    """"
        Returns a dict of {year: unc}
    """
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
    oldest_year_txt = self.dockwidget.cb_stats_oldest_year.currentText()
    newest_year_txt = self.dockwidget.cb_stats_newest_year.currentText()

    newest_date_unc = get_unc_by_date(self, newest_year_txt)
    oldest_date_unc = get_unc_by_date(self, oldest_year_txt)

    if is_no_unc_value(newest_date_unc):
        newest_date_unc = default_unc
    if is_no_unc_value(oldest_date_unc):
        oldest_date_unc = default_unc

    EPR_unc_numerator = (newest_date_unc**2 + oldest_date_unc**2)
    EPR_unc = math.sqrt(EPR_unc_numerator) \
        / (convert_to_decimal_year(newest_year_txt)-convert_to_decimal_year(oldest_year_txt))

    return round(EPR_unc, 2)


def filter_years_intersections_by_range(years_intersections, newest_year, oldest_year):
    """Filter years_intersections dict by range of years.

    Args:
        newest_year (float): decimal year
        oldest_year (float): decimal year
        years_intersections (dict): {year: {'unc': unc, 'distance': distance, 'intersect_x': x, 'intersect_y': y}}

    Returns:
        dict: {year: {'unc': unc, 'distance': distance, 'intersect_x': x, 'intersect_y': y}}
    
    Raises:
        TODO: TypeError: if newest_year or oldest_year is not a float
        TODO: ValueError: if newest_year is less than oldest_year
        TODO: Check if years is sorted

    Example:
        data = {
        1.2: {'unc': 10, 'distance': 5, 'intersect_x': 2, 'intersect_y': 3},
        2.5: {'unc': 8, 'distance': 7, 'intersect_x': 4, 'intersect_y': 1},
        3.7: {'unc': 15, 'distance': 2, 'intersect_x': 7, 'intersect_y': 8},
        4.9: {'unc': 12, 'distance': 6, 'intersect_x': 5, 'intersect_y': 6}
        }
        say, lowest = 2.5, highest 4.9

        it should remove the dict entry of 1.2 since it is not on the range of 2.5 to 4.9
    """
    years_intersections_copy = years_intersections.copy()
    years_to_remove = [year for year in years_intersections_copy.keys() if year < oldest_year or year > newest_year]
    for year in years_to_remove:
        del years_intersections_copy[year]
    return years_intersections_copy


def filter_uncs_by_range(year_uncs, newest_year, oldest_year):
    """
    Example input data:
        {2003.0: 15.0, 2006.0: 15.0, 2009.0: 15.0, 2014.0: 15.0, 2016.0: 15.0, 2018.0: 1.0, 2020.0: 15.0, 2022.0: 1.0, 1977.0: 25.0, 2011.0: 15.0}
    """
    year_uncs_copy = year_uncs.copy()
    years_to_remove = [year for year in year_uncs_copy.keys() if year < oldest_year or year > newest_year]
    for year in years_to_remove:
        del year_uncs_copy[year]
    return year_uncs_copy