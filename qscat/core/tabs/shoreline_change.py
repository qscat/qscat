# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import math
import time

import numpy as np
from PyQt5.QtCore import QVariant
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsGeometry,
    QgsMessageLog,
    QgsPointXY,
    QgsTask,
    QgsWkbTypes,
)
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.utils import iface

from qscat.core.constants import Statistic, Trend
from qscat.core.inputs import Inputs
from qscat.core.intersections import load_all_years_intersections
from qscat.core.layer import create_add_layer, load_shorelines, load_transects
from qscat.core.messages import display_message
from qscat.core.tabs.reports import SummaryReport
from qscat.core.utils.date import datetime_now
from qscat.lib.xalglib import invstudenttdistribution


def compute_shoreline_change_button_clicked(qdw):
    """Compute shoreline change stats (on button clicked).

    Args:
        qdw (QscatDockWidget): QscatDockWidget instance.
    """
    inputs = Inputs(qdw)

    baseline_inputs = inputs.baseline()
    shorelines_inputs = inputs.shorelines()
    transects_inputs = inputs.transects()
    shoreline_change_inputs = inputs.shoreline_change()
    summary_reports_inputs = inputs.summary_reports()

    transects = load_transects(
        qdw.qmlcb_shoreline_change_transects_layer.currentLayer()
    )
    shorelines = load_shorelines(shorelines_inputs)
    transects_layer_widget = shoreline_change_inputs["transects_layer_widget"]

    report = SummaryReport(qdw)

    shoreline_change = ShorelineChange(
        baseline_inputs,
        shorelines_inputs,
        transects_inputs,
        shoreline_change_inputs,
        summary_reports_inputs,
        transects,
        shorelines,
        transects_layer_widget,
        report,
    )

    shoreline_change.compute_shoreline_change()


class ShorelineChange:
    def __init__(
        self,
        baseline_inputs,
        shorelines_inputs,
        transects_inputs,
        shoreline_change_inputs,
        summary_reports_inputs,
        transects,
        shorelines,
        transects_layer_widget,
        reports,
    ):
        # Inputs
        self.baseline_inputs = baseline_inputs
        self.shorelines_inputs = shorelines_inputs
        self.transects_inputs = transects_inputs
        self.shoreline_change_inputs = shoreline_change_inputs
        self.summary_reports_inputs = summary_reports_inputs

        self.transects = transects
        self.shorelines = shorelines
        self.transects_layer_widget = transects_layer_widget
        self.reports = reports

        # Layer fields
        self.fields = {
            Statistic.SCE: [
                {"name": "SCE", "type": QVariant.Double},
                {"name": "SCE_highest_unc", "type": QVariant.Double},
                {"name": "SCE_trend", "type": QVariant.String},
                {"name": "SCE_closest_year", "type": QVariant.Int},
                {"name": "SCE_farthest_year", "type": QVariant.Int},
            ],
            Statistic.NSM: [
                {"name": "NSM", "type": QVariant.Double},
                {"name": "NSM_highest_unc", "type": QVariant.Double},
                {"name": "NSM_trend", "type": QVariant.String},
                # {'name': 'NSM_full_transect_point1_x', 'type': QVariant.Double},
                # {'name': 'NSM_full_transect_point1_y', 'type': QVariant.Double},
                # {'name': 'NSM_full_transect_point2_x', 'type': QVariant.Double},
                # {'name': 'NSM_full_transect_point2_y', 'type': QVariant.Double},
            ],
            Statistic.EPR: [
                {"name": "EPR", "type": QVariant.Double},
                {"name": "EPR_unc", "type": QVariant.Double},
                {"name": "EPR_trend", "type": QVariant.String},
            ],
            Statistic.LRR: [
                {"name": "LRR", "type": QVariant.Double},
                {"name": "LR2", "type": QVariant.Double},
                {"name": "LSE", "type": QVariant.Double},
                {"name": "LCI", "type": QVariant.Double},
            ],
            Statistic.WLR: [
                {"name": "WLR", "type": QVariant.Double},
                {"name": "WR2", "type": QVariant.Double},
                {"name": "WSE", "type": QVariant.Double},
                {"name": "WCI", "type": QVariant.Double},
            ],
        }

        self.stat_map = {
            Statistic.SCE: {
                "get_year1": self.get_closest_distance_year,
                "get_year2": self.get_farthest_distance_year,
                "get_main_values": [self.get_SCE],
                "get_trend_ref": self.shoreline_change_inputs["highest_unc"],
                "get_extra_values": [
                    self.get_closest_distance_year,
                    self.get_farthest_distance_year,
                ],
            },
            Statistic.NSM: {
                "get_year1": self.get_oldest_year,
                "get_year2": self.get_newest_year,
                "get_main_values": [self.get_NSM],
                "get_trend_ref": self.shoreline_change_inputs["highest_unc"],
                "get_extra_values": None,
                # 'get_extra_values': [
                #     get_fullest_transect_point1_x,
                #     get_fullest_transect_point1_y,
                #     get_fullest_transect_point2_x,
                #     get_fullest_transect_point2_y,
                #     get_fullest_transect_trend,
                # ],
            },
            Statistic.EPR: {
                "get_year1": self.get_oldest_year,
                "get_year2": self.get_newest_year,
                "get_main_values": [self.get_EPR],
                "get_trend_ref": self.shoreline_change_inputs["epr_unc"],
                "get_extra_values": None,
            },
            Statistic.LRR: {
                "get_year1": self.get_closest_distance_year,
                "get_year2": self.get_farthest_distance_year,
                "get_main_values": [
                    self.get_LRR,
                    self.get_LR2,
                    self.get_LSE,
                    self.get_LCI,
                ],
                "get_trend_ref": None,
                "get_extra_values": None,
            },
            Statistic.WLR: {
                "get_year1": self.get_closest_distance_year,
                "get_year2": self.get_farthest_distance_year,
                "get_main_values": [
                    self.get_WLR,
                    self.get_WR2,
                    self.get_WSE,
                    self.get_WCI,
                ],
                "get_trend_ref": None,
                "get_extra_values": None,
            },
        }

    def compute_shoreline_change(self):
        """Compute shoreline change stats."""
        start_time = time.perf_counter()

        globals()["get_transects_intersections_task"] = GetTransectsIntersectionsTask(
            self.transects,
            self.shorelines,
            self.shorelines_inputs,
            self.transects_inputs,
            self.baseline_inputs,
            self.shoreline_change_inputs,
        )
        globals()["get_transects_intersections_task"].taskCompleted.connect(
            lambda: self.get_transects_intersections_task_state_changed(start_time)
        )
        QgsApplication.taskManager().addTask(
            globals()["get_transects_intersections_task"]
        )

    def get_transects_intersections_task_state_changed(self, start_time):
        task = globals()["get_transects_intersections_task"]

        if task.status() == QgsTask.Complete:
            all_years_intersections = load_all_years_intersections(
                task.transects_intersects
            )

            # One layer for all stats
            all_fields = []
            all_values = np.array([])
            all_geoms = []

            # For summary reports
            stat_values = {}

            # Compute all selected stats
            for stat in self.shoreline_change_inputs["selected_stats"]:
                if self.compute_shoreline_change_stat_prechecks(stat):
                    values, geoms = self.compute_single_stat_all_transects(
                        stat,
                        all_years_intersections,
                    )

                    self.add_shoreline_change_stat_layer(
                        stat,
                        values,
                        geoms,
                        self.fields[stat],
                    )

                    # One layer for all stats
                    all_fields += self.fields[stat]
                    if not all_values.size > 0:
                        all_values = np.array(values)
                    else:
                        all_values = np.hstack((all_values, values))

                    # Get first stat geom computed as the geom representation
                    if not all_geoms:
                        all_geoms = geoms

                    # For summary reports, extract main values as a 1d list
                    stat_values[stat] = [sublist[0] for sublist in values]

            # One layer for all stats
            create_add_layer(
                geometry="LineString",
                geometries=all_geoms,
                name="ALL STATS",
                fields=all_fields,
                values=all_values.tolist(),
            )

            # Summary
            if (
                self.summary_reports_inputs["is_report"]
                and self.summary_reports_inputs["is_shoreline_change_report"]
            ):
                self.create_summary_report(stat_values)

            elapsed_time = round((time.perf_counter() - start_time) * 1000, 2)
            QgsMessageLog.logMessage(
                f"Shoreline change in {elapsed_time} ms",
                "Execution time",
                level=Qgis.Info,
            )

    def create_summary_report(self, stat_values):
        """Create summary report for shoreline change stats.

        Args:
            stat_values (dict): Dictionary of shoreline change stats values.

        Example:
            { 'SCE': [0.1, 0.2, 0.3, ...], ... }
        """
        # Summary
        summary = {}

        summary["datetime"] = datetime_now()
        transects = load_transects(self.shoreline_change_inputs["transects_layer"])
        summary["num_of_transects"] = len(transects)

        # Results
        if Statistic.SCE in self.shoreline_change_inputs["selected_stats"]:
            SCE = stat_values[Statistic.SCE]
            summary["SCE_avg"] = round(sum(SCE) / len(SCE), 2)
            summary["SCE_max"] = round(max(SCE), 2)
            summary["SCE_min"] = round(min(SCE), 2)

        if Statistic.NSM in self.shoreline_change_inputs["selected_stats"]:
            NSM = stat_values[Statistic.NSM]
            unc = self.shoreline_change_inputs["highest_unc"]
            summary["NSM_avg"] = round(sum(NSM) / len(NSM), 2)

            NSM_e = [x for x in NSM if x < -unc]
            erosion_count = len(NSM_e)
            summary["NSM_erosion_num_of_transects"] = erosion_count
            summary["NSM_erosion_pct_transects"] = (
                f"{(erosion_count / len(NSM)) * 100:.2f} %"
            )
            summary["NSM_erosion_avg"] = round(sum(NSM_e) / len(NSM_e), 2)
            summary["NSM_erosion_max"] = round(max(NSM_e), 2)
            summary["NSM_erosion_min"] = round(min(NSM_e), 2)

            NSM_a = [x for x in NSM if x > unc]
            accretion_count = len(NSM_a)
            summary["NSM_accretion_num_of_transects"] = accretion_count
            summary["NSM_accretion_pct_transects"] = (
                f"{(accretion_count / len(NSM)) * 100:.2f} %"
            )
            summary["NSM_accretion_avg"] = round(sum(NSM_a) / len(NSM_a), 2)
            summary["NSM_accretion_max"] = round(max(NSM_a), 2)
            summary["NSM_accretion_min"] = round(min(NSM_a), 2)

            NSM_s = [x for x in NSM if x >= -unc and x <= unc]
            stable_count = len(NSM_s)
            summary["NSM_stable_num_of_transects"] = stable_count
            summary["NSM_stable_pct_transects"] = (
                f"{(stable_count / len(NSM)) * 100:.2f} %"
            )
            summary["NSM_stable_avg"] = round(sum(NSM_s) / len(NSM_s), 2)
            summary["NSM_stable_max"] = round(max(NSM_s), 2)
            summary["NSM_stable_min"] = round(min(NSM_s), 2)

        if Statistic.EPR in self.shoreline_change_inputs["selected_stats"]:
            EPR = stat_values[Statistic.EPR]
            unc = self.shoreline_change_inputs["epr_unc"]
            summary["EPR_avg"] = round(sum(EPR) / len(EPR), 2)

            EPR_e = [x for x in EPR if x < -unc]
            erosion_count = len(EPR_e)
            summary["EPR_erosion_num_of_transects"] = erosion_count
            summary["EPR_erosion_pct_transects"] = (
                f"{(erosion_count / len(EPR)) * 100:.2f} %"
            )
            summary["EPR_erosion_avg"] = round(sum(EPR_e) / len(EPR_e), 2)
            summary["EPR_erosion_max"] = round(max(EPR_e), 2)
            summary["EPR_erosion_min"] = round(min(EPR_e), 2)

            EPR_a = [x for x in EPR if x > unc]
            accretion_count = len(EPR_a)
            summary["EPR_accretion_num_of_transects"] = accretion_count
            summary["EPR_accretion_pct_transects"] = (
                f"{(accretion_count / len(EPR)) * 100:.2f} %"
            )
            summary["EPR_accretion_avg"] = round(sum(EPR_a) / len(EPR_a), 2)
            summary["EPR_accretion_max"] = round(max(EPR_a), 2)
            summary["EPR_accretion_min"] = round(min(EPR_a), 2)

            EPR_s = [x for x in EPR if x >= -unc and x <= unc]
            stable_count = len(EPR_s)
            summary["EPR_stable_num_of_transects"] = stable_count
            summary["EPR_stable_pct_transects"] = (
                f"{(stable_count / len(EPR)) * 100:.2f} %"
            )
            summary["EPR_stable_avg"] = round(sum(EPR_s) / len(EPR_s), 2)
            summary["EPR_stable_max"] = round(max(EPR_s), 2)
            summary["EPR_stable_min"] = round(min(EPR_s), 2)

        if Statistic.LRR in self.shoreline_change_inputs["selected_stats"]:
            LRR = stat_values[Statistic.LRR]
            summary["LRR_avg"] = round(sum(LRR) / len(LRR), 2)

            LRR_e = [x for x in LRR if x < 0]
            erosion_count = len(LRR_e)
            summary["LRR_erosion_num_of_transects"] = erosion_count
            summary["LRR_erosion_pct_transects"] = (
                f"{(erosion_count / len(LRR)) * 100:.2f} %"
            )
            summary["LRR_erosion_avg"] = round(sum(LRR_e) / len(LRR_e), 2)
            summary["LRR_erosion_max"] = round(max(LRR_e), 2)
            summary["LRR_erosion_min"] = round(min(LRR_e), 2)

            LRR_a = [x for x in LRR if x >= 0]
            accretion_count = len(LRR_a)
            summary["LRR_accretion_num_of_transects"] = accretion_count
            summary["LRR_accretion_pct_transects"] = (
                f"{(accretion_count / len(LRR)) * 100:.2f} %"
            )
            summary["LRR_accretion_avg"] = round(sum(LRR_a) / len(LRR_a), 2)
            summary["LRR_accretion_max"] = round(max(LRR_a), 2)
            summary["LRR_accretion_min"] = round(min(LRR_a), 2)

        if Statistic.WLR in self.shoreline_change_inputs["selected_stats"]:
            WLR = stat_values[Statistic.WLR]
            summary["WLR_avg"] = round(sum(WLR) / len(WLR), 2)

            WLR_e = [x for x in WLR if x < 0]
            erosion_count = len(WLR_e)
            summary["WLR_erosion_num_of_transects"] = erosion_count
            summary["WLR_erosion_pct_transects"] = (
                f"{(erosion_count / len(WLR)) * 100:.2f} %"
            )
            summary["WLR_erosion_avg"] = round(sum(WLR_e) / len(WLR_e), 2)
            summary["WLR_erosion_max"] = round(max(WLR_e), 2)
            summary["WLR_erosion_min"] = round(min(WLR_e), 2)

            WLR_a = [x for x in WLR if x >= 0]
            accretion_count = len(WLR_a)
            summary["WLR_accretion_num_of_transects"] = accretion_count
            summary["WLR_accretion_pct_transects"] = (
                f"{(accretion_count / len(WLR)) * 100:.2f} %"
            )
            summary["WLR_accretion_avg"] = round(sum(WLR_a) / len(WLR_a), 2)
            summary["WLR_accretion_max"] = round(max(WLR_a), 2)
            summary["WLR_accretion_min"] = round(min(WLR_a), 2)

        self.reports.summary = summary
        self.reports.shoreline_change()

    def compute_single_stat_all_transects(self, stat, all_years_intersections):
        """Compute a single shoreline change stat for all transects.

        Args:
            stat (Statistic): Shoreline change statistic.
            all_years_intersections (list[dict]): List of all years intersections.

        Returns:
            all_values: List of computed values
            geoms: List of transect geometries
        """
        all_values = []
        geoms = []

        for years_intersections in all_years_intersections:
            values, geom = self.compute_single_stat_single_transects(
                stat,
                years_intersections,
            )
            all_values.append(values)
            geoms.append(geom)

        return all_values, geoms

    def compute_single_stat_single_transects(self, stat, years_intersections):
        """Compute a single shoreline change stat for a single transect.

        Args:
            stat (Statistic): Shoreline change statistic.
            years_intersections (dict): Dictionary of years intersections.

        Returns:
            values: List of computed values (per column)
            geom: Transect geometry
        """
        year1 = self.stat_map[stat]["get_year1"](years_intersections)
        year2 = self.stat_map[stat]["get_year2"](years_intersections)

        distance1 = years_intersections[year1]["distance"]
        distance2 = years_intersections[year2]["distance"]

        # Get main stat values
        compute_params = {
            "year1": year1,
            "year2": year2,
            "distance1": distance1,
            "distance2": distance2,
            "years_intersections": years_intersections,
        }
        values = []

        # Main values (e.g. SCE, LRR, LR2 etc.)
        main_values_funcs = self.stat_map[stat]["get_main_values"]
        for main_values_func in main_values_funcs:
            values.append(main_values_func(compute_params))

        # Trends
        trend_reference = self.stat_map[stat]["get_trend_ref"]
        if trend_reference:
            # Append the unc value (e.g. SCE_highest_unc, NSM_highest_unc, EPR_unc)
            values.append(trend_reference)

            # Get change trend (e.g. stable, accreting, eroding)
            stat_value_trend = get_change_trend(values[0], trend_reference)

            # Append the trend string (e.g. SCE_trend, NSM_trend, EPR_trend)
            values.append(stat_value_trend)

        # Extra values
        get_extra_values_funcs = self.stat_map[stat]["get_extra_values"]
        if get_extra_values_funcs:
            for get_extra_values_func in get_extra_values_funcs:
                values.append(get_extra_values_func(years_intersections))

        # Clip transects
        if self.shoreline_change_inputs["is_clip_transects"]:
            start_pt = QgsPointXY(
                years_intersections[year1]["intersect_x"],
                years_intersections[year1]["intersect_y"],
            )
            end_pt = QgsPointXY(
                years_intersections[year2]["intersect_x"],
                years_intersections[year2]["intersect_y"],
            )
            geom = QgsGeometry.fromPolylineXY([start_pt, end_pt])
        else:
            geom = years_intersections[year1]["orig_transect_geom"]

        return values, geom

    def add_shoreline_change_stat_layer(self, stat, all_values, geoms, fields):
        """Add shoreline change stat layer to the map canvas.

        Args:
            stat (Statistic): Shoreline change statistic.
            all_values (list): List of computed values.
            geoms (list): List of transect geometries.
            fields (list): List of layer fields.
        """
        # Layer names
        if stat in [Statistic.NSM, Statistic.EPR]:
            name = f'{stat} ({self.shoreline_change_inputs["newest_year"]}-{self.shoreline_change_inputs["oldest_year"]})'
        elif stat in [Statistic.SCE, Statistic.LRR, Statistic.WLR]:
            name = f"{stat}"

        # Custom properties
        dates = {
            "newest_date": self.shoreline_change_inputs["newest_date"],
            "oldest_date": self.shoreline_change_inputs["oldest_date"],
            "stat": stat,
        }

        # Add uncertainty value in custom properties
        if stat in [Statistic.SCE, Statistic.NSM]:
            dates["unc"] = self.shoreline_change_inputs["highest_unc"]
        elif stat == Statistic.EPR:
            dates["unc"] = self.shoreline_change_inputs["epr_unc"]

        create_add_layer(
            geometry="LineString",
            geometries=geoms,
            name=name,
            fields=fields,
            values=all_values,
            extra_values=dates,
        )

    def compute_shoreline_change_stat_prechecks(self, stat):
        """Prechecks for computation of any shoreline change stats.

        Args:
            stat (Statistic): Shoreline change statistic.

        Returns:
            boolean
        """
        shoreline_layer = self.shorelines_inputs["shorelines_layer"]

        if stat in [Statistic.LRR, Statistic.WLR]:
            if shoreline_layer.featureCount() < 3:
                display_message(
                    "LRR and WLR requires atleast 3 shorelines.",
                    Qgis.Warning,
                )
                return False
        return True

    # Get year 1 and year 2 functions
    def get_closest_distance_year(self, years_intersections):
        closest_distance_year = min(
            years_intersections.items(), key=lambda x: x[1]["distance"]
        )[0]
        return closest_distance_year

    def get_farthest_distance_year(self, years_intersections):
        farthest_distance_year = max(
            years_intersections.items(), key=lambda x: x[1]["distance"]
        )[0]
        return farthest_distance_year

    def get_oldest_year(self, years_intersections):
        oldest_year = self.shoreline_change_inputs["oldest_year"]
        return oldest_year

    def get_newest_year(self, years_intersections):
        newest_year = self.shoreline_change_inputs["newest_year"]
        return newest_year

    # Get main values functions
    def get_SCE(self, compute_params):
        SCE_value = compute_SCE(
            compute_params["distance1"], compute_params["distance2"]
        )
        return round(SCE_value, 2)

    def get_NSM(self, compute_params):
        NSM_value = compute_NSM(
            compute_params["distance1"], compute_params["distance2"]
        )
        return round(NSM_value, 2)

    def get_EPR(self, compute_params):
        NSM_value = compute_NSM(
            compute_params["distance1"], compute_params["distance2"]
        )
        EPR_value = compute_EPR(
            NSM_value, compute_params["year1"], compute_params["year2"]
        )
        return round(EPR_value, 2)

    def get_LRR(self, compute_params):
        years, distances = get_sorted_years_distances(
            compute_params["years_intersections"]
        )
        LRR_value = compute_LRR(years, distances)
        return round(LRR_value, 2)

    def get_LR2(self, compute_params):
        years, distances = get_sorted_years_distances(
            compute_params["years_intersections"]
        )
        LR2_value = compute_LR2(years, distances)
        return round(LR2_value, 2)

    def get_LSE(self, compute_params):
        years, distances = get_sorted_years_distances(
            compute_params["years_intersections"]
        )
        LSE_value = compute_LSE(years, distances)
        return round(LSE_value, 2)

    def get_LCI(self, compute_params):
        years, distances = get_sorted_years_distances(
            compute_params["years_intersections"]
        )
        LCI_value = compute_LCI(
            years, distances, self.shoreline_change_inputs["confidence_interval"]
        )
        return round(LCI_value, 2)

    def get_WLR(self, compute_params):
        years, distances = get_sorted_years_distances(
            compute_params["years_intersections"]
        )
        uncs = get_sorted_uncs(self.shoreline_change_inputs["years_uncs"])
        WLR_value = compute_WLR(years, distances, uncs)
        return round(WLR_value, 2)

    def get_WR2(self, compute_params):
        years, distances = get_sorted_years_distances(
            compute_params["years_intersections"]
        )
        uncs = get_sorted_uncs(self.shoreline_change_inputs["years_uncs"])
        WR2_value = compute_WR2(years, distances, uncs)
        return round(WR2_value, 2)

    def get_WSE(self, compute_params):
        years, distances = get_sorted_years_distances(
            compute_params["years_intersections"]
        )
        uncs = get_sorted_uncs(self.shoreline_change_inputs["years_uncs"])
        WSE_value = compute_WSE(years, distances, uncs)
        return round(WSE_value, 2)

    def get_WCI(self, compute_params):
        years, distances = get_sorted_years_distances(
            compute_params["years_intersections"]
        )
        uncs = get_sorted_uncs(self.shoreline_change_inputs["years_uncs"])
        WCI_value = compute_WCI(
            years, distances, uncs, self.shoreline_change_inputs["confidence_interval"]
        )
        return round(WCI_value, 2)


