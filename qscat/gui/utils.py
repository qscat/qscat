# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

def enable_disable_by_radio_button(radio_button, widget_to_enable, widget_to_disable):
    if radio_button.isChecked():
        widget_to_enable.setEnabled(True)
        widget_to_disable.setEnabled(False)

# def enable_disable_by_radio_button(
#     radio_button1,
#     radio_button2,
#     widget1,
#     widget2,
# ):
#     if radio_button1.isChecked():
#         widget1.setEnabled(True)
#         widget2.setEnabled(False)
#     elif radio_button2.isChecked():
#         widget1.setEnabled(False)
#         widget2.setEnabled(True)