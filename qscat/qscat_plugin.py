# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from pathlib import Path

from PyQt5.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qscat.core.settings import Settings
from qscat.core.tabs.area_change.main import compute_area_change_stats
from qscat.core.tabs.automator import (
    automate_baseline_buffer_button_clicked,
    automate_baseline_field_button_clicked,
    automate_shoreline_field_button_clicked,
)
from qscat.core.tabs.baseline import show_hide_baseline_orientation
from qscat.core.tabs.forecasting import run_forecasting
from qscat.core.tabs.shoreline_change import compute_shoreline_change_button_clicked
from qscat.core.tabs.transects import cast_transects_button_clicked
from qscat.core.tabs.visualization import apply_color_ramp_button_clicked
from qscat.core.update import check_updates_button_clicked
from qscat.core.utils.plugin import get_plugin_dir
from qscat.gui.shoreline_change import select_all_stats_checkbox
from qscat.gui.shorelines import shorelines_layer_actions
from qscat.gui.utils import (
    enable_disable_groupbox_by_checkbox,
    enable_disable_widgets_by_radio_button,
)
from qscat.gui.widget_properties import set_plugin_widget_properties
from qscat.qscat_dockwidget import QscatDockWidget


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

        # ---------------------------------------------------------------------
        # SIGNALS
        # ---------------------------------------------------------------------

        # Automator Tab
        self.dockwidget.pb_automator_field_shoreline_apply.clicked.connect(
            lambda: automate_shoreline_field_button_clicked(self)
        )
        self.dockwidget.pb_automator_field_baseline_apply.clicked.connect(
            lambda: automate_baseline_field_button_clicked(self)
        )
        self.dockwidget.pb_automator_baseline_buffer_create.clicked.connect(
            lambda: automate_baseline_buffer_button_clicked(self)
        )

        # Shorelines Tab
        shorelines_layer_widget = self.dockwidget.qmlcb_shorelines_layer
        # shorelines_layer_widget.layerChanged.connect(
        shorelines_layer_widget.layerChanged.connect(
            lambda: self.dockwidget.qfcb_shorelines_date_field.setLayer(
                shorelines_layer_widget.currentLayer()
            )
        )
        shorelines_layer_widget.layerChanged.connect(
            lambda: self.dockwidget.qfcb_shorelines_unc_field.setLayer(
                shorelines_layer_widget.currentLayer()
            )
        )

        # Update newest and oldest date lists on changing shorelines layer
        # shorelines_layer_widget.layerChanged.connect(
        #     lambda: validate_shorelines_layer(self)
        # )

        # Baseline Tab
        self.dockwidget.cb_baseline_show_orientation.stateChanged.connect(
            lambda: show_hide_baseline_orientation(self)
        )
        self.dockwidget.qmlcb_baseline_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_baseline_placement_field.setLayer(
                self.dockwidget.qmlcb_baseline_layer.currentLayer()
            )
        )
        self.dockwidget.qmlcb_baseline_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_baseline_orientation_field.setLayer(
                self.dockwidget.qmlcb_baseline_layer.currentLayer()
            )
        )
        self.dockwidget.qmlcb_baseline_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_baseline_length_field.setLayer(
                self.dockwidget.qmlcb_baseline_layer.currentLayer()
            )
        )
        self.dockwidget.qmlcb_baseline_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_baseline_smoothing_field.setLayer(
                self.dockwidget.qmlcb_baseline_layer.currentLayer()
            )
        )

        # Transects Tab
        self.dockwidget.pb_transects_cast.clicked.connect(
            lambda: cast_transects_button_clicked(self.dockwidget)
        )
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

        # Shoreline Change Tab
        self.dockwidget.pb_stats_compute_shoreline_change.clicked.connect(
            lambda: compute_shoreline_change_button_clicked(self.dockwidget)
        )
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
        self.dockwidget.cb_stats_select_all.stateChanged.connect(
            lambda: select_all_stats_checkbox(self)
        )

        # Area Change Tab
        self.dockwidget.pb_stats_compute_area_change.clicked.connect(
            lambda: compute_area_change_stats(self.dockwidget)
        )

        # Forecasting Tab
        self.dockwidget.pb_forecasting_run_forecasting.clicked.connect(
            lambda: run_forecasting(self.dockwidget)
        )

        # Visualization Tab
        self.dockwidget.pb_vis_apply.clicked.connect(
            lambda: apply_color_ramp_button_clicked(self.dockwidget)
        )
        self.dockwidget.qmlcb_vis_stat_layer.layerChanged.connect(
            lambda: self.dockwidget.qfcb_vis_stat_field.setLayer(
                self.dockwidget.qmlcb_vis_stat_layer.currentLayer()
            )
        )

        # Summary Reports Tab
        self.dockwidget.cb_enable_report_generation.toggled.connect(
            lambda: enable_disable_groupbox_by_checkbox(
                self.dockwidget.cb_enable_report_generation,
                self.dockwidget.gb_enable_individual_reports,
            )
        )

        # About Tab
        self.dockwidget.pb_about_check_for_updates.clicked.connect(
            lambda: check_updates_button_clicked(self)
        )

        # Tabs "Save" input parameters
        settings = Settings(self.dockwidget)
        self.dockwidget.pb_project_save_inputs.clicked.connect(
            lambda: settings.save_project()
        )
        self.dockwidget.pb_shorelines_save_inputs.clicked.connect(
            lambda: settings.save_shorelines()
        )
        self.dockwidget.pb_baseline_save_inputs.clicked.connect(
            lambda: settings.save_baseline()
        )
        self.dockwidget.pb_transects_save_inputs.clicked.connect(
            lambda: settings.save_transects()
        )
        self.dockwidget.pb_shoreline_change_save_inputs.clicked.connect(
            lambda: settings.save_shoreline_change()
        )
        self.dockwidget.pb_area_change_save_inputs.clicked.connect(
            lambda: settings.save_area_change()
        )
        self.dockwidget.pb_forecasting_save_inputs.clicked.connect(
            lambda: settings.save_forecasting()
        )
        self.dockwidget.pb_visualization_save_inputs.clicked.connect(
            lambda: settings.save_visualization()
        )
        self.dockwidget.pb_reports_save_inputs.clicked.connect(
            lambda: settings.save_summary_reports()
        )

        if not test:
            # Set custom widget properties
            set_plugin_widget_properties(self)

            # Load saved input parameters
            settings.load_all()

            # Set custom widget properties after loading saved input parameters
            if self.dockwidget.rb_choose_by_distance.isChecked():
                self.dockwidget.gb_choose_by_placement.setEnabled(False)
            elif self.dockwidget.rb_choose_by_placement.isChecked():
                self.dockwidget.gb_choose_by_distance.setEnabled(False)

            if shorelines_layer_widget.currentLayer():
                shorelines_layer_actions(self.dockwidget)

            # -----------------------------------------------------------------
            # SIGNALS AFTER LOADING SAVED INPUT PARAMETERS
            # -----------------------------------------------------------------

            shorelines_layer_widget.layerChanged.connect(
                lambda: shorelines_layer_actions(self.dockwidget)
            )

            shorelines_layer_widget.layerChanged.connect(
                lambda: shorelines_layer_widget.currentLayer().committedAttributeValuesChanges.connect(
                    lambda: shorelines_layer_actions(self.dockwidget)
                )
            )

            # Check QSCAT updates on start
            # check_updates_on_start()