# Computation functions
def compute_SCE(closest_distance, farthest_distance):
    """Compute Shoreline Change Envelope (SCE) value.

    Args:
        closest_distance (float): Distance value 1.
        farthest_distance (float): Distance value 2.

    Returns:
        float: SCE value.
    """
    SCE_value = farthest_distance - closest_distance
    return abs(SCE_value)


def compute_NSM(distance1, distance2):
    """Compute Net Shoreline Movement (NSM) value.

    Args:
        distance1 (float): Distance value 1.
        distance2 (float): Distance value 2.

    Returns:
        float: NSM value.
    """
    NSM_value = distance2 - distance1
    return NSM_value


def compute_EPR(NSM_value, oldest_year, newest_year):
    """Compute End Point Rate (EPR) value.

    Args:
        NSM_value (float): Net Shoreline Movement value.
        oldest_year (float): Oldest year value.
        newest_year (float): Newest year value.

    Returns:
        float: EPR value.

    Raises:
        TypeError: If NSM, newest year, or oldest year values are None.
        TypeError: If NSM, newest year, or oldest year values are not floats.
        ValueError: If oldest year is equal to newest year.
        ValueError: If newest year is greater than oldest year.
        ValueError: If newest year, or oldest year values are negative.
    """
    if NSM_value is None:
        raise TypeError("NSM values cannot be None.")
    if oldest_year is None:
        raise TypeError("Oldest year value cannot be None.")
    if newest_year is None:
        raise TypeError("Newest year value cannot be None.")

    if not isinstance(NSM_value, float):
        raise TypeError("NSM value must be float.")
    if not isinstance(oldest_year, float):
        raise TypeError("Oldest year must be float.")
    if not isinstance(newest_year, float):
        raise TypeError("Newest year must be float.")

    if oldest_year == newest_year:
        raise ValueError("Oldest year cannot be equal to newest year.")

    if oldest_year > newest_year:
        raise ValueError("Oldest year cannot be greater than newest year.")

    if oldest_year < 0:
        raise ValueError("Oldest year must be positive.")
    if newest_year < 0:
        raise ValueError("Newest year must be positive.")

    EPR_value = NSM_value / (newest_year - oldest_year)
    return EPR_value


