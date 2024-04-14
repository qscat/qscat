# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import json
import math
import numpy as np
import time

from qscat.lib.xalglib import invstudenttdistribution

from PyQt5.QtCore import QVariant
from qgis.core import Qgis
from qgis.core import QgsGeometry
from qgis.core import QgsPointXY
from qgis.core import QgsApplication
from qgis.core import QgsMessageLog
from qgis.core import QgsPointXY
from qgis.core import QgsTask
from qgis.core import QgsWkbTypes

from qgis.utils import iface
from qgis.PyQt.QtWidgets import QMessageBox

from qscat.core.layers import create_add_layer
from qscat.core.messages import display_message
from qscat.core.utils.date import convert_to_decimal_year
from qscat.core.utils.input import get_epr_unc_from_input
from qscat.core.utils.input import get_highest_unc_from_input
from qscat.core.utils.input import get_baseline_input_params
from qscat.core.utils.input import get_shoreline_change_input_params
from qscat.core.utils.input import get_shorelines_input_params
from qscat.core.utils.input import get_transects_input_params
from qscat.core.layers import load_shorelines

TREND_STABLE = "stable"
TREND_ACCRETION = "accretion"
TREND_EROSION = "erosion"
STAT_EPR = "EPR"
STAT_SCE = "SCE"
STAT_NSM = "NSM"
STAT_LRR = "LRR"
STAT_LR2 = "LR2"
STAT_LSE = "LSE"
STAT_LCI = "LCI"
STAT_WLR = "WLR"
STAT_WR2 = "WR2"
STAT_WCI = "WCI"
STAT_WSE = "WSE"

from qscat.core.utils.plugin import get_project_dir
from qscat.core.intersects import load_list_years_intersections
from qscat.core.utils.input import get_shoreline_change_stat_selected
from qscat.core.utils.date import datetime_now
# from qscat.core.utils.input import filter_years_intersections_by_range
# from qscat.core.utils.input import filter_uncs_by_range
from qscat.core.layers import load_transects
from qscat.core.summary_reports import create_summary_shoreline_change
from qscat.core.utils.input import get_shorelines_years_uncs_from_input

class GetTransectsIntersectionsTask(QgsTask):
    def __init__(
        self,
        transects,
        shorelines,
        shorelines_params,
        transects_params,
        baseline_params,
        shoreline_change_params,
        qmlcb_stats_transects_layer
    ):
        super().__init__("Getting transects intersections", QgsTask.CanCancel)
        self.transects = transects
        self.shorelines = shorelines
        self.shorelines_params = shorelines_params
        self.transects_params = transects_params
        self.baseline_params = baseline_params
        self.shoreline_change_params = shoreline_change_params
        self.qmlcb_stats_transects_layer = qmlcb_stats_transects_layer

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
                    for segment in shoreline['geoms']:
                        intersect = transect.intersection(segment)
                        
                        if not intersect.isEmpty():
                            if intersect.wkbType() == QgsWkbTypes.MultiPoint:
                                for i in intersect.asMultiPoint():
                                    i = QgsGeometry.fromPointXY(i)
                                    intersections[i] = i.distance(transect_origin) 
                            else:
                                intersections[intersect] = intersect.distance(transect_origin)

                    if intersections:
                        if self.shoreline_change_params['is_choose_by_distance']:
                            if self.shoreline_change_params['is_choose_by_distance_farthest']:
                                final_intersect = max(intersections, key=intersections.get)
                            elif self.shoreline_change_params['is_choose_by_distance_closest']:
                                final_intersect = min(intersections, key=intersections.get)
                        elif self.shoreline_change_params['is_choose_by_placement']:
                            if self.shoreline_change_params['is_choose_by_placement_seaward']:
                                if self.baseline_params['is_baseline_placement_sea']:
                                    final_intersect = min(intersections, key=intersections.get)
                                elif self.baseline_params['is_baseline_placement_land']:
                                    final_intersect = max(intersections, key=intersections.get)
                            elif self.shoreline_change_params['is_choose_by_placement_landward']:
                                if self.baseline_params['is_baseline_placement_sea']:
                                    final_intersect = max(intersections, key=intersections.get)
                                elif self.baseline_params['is_baseline_placement_land']:
                                    final_intersect = min(intersections, key=intersections.get)
                        
                        # Keep track of "fullest" intersection regardless
                        # of chosen transect-shoreline intersections
                        if self.baseline_params['is_baseline_placement_sea']:
                            final_fullest_intersect = min(intersections, key=intersections.get)
                        elif self.baseline_params['is_baseline_placement_land']:
                            final_fullest_intersect = min(intersections, key=intersections.get)

                        # individual_shoreline_intersects['fullest_intersect_x']
                        # individual_shoreline_intersects['fullest_intersect_y']

                        individual_shoreline_intersects['transect_origin'] = transect_origin #.asWkt() # so we can pickle
                        individual_shoreline_intersects['geom'] = final_intersect #.asWkt() # so we can pickle (adding intersection points layer)
                        individual_shoreline_intersects['id'] = intersect_id
                        individual_shoreline_intersects['transect_id'] = ti+1
                        individual_shoreline_intersects['shoreline_id'] =  si+1
                        individual_shoreline_intersects['shoreline_year'] = shoreline['year']
                        individual_shoreline_intersects['shoreline_unc'] = shoreline['unc']
                        
                        # DSAS way
                        # They apply negatives if baseline is placed on sea
                        # This is the value passed to the stat calculations
                        if self.baseline_params['is_baseline_placement_sea']:
                            individual_shoreline_intersects['distance'] = -intersections[final_intersect]
                        else:
                            individual_shoreline_intersects['distance'] = intersections[final_intersect]

                        individual_shoreline_intersects['intersect_x'] = float((final_intersect.asPoint().x()))
                        individual_shoreline_intersects['intersect_y'] = float((final_intersect.asPoint().y()))
                        
                        # TODO: store only one time
                        individual_shoreline_intersects['orig_transect_geom'] = transect

                        individual_transect_intersects.append(individual_shoreline_intersects)

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
            #self.execution_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
            print(f"Intersection: {elapsed_time:.2f} ms")
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
        # TODO: caching


