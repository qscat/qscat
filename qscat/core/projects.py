# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsProject

from qgis.gui import QgsProjectionSelectionDialog


# PROJECT SETTINGS
def select_projection(self):
    crs = QgsCoordinateReferenceSystem()
    selector = QgsProjectionSelectionDialog(self.iface.mainWindow())
    selector.setCrs(crs)

    if selector.exec():
        selected_crs =  selector.crs()
        self.dockwidget.le_proj_selected_crs_authid.setText(selected_crs.authid())

  
def load_current_projection(self):
    project = QgsProject.instance()
    crs = project.crs()
    self.dockwidget.lbl_proj_current_crs.setText(
        f"{crs.authid()} ({crs.description()})"
    )