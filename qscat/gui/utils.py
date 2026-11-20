# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qgis.PyQt.QtWidgets import QRadioButton, QWidget


def enable_disable_widgets_by_radio_button(
    radio_button: QRadioButton, widget_to_enable: QWidget, widget_to_disable: QWidget
):
    """Enable a widget (a) and disable a widget (b) at the same time based on the
    state of a radio button.

    Args:
        radio_button: The radio button that will be checked.
        widget_to_enable: The widget that will be enabled.
        widget_to_disable: The widget that will be disabled.

    Usages:
        1) Transect Count section in the Transect tab.
        2) Transect-Shoreline Intersections in Shoreline Change tab.
    """
    if radio_button.isChecked():
        widget_to_enable.setEnabled(True)
        widget_to_disable.setEnabled(False)


def enable_disable_groupbox_by_checkbox(checkbox, groupbox):
    """Enable and disable a groupbox based on the state of a checkbox."""
    if checkbox.isChecked():
        groupbox.setEnabled(True)
    else:
        groupbox.setEnabled(False)