def get_transects_intersections_task_state_changed(
    self,
    selected_stats,
    user_params
):
    task = globals()['get_transects_intersections_task']

    if task.status() == QgsTask.Complete:
        list_years_intersections = load_list_years_intersections(task.transects_intersects)

        # Init for storing fields and values for one QgsVectorLayer combined stats
        all_fields = []  # refers to attribute fields to be added
        all_values = []  # refers to attribute values to be added    
        # For summary results, refers to distance and rate values

        # E.g. excludes trends, years, unc details
        stat_values = {}

        # COMPUTE SELECTED STATS
        for stat_name in selected_stats:
            if compute_shoreline_change_stat_pre_checks(self, stat_name):
                result = compute_single_stat_list_transects(
                    stat_name, 
                    list_years_intersections, 
                    user_params,
                )
                all_fields += result['fields']
                all_values = combine_result_values(all_values, result['values'])
                add_shoreline_change_stat_layer(stat_name, result, user_params)

                # For summary result
                # Transpose the list first since values are placed vertically,
                # then only get the first list element where these are the values
                # on each stat based on the fields @compute_shoreline_change_single_stat()
                stat_values[stat_name] = transpose_list(result['values'])[0]
                # [0] consider just the first column value (e.g. SCE, exluding the
                # years, trends, unc details)


        # All stats in one layer
        current_datetime = datetime_now()
        transects = load_transects(self.dockwidget.qmlcb_stats_transects_layer.currentLayer())
        create_add_layer(
            geometry='LineString', 
            geometries=transects,
            name='ALL',
            fields=all_fields,
            values=all_values,
            datetime=current_datetime,
        )

        # Summary
        summary = {}
        
        # General
        summary['datetime'] = current_datetime
        summary['num_of_transects'] = len(transects)

        # Results
        if 'SCE' in selected_stats:
            SCE = stat_values['SCE']
            summary['SCE_avg'] = round(sum(SCE) / len(SCE), 2)
            summary['SCE_max'] = round(max(SCE), 2)
            summary['SCE_min'] = round(min(SCE), 2)

        if 'NSM' in selected_stats:
            NSM = stat_values['NSM']
            unc = get_highest_unc_from_input(self)
            summary['NSM_avg'] = round(sum(NSM) / len(NSM), 2)
            
            NSM_e = [x for x in NSM if x < -unc]
            erosion_count = len(NSM_e)
            summary['NSM_erosion_num_of_transects'] = erosion_count
            summary['NSM_erosion_pct_transects'] = f'{(erosion_count / len(NSM)) * 100:.2f} %'
            summary['NSM_erosion_avg'] = round(sum(NSM_e) / len(NSM_e), 2)
            summary['NSM_erosion_max'] = round(max(NSM_e), 2)
            summary['NSM_erosion_min'] = round(min(NSM_e), 2)

            NSM_a = [x for x in NSM if x > unc]
            accretion_count = len(NSM_a)
            summary['NSM_accretion_num_of_transects'] = accretion_count
            summary['NSM_accretion_pct_transects'] = f'{(accretion_count / len(NSM)) * 100:.2f} %'
            summary['NSM_accretion_avg'] = round(sum(NSM_a) / len(NSM_a), 2)
            summary['NSM_accretion_max'] = round(max(NSM_a), 2)
            summary['NSM_accretion_min'] = round(min(NSM_a), 2)

            NSM_s = [x for x in NSM if x >= -unc and x <= unc]
            stable_count = len(NSM_s)
            summary['NSM_stable_num_of_transects'] = stable_count
            summary['NSM_stable_pct_transects'] = f'{(stable_count / len(NSM)) * 100:.2f} %'
            summary['NSM_stable_avg'] = round(sum(NSM_s) / len(NSM_s), 2)
            summary['NSM_stable_max'] = round(max(NSM_s), 2)
            summary['NSM_stable_min'] = round(min(NSM_s), 2)

        if 'EPR' in selected_stats:
            EPR = stat_values['EPR']
            unc = get_epr_unc_from_input(self)
            summary['EPR_avg'] = round(sum(EPR) / len(EPR), 2)
            
            EPR_e = [x for x in EPR if x < -unc]
            erosion_count = len(EPR_e)
            summary['EPR_erosion_num_of_transects'] = erosion_count
            summary['EPR_erosion_pct_transects'] = f'{(erosion_count / len(EPR)) * 100:.2f} %'
            summary['EPR_erosion_avg'] = round(sum(EPR_e) / len(EPR_e), 2)
            summary['EPR_erosion_max'] = round(max(EPR_e), 2)
            summary['EPR_erosion_min'] = round(min(EPR_e), 2)

            EPR_a = [x for x in EPR if x > unc]
            accretion_count = len(EPR_a)
            summary['EPR_accretion_num_of_transects'] = accretion_count
            summary['EPR_accretion_pct_transects'] = f'{(accretion_count / len(EPR)) * 100:.2f} %'
            summary['EPR_accretion_avg'] = round(sum(EPR_a) / len(EPR_a), 2)
            summary['EPR_accretion_max'] = round(max(EPR_a), 2)
            summary['EPR_accretion_min'] = round(min(EPR_a), 2)

            EPR_s = [x for x in EPR if x >= -unc and x <= unc]
            stable_count = len(EPR_s)
            summary['EPR_stable_num_of_transects'] = stable_count
            summary['EPR_stable_pct_transects'] = f'{(stable_count / len(EPR)) * 100:.2f} %'
            summary['EPR_stable_avg'] = round(sum(EPR_s) / len(EPR_s), 2)
            summary['EPR_stable_max'] = round(max(EPR_s), 2)
            summary['EPR_stable_min'] = round(min(EPR_s), 2)

        if 'LRR' in selected_stats:
            LRR = stat_values['LRR']
            summary['LRR_avg'] = round(sum(LRR) / len(LRR), 2)
            
            LRR_e = [x for x in LRR if x < 0]
            erosion_count = len(LRR_e)
            summary['LRR_erosion_num_of_transects'] = erosion_count
            summary['LRR_erosion_pct_transects'] = f'{(erosion_count / len(LRR)) * 100:.2f} %'
            summary['LRR_erosion_avg'] = round(sum(LRR_e) / len(LRR_e), 2)
            summary['LRR_erosion_max'] = round(max(LRR_e), 2)
            summary['LRR_erosion_min'] = round(min(LRR_e), 2)

            LRR_a = [x for x in LRR if x >= 0]
            accretion_count = len(LRR_a)
            summary['LRR_accretion_num_of_transects'] = accretion_count
            summary['LRR_accretion_pct_transects'] = f'{(accretion_count / len(LRR)) * 100:.2f} %'
            summary['LRR_accretion_avg'] = round(sum(LRR_a) / len(LRR_a), 2)
            summary['LRR_accretion_max'] = round(max(LRR_a), 2)
            summary['LRR_accretion_min'] = round(min(LRR_a), 2)

        if 'WLR' in selected_stats:
            WLR = stat_values['WLR']
            summary['WLR_avg'] = round(sum(WLR) / len(WLR), 2)
            
            WLR_e = [x for x in WLR if x < 0]
            erosion_count = len(WLR_e)
            summary['WLR_erosion_num_of_transects'] = erosion_count
            summary['WLR_erosion_pct_transects'] = f'{(erosion_count / len(WLR)) * 100:.2f} %'
            summary['WLR_erosion_avg'] = round(sum(WLR_e) / len(WLR_e), 2)
            summary['WLR_erosion_max'] = round(max(WLR_e), 2)
            summary['WLR_erosion_min'] = round(min(WLR_e), 2)

            WLR_a = [x for x in WLR if x >= 0]
            accretion_count = len(WLR_a)
            summary['WLR_accretion_num_of_transects'] = accretion_count
            summary['WLR_accretion_pct_transects'] = f'{(accretion_count / len(WLR)) * 100:.2f} %'
            summary['WLR_accretion_avg'] = round(sum(WLR_a) / len(WLR_a), 2)
            summary['WLR_accretion_max'] = round(max(WLR_a), 2)
            summary['WLR_accretion_min'] = round(min(WLR_a), 2)

        create_summary_shoreline_change(self, summary)

    