def compute_EPR_unc(newest_year_unc, oldest_year_unc, newest_year, oldest_year):
    """Compute End Point Rate (EPR) uncertainty value."""
    if newest_year_unc is None:
        raise TypeError("Newest year uncertainty value cannot be None.")
    if oldest_year_unc is None:
        raise TypeError("Oldest year uncertainty value cannot be None.")
    if newest_year is None:
        raise TypeError("Newest year value cannot be None.")
    if oldest_year is None:
        raise TypeError("Oldest year value cannot be None.")

    if not isinstance(newest_year_unc, float):
        raise TypeError("Newest year uncertainty value must be float.")
    if not isinstance(oldest_year_unc, float):
        raise TypeError("Oldest year uncertainty value must be float.")
    if not isinstance(newest_year, float):
        raise TypeError("Newest year must be float.")
    if not isinstance(oldest_year, float):
        raise TypeError("Oldest year must be float.")

    if newest_year < oldest_year:
        raise ValueError("Newest year cannot be less than oldest year.")

    if newest_year_unc < 0:
        raise ValueError("Newest year uncertainty value must be positive.")
    if oldest_year_unc < 0:
        raise ValueError("Oldest year uncertainty value must be positive.")
    if newest_year < 0:
        raise ValueError("Newest year must be positive.")
    if oldest_year < 0:
        raise ValueError("Oldest year must be positive.")

    EPR_unc_numerator = newest_year_unc**2 + oldest_year_unc**2
    EPR_unc_value = math.sqrt(EPR_unc_numerator) / (newest_year - oldest_year)
    return EPR_unc_value


