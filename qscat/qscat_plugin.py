# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from pathlib import Path
from PyQt5.QtCore import Qt

from qgis.PyQt.QtGui import QIcon

from qgis.PyQt.QtWidgets import QAction

from qscat.qscat_dockwidget import QscatDockWidget

from qscat.core.automator import automate_shoreline_field_button_clicked
from qscat.core.automator import automate_baseline_field_button_clicked
from qscat.core.automator import automate_baseline_buffer_button_clicked
from qscat.core.baseline import show_hide_baseline_orientation
from qscat.core.forecasting import run_forecasting
from qscat.core.settings import load_plugin_project_settings
from qscat.core.settings import save_baseline_tab_project_settings
from qscat.core.settings import save_project_tab_project_settings
from qscat.core.settings import save_shorelines_tab_project_settings
from qscat.core.settings import save_transects_tab_project_settings
from qscat.core.shoreline_change import compute_shoreline_change_button_clicked

# from qscat.core.shoreline_change import compute_shoreline_change_stats
from qscat.core.area_change.main import compute_area_change_stats
from qscat.core.transects import cast_transects_button_clicked
from qscat.core.update import check_updates_button_clicked
from qscat.core.utils.plugin import get_plugin_dir
from qscat.core.visualization import apply_color_ramp_button_clicked

from qscat.gui.statistics import update_newest_oldest_date
from qscat.gui.statistics import select_all_stats_checkbox
from qscat.gui.utils import enable_disable_widgets_by_radio_button
from qscat.gui.utils import enable_disable_groupbox_by_checkbox
from qscat.gui.widget_properties import set_plugin_widget_properties


