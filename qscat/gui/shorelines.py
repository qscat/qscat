from __future__ import annotations

from typing import TYPE_CHECKING

from qscat.core.inputs import Inputs
from qscat.core.validator import validate_shorelines_layer
from qscat.gui.shoreline_change import update_newest_oldest_date

if TYPE_CHECKING:
    from qscat.qscat_dockwidget import QscatDockWidget


def shorelines_layer_actions(qdw: QscatDockWidget):
    """Perform actions for the selected shorelines layer."""
    # Validate the selected shorelines layer
    valid = validate_shorelines_layer(qdw)

    # Update the newest and oldest dates in the combo boxes
    cb_newest_date = qdw.cb_shoreline_change_newest_date
    cb_oldest_date = qdw.cb_shoreline_change_oldest_date
    cb_newest_date.clear()
    cb_oldest_date.clear()

    if valid:
        inputs = Inputs(qdw)
        dates = inputs.shorelines_dates()
        update_newest_oldest_date(
            dates,
            cb_newest_date,
            cb_oldest_date,
        )
