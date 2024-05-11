# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license


def enable_disable_widgets_by_radio_button(
    radio_button, widget_to_enable, widget_to_disable
):
    """
    Enable a widget (a) and disable a widget (b) at the same time based on the
    state of a radio button.

    Args:
        radio_button (QRadioButton): The radio button that will be checked.
        widget_to_enable (QWidget): The widget that will be enabled.
        widget_to_disable (QWidget): The widget that will be disabled.

    Usages:
        1) Transect Count section in the Transect tab.
        2) Transect-Shoreline Intersections in Shoreline Change tab.
    """
    if radio_button.isChecked():
        widget_to_enable.setEnabled(True)
        widget_to_disable.setEnabled(False)


def enable_disable_groupbox_by_checkbox(checkbox, groupbox):
    """
    Enable and disable a groupbox based on the state of a checkbox.
    """
    if checkbox.isChecked():
        groupbox.setEnabled(True)
    else:
        groupbox.setEnabled(False)
