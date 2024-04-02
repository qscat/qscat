import re

from PyQt5.QtCore import Qt

from qgis.core import Qgis

from qscat.core.messages import display_message
from qscat.core.utils import get_shorelines_dates

"""
def update_selected_text(self):
    if self.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer() is not None:
        self.dockwidget.lbl_stats_current_shorelines_layer.setText(
            self.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer().name())

    if self.dockwidget.qfcb_shorelines_date_field.currentField() is not None:
        self.dockwidget.lbl_stats_current_field_name.setText(
            self.dockwidget.qfcb_shorelines_date_field.currentField())
"""

def select_all_stats_checkbox(self):
    if self.dockwidget.cb_stats_select_all.isChecked():
        # TODO: make a list?
        self.dockwidget.cb_stats_SCE.setChecked(True)
        self.dockwidget.cb_stats_NSM.setChecked(True)
        self.dockwidget.cb_stats_EPR.setChecked(True)
        self.dockwidget.cb_stats_LRR.setChecked(True)
        self.dockwidget.cb_stats_WLR.setChecked(True)
    else:
        self.dockwidget.cb_stats_SCE.setChecked(False)
        self.dockwidget.cb_stats_NSM.setChecked(False)
        self.dockwidget.cb_stats_EPR.setChecked(False)
        self.dockwidget.cb_stats_LRR.setChecked(False)
        self.dockwidget.cb_stats_WLR.setChecked(False)

def update_newest_oldest_year(self):
    if self.dockwidget.qfcb_shorelines_date_field.count() > 0:
        cb_newest_year = self.dockwidget.cb_stats_newest_year
        cb_oldest_year = self.dockwidget.cb_stats_oldest_year
        cb_newest_year.clear()
        cb_oldest_year.clear()

        years = get_shorelines_dates(self)

        if not is_valid_date_inputs(years):
            display_message(
                'One of the date input is invalid! Must be MM/YYYY or invalid.', 
                Qgis.Critical,
            )   
        else:
            years = sorted(years, reverse=True)
            oldest_year_curr = min(years)
            newest_year_curr = max(years)

            cb_newest_year.addItems(years)
            cb_oldest_year.addItems(years)

            newest_idx = cb_newest_year.findText(
                newest_year_curr, Qt.MatchExactly
            )
            oldest_idx = cb_oldest_year.findText(
                oldest_year_curr, Qt.MatchExactly
            )
            cb_newest_year.setCurrentIndex(newest_idx)
            cb_oldest_year.setCurrentIndex(oldest_idx)
    else:
        # No date field string for the current selected layer
        display_message(
            'No candidate date field exists with type (String) for the current selected shoreline layer.', 
            Qgis.Critical,
        )   

# TODO: move to core.utils
def is_valid_date_input(date):
    """Validate if date has format mm/yyyy, but month should be 1-12 and
    year should be 1900-2100.
    """
    if not date: # Null fields
        return False
    
    pattern = r'^(0[1-9]|1[0-2])/(\d{4})$'
    match = re.match(pattern, date)

    if match:
        month = int(match.group(1))
        year = int(match.group(2))
        if 1 <= month <= 12 and 1900 <= year <= 2100:
            return True
        else:
            return False
    else:
        return False

# TODO: move to core.utils
def is_valid_date_inputs(dates):
    """Uses is_valid_date_input() on a list. All dates should be valid."""
    for date in dates:
        if not is_valid_date_input(date):
            return False
    return True