def compute_least_square_fit(years, distances):
    """Compute least square fit.

    Args:
        years (np.ndarray): Numpy array of years.
        distances (np.ndarray): Numpy array of distances.

    Returns:
        tuple: Tuple of slope and intercept values.

    Raises:
        TypeError: If year or distance values are None.
        ValueError: If year and distance values are not the same length.
        ValueError: If year and distance values have less than 3 elements.
        ValueError: If year values are not in ascending order.
    """
    if years is None:
        raise TypeError("Year values cannot be None.")
    if distances is None:
        raise TypeError("Distance values cannot be None.")

    if not isinstance(distances, np.ndarray) or distances.dtype != np.float64:
        raise TypeError("Distance values must be numpy floats.")

    if len(years) != len(distances):
        raise ValueError("Year and distance values must have the same length.")

    if len(years) < 3:
        raise ValueError("Years must be atleast 3 members.")
    if len(distances) < 3:
        raise ValueError("Distances must be atleast 3 members.")

    if not np.all(years[:-1] <= years[1:]):
        raise ValueError("Year values must be in ascending order.")

    if np.any(years < 0):
        raise ValueError("Year values must be non-negative.")

    slope, intercept = np.polyfit(years, distances, 1)
    return slope, intercept


def compute_LRR(years, distances):
    """Compute Linear Regression Rate (LRR) value.

    Args:
        years (np.ndarray): Numpy array of years.
        distances (np.ndarray): Numpy array of distances.

    Returns:
        float: LRR value.
    """

    slope, _ = compute_least_square_fit(years, distances)
    LRR_value = float(slope)  # previously numpy
    return LRR_value


