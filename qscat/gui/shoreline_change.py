# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from datetime import datetime

from PyQt5.QtCore import Qt

from qscat.core.inputs import Inputs


def select_all_stats_checkbox(qdw):
    """Select and deselect all statistics checkboxes if the select all checkbox
    is checked or unchecked.

    Args:
        qdw (QscatDockWidget): QscatDockWidget instance.
    """
    if qdw.cb_stats_select_all.isChecked():
        qdw.cb_stats_SCE.setChecked(True)
        qdw.cb_stats_NSM.setChecked(True)
        qdw.cb_stats_EPR.setChecked(True)
        qdw.cb_stats_LRR.setChecked(True)
        qdw.cb_stats_WLR.setChecked(True)
    else:
        qdw.cb_stats_SCE.setChecked(False)
        qdw.cb_stats_NSM.setChecked(False)
        qdw.cb_stats_EPR.setChecked(False)
        qdw.cb_stats_LRR.setChecked(False)
        qdw.cb_stats_WLR.setChecked(False)


def update_newest_oldest_date_called(qdw):
    """Update the newest and oldest date combo boxes.

    Args:
       qdw (QscatDockWidget): QscatDockWidget instance.
    """
    cb_newest_date = qdw.cb_shoreline_change_newest_date
    cb_oldest_date = qdw.cb_shoreline_change_oldest_date
    cb_newest_date.clear()
    cb_oldest_date.clear()

    inputs = Inputs(qdw)
    dates = inputs.shorelines_dates()

    update_newest_oldest_date(
        dates,
        cb_newest_date,
        cb_oldest_date,
    )


def update_newest_oldest_date(dates, cb_newest_date, cb_oldest_date):
    """Update the newest and oldest date combo boxes.

    Args:
        dates (list[str]): A list of valid date input values in selected shoreline date field.
        cb_newest_date (QComboBox): The combo box for the newest date.
        cb_oldest_date (QComboBox): The combo box for the oldest date.
    """
    # Sort and get the oldest and newest date
    dates_sorted = sorted(dates, key=lambda x: datetime.strptime(x, "%m/%Y"))
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