def compute_shoreline_change_stats(self):
    baseline_params = get_baseline_input_params(self)
    shorelines_params = get_shorelines_input_params(self)
    transects_params = get_transects_input_params(self)
    shoreline_change_params = get_shoreline_change_input_params(self)

    start_time = time.perf_counter()
    selected_stats = get_shoreline_change_stat_selected(self)

    user_params = {
        'confidence_interval': float(
            self.dockwidget.qdsb_stats_confidence_interval.text()),
        'oldest_year': convert_to_decimal_year(
            self.dockwidget.cb_shoreline_change_oldest_date.currentText()),
        'newest_year': convert_to_decimal_year(
            self.dockwidget.cb_shoreline_change_newest_date.currentText()),
        'oldest_date': self.dockwidget.cb_shoreline_change_oldest_date.currentText(),
        'newest_date': self.dockwidget.cb_shoreline_change_newest_date.currentText(),
        'epr_unc': get_epr_unc_from_input(self),
        'highest_unc': get_highest_unc_from_input(self),
        'years_uncs': get_shorelines_years_uncs_from_input(self),
        'clip_transects' : self.dockwidget.cb_stats_clip_transects.isChecked(),
    }

    # TODO: Remove, not needed
    # Filter uncertainty by year range
    # Used for filtering LRR and WLR
    # user_params['years_uncs'] = filter_uncs_by_range(
    #     user_params['years_uncs'],
    #     user_params['newest_year'],
    #     user_params['oldest_year'],
    # )

    transects = load_transects(self.dockwidget.qmlcb_stats_transects_layer.currentLayer())
    shorelines = load_shorelines(shorelines_params)
    
    globals()['get_transects_intersections_task'] = GetTransectsIntersectionsTask(
        transects,
        shorelines,
        shorelines_params,
        transects_params,
        baseline_params,
        shoreline_change_params,
        self.dockwidget.qmlcb_stats_transects_layer,
    )
    globals()['get_transects_intersections_task'].taskCompleted.connect(
        lambda: get_transects_intersections_task_state_changed(
            self, 
            selected_stats, 
            user_params,
        )
    )
    QgsApplication.taskManager().addTask(globals()['get_transects_intersections_task'])

    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000
    print(f"Shoreline change: {elapsed_time:.2f} ms")


