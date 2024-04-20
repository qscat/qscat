# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import os
import platform

from qgis.core import Qgis

from qscat.core.utils.input import get_baseline_input_params
from qscat.core.utils.input import get_project_settings_input_params
from qscat.core.utils.input import get_shorelines_input_params
from qscat.core.utils.input import get_shorelines_dates
from qscat.core.utils.input import get_shorelines_uncs
from qscat.core.utils.input import get_area_change_input_params
from qscat.core.utils.input import get_shoreline_change_input_params
from qscat.core.utils.input import get_transects_input_params
from qscat.core.utils.plugin import get_metadata_version
from qscat.core.utils.plugin import get_project_dir
from qscat.core.constants import Statistic

class ComputationType:
    SHORELINE_CHANGE = 0
    AREA_CHANGE = 1
    FORECASTING = 2


class SummaryReport:
    def __init__(self, qscat, summary=None):
        """Create a summary report for shoreline change, area change, and forecasting computations.
        
        Args:
            qscat (QscatPlugin): QscatPlugin instance.
            summary (dict): Summary of results.
        """
        self.qscat = qscat
        self.summary = summary


    def create(self, computation_type):
        """Create the base file that contains the general informations such as 
           project crs, author information, and sytem information.

        Args:
            computation_type (int): Computation type.

        Returns:
            f (io.TextIOWrapper): A file object opened in text mode.

        Example:
            ── shoreline_change/
            │   ├── qscat_0.1.0_shoreline_change_20240409-192203.txt
            │   ├── qscat_0.1.0_shoreline_change_20240410-080512.txt
            │   └── ...
            │
            ├── area_change/
            │   ├── qscat_0.1.0_area_change_20240409-192203.txt
            │   ├── qscat_0.1.0_area_change_20240410-080512.txt
            │   └── ...
            │
            └── forecasting/
                ├── qscat_0.1.0_forecasting_20240409-192203.txt
                ├── qscat_0.1.0_forecasting_20240410-080512.txt
                └── ...
        """
        base_dir = self.qscat.dockwidget.qfw_report_save_location.filePath()

        if computation_type == ComputationType.SHORELINE_CHANGE:
            summary_reports_dir = os.path.join(base_dir, 'shoreline_change')
            file_name = f"qscat_{get_metadata_version()}_shoreline_change_{self.summary['datetime']}.txt"
        elif computation_type == ComputationType.AREA_CHANGE:
            summary_reports_dir = os.path.join(base_dir, 'area_change')
            file_name = f"qscat_{get_metadata_version()}_area_change_{self.summary['datetime']}.txt"
        elif computation_type == ComputationType.FORECASTING:
            summary_reports_dir = os.path.join(base_dir, 'forecasting')
            file_name = f"qscat_{get_metadata_version()}_forecasting_{self.summary['datetime']}.txt"

        # Ensure the directory exists
        os.makedirs(summary_reports_dir, exist_ok=True)

        summary_report_file_path = os.path.join(summary_reports_dir, file_name)

        project = get_project_settings_input_params(self.qscat)
        f = open(summary_report_file_path, 'w', encoding='utf-8')
        f.write('[PROJECT DETAILS]\n')
        f.write('\n')
        f.write('GENERAL:\n')
        f.write(f'Time generated: {self.summary["datetime"]}\n')
        f.write(f'Project location: {get_project_dir()}\n')
        f.write('\n')
        f.write('PROJECTION:\n')
        f.write(f'CRS auth id: {project["crs_id"]}\n')
        f.write('\n')
        f.write('AUTHOR:\n')
        f.write(f'Full name: {project["author_full_name"]}\n')
        f.write(f'Affiliation: {project["author_affiliation"]}\n')
        f.write(f'Email: {project["author_email"]}\n')
        f.write('\n')
        f.write('[SYSTEM DETAILS]\n')
        f.write('\n')
        f.write(f'OS version: {platform.system()} {platform.release()}\n')
        f.write(f'QGIS version: {Qgis.QGIS_VERSION}\n')
        f.write(f'QSCAT version: {get_metadata_version()}\n')
        f.write('\n')

        return f


    def shoreline_change(self):
        """Create a summary report for shoreline change computation."""
        f = self.create(ComputationType.SHORELINE_CHANGE)

        shorelines = get_shorelines_input_params(self.qscat)
        baseline = get_baseline_input_params(self.qscat)
        transects = get_transects_input_params(self.qscat)
        shoreline_change = get_shoreline_change_input_params(self.qscat)

        uncs = ", ".join([f"{x:.2f}" for x in get_shorelines_uncs(self.qscat)])

        f.write('[INPUT PARAMETERS]\n')
        f.write('\n')
        f.write('SHORELINES TAB:\n')
        f.write(f'Layer: {shorelines["shorelines_layer"].name()}\n')
        f.write(f'Default data uncertainty: {shorelines["default_data_uncertainty"]}\n')
        f.write(f'Date field: {shorelines["date_field"]}\n')
        f.write(f'Uncertainty field: {shorelines["uncertainty_field"]}\n')
        f.write(f'Dates: {", ".join(get_shorelines_dates(self.qscat))}\n')
        f.write(f'Uncertainties: {uncs}\n')
        f.write('\n')

        if baseline["is_baseline_placement_sea"]:
            placement = "Sea or Offshore"
        elif baseline["is_baseline_placement_land"]:
            placement = "Land or Onshore"
        if baseline["is_baseline_orientation_land_right"]:
            orientation = "Land is to the RIGHT" 
        elif baseline["is_baseline_orientation_land_left"]:
            orientation = "Land is to the LEFT"

        f.write('BASELINE TAB:\n')
        f.write(f'Layer: {baseline["baseline_layer"].name()}\n')
        f.write(f'Placement: {placement}\n')
        f.write(f'Orientation: {orientation}\n')
        f.write('\n')
        f.write('TRANSECTS TAB:\n')
        f.write(f'Layer output name: {transects["layer_output_name"]}\n')

        if transects['is_by_transect_spacing']:
            f.write('Transect count: By transect spacing\n')
            f.write(f'Transect spacing: {transects["by_transect_spacing"]} meters\n')
        elif transects['is_by_number_of_transects']:
            f.write('Transect count: By number of transects\n')
            f.write(f'Number of transects: {transects["by_number_of_transects"]} transects\n')
        f.write(f'Transect length: {transects["length"]} meters\n')
        f.write(f'Smoothing distance: {transects["smoothing_distance"]} meters\n')

        f.write('\n')
        f.write('STATISTICS TAB:\n')
        f.write(f'Transect layer: {shoreline_change["transects_layer"].name()}\n')

        if shoreline_change["is_choose_by_distance"]:
            f.write('Intersection: Choose by distance\n')
            if shoreline_change["is_choose_by_distance_farthest"]:
                f.write('By distance: Farthest\n')
            elif shoreline_change["is_choose_by_distance_closest"]: 
                f.write('By distance: Closest\n')
        elif shoreline_change["is_choose_by_placement"]:
            f.write('Intersection: Choose by placement\n')
            if shoreline_change["is_choose_by_placement_seaward"]:
                f.write('By distance: Seaward\n')
            elif shoreline_change["is_choose_by_placement_landward"]: 
                f.write('By distance: Landward\n')

        clip_transects = "Yes" if shoreline_change["is_clip_transects"] else "No"
        f.write(f'Clip transects: {clip_transects}\n')
        f.write(f'Selected statistics: {", ".join(shoreline_change["selected_stats"])}\n')
        f.write(f'Newest date: {shoreline_change["newest_year"]}\n')
        f.write(f'Oldest date: {shoreline_change["oldest_year"]}\n')
        f.write('\n')
        f.write('[SUMMARY OF RESULTS]\n')
        f.write('\n')
        f.write(f'Total no. of transects: {self.summary["num_of_transects"]}\n')
        f.write('\n')

        selected_stats = shoreline_change['selected_stats']

        if Statistic.SCE in selected_stats:
            f.write('SHORELINE CHANGE ENVELOPE (SCE):\n')
            f.write(f'Avg. value: {self.summary["SCE_avg"]}\n')
            f.write(f'Max. value: {self.summary["SCE_max"]}\n')
            f.write(f'Min. value: {self.summary["SCE_min"]}\n')
            f.write('\n')

        if Statistic.NSM in selected_stats:
            f.write('NET SHORELINE MOVEMENT (NSM):\n')
            f.write(f'Avg. distance: {self.summary["NSM_avg"]}:\n')
            f.write('\n')
            f.write('Erosion:\n')
            f.write(f'No. of transects: {self.summary["NSM_erosion_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["NSM_erosion_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["NSM_erosion_avg"]}\n')
            f.write(f'Max. value: {self.summary["NSM_erosion_max"]}\n')
            f.write(f'Min. value: {self.summary["NSM_erosion_min"]}\n')
            f.write('\n')
            f.write('Accretion:\n')
            f.write(f'No. of transects: {self.summary["NSM_accretion_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["NSM_accretion_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["NSM_accretion_avg"]}\n')
            f.write(f'Max. value: {self.summary["NSM_accretion_max"]}\n')
            f.write(f'Min. value: {self.summary["NSM_accretion_min"]}\n')
            f.write('\n')
            f.write('Stable:\n')
            f.write(f'No. of transects: {self.summary["NSM_stable_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["NSM_stable_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["NSM_stable_avg"]}\n')
            f.write(f'Max. value: {self.summary["NSM_stable_max"]}\n')
            f.write(f'Min. value: {self.summary["NSM_stable_min"]}\n')
            f.write('\n')

        if Statistic.EPR in selected_stats:
            f.write('END POINT RATE (EPR):\n')
            f.write(f'Avg. rate: {None}:\n')
            f.write('\n')
            f.write('Erosion:\n')
            f.write(f'No. of transects: {self.summary["EPR_erosion_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["EPR_erosion_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["EPR_erosion_avg"]}\n')
            f.write(f'Max. value: {self.summary["EPR_erosion_max"]}\n')
            f.write(f'Min. value: {self.summary["EPR_erosion_min"]}\n')
            f.write('\n')
            f.write('Accretion:\n')
            f.write(f'No. of transects: {self.summary["EPR_accretion_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["EPR_accretion_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["EPR_accretion_avg"]}\n')
            f.write(f'Max. value: {self.summary["EPR_accretion_max"]}\n')
            f.write(f'Min. value: {self.summary["EPR_accretion_min"]}\n')
            f.write('\n')
            f.write('Stable:\n')
            f.write(f'No. of transects: {self.summary["EPR_stable_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["EPR_stable_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["EPR_stable_avg"]}\n')
            f.write(f'Max. value: {self.summary["EPR_stable_max"]}\n')
            f.write(f'Min. value: {self.summary["EPR_stable_min"]}\n')
            f.write('\n')

        if Statistic.LRR in selected_stats:
            f.write('LINEAR REGRESSION RATE (LRR):\n')
            f.write('Erosion:\n')
            f.write(f'No. of transects: {self.summary["LRR_erosion_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["LRR_erosion_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["LRR_erosion_avg"]}\n')
            f.write(f'Max. value: {self.summary["LRR_erosion_max"]}\n')
            f.write(f'Min. value: {self.summary["LRR_erosion_min"]}\n')
            f.write('\n')
            f.write('Accretion:\n')
            f.write(f'No. of transects: {self.summary["LRR_accretion_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["LRR_accretion_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["LRR_accretion_avg"]}\n')
            f.write(f'Max. value: {self.summary["LRR_accretion_max"]}\n')
            f.write(f'Min. value: {self.summary["LRR_accretion_min"]}\n')
            f.write('\n')

        if Statistic.WLR in selected_stats:
            f.write('WEIGHTED LINEAR REGRESSION (WLR):\n')
            f.write('Erosion:\n')
            f.write(f'No. of transects: {self.summary["WLR_erosion_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["WLR_erosion_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["WLR_erosion_avg"]}\n')
            f.write(f'Max. value: {self.summary["WLR_erosion_max"]}\n')
            f.write(f'Min. value: {self.summary["WLR_erosion_min"]}\n')
            f.write('\n')
            f.write('Accretion:\n')
            f.write(f'No. of transects: {self.summary["WLR_accretion_num_of_transects"]}\n')
            f.write(f'(%) transects: {self.summary["WLR_accretion_pct_transects"]}\n')
            f.write(f'Avg. value: {self.summary["WLR_accretion_avg"]}\n')
            f.write(f'Max. value: {self.summary["WLR_accretion_max"]}\n')
            f.write(f'Min. value: {self.summary["WLR_accretion_min"]}\n')
            f.write('\n')

        f.close()


    def area_change(self):
        """Create a summary report for area change computation."""
        f = self.create(ComputationType.AREA_CHANGE)

        area = get_area_change_input_params(self.qscat)

        f.write('[INPUT PARAMETERS]\n')
        f.write('\n')
        f.write('AREA:\n')
        f.write(f'Stat layer: {area["stat_layer"].name()}\n')
        f.write(f'Polygon area layer: {area["polygon_layer"].name()}\n')

        f.write('\n')
        f.write('[SUMMARY OF RESULTS]\n')
        f.write('\n')

        f.write('AREA:\n')
        f.write('\n')
        f.write(f'Total area: {self.summary["total_area"]}\n')
        f.write('\n')

        f.write('Erosion:\n')
        f.write(f'Total of areas: {self.summary["area_erosion_total_of_areas"]}\n')
        f.write(f'(%) of areas: {self.summary["area_erosion_pct_of_areas"]}\n')
        f.write(f'No. of areas: {self.summary["area_erosion_num_of_areas"]}\n')
        f.write(f'(%) of no. of areas: {self.summary["area_erosion_pct_of_num_of_areas"]}\n')
        f.write(f'Avg. value: {self.summary["area_erosion_avg"]}\n')
        f.write(f'Max. value: {self.summary["area_erosion_max"]}\n')
        f.write(f'Min. value: {self.summary["area_erosion_min"]}\n')
        f.write('\n')

        f.write('Accretion:\n')
        f.write(f'Total of areas: {self.summary["area_accretion_total_of_areas"]}\n')
        f.write(f'(%) of areas: {self.summary["area_accretion_pct_of_areas"]}\n')
        f.write(f'No. of areas: {self.summary["area_accretion_num_of_areas"]}\n')
        f.write(f'(%) of no. of areas: {self.summary["area_accretion_pct_of_num_of_areas"]}\n')
        f.write(f'Avg. value: {self.summary["area_accretion_avg"]}\n')
        f.write(f'Max. value: {self.summary["area_accretion_max"]}\n')
        f.write(f'Min. value: {self.summary["area_accretion_min"]}\n')
        f.write('\n')

        f.write('Stable:\n')
        f.write(f'Total of areas: {self.summary["area_stable_total_of_areas"]}\n')
        f.write(f'(%) of areas: {self.summary["area_stable_pct_of_areas"]}\n')
        f.write(f'No. of areas: {self.summary["area_stable_num_of_areas"]}\n')
        f.write(f'(%) of no. of areas: {self.summary["area_stable_pct_of_num_of_areas"]}\n')
        f.write(f'Avg. value: {self.summary["area_stable_avg"]}\n')
        f.write(f'Max. value: {self.summary["area_stable_max"]}\n')
        f.write(f'Min. value: {self.summary["area_stable_min"]}\n')
        f.write('\n')

        f.write('SHORELINE (LENGTH):\n')
        f.write('\n')
        f.write(f'Total shoreline (length): {self.summary["total_length"]}\n')
        f.write('\n')

        f.write('Erosion:\n')
        f.write(f'Total of lengths: {self.summary["length_erosion_total_of_lengths"]}\n')
        f.write(f'(%) of lengths: {self.summary["length_erosion_pct_of_lengths"]}\n')
        f.write(f'No. of lengths: {self.summary["length_erosion_num_of_lengths"]}\n')
        f.write(f'(%) of no. of lengths: {self.summary["length_erosion_pct_of_num_of_lengths"]}\n')
        f.write(f'Avg. value: {self.summary["length_erosion_avg"]}\n')
        f.write(f'Max. value: {self.summary["length_erosion_max"]}\n')
        f.write(f'Min. value: {self.summary["length_erosion_min"]}\n')
        f.write('\n')

        f.write('Accretion:\n')
        f.write(f'Total of lengths: {self.summary["length_accretion_total_of_lengths"]}\n')
        f.write(f'(%) of lengths: {self.summary["length_accretion_pct_of_lengths"]}\n')
        f.write(f'No. of lengths: {self.summary["length_accretion_num_of_lengths"]}\n')
        f.write(f'(%) of no. of lengths: {self.summary["length_accretion_pct_of_num_of_lengths"]}\n')
        f.write(f'Avg. value: {self.summary["length_accretion_avg"]}\n')
        f.write(f'Max. value: {self.summary["length_accretion_max"]}\n')
        f.write(f'Min. value: {self.summary["length_accretion_min"]}\n')
        f.write('\n')

        f.write('Stable:\n')
        f.write(f'Total of lengths: {self.summary["length_stable_total_of_lengths"]}\n')
        f.write(f'(%) of lengths: {self.summary["length_stable_pct_of_lengths"]}\n')
        f.write(f'No. of lengths: {self.summary["length_stable_num_of_lengths"]}\n')
        f.write(f'(%) of no. of lengths: {self.summary["length_stable_pct_of_num_of_lengths"]}\n')
        f.write(f'Avg. value: {self.summary["length_stable_avg"]}\n')
        f.write(f'Max. value: {self.summary["length_stable_max"]}\n')
        f.write(f'Min. value: {self.summary["length_stable_min"]}\n')
        f.write('\n')

        f.close()


    def forecasting(self):
        """Create a summary report for forecasting computation."""
        f = self.create(ComputationType.FORECASTING)

        f.write('INPUT PARAMETERS\n')
        f.write('\n')
        f.write('Transects layer:\n')
        #f.write(f'Layer: {area["transect_layer"].name()}\n')
        #f.write(f'Algorithm: {area["algorithm"]}\n')

        f.write('\n')
        f.write('SUMMARY OF RESULTS\n')
        f.write('\n')

        f.write('FORECASTING\n')

        f.close()