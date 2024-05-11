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
from qscat.gui.widget_properties import WidgetProperties
from qscat.qscat_dockwidget import QscatDockWidget


class QscatPlugin:
    def __init__(self, iface):
        self.iface = iface
        # self.actions = []
        self.action = None
        self.dw = None
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
        self.dw.closingPlugin.disconnect(self.onClosePlugin)
        # self.plugin_is_active = False

    def unload(self):
        # Remove from Plugins Toolbar
        self.iface.removeToolBarIcon(self.action)

        # Remove from Plugins Menu
        self.iface.removePluginMenu("QSCAT", self.action)

        del self.action

    def run(self, test=False):
        self.dw = QscatDockWidget()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dw)
        self.dw.setWindowTitle("QSCAT")
        self.dw.show()
        self.dw.tw_qscat.setStyleSheet("QTabWidget::tab { text-align: left; }")

        # ---------------------------------------------------------------------
        # SIGNALS
        # ---------------------------------------------------------------------

        # Automator Tab
        self.dw.pb_automator_field_shoreline_apply.clicked.connect(
            lambda: automate_shoreline_field_button_clicked(self.dw)
        )
        self.dw.pb_automator_field_baseline_apply.clicked.connect(
            lambda: automate_baseline_field_button_clicked(self.dw)
        )
        self.dw.pb_automator_baseline_buffer_create.clicked.connect(
            lambda: automate_baseline_buffer_button_clicked(self.dw)
        )

        # Shorelines Tab
        shorelines_layer_widget = self.dw.qmlcb_shorelines_layer
        shorelines_layer_widget.layerChanged.connect(
            lambda: self.dw.qfcb_shorelines_date_field.setLayer(
                shorelines_layer_widget.currentLayer()
            )
        )
        shorelines_layer_widget.layerChanged.connect(
            lambda: self.dw.qfcb_shorelines_unc_field.setLayer(
                shorelines_layer_widget.currentLayer()
            )
        )

        # Update newest and oldest date lists on changing shorelines layer
        # shorelines_layer_widget.layerChanged.connect(
        #     lambda: validate_shorelines_layer(self)
        # )

        # Baseline Tab
        self.dw.cb_baseline_show_orientation.stateChanged.connect(
            lambda: show_hide_baseline_orientation(self.dw)
        )
        self.dw.qmlcb_baseline_layer.layerChanged.connect(
            lambda: self.dw.qfcb_baseline_placement_field.setLayer(
                self.dw.qmlcb_baseline_layer.currentLayer()
            )
        )
        self.dw.qmlcb_baseline_layer.layerChanged.connect(
            lambda: self.dw.qfcb_baseline_orientation_field.setLayer(
                self.dw.qmlcb_baseline_layer.currentLayer()
            )
        )
        self.dw.qmlcb_baseline_layer.layerChanged.connect(
            lambda: self.dw.qfcb_baseline_length_field.setLayer(
                self.dw.qmlcb_baseline_layer.currentLayer()
            )
        )
        self.dw.qmlcb_baseline_layer.layerChanged.connect(
            lambda: self.dw.qfcb_baseline_smoothing_field.setLayer(
                self.dw.qmlcb_baseline_layer.currentLayer()
            )
        )

        # Transects Tab
        self.dw.pb_transects_cast.clicked.connect(
            lambda: cast_transects_button_clicked(self.dw)
        )
        self.dw.rb_transects_by_transect_spacing.toggled.connect(
            lambda: enable_disable_widgets_by_radio_button(
                self.dw.rb_transects_by_transect_spacing,
                self.dw.qsb_transects_by_transect_spacing,
                self.dw.qsb_transects_by_number_of_transects,
            )
        )
        self.dw.rb_transects_by_number_of_transects.toggled.connect(
            lambda: enable_disable_widgets_by_radio_button(
                self.dw.rb_transects_by_number_of_transects,
                self.dw.qsb_transects_by_number_of_transects,
                self.dw.qsb_transects_by_transect_spacing,
            )
        )

        # Shoreline Change Tab
        self.dw.pb_stats_compute_shoreline_change.clicked.connect(
            lambda: compute_shoreline_change_button_clicked(self.dw)
        )
        self.dw.rb_choose_by_distance.toggled.connect(
            lambda: enable_disable_widgets_by_radio_button(
                self.dw.rb_choose_by_distance,
                self.dw.gb_choose_by_distance,
                self.dw.gb_choose_by_placement,
            )
        )
        self.dw.rb_choose_by_placement.toggled.connect(
            lambda: enable_disable_widgets_by_radio_button(
                self.dw.rb_choose_by_placement,
                self.dw.gb_choose_by_placement,
                self.dw.gb_choose_by_distance,
            )
        )
        self.dw.cb_stats_select_all.stateChanged.connect(
            lambda: select_all_stats_checkbox(self.dw)
        )

        # Area Change Tab
        self.dw.pb_stats_compute_area_change.clicked.connect(
            lambda: compute_area_change_stats(self.dw)
        )

        # Forecasting Tab
        self.dw.pb_forecasting_run_forecasting.clicked.connect(
            lambda: run_forecasting(self.dw)
        )

        # Visualization Tab
        self.dw.pb_vis_apply.clicked.connect(
            lambda: apply_color_ramp_button_clicked(self.dw)
        )
        self.dw.qmlcb_vis_stat_layer.layerChanged.connect(
            lambda: self.dw.qfcb_vis_stat_field.setLayer(
                self.dw.qmlcb_vis_stat_layer.currentLayer()
            )
        )

        # Summary Reports Tab
        self.dw.cb_enable_report_generation.toggled.connect(
            lambda: enable_disable_groupbox_by_checkbox(
                self.dw.cb_enable_report_generation,
                self.dw.gb_enable_individual_reports,
            )
        )

        # Help Tab
        self.dw.pb_about_check_for_updates.clicked.connect(
            lambda: check_updates_button_clicked(self.dw)
        )

        # Tabs "Save" input parameters
        settings = Settings(self.dw)
        self.dw.pb_project_save_inputs.clicked.connect(lambda: settings.save_project())
        self.dw.pb_shorelines_save_inputs.clicked.connect(
            lambda: settings.save_shorelines()
        )
        self.dw.pb_baseline_save_inputs.clicked.connect(
            lambda: settings.save_baseline()
        )
        self.dw.pb_transects_save_inputs.clicked.connect(
            lambda: settings.save_transects()
        )
        self.dw.pb_shoreline_change_save_inputs.clicked.connect(
            lambda: settings.save_shoreline_change()
        )
        self.dw.pb_area_change_save_inputs.clicked.connect(
            lambda: settings.save_area_change()
        )
        self.dw.pb_forecasting_save_inputs.clicked.connect(
            lambda: settings.save_forecasting()
        )
        self.dw.pb_visualization_save_inputs.clicked.connect(
            lambda: settings.save_visualization()
        )
        self.dw.pb_reports_save_inputs.clicked.connect(
            lambda: settings.save_summary_reports()
        )

        if not test:
            # Set custom widget properties
            widget_properties = WidgetProperties(self.dw)
            widget_properties.set()

            # Load saved input parameters
            settings.load_all()

            # Set custom widget properties after loading saved input parameters
            if self.dw.rb_choose_by_distance.isChecked():
                self.dw.gb_choose_by_placement.setEnabled(False)
            elif self.dw.rb_choose_by_placement.isChecked():
                self.dw.gb_choose_by_distance.setEnabled(False)

            if shorelines_layer_widget.currentLayer():
                shorelines_layer_actions(self.dw)

            # -----------------------------------------------------------------
            # SIGNALS AFTER LOADING SAVED INPUT PARAMETERS
            # -----------------------------------------------------------------

            shorelines_layer_widget.layerChanged.connect(
                lambda: shorelines_layer_actions(self.dw)
            )

            shorelines_layer_widget.layerChanged.connect(
                lambda: shorelines_layer_widget.currentLayer().committedAttributeValuesChanges.connect(
                    lambda: shorelines_layer_actions(self.dw)
                )
            )

            # Check QSCAT updates on start
            # check_updates_on_start()