def compute_LR2(years, distances):
    """Compute Linear Regression R-squared (LR2) value.

    Args:
        years (np.ndarray): Numpy array of years.
        distances (np.ndarray): Numpy array of distances.

    Returns:
        float: LR2 value.
    """
    slope, intercept = compute_least_square_fit(years, distances)

    pred = slope * years + intercept
    ss_res = np.sum((distances - pred) ** 2)
    y_mean = np.mean(distances)
    ss_tot = np.sum((distances - y_mean) ** 2)
    r_squared = 1 - ss_res / ss_tot

    LR2_value = float(r_squared)  # previously numpy
    return LR2_value


def compute_LSE(years, distances):
    """Compute Linear Regression Standard Error

    Args:
        years (np.ndarray): Numpy array of years.
        distances (np.ndarray): Numpy array of distances.

    Returns:
        float: LSE value.
    """
    slope, intercept = compute_least_square_fit(years, distances)
    ss_res = np.sum((distances - (slope * years + intercept)) ** 2)
    n = len(years)
    standard_error = np.sqrt(ss_res / (n - 2))
    LSE_value = float(standard_error)  # previously numpy
    return LSE_value


def compute_LCI(years, distances, conf=99.7):
    x_mean = np.mean(years)
    sum_sq_diff = np.sum((years - x_mean) ** 2)
    standard_error = compute_LSE(years, distances)
    standard_error_slope = np.sqrt(standard_error**2 / sum_sq_diff)

    alpha = 1 - (float(conf) * 0.01)
    n = len(years)
    t_value = invstudenttdistribution(n - 2, 1 - alpha / 2)
    ci = t_value * standard_error_slope
    LCI_value = float(ci)
    # print("LCI", ci)
    return LCI_value


def compute_weighted_least_square_fit(years, distances, uncertainties):
    """Compute weighted least square fit.

    Args:
        years (np.ndarray): Numpy array of years.
        distances (np.ndarray): Numpy array of distances.
        uncertainties (np.ndarray): Numpy array of uncertainties.

    Returns:
        tuple: Tuple of slope and intercept values.

    Raises:
        TypeError: If year, distance, or uncertainties values are None.
        TypeError: If year, distance, or uncertainties values are not numpy floats.
        ValueError: If year, distance, and uncertainties values are not the same length.
        ValueError: If year, distance, and uncertainties values have less than 3 elements.
        ValueError: If year values are not in ascending order.
        ValueError: If year, or uncertainties values are negative.
    """
    if years is None:
        raise TypeError("Year values cannot be None.")
    if distances is None:
        raise TypeError("Distance values cannot be None.")
    if uncertainties is None:
        raise TypeError("Uncertainties values cannot be None.")

    if not isinstance(years, np.ndarray) or years.dtype != np.float64:
        raise TypeError("Year values must be numpy floats.")
    if not isinstance(distances, np.ndarray) or distances.dtype != np.float64:
        raise TypeError("Distance values must be numpy floats.")
    if not isinstance(uncertainties, np.ndarray) or uncertainties.dtype != np.float64:
        raise TypeError("Uncertainties values must be numpy floats.")

    if len(years) != len(distances) or len(years) != len(uncertainties):
        raise ValueError(
            "Year, distance, and uncertainties arrays must have the same length."
        )

    if len(years) < 3:
        raise ValueError("Years must be atleast 3 members.")
    if len(distances) < 3:
        raise ValueError("Distances must be atleast 3 members.")
    if len(uncertainties) < 3:
        raise ValueError("Uncertainties must be atleast 3 members.")

    if not np.all(years[:-1] <= years[1:]):
        raise ValueError("Year values must be in ascending order.")

    if np.any(years < 0):
        raise ValueError("Year values must be non-negative.")
    if np.any(uncertainties < 0):
        raise ValueError("Uncertainties values must be non-negative.")

    # uncertainties = np.array([1/float(u**2) for u in uncertainties])
    wmean_x = np.average(years, weights=uncertainties)
    wmean_y = np.average(distances, weights=uncertainties)
    cov_xy = np.sum(uncertainties * (years - wmean_x) * (distances - wmean_y))
    var_x = np.sum(uncertainties * (years - wmean_x) ** 2)
    slope = cov_xy / var_x
    intercept = wmean_y - slope * wmean_x

    return slope, intercept