def compute_single_stat_list_transects(
    stat_name,
    list_years_intersections,
    user_params
):
    # Setup fields
    fields = {
        'SCE': [
            {'name': 'SCE', 'type': QVariant.Double},
            {'name': 'SCE_highest_unc', 'type': QVariant.Double},
            {'name': 'SCE_trend', 'type': QVariant.String},
            {'name': 'SCE_closest_year', 'type': QVariant.Int},
            {'name': 'SCE_farthest_year', 'type': QVariant.Int},
        ],
        'NSM': [
            {'name': 'NSM', 'type': QVariant.Double},
            {'name': 'NSM_highest_unc', 'type': QVariant.Double},
            {'name': 'NSM_trend', 'type': QVariant.String},
            {'name': 'NSM_full_transect_point1_x', 'type': QVariant.Double},
            {'name': 'NSM_full_transect_point1_y', 'type': QVariant.Double},
            {'name': 'NSM_full_transect_point2_x', 'type': QVariant.Double},
            {'name': 'NSM_full_transect_point2_y', 'type': QVariant.Double},
        ],
        'EPR': [
            {'name': 'EPR', 'type': QVariant.Double},
            {'name': 'EPR_unc', 'type': QVariant.Double},
            {'name': 'EPR_trend', 'type': QVariant.String},
        ],
        'LRR': [
            {'name': 'LRR', 'type': QVariant.Double},
            {'name': 'LR2', 'type': QVariant.Double},
            {'name': 'LSE', 'type': QVariant.Double},
            {'name': 'LCI', 'type': QVariant.Double},
        ],
        'WLR': [
            {'name': 'WLR', 'type': QVariant.Double},
            {'name': 'WR2', 'type': QVariant.Double},
            {'name': 'WSE', 'type': QVariant.Double},
            {'name': 'WCI', 'type': QVariant.Double},
        ]
    }
    values = []
    clipped_transect_geoms = []
    
    for years_intersections in list_years_intersections:
        # Filter years intersections first by user params oldest year and newest year
        
        # TODO: remove me, not needed
        # years_intersections = filter_years_intersections_by_range(
        #     years_intersections,
        #     user_params['newest_year'],
        #     user_params['oldest_year'],
        # )
        value, clipped_transect_geom = compute_single_stat_single_transects(
            stat_name,
            years_intersections, 
            user_params,
        )
        values.append(value)
        clipped_transect_geoms.append(clipped_transect_geom)

    result =  {
        'fields': fields[stat_name], 
        'values': values, 
        'clipped_transect_geoms': clipped_transect_geoms
    }
    return result


