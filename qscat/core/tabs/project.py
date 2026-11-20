# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from __future__ import annotations

from typing import TYPE_CHECKING

from qgis.core import QgsCoordinateReferenceSystem, QgsProject
from qgis.gui import QgsProjectionSelectionDialog

if TYPE_CHECKING:
    from qscat.qscat_dockwidget import QscatDockWidget


# PROJECT SETTINGS
def select_projection(self):
    crs = QgsCoordinateReferenceSystem()
    selector = QgsProjectionSelectionDialog(self.iface.mainWindow())
    selector.setCrs(crs)

    if selector.exec():
        selected_crs = selector.crs()
        self.dockwidget.le_proj_selected_crs_authid.setText(selected_crs.authid())


def load_current_projection(qdw: QscatDockWidget):
    """Load the current projection of the project to the label."""
    project = QgsProject.instance()
    crs = project.crs()
    qdw.lbl_proj_current_crs.setText(f"{crs.authid()} ({crs.description()})")
