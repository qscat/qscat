# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import os
import platform

from qgis.core import Qgis

from qscat.core.utils import get_baseline_input_params
from qscat.core.utils import get_metadata_version
from qscat.core.utils import get_project_input_params
from qscat.core.utils import get_project_dir
from qscat.core.utils import get_shorelines_input_params
from qscat.core.utils import get_shorelines_dates
from qscat.core.utils import get_shorelines_uncs
from qscat.core.utils import get_stats_area_change_input_params
from qscat.core.utils import get_shoreline_change_input_params
from qscat.core.utils import get_transects_input_params


COMP_SHORELINE_CHANGE = 0
COMP_AREA_CHANGE = 1
COMP_FORECASTING = 2


def create_summary_base_file(qscat, datetime, computation):
    """Create the base file for both shoreline and area change summary report.
    Contains the general information such as project crs, author information, 
    and sytem information.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.
        summary (dict): Contains info about stats
        computation (int): 0 for shoreline change, 1 for area change, 2 for forecasting.

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
    base_dir = qscat.dockwidget.qfw_report_save_location.filePath()

    if computation == COMP_SHORELINE_CHANGE:
        summary_reports_dir = os.path.join(base_dir, 'shoreline_change')
        file_name = f'qscat_{get_metadata_version()}_shoreline_change_{datetime}.txt'
    elif computation == COMP_AREA_CHANGE:
        summary_reports_dir = os.path.join(base_dir, 'area_change')
        file_name = f'qscat_{get_metadata_version()}_area_change_{datetime}.txt'
    elif computation == COMP_FORECASTING:
        summary_reports_dir = os.path.join(base_dir, 'forecasting')
        file_name = f'qscat_{get_metadata_version()}_forecasting_{datetime}.txt'

    # Ensure the directory exists
    os.makedirs(summary_reports_dir, exist_ok=True)

    summary_report_file_path = os.path.join(summary_reports_dir, file_name)

    project = get_project_input_params(qscat)
    f = open(summary_report_file_path, 'w')
    f.write(f'[PROJECT DETAILS]\n')
    f.write(f'\n')
    f.write(f'GENERAL:\n')
    f.write(f'Time generated: {datetime}\n')
    f.write(f'Project location: {get_project_dir()}\n')
    f.write(f'\n')
    f.write(f'PROJECTION:\n')
    f.write(f'CRS auth id: {project["crs_id"]}\n')
    f.write(f'\n')
    f.write(f'AUTHOR:\n')
    f.write(f'Full name: {project["author_full_name"]}\n')
    f.write(f'Affiliation: {project["author_affiliation"]}\n')
    f.write(f'Email: {project["author_email"]}\n')
    f.write(f'\n')
    f.write(f'[SYSTEM DETAILS]\n')
    f.write(f'\n')
    f.write(f'OS version: {platform.system()} {platform.release()}\n')
    f.write(f'QGIS version: {Qgis.QGIS_VERSION}\n')
    f.write(f'QSCAT version: {get_metadata_version()}\n')
    f.write(f'\n')

    return f


def create_summary_area_change(qscat, summary):
    """
    Args:
        qscat (QscatPlugin): QscatPlugin instance.
        summary (dict): Contains info about stats.
    """
    # Create the file
    f = create_summary_base_file(qscat, summary['datetime'], COMP_AREA_CHANGE)

    # Ready the data
    area = get_stats_area_change_input_params(qscat)

    f.write(f'[INPUT PARAMETERS]\n')
    f.write(f'\n')
    f.write(f'AREA:\n')
    f.write(f'NSM layer: {area["NSM_layer"].name()}\n')
    f.write(f'Polygon area layer: {area["polygon_layer"].name()}\n')

    f.write(f'\n')
    f.write(f'[SUMMARY OF RESULTS]\n')
    f.write(f'\n')

    f.write(f'AREA:\n')
    f.write(f'\n')
    f.write(f'Total area: {summary["total_area"]}\n')
    f.write(f'\n')

    f.write(f'Erosion:\n')
    f.write(f'Total of areas: {summary["area_erosion_total_of_areas"]}\n')
    f.write(f'(%) of areas: {summary["area_erosion_pct_of_areas"]}\n')
    f.write(f'No. of areas: {summary["area_erosion_num_of_areas"]}\n')
    f.write(f'(%) of no. of areas: {summary["area_erosion_pct_of_num_of_areas"]}\n')
    f.write(f'Avg. value: {summary["area_erosion_avg"]}\n')
    f.write(f'Max. value: {summary["area_erosion_max"]}\n')
    f.write(f'Min. value: {summary["area_erosion_min"]}\n')
    f.write(f'\n')

    f.write(f'Accretion:\n')
    f.write(f'Total of areas: {summary["area_accretion_total_of_areas"]}\n')
    f.write(f'(%) of areas: {summary["area_accretion_pct_of_areas"]}\n')
    f.write(f'No. of areas: {summary["area_accretion_num_of_areas"]}\n')
    f.write(f'(%) of no. of areas: {summary["area_accretion_pct_of_num_of_areas"]}\n')
    f.write(f'Avg. value: {summary["area_accretion_avg"]}\n')
    f.write(f'Max. value: {summary["area_accretion_max"]}\n')
    f.write(f'Min. value: {summary["area_accretion_min"]}\n')
    f.write(f'\n')

    f.write(f'Stable:\n')
    f.write(f'Total of areas: {summary["area_stable_total_of_areas"]}\n')
    f.write(f'(%) of areas: {summary["area_stable_pct_of_areas"]}\n')
    f.write(f'No. of areas: {summary["area_stable_num_of_areas"]}\n')
    f.write(f'(%) of no. of areas: {summary["area_stable_pct_of_num_of_areas"]}\n')
    f.write(f'Avg. value: {summary["area_stable_avg"]}\n')
    f.write(f'Max. value: {summary["area_stable_max"]}\n')
    f.write(f'Min. value: {summary["area_stable_min"]}\n')
    f.write(f'\n')

    f.write(f'SHORELINE (LENGTH):\n')
    f.write(f'\n')
    f.write(f'Total shoreline (length): {summary["total_length"]}\n')
    f.write(f'\n')

    f.write(f'Erosion:\n')
    f.write(f'Total of lengths: {summary["length_erosion_total_of_lengths"]}\n')
    f.write(f'(%) of lengths: {summary["length_erosion_pct_of_lengths"]}\n')
    f.write(f'No. of lengths: {summary["length_erosion_num_of_lengths"]}\n')
    f.write(f'(%) of no. of lengths: {summary["length_erosion_pct_of_num_of_lengths"]}\n')
    f.write(f'Avg. value: {summary["length_erosion_avg"]}\n')
    f.write(f'Max. value: {summary["length_erosion_max"]}\n')
    f.write(f'Min. value: {summary["length_erosion_min"]}\n')
    f.write(f'\n')

    f.write(f'Accretion:\n')
    f.write(f'Total of lengths: {summary["length_accretion_total_of_lengths"]}\n')
    f.write(f'(%) of lengths: {summary["length_accretion_pct_of_lengths"]}\n')
    f.write(f'No. of lengths: {summary["length_accretion_num_of_lengths"]}\n')
    f.write(f'(%) of no. of lengths: {summary["length_accretion_pct_of_num_of_lengths"]}\n')
    f.write(f'Avg. value: {summary["length_accretion_avg"]}\n')
    f.write(f'Max. value: {summary["length_accretion_max"]}\n')
    f.write(f'Min. value: {summary["length_accretion_min"]}\n')
    f.write(f'\n')

    f.write(f'Stable:\n')
    f.write(f'Total of lengths: {summary["length_stable_total_of_lengths"]}\n')
    f.write(f'(%) of lengths: {summary["length_stable_pct_of_lengths"]}\n')
    f.write(f'No. of lengths: {summary["length_stable_num_of_lengths"]}\n')
    f.write(f'(%) of no. of lengths: {summary["length_stable_pct_of_num_of_lengths"]}\n')
    f.write(f'Avg. value: {summary["length_stable_avg"]}\n')
    f.write(f'Max. value: {summary["length_stable_max"]}\n')
    f.write(f'Min. value: {summary["length_stable_min"]}\n')
    f.write(f'\n')

    f.close()


def create_summary_shoreline_change(self, summary):
    # Create the file
    f = create_summary_base_file(self, summary['datetime'], COMP_SHORELINE_CHANGE)
    
    # Ready the data
    # Should we use the data from the summary dict or the input params?
    shorelines = get_shorelines_input_params(self)
    baseline = get_baseline_input_params(self)
    transects = get_transects_input_params(self)
    shoreline_change = get_shoreline_change_input_params(self)

    uncs = ", ".join("{:.2f}".format(x) for x in get_shorelines_uncs(self))
    
    f.write(f'[INPUT PARAMETERS]\n')
    f.write(f'\n')
    f.write(f'SHORELINES TAB:\n')
    f.write(f'Layer: {shorelines["shorelines_layer"].name()}\n')
    f.write(f'Default data uncertainty: {shorelines["default_data_uncertainty"]}\n')
    f.write(f'Date field: {shorelines["date_field"]}\n')
    f.write(f'Uncertainty field: {shorelines["uncertainty_field"]}\n')
    f.write(f'Dates: {", ".join(get_shorelines_dates(self))}\n')
    f.write(f'Uncertainties: {uncs}\n')
    f.write(f'\n')
    
    if baseline["is_baseline_placement_sea"]:
        placement = "Sea or Offshore"
    elif baseline["is_baseline_placement_land"]:
        placement = "Land or Onshore"
    if baseline["is_baseline_orientation_land_right"]:
        orientation = "Land is to the RIGHT" 
    elif baseline["is_baseline_orientation_land_left"]:
        orientation = "Land is to the LEFT"

    f.write(f'BASELINE TAB:\n')
    f.write(f'Layer: {baseline["baseline_layer"].name()}\n')
    f.write(f'Placement: {placement}\n')
    f.write(f'Orientation: {orientation}\n')
    f.write(f'\n')
    f.write(f'TRANSECTS TAB:\n')
    f.write(f'Layer output name: {transects["layer_output_name"]}\n')

    if transects['is_by_transect_spacing']:
        f.write(f'Transect count: By transect spacing\n')
        f.write(f'Transect spacing: {transects["by_transect_spacing"]} meters\n')
    elif transects['is_by_number_of_transects']:
        f.write(f'Transect count: By number of transects\n')
        f.write(f'Number of transects: {transects["by_number_of_transects"]} transects\n')
    f.write(f'Transect length: {transects["length"]} meters\n')
    f.write(f'Smoothing distance: {transects["smoothing_distance"]} meters\n')

    f.write(f'\n')
    f.write(f'STATISTICS TAB:\n')
    f.write(f'Transect layer: {shoreline_change["transect_layer"].name()}\n')

    if shoreline_change["is_choose_by_distance"]:
        f.write(f'Intersection: Choose by distance\n')
        if shoreline_change["is_choose_by_distance_farthest"]:
            f.write(f'By distance: Farthest\n')
        elif shoreline_change["is_choose_by_distance_closest"]: 
            f.write(f'By distance: Closest\n')
    elif shoreline_change["is_choose_by_placement"]:
        f.write(f'Intersection: Choose by placement\n')
        if shoreline_change["is_choose_by_placement_seaward"]:
            f.write(f'By distance: Seaward\n')
        elif shoreline_change["is_choose_by_placement_landward"]: 
            f.write(f'By distance: Landward\n')

    clip_transects = "Yes" if shoreline_change["is_clip_transects"] else "No"
    f.write(f'Clip transects: {clip_transects}\n')
    f.write(f'Selected statistics: {", ".join(shoreline_change["selected_stats"])}\n')
    f.write(f'Newest date: {shoreline_change["newest_year"]}\n')
    f.write(f'Oldest date: {shoreline_change["oldest_year"]}\n')
    f.write(f'\n')
    f.write(f'[SUMMARY OF RESULTS]\n')
    f.write(f'\n')
    f.write(f'Total no. of transects: {summary["num_of_transects"]}\n')
    f.write(f'\n')

    selected_stats = shoreline_change['selected_stats']

    if 'SCE' in selected_stats:
        f.write(f'SHORELINE CHANGE ENVELOPE (SCE):\n')
        f.write(f'Avg. value: {summary["SCE_avg"]}\n')
        f.write(f'Max. value: {summary["SCE_max"]}\n')
        f.write(f'Min. value: {summary["SCE_min"]}\n')
        f.write(f'\n')

    if 'NSM' in selected_stats:
        f.write(f'NET SHORELINE MOVEMENT (NSM):\n')
        f.write(f'Avg. distance: {summary["NSM_avg"]}:\n')
        f.write(f'\n')
        f.write(f'Erosion:\n')
        f.write(f'No. of transects: {summary["NSM_erosion_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["NSM_erosion_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["NSM_erosion_avg"]}\n')
        f.write(f'Max. value: {summary["NSM_erosion_max"]}\n')
        f.write(f'Min. value: {summary["NSM_erosion_min"]}\n')
        f.write(f'\n')
        f.write(f'Accretion:\n')
        f.write(f'No. of transects: {summary["NSM_accretion_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["NSM_accretion_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["NSM_accretion_avg"]}\n')
        f.write(f'Max. value: {summary["NSM_accretion_max"]}\n')
        f.write(f'Min. value: {summary["NSM_accretion_min"]}\n')
        f.write(f'\n')
        f.write(f'Stable:\n')
        f.write(f'No. of transects: {summary["NSM_stable_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["NSM_stable_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["NSM_stable_avg"]}\n')
        f.write(f'Max. value: {summary["NSM_stable_max"]}\n')
        f.write(f'Min. value: {summary["NSM_stable_min"]}\n')
        f.write(f'\n')

    if 'EPR' in selected_stats:
        f.write(f'END POINT RATE (EPR):\n')
        f.write(f'Avg. rate: {None}:\n')
        f.write(f'\n')
        f.write(f'Erosion:\n')
        f.write(f'No. of transects: {summary["EPR_erosion_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["EPR_erosion_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["EPR_erosion_avg"]}\n')
        f.write(f'Max. value: {summary["EPR_erosion_max"]}\n')
        f.write(f'Min. value: {summary["EPR_erosion_min"]}\n')
        f.write(f'\n')
        f.write(f'Accretion:\n')
        f.write(f'No. of transects: {summary["EPR_accretion_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["EPR_accretion_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["EPR_accretion_avg"]}\n')
        f.write(f'Max. value: {summary["EPR_accretion_max"]}\n')
        f.write(f'Min. value: {summary["EPR_accretion_min"]}\n')
        f.write(f'\n')
        f.write(f'Stable:\n')
        f.write(f'No. of transects: {summary["EPR_stable_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["EPR_stable_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["EPR_stable_avg"]}\n')
        f.write(f'Max. value: {summary["EPR_stable_max"]}\n')
        f.write(f'Min. value: {summary["EPR_stable_min"]}\n')
        f.write(f'\n')

    if 'LRR' in selected_stats:
        f.write(f'LINEAR REGRESSION RATE (LRR):\n')
        f.write(f'Erosion:\n')
        f.write(f'No. of transects: {summary["LRR_erosion_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["LRR_erosion_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["LRR_erosion_avg"]}\n')
        f.write(f'Max. value: {summary["LRR_erosion_max"]}\n')
        f.write(f'Min. value: {summary["LRR_erosion_min"]}\n')
        f.write(f'\n')
        f.write(f'Accretion:\n')
        f.write(f'No. of transects: {summary["LRR_accretion_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["LRR_accretion_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["LRR_accretion_avg"]}\n')
        f.write(f'Max. value: {summary["LRR_accretion_max"]}\n')
        f.write(f'Min. value: {summary["LRR_accretion_min"]}\n')
        f.write(f'\n')

    if 'WLR' in selected_stats:
        f.write(f'WEIGHTED LINEAR REGRESSION (WLR):\n')
        f.write(f'Erosion:\n')
        f.write(f'No. of transects: {summary["WLR_erosion_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["WLR_erosion_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["WLR_erosion_avg"]}\n')
        f.write(f'Max. value: {summary["WLR_erosion_max"]}\n')
        f.write(f'Min. value: {summary["WLR_erosion_min"]}\n')
        f.write(f'\n')
        f.write(f'Accretion:\n')
        f.write(f'No. of transects: {summary["WLR_accretion_num_of_transects"]}\n')
        f.write(f'(%) transects: {summary["WLR_accretion_pct_transects"]}\n')
        f.write(f'Avg. value: {summary["WLR_accretion_avg"]}\n')
        f.write(f'Max. value: {summary["WLR_accretion_max"]}\n')
        f.write(f'Min. value: {summary["WLR_accretion_min"]}\n')
        f.write(f'\n')
    
    f.close()