def compute_single_stat_single_transects(
    stat_name,
    years_intersections,
    user_params
):
    """Compute a specific statistic value for a single transect.
    
    Args:
        stat_name (str): Statistic name (e.g. EPR, SCE, NSM, LRR, LR2, WLR, WR2).
        years_intersections (dict): Dictionary of year intersections

    Return:
        tuple: Tuple of statistic value and clipped transect geometry.
    """

    # validate if higher unc matches the current years intersections


    # validate if epr unc matches the current years intersections


    # validate if user params oldest_year and newest year are in years_intersections
    stat_map = {
        STAT_SCE: {
            "get_year1": get_closest_distance_year,
            "get_year2": get_farthest_distance_year,
            "get_main_values": [get_SCE],
            "get_trend_ref": user_params['highest_unc'],
            "get_extra_values": [
                get_closest_distance_year,
                get_farthest_distance_year,
            ],
        },
        STAT_NSM: {
            "get_year1": get_oldest_year,
            "get_year2": get_newest_year,
            "get_main_values": [get_NSM],
            "get_trend_ref": user_params['highest_unc'],
            "get_extra_values": [
                get_fullest_transect_point1_x,
                get_fullest_transect_point1_y,
                get_fullest_transect_point2_x,
                get_fullest_transect_point2_y,
                get_fullest_transect_trend,
            ],
        },
        STAT_EPR: {
            "get_year1": get_oldest_year,
            "get_year2": get_newest_year,
            "get_main_values": [get_EPR],
            "get_trend_ref": user_params['epr_unc'],
            "get_extra_values": None,
        },
        STAT_LRR: {
            "get_year1": get_closest_distance_year,
            "get_year2": get_farthest_distance_year,
            "get_main_values": [get_LRR, get_LR2, get_LSE, get_LCI],
            "get_trend_ref": None,
            "get_extra_values": None,
        },
        STAT_WLR: {
            "get_year1": get_closest_distance_year,
            "get_year2": get_farthest_distance_year,
            "get_main_values": [get_WLR, get_WR2, get_WSE, get_WCI],
            "get_trend_ref": None,
            "get_extra_values": None,
        },
    }
    
    year1 = stat_map[stat_name]["get_year1"](years_intersections, user_params)
    year2 = stat_map[stat_name]["get_year2"](years_intersections, user_params)

    distance1 = years_intersections[year1]['distance']
    distance2 = years_intersections[year2]['distance']
    
    # Get main stat values
    compute_params = {
        "year1": year1,
        "year2": year2,
        "distance1": distance1,
        "distance2": distance2,
        "years_intersections": years_intersections, # Dictionary
        "user_params": user_params, # Dictionary
    }
    single_transect_values = []

    # Get main value functions (e.g. SCE, LRR, LR2 etc.)
    main_values_functions = stat_map[stat_name]["get_main_values"]
    for mvf in main_values_functions:
        single_transect_values.append(mvf(compute_params))

    # Are there trends?
    trend_reference = stat_map[stat_name]["get_trend_ref"]
    if trend_reference:
        # Append the unc value (e.g. SCE_highest_unc, NSM_highest_unc, EPR_unc)
        single_transect_values.append(trend_reference)

        # Get change trend (e.g. stable, accretion, erosion)
        stat_value_trend = get_change_trend(
            single_transect_values[0], 
            trend_reference
        )
        
        # Append the trend string (e.g. SCE_trend, NSM_trend, EPR_trend)
        single_transect_values.append(stat_value_trend)

    # Are there extra values?
    extra_values_functions = stat_map[stat_name]["get_extra_values"]
    if extra_values_functions:
        for evf in extra_values_functions:
            single_transect_values.append(
                evf(years_intersections, user_params)
            )

    if user_params['clip_transects']:
        start_pt = QgsPointXY(years_intersections[year1]['intersect_x'], 
                            years_intersections[year1]['intersect_y'])
        end_pt = QgsPointXY(years_intersections[year2]['intersect_x'], 
                            years_intersections[year2]['intersect_y'])
        transect_geom = QgsGeometry.fromPolylineXY([start_pt, end_pt])
    else:
        transect_geom = years_intersections[year1]['orig_transect_geom']

    # modify SCE_values as absolute
    # TODO: simplify code
    if stat_name == STAT_SCE:
        values_temp = []
        for vi, v in enumerate(single_transect_values):
            if vi == 0:
                values_temp.append(abs(v))
            else:
                values_temp.append(v)
        single_transect_values = values_temp

    return single_transect_values, transect_geom


