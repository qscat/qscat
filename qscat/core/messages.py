# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from __future__ import annotations

from qgis.core import Qgis
from qgis.utils import iface


def display_message(
    description: str, level: Qgis.MessageLevel, duration: int | None = None
):
    """Display a message in the QGIS message bar.

    Args:
        description: The message to display.
        duration: The duration of the message in seconds.
                defaults to None.
    """
    if level == Qgis.Info:
        title = "QSCAT Notice"
        fixed_duration = 4
    elif level == Qgis.Warning:
        title = "QSCAT Warning"
        fixed_duration = 0
    elif level == Qgis.Critical:
        title = "QSCAT Error"
        fixed_duration = 0
    elif level == Qgis.Success:
        title = "QSCAT Success"
        fixed_duration = 4

    if duration is None:
        duration = fixed_duration

    iface.messageBar().pushMessage(
        title,
        description,
        level=level,
        duration=duration,
    )
