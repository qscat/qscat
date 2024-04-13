# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import re
from datetime import datetime

from PyQt5.QtCore import Qt

from qgis.core import Qgis

from qscat.core.messages import display_message
from qscat.core.utils.input import get_shorelines_dates

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
        # TODO: Make as a list
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


def update_newest_oldest_date(qscat):
    """Update the newest and oldest date combo boxes based on the current
    selected shoreline layer and selected date field.
    
    Args:
        qscat (QscatPlugin): QscatPlugin instance.
    """
    if qscat.dockwidget.qfcb_shorelines_date_field.count() > 0:
        cb_newest_date = qscat.dockwidget.cb_shoreline_change_newest_date
        cb_oldest_date = qscat.dockwidget.cb_shoreline_change_oldest_date
        cb_newest_date.clear()
        cb_oldest_date.clear()
        
        # Get dates as list of strings (MM/YYYY)
        dates = get_shorelines_dates(qscat)

        if not is_valid_date_inputs(dates):
            display_message(
                'One of the date inputs is invalid! Must be MM/YYYY.', 
                Qgis.Critical,
            )   
            return
        
        # Sort and get the oldest and newest date
        dates_sorted = sorted(dates, key=lambda x: datetime.strptime(x, '%m/%Y'))
        oldest_date = dates_sorted[0]
        newest_date = dates_sorted[-1]
        
        # Add the dates to the combo boxes
        cb_newest_date.addItems(dates)
        cb_oldest_date.addItems(dates)

        # Find the index of the oldest and newest date
        newest_date_i = cb_newest_date.findText(newest_date, Qt.MatchExactly)
        oldes_date_i = cb_oldest_date.findText(oldest_date, Qt.MatchExactly)

        # Set the current index of the combo boxes
        cb_newest_date.setCurrentIndex(newest_date_i)
        cb_oldest_date.setCurrentIndex(oldes_date_i)
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