# GET VALUES FUNCTIONS
def get_SCE(compute_params):
    SCE_value = compute_SCE(
        compute_params['distance1'],
        compute_params['distance2']
    )
    return round(SCE_value, 2)


def get_NSM(compute_params):
    NSM_value = compute_NSM(
        compute_params['distance1'], 
        compute_params['distance2']
    )
    return round(NSM_value, 2)


def get_EPR(compute_params):
    NSM_value = compute_NSM(
        compute_params['distance1'], 
        compute_params['distance2']
    )
    EPR_value = compute_EPR(
        NSM_value, 
        compute_params['year1'], 
        compute_params['year2']
    )
    return round(EPR_value, 2)


def get_EPR_unc(compute_params):
    pass

"""
def get_EPR_unc(compute_params):
    oldest_year_unc = compute_params['years_intersections'][compute_params['year1']]['unc']
    newest_year_unc = compute_params['years_intersections'][compute_params['year2']]['unc']
    oldest_year = compute_params['year1']
    newest_year = compute_params['year2']
    EPR_unc_value = compute_EPR_unc(newest_year_unc, oldest_year_unc, newest_year, oldest_year)
    return round(EPR_unc_value, 2)
"""

def get_LRR(compute_params):
    years, distances = get_sorted_years_distances(
        compute_params['years_intersections']
    )
    LRR_value = compute_LRR(years, distances)
    return round(LRR_value, 2)


def get_LR2(compute_params):
    years, distances = get_sorted_years_distances(
        compute_params['years_intersections']
    )
    LR2_value = compute_LR2(years, distances)
    return round(LR2_value, 2)


def get_LSE(compute_params):
    years, distances = get_sorted_years_distances(
        compute_params['years_intersections']
    )
    LSE_value = compute_LSE(years, distances)
    return round(LSE_value, 2)


def get_LCI(compute_params):
    years, distances = get_sorted_years_distances(
        compute_params['years_intersections']
    )
    LCI_value = compute_LCI(
        years,
        distances,
        compute_params['user_params']['confidence_interval'])
    return round(LCI_value, 2)


def get_WLR(compute_params):
    # validate if dict key years in years_intersections and uncs are existing in both dict

    years, distances = get_sorted_years_distances(
        compute_params['years_intersections']
    )
    uncs = get_sorted_uncs(compute_params['user_params']['years_uncs'])
    WLR_value = compute_WLR(years, distances, uncs)
    return round(WLR_value, 2)


def get_WR2(compute_params):
    # validate if dict key years in years_intersections and uncs are existing in both dict
    years, distances = get_sorted_years_distances(
        compute_params['years_intersections']
    )
    uncs = get_sorted_uncs(compute_params['user_params']['years_uncs'])
    WR2_value = compute_WR2(years, distances, uncs)
    return round(WR2_value, 2)


def get_WSE(compute_params):
    years, distances = get_sorted_years_distances(
        compute_params['years_intersections']
    )
    uncs = get_sorted_uncs(compute_params['user_params']['years_uncs'])
    WSE_value = compute_WSE(years, distances, uncs)
    return round(WSE_value, 2)


def get_WCI(compute_params):
    years, distances = get_sorted_years_distances(
        compute_params['years_intersections']
    )
    uncs = get_sorted_uncs(compute_params['user_params']['years_uncs'])
    WCI_value = compute_WCI(
        years,
        distances,
        uncs,
        compute_params['user_params']['confidence_interval'])
    return round(WCI_value, 2)


# COMPUTATION FUNCTIONS
def subtract_two_distances(distance1, distance2):
    """Subtract two distance values. Used for SCE and NSM.
    
    Args:
        distance1 (float)
        distance2 (float)

    Returns:
        float: Difference of distance2 and distance1.
    
    Raises:
        TypeError: If distance 1 and 2 values are None.
        TypeError: If distance 1 and 2 values are not floats.
    """
    if distance1 is None:
      raise TypeError("Distance 1 value cannot be None.") 
    if distance2 is None:
         raise TypeError("Distance 2 value cannot be None.")

    if not isinstance(distance1, float):
        raise TypeError("Distance 1 value must be float.")
    if not isinstance(distance2, float):
        raise TypeError("Distance 2 value must be float.")
    
    return distance2 - distance1


def compute_SCE(closest_distance, farthest_distance):
    """Compute Shoreline Change Envelope (SCE) value.

    Args:
        closest_distance (float): Distance value 1.
        farthest_distance (float): Distance value 2.

    Returns:
        float: SCE value.
    """
    # TODO: validate closest distance always < farthest distance
    SCE_value = subtract_two_distances(closest_distance, farthest_distance)
    return SCE_value


