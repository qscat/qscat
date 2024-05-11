from qscat.core.inputs import Inputs
from qscat.core.validator import validate_shorelines_layer
from qscat.gui.shoreline_change import update_newest_oldest_date


def shorelines_layer_actions(qdw):
    """Perform actions for the selected shorelines layer.

    Args:
        qdw (QscatDockWidget): QscatDockWidget instance.
    """
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