def compute_WLR(years, distances, uncertainties):
    """Compute Weighted Linear Regression (WLR) value.

    Args:
        years (np.ndarray): Numpy array of years.
        distances (np.ndarray): Numpy array of distances.
        uncertainties (np.ndarray): Numpy array of uncertainties.

    Returns:
        float: WLR value.
    """
    uncertainties = np.array([1 / float(u**2) for u in uncertainties])
    (
        slope,
        _,
    ) = compute_weighted_least_square_fit(years, distances, uncertainties)
    WLR_value = float(slope)  # previously numpy
    return WLR_value


def compute_WR2(years, distances, uncertainties):
    """Compute Weighted Linear Regression R-squared (WR2) value.

    Args:
        years (np.ndarray): Numpy array of years.
        distances (np.ndarray): Numpy array of distances.
        uncertainties (np.ndarray): Numpy array of uncertainties.

    Returns:
        float: WR2 value.
    """
    uncertainties = np.array([1 / float(u**2) for u in uncertainties])
    slope, intercept = compute_weighted_least_square_fit(
        years, distances, uncertainties
    )
    pred = slope * years + intercept
    residuals = distances - pred
    rss = np.sum(uncertainties * residuals**2)
    wmean_y = np.average(distances, weights=uncertainties)
    tss = np.sum(uncertainties * (distances - wmean_y) ** 2)
    r2 = 1 - rss / tss
    WR2_value = float(r2)  # previously numpy
    return WR2_value


def compute_WSE(years, distances, uncertainties):
    uncertainties = np.array([1 / float(u**2) for u in uncertainties])
    slope, intercept = compute_weighted_least_square_fit(
        years, distances, uncertainties
    )

    pred = slope * years + intercept
    residuals = distances - pred
    ss_res = np.sum(uncertainties * residuals**2)
    n = len(years)
    standard_error = np.sqrt(ss_res / (n - 2))
    WSE_value = float(standard_error)  # previously numpy
    return WSE_value


def compute_WCI(years, distances, uncertainties, conf=99.7):
    # we shouldn't pass unc=1/u^2 here
    # its already applied in compute_WSE
    standard_error = compute_WSE(years, distances, uncertainties)

    uncs = np.array([1 / float(u**2) for u in uncertainties])
    wmean_x = np.average(years, weights=uncs)
    sum_sq_diff = np.sum(uncs * (years - wmean_x) ** 2)

    standard_error_slope = np.sqrt(standard_error**2 / sum_sq_diff)

    alpha = 1 - (float(conf) * 0.01)
    n = len(years)
    t_value = invstudenttdistribution(n - 2, 1 - alpha / 2)
    ci = t_value * standard_error_slope
    WCI_value = float(ci)
    return WCI_value


def get_change_trend(stat_value, unc_value):
    """Get change trend based on statistic value's (e.g. SCE, NSM, EPR..) sign,
    and uncertainty value. The positive-negative uncertainty value is used
    as `stable` trend.

    Args:
        stat_value (float): Statistic value (e.g. SCE, NSM, EPR..).
        unc_value (float): Uncertainty value (highest).

    Returns:
        str: Change trend (e.g. stable, accretion, erosion).

    Raises:
        TypeError: If statistic or uncertainty values are None.
        ValueError: If uncertainty value is zero.
    """
    if stat_value is None or unc_value is None:
        raise TypeError("Statistic or uncertainty values cannot be None.")
    if unc_value == 0:
        raise ValueError("Uncertainty value cannot be zero.")

    if stat_value >= -unc_value and stat_value <= unc_value:
        return Trend.STABLE
    elif stat_value > unc_value:
        return Trend.ACCRETING
    elif stat_value < -unc_value:
        return Trend.ERODING


def get_sorted_years_distances(years_intersections):
    """Get sorted years(X), distances(Y) and uncertainties(W) in a single
    transect intersections used as an X and Y input for least square fit and
    weighted least square fit.

    Args:
        years_intersections(dict): Dictionary of year intersections on a single
            transect

    Returns:
        tuple: Tuple of years and distances

    Example:
        years_intersections = {
            1990: {
                'intersect_x': 0,
                'intersect_y': 0,
                'unc': 0.1,
                'distance': 0.1
            },
            1995: {
                'intersect_x': 0,
                'intersect_y': 0,
                'unc': 0.1,
                'distance': 0.2
            },
            2000: {
                'intersect_x': 0,
                'intersect_y': 0,
                'unc': 0.1,
                'distance': 0.3
            }...
    """
    # validate_years_intersections(years_intersections)

    yi_sorted = sorted(years_intersections)
    years_intersections = {key: years_intersections[key] for key in yi_sorted}
    years = np.array([k for k in years_intersections.keys()])
    distances = np.array([v["distance"] for v in years_intersections.values()])

    return (years, distances)


def get_sorted_uncs(uncs):
    uncs_sorted = sorted(uncs)
    uncs = {key: uncs[key] for key in uncs_sorted}
    uncs = np.array([v for v in uncs.values()])
    return uncs