class QscatPlugin:
    def __init__(self, iface):
        self.iface = iface
        # self.actions = []
        self.action = None
        self.dockwidget = None
        # self.layers = None
        # self.plugin_is_active = None
        self.icon = QIcon(str(Path(get_plugin_dir(), "gui", "icons", "qscat.svg")))

    def initGui(self):
        self.action = QAction(self.icon, "QSCAT", self.iface.mainWindow())
        self.action.triggered.connect(self.run)

        # Add to Plugins Toolbar
        self.iface.addToolBarIcon(self.action)

        # Add to Plugins Menu
        self.iface.addPluginToMenu("QSCAT", self.action)

    def onClosePlugin(self):
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)
        # self.plugin_is_active = False

    def unload(self):
        # Remove from Plugins Toolbar
        self.iface.removeToolBarIcon(self.action)

        # Remove from Plugins Menu
        self.iface.removePluginMenu("QSCAT", self.action)

        del self.action

    def run(self, test=False):
        self.dockwidget = QscatDockWidget()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
        self.dockwidget.setWindowTitle("QSCAT")
        self.dockwidget.show()
        self.dockwidget.tw_qscat.setStyleSheet("QTabWidget::tab { text-align: left; }")

        # Signals
        # Buttons in Automator Tab
        self.dockwidget.pb_automator_field_shoreline_apply.clicked.connect(
            lambda: automate_shoreline_field_button_clicked(self)
        )
        self.dockwidget.pb_automator_field_baseline_apply.clicked.connect(
            lambda: automate_baseline_field_button_clicked(self)
        )
        self.dockwidget.pb_automator_baseline_buffer_create.clicked.connect(
            lambda: automate_baseline_buffer_button_clicked(self)
        )

        # Baseline Tab "Show baseline orientation" button
        self.dockwidget.cb_baseline_orientation.stateChanged.connect(
            lambda: show_hide_baseline_orientation(self)
        )

        # Transect Tab "Cast Transect" button
        self.dockwidget.pb_transects_cast.clicked.connect(
            lambda: cast_transects_button_clicked(self)
        )

        # Shoreline Change Tab "Compute Shoreline Change" button
        self.dockwidget.pb_stats_compute_shoreline_change.clicked.connect(
            lambda: compute_shoreline_change_button_clicked(self)
        )
        # self.dockwidget.pb_stats_compute_shoreline_change.clicked.connect(
        #     lambda: compute_shoreline_change_stats(self)
        # )
        # Area Change Tab "Compute Area Change" button
        self.dockwidget.pb_stats_compute_area_change.clicked.connect(
            lambda: compute_area_change_stats(self)
        )

        # Forecasting Tab "Forecast" button
        self.dockwidget.pb_forecasting_run_forecasting.clicked.connect(
            lambda: run_forecasting(self)
        )

        # Visualization Tab "Visualize" button
        self.dockwidget.pb_vis_apply.clicked.connect(
            lambda: apply_color_ramp_button_clicked(self)
        )

        # About Tab "Check for updates" button
        self.dockwidget.pb_about_check_for_updates.clicked.connect(
            lambda: check_updates_button_clicked(self)
        )

        # Shorelines Tab "Shorelines fields"
        self.dockwidget.qmlcb_shorelines_shorelines_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_shorelines_date_field.setLayer(
                self.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer()
            )
        )
        self.dockwidget.qmlcb_shorelines_shorelines_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_shorelines_uncertainty_field.setLayer(
                self.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer()
            )
        )

        # Baseline Tab "Baseline fields"
        self.dockwidget.qmlcb_baseline_baseline_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_baseline_placement_field.setLayer(
                self.dockwidget.qmlcb_baseline_baseline_layer.currentLayer()
            )
        )
        self.dockwidget.qmlcb_baseline_baseline_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_baseline_orientation_field.setLayer(
                self.dockwidget.qmlcb_baseline_baseline_layer.currentLayer()
            )
        )
        self.dockwidget.qmlcb_baseline_baseline_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_baseline_length_field.setLayer(
                self.dockwidget.qmlcb_baseline_baseline_layer.currentLayer()
            )
        )

        # Shoreline Change Tab "Select/Deselect All" checkbox
        self.dockwidget.cb_stats_select_all.stateChanged.connect(
            lambda: select_all_stats_checkbox(self)
        )

        # Shoreline Change Tab "Update" button
        self.dockwidget.pb_stats_update_newest_oldest_year.clicked.connect(
            lambda: update_newest_oldest_date(self)
        )

        # Transect Tab "Transect Count"
        self.dockwidget.rb_transects_by_transect_spacing.toggled.connect(
            lambda: enable_disable_widgets_by_radio_button(
                self.dockwidget.rb_transects_by_transect_spacing,
                self.dockwidget.qsb_transects_by_transect_spacing,
                self.dockwidget.qsb_transects_by_number_of_transects,
            )
        )
        self.dockwidget.rb_transects_by_number_of_transects.toggled.connect(
            lambda: enable_disable_widgets_by_radio_button(
                self.dockwidget.rb_transects_by_number_of_transects,
                self.dockwidget.qsb_transects_by_number_of_transects,
                self.dockwidget.qsb_transects_by_transect_spacing,
            )
        )

        # Shorelines Tab "Transect-Shoreline Intersections"
        self.dockwidget.rb_choose_by_distance.toggled.connect(
            lambda: enable_disable_widgets_by_radio_button(
                self.dockwidget.rb_choose_by_distance,
                self.dockwidget.gb_choose_by_distance,
                self.dockwidget.gb_choose_by_placement,
            )
        )
        self.dockwidget.rb_choose_by_placement.toggled.connect(
            lambda: enable_disable_widgets_by_radio_button(
                self.dockwidget.rb_choose_by_placement,
                self.dockwidget.gb_choose_by_placement,
                self.dockwidget.gb_choose_by_distance,
            )
        )

        # Summary Reports Tab "General" section
        self.dockwidget.cb_enable_report_generation.toggled.connect(
            lambda: enable_disable_groupbox_by_checkbox(
                self.dockwidget.cb_enable_report_generation,
                self.dockwidget.gb_enable_individual_reports,
            )
        )

        # Tabs "Save" input parameters
        self.dockwidget.pb_proj_save_settings.clicked.connect(
            lambda: save_project_tab_project_settings(self)
        )
        self.dockwidget.pb_baseline_save_settings.clicked.connect(
            lambda: save_baseline_tab_project_settings(self)
        )
        self.dockwidget.pb_transects_save_settings.clicked.connect(
            lambda: save_transects_tab_project_settings(self)
        )
        self.dockwidget.pb_shorelines_save_settings.clicked.connect(
            lambda: save_shorelines_tab_project_settings(self)
        )

        if not test:
            # Set custom widget properties
            set_plugin_widget_properties(self)

            # Load saved input parameters
            load_plugin_project_settings(self)

            # Check QSCAT updates on start
            # check_updates_on_start()
