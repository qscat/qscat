# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from qgis.utils import iface

from qgis.core import Qgis


def display_message(description, level, duration=None):
    if level == Qgis.Info:
        title = 'Notice'
        fixed_duration = 4
    elif level == Qgis.Warning:
        title = 'Warning'
        fixed_duration = 0
    elif level == Qgis.Critical:
        title = 'Error'
        fixed_duration = 0
    elif level == Qgis.Success:
        title = 'Success'
        fixed_duration = 4
    else:
        raise ValueError('Invalid message level')

    if duration is None:
        duration = fixed_duration
       
    iface.messageBar().pushMessage(
        title,
        description,
        level=level,
        duration=duration,
    )