class GetTransectsIntersectionsTask(QgsTask):
    def __init__(
        self,
        transects,
        shorelines,
        shorelines_params,
        transects_params,
        baseline_params,
        shoreline_change_params,
    ):
        super().__init__("Getting transects intersections", QgsTask.CanCancel)
        self.transects = transects
        self.shorelines = shorelines
        self.shorelines_params = shorelines_params
        self.transects_params = transects_params
        self.baseline_params = baseline_params
        self.shoreline_change_params = shoreline_change_params

        self.execution_time = ""
        self.transects_intersects = []

        self.exception = None

    def run(self):
        QgsMessageLog.logMessage(
            message=f"Started task: <b>{self.description()}</b>.",
            level=Qgis.Info,
        )

        try:
            start_time = time.perf_counter()
            intersect_id = 1

            for ti, transect in enumerate(self.transects):
                if self.isCanceled():
                    return False

                skip_transect = False

                # List of intersections per one transect
                individual_transect_intersects = []

                transect_origin = QgsGeometry.fromPointXY(
                    QgsPointXY(transect.vertexAt(0))
                )
                # Loop through individual shoreline MultiLineString features
                for si, shoreline in enumerate(self.shorelines):
                    # Used to store multiple intersections at one shoreline
                    # Because a unique shoreline for a single can consists
                    # # segments
                    individual_shoreline_intersects = {}

                    # Used to track intersections' distance from transect
                    # origin
                    intersections = {}

                    # Check intersections per segments
                    for segment in shoreline["geoms"]:
                        intersect = transect.intersection(segment)

                        if not intersect.isEmpty():
                            if intersect.wkbType() == QgsWkbTypes.MultiPoint:
                                for i in intersect.asMultiPoint():
                                    i = QgsGeometry.fromPointXY(i)
                                    intersections[i] = i.distance(transect_origin)
                            else:
                                intersections[intersect] = intersect.distance(
                                    transect_origin
                                )

                    if intersections:
                        if self.shoreline_change_params["is_choose_by_distance"]:
                            if self.shoreline_change_params[
                                "is_choose_by_distance_farthest"
                            ]:
                                final_intersect = max(
                                    intersections, key=intersections.get
                                )
                            elif self.shoreline_change_params[
                                "is_choose_by_distance_closest"
                            ]:
                                final_intersect = min(
                                    intersections, key=intersections.get
                                )
                        elif self.shoreline_change_params["is_choose_by_placement"]:
                            if self.shoreline_change_params[
                                "is_choose_by_placement_seaward"
                            ]:
                                if self.baseline_params["is_baseline_placement_sea"]:
                                    final_intersect = min(
                                        intersections, key=intersections.get
                                    )
                                elif self.baseline_params["is_baseline_placement_land"]:
                                    final_intersect = max(
                                        intersections, key=intersections.get
                                    )
                            elif self.shoreline_change_params[
                                "is_choose_by_placement_landward"
                            ]:
                                if self.baseline_params["is_baseline_placement_sea"]:
                                    final_intersect = max(
                                        intersections, key=intersections.get
                                    )
                                elif self.baseline_params["is_baseline_placement_land"]:
                                    final_intersect = min(
                                        intersections, key=intersections.get
                                    )

                        # Keep track of "fullest" intersection regardless
                        # of chosen transect-shoreline intersections
                        if self.baseline_params["is_baseline_placement_sea"]:
                            final_fullest_intersect = min(
                                intersections, key=intersections.get
                            )
                        elif self.baseline_params["is_baseline_placement_land"]:
                            final_fullest_intersect = min(
                                intersections, key=intersections.get
                            )

                        # individual_shoreline_intersects['fullest_intersect_x']
                        # individual_shoreline_intersects['fullest_intersect_y']

                        individual_shoreline_intersects["transect_origin"] = (
                            transect_origin  # .asWkt() # so we can pickle
                        )
                        individual_shoreline_intersects["geom"] = (
                            final_intersect  # .asWkt() # so we can pickle (adding intersection points layer)
                        )
                        individual_shoreline_intersects["id"] = intersect_id
                        individual_shoreline_intersects["transect_id"] = ti + 1
                        individual_shoreline_intersects["shoreline_id"] = si + 1
                        individual_shoreline_intersects["shoreline_year"] = shoreline[
                            "year"
                        ]
                        individual_shoreline_intersects["shoreline_unc"] = shoreline[
                            "unc"
                        ]

                        # DSAS way
                        # They apply negatives if baseline is placed on sea
                        # This is the value passed to the stat calculations
                        if self.baseline_params["is_baseline_placement_sea"]:
                            individual_shoreline_intersects[
                                "distance"
                            ] = -intersections[final_intersect]
                        else:
                            individual_shoreline_intersects["distance"] = intersections[
                                final_intersect
                            ]

                        individual_shoreline_intersects["intersect_x"] = float(
                            (final_intersect.asPoint().x())
                        )
                        individual_shoreline_intersects["intersect_y"] = float(
                            (final_intersect.asPoint().y())
                        )

                        # TODO: store only one time
                        individual_shoreline_intersects["orig_transect_geom"] = transect

                        individual_transect_intersects.append(
                            individual_shoreline_intersects
                        )

                        intersect_id += 1

                    # No intersections means this transect is not intersecting
                    # all shorelines, so it must be skipped
                    else:
                        skip_transect = True
                        break

                if skip_transect:
                    self.setProgress((ti / len(self.transects)) * 100)
                    continue
                else:
                    self.transects_intersects.append(individual_transect_intersects)
                    self.setProgress((ti / len(self.transects)) * 100)

            end_time = time.perf_counter()
            elapsed_time = (end_time - start_time) * 1000
            self.execution_time = f"{elapsed_time:.2f} ms"
            # self.execution_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
            return True

        except Exception as e:
            self.exception = e
            return False

    def finished(self, result):
        if self.isCanceled():
            QgsMessageLog.logMessage(
                message=f"Canceled task: <b>{self.description()}</b>.",
                level=Qgis.Warning,
            )
            return

        elif not result:
            QMessageBox.critical(
                iface.mainWindow(),
                f"Task error: : <b>{self.description()}</b>.",
                f"The following error occurred:\n{self.exception.__class__.__name__}: {self.exception}",
            )
            return

        QgsMessageLog.logMessage(
            message=f"Success task: <b>{self.description()}</b> in {self.execution_time}.",
            level=Qgis.Success,
        )