def compute_NSM(distance1, distance2):
    """Compute Net Shoreline Movement (NSM) value.

    Args:
        distance1 (float): Distance value 1.
        distance2 (float): Distance value 2.

    Returns:
        float: NSM value.
    """
    NSM_value = subtract_two_distances(distance1, distance2)
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
    """Compute End Point Rate (EPR) uncertainty value.

    """
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

    EPR_unc_numerator = (newest_year_unc**2 + oldest_year_unc**2)
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
        TypeError: If year or distance values are not numpy floats.
        ValueError: If year and distance values are not the same length.
        ValueError: If year and distance values have less than 3 elements.
        ValueError: If year values are not in ascending order.
    """
    if years is None:
        raise TypeError("Year values cannot be None.")
    if distances is None:
        raise TypeError("Distance values cannot be None.")

    if not isinstance(years, np.ndarray) or years.dtype != np.float64:
        raise TypeError("Year values must be numpy floats.")
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
    ss_res = np.sum((distances - pred)**2)
    y_mean = np.mean(distances)
    ss_tot = np.sum((distances - y_mean)**2)
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
    ss_res = np.sum((distances - (slope * years + intercept))**2)
    n = len(years)
    standard_error = np.sqrt(ss_res / (n - 2))
    LSE_value = float(standard_error)  # previously numpy
    return LSE_value


def compute_LCI(years, distances, conf=99.7):
    x_mean = np.mean(years)
    sum_sq_diff = np.sum((years - x_mean)**2)
    standard_error = compute_LSE(years, distances)
    standard_error_slope = np.sqrt(standard_error**2 / sum_sq_diff)

    alpha =  1 - (float(conf)*.01)
    n = len(years)
    t_value = invstudenttdistribution(n-2, 1-alpha/2)
    ci = t_value * standard_error_slope
    LCI_value = float(ci)
    #print("LCI", ci)
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
        raise ValueError("Year, distance, and uncertainties arrays must have the same length.")

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
    
    #uncertainties = np.array([1/float(u**2) for u in uncertainties])
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
    uncertainties = np.array([1/float(u**2) for u in uncertainties])
    slope, _, = compute_weighted_least_square_fit(years, distances, uncertainties)
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
    uncertainties = np.array([1/float(u**2) for u in uncertainties])
    slope, intercept = compute_weighted_least_square_fit(years, distances, uncertainties)
    pred = slope * years + intercept
    residuals = distances - pred
    rss = np.sum(uncertainties * residuals**2)
    wmean_y = np.average(distances, weights=uncertainties)
    tss = np.sum(uncertainties * (distances - wmean_y)**2)
    r2 = 1 - rss / tss
    WR2_value = float(r2)  # previously numpy
    return WR2_value


def compute_WSE(years, distances, uncertainties):
    uncertainties = np.array([1/float(u**2) for u in uncertainties])
    slope, intercept = compute_weighted_least_square_fit(years, distances, uncertainties)
    
    pred = slope * years + intercept
    residuals = distances - pred
    ss_res = np.sum(uncertainties * residuals ** 2)
    n = len(years)
    standard_error = np.sqrt(ss_res / (n - 2))
    WSE_value = float(standard_error)  # previously numpy
    return WSE_value


def compute_WCI(years, distances, uncertainties, conf=99.7):
    # we shouldn't pass unc=1/u^2 here
    # its already applied in compute_WSE
    standard_error = compute_WSE(years, distances, uncertainties) 

    uncs = np.array([1/float(u**2) for u in uncertainties])
    wmean_x = np.average(years, weights=uncs)
    sum_sq_diff = np.sum(uncs * (years - wmean_x)**2)

    standard_error_slope = np.sqrt(standard_error**2 / sum_sq_diff)

    alpha =  1 - (float(conf)*.01)
    n = len(years)
    t_value = invstudenttdistribution(n-2, 1-alpha/2)
    ci = t_value * standard_error_slope
    WCI_value = float(ci)
    return WCI_value


def validate_years_intersections(years_intersections):
    # validate if years_intersections is not None
    if years_intersections is None:
        raise TypeError("Years intersections cannot be None.")
    
    # validate if years_intersections is not empty
    if len(years_intersections) == 0:
        raise ValueError("Years intersections cannot be empty.")
    
    # validate if years_intersections is not dictionary
    if not isinstance(years_intersections, dict):
        raise TypeError("Years intersections must be dictionary.")
    
    # validate if keys are not float
    if not all(isinstance(k, float) for k in years_intersections.keys()):
        raise TypeError("Keys must be float.")
    
    # validate if values are not dictionary
    if not all(isinstance(v, dict) for v in years_intersections.values()):
        raise TypeError("Values must be dictionary.")


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
        return TREND_STABLE
    elif stat_value > unc_value:
        return TREND_ACCRETION
    elif stat_value < -unc_value:
        return TREND_EROSION


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
    validate_years_intersections(years_intersections)

    yi_sorted = sorted(years_intersections)
    years_intersections = {key:years_intersections[key] for key in yi_sorted}
    years = np.array([k for k in years_intersections.keys()])
    distances = np.array([v['distance'] for v in years_intersections.values()])
   
    return (years, distances)


def get_sorted_uncs(uncs):
    # SORT UNCS BASED ON YEAR?  
    uncs_sorted = sorted(uncs)
    uncs = {key:uncs[key] for key in uncs_sorted}
    uncs = np.array([v for v in uncs.values()])
    return uncs


def get_closest_distance_year(years_intersections, user_params):
    closest_distance_year = min(
        years_intersections.items(), key=lambda x: x[1]['distance'])[0]
    return closest_distance_year



def get_farthest_distance_year(years_intersections, user_params):
    farthest_distance_year = max(
        years_intersections.items(), key=lambda x: x[1]['distance'])[0]
    return farthest_distance_year


def get_fullest_transect_points(years_intersections):
    """Get fullest transect regardless of transect-shoreline intersections chosen.
    """
    min_distance = float('inf')
    max_distance = float('-inf')
    min_coordinates = None
    max_coordinates = None

    for _, value in years_intersections.items():
        if value['distance'] < min_distance:
            min_distance = value['distance']
            min_coordinates = (value['intersect_x'], value['intersect_y'])
        if value['distance'] > max_distance:
            max_distance = value['distance']
            max_coordinates = (value['intersect_x'], value['intersect_y'])

    return min_coordinates, max_coordinates


def get_fullest_transect_point1(years_intersections):
    min, _ = get_fullest_transect_points(years_intersections)
    return min


def get_fullest_transect_point1_x(years_intersections, user_params):
    x, _ = get_fullest_transect_point1(years_intersections)
    return x


def get_fullest_transect_point1_y(years_intersections, user_params):
    _, y = get_fullest_transect_point1(years_intersections)
    return y


def get_fullest_transect_point2(years_intersections):
    _, max = get_fullest_transect_points(years_intersections)
    return max


def get_fullest_transect_point2_x(years_intersections, user_params):
    x, _ = get_fullest_transect_point2(years_intersections)
    return x


def get_fullest_transect_point2_y(years_intersections, user_params):
    _, y = get_fullest_transect_point2(years_intersections)
    return y


def get_fullest_transect_trend(years_intersections, user_params):
    user_params['highest_unc']


def get_oldest_year(years_intersections, user_params):
    oldest_year = user_params['oldest_year']
    return oldest_year


def get_newest_year(years_intersections, user_params):
    newest_year = user_params['newest_year']
    return newest_year


def compute_shoreline_change_stat_pre_checks(self, stat):
    """Pre-checks for computation of any shoreline change stats.
    
    Args:
        self (QtDockWidget)
        stat (str): Stat name to check.

    Returns:
        boolean
    """
    shoreline_layer = self.dockwidget.qmlcb_shorelines_shorelines_layer.currentLayer()

    if stat in ('LRR', 'WLR'):
        if shoreline_layer.featureCount() < 3:
            display_message(
                'LRR and WLR requires atleast 3 shorelines.', 
                Qgis.Warning,
            )
            return False
    
    return True


def combine_result_values(existing_values, new_values):
    """Used for creating one layer statistics. Combine result values into
    existing result values. Includes condition, if existing_values is empty
    then just return the new_values.

    Example:
        existing_values = [[1, 2, 3],
                           [1, 2, 3]]

        new_values = [[4],
                      [4]]

        combined_values = [[1, 2, 3, 4],
                           [1, 2, 3, 4]]

    Args:
        existing_result_values (list)

    Returns:
        list
    """
    if existing_values:
        combined_values = []
        for ev, nv in zip(existing_values, new_values):
            combined_value = ev + nv
            combined_values.append(combined_value)
        return combined_values
    else:
        return new_values


def add_shoreline_change_stat_layer(stat, result, user_params):
    """ 
    Args:
        stat_acronym (str): statistic ACRONYM (SCE, NSM, LRR etc.)
        result (dict): 
    """
    # Layer names
    if stat in ('NSM', 'EPR'):
        name = f'{stat} ({user_params["newest_year"]}-{user_params["oldest_year"]})'
    elif stat in ('SCE', 'LRR', 'WLR'):
        name = f'{stat}'

    # Metadata dict
    dates = {
        'newest_date': user_params['newest_date'],
        'oldest_date': user_params['oldest_date'],
    }
    
    create_add_layer(
        geometry='LineString',
        geometries=result['clipped_transect_geoms'], 
        name=name,
        fields=result['fields'],
        values=result['values'],
        extra_values=dates,
    )


def transpose_list(old_list):
    return [list(x) for x in zip(*old_list)]