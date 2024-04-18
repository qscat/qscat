# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

import datetime
import math
import numpy as np
import time

from PyQt5.QtCore import QVariant

from qgis.PyQt.QtWidgets import QMessageBox

from qgis.core import Qgis
from qgis.core import QgsApplication
from qgis.core import QgsGeometry
from qgis.core import QgsMessageLog
from qgis.core import QgsPointXY
from qgis.core import QgsTask

from qgis.utils import iface

from qscat.core.intersections import load_all_years_intersections
from qscat.core.layers import create_add_layer
from qscat.core.layers import load_shorelines
from qscat.core.layers import load_transects
from qscat.core.shoreline_change import GetTransectsIntersectionsTask
from qscat.core.shoreline_change import compute_LCI
from qscat.core.shoreline_change import compute_LSE
from qscat.core.shoreline_change import get_sorted_uncs
from qscat.core.shoreline_change import get_sorted_years_distances
from qscat.core.report import SummaryReport
from qscat.core.utils.date import datetime_now
from qscat.core.utils.input import get_baseline_input_params
from qscat.core.utils.input import get_shorelines_years_uncs_from_input
from qscat.core.utils.input import get_shorelines_input_params
from qscat.core.utils.input import get_shoreline_change_input_params
from qscat.core.utils.input import get_transects_input_params


class ForecastAlgorithms:
    KALMAN_FILTER = 1

class ForecastTimePeriods:
    TEN_YEARS = 10
    TWENTY_YEARS = 20

class GetForecastTask(QgsTask):
    def __init__(
        self,
        forecast_length,
        all_years_intersections,
        years_uncs,
        confidence_interval
    ):
        super().__init__("Forecasting", QgsTask.CanCancel)
        self.forecast_length = forecast_length
        self.all_years_intersections = all_years_intersections
        self.years_uncs = years_uncs
        self.confidence_interval = confidence_interval
        
        self.forecasted_year = None
        self.forecasted_points = []
        self.forecasted_points_line = []
        self.forecasted_distances = []
        self.forecasted_distances_unc_neg = []
        self.forecasted_distances_unc_pos = []
        self.forecasted_distances_uncs = []

        self.exception = None


    def run(self):
        QgsMessageLog.logMessage(
            message=f"Started task: <b>{self.description()}</b>.",
            level=Qgis.Info,
        )

        try:
            start_time = time.perf_counter()
            for yid, years_intersections in enumerate(self.all_years_intersections):
                if self.isCanceled():
                    return False
                
                forecast = run_forecasting_single_transect(
                    self.forecast_length,
                    years_intersections,
                    self.years_uncs,
                    self.confidence_interval,
                )

                self.forecasted_year = forecast[0]
                self.forecasted_points.append(forecast[1])
                self.forecasted_points_line.append(forecast[1].asPoint())
                self.forecasted_distances.append(forecast[2])
                self.forecasted_distances_unc_neg.append(forecast[3])
                self.forecasted_distances_unc_pos.append(forecast[5])
                self.forecasted_distances_uncs.append(abs(forecast[4]-forecast[2]))

                self.setProgress((yid / len(self.all_years_intersections)) * 100)

            end_time = time.perf_counter()
            elapsed_time = (end_time - start_time) * 1000
            self.execution_time = f"{elapsed_time:.2f} ms"
            print(f"Forecast compute: {elapsed_time:.2f} ms")
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
            message=f"Success task: <b>{self.description()}</b>",
            level=Qgis.Success,
        )


def run_forecasting(qscat):
    start_time = time.perf_counter()

    years_uncs = get_shorelines_years_uncs_from_input(qscat)
    confidence_interval = float(qscat.dockwidget.qdsb_stats_confidence_interval.text())
    
    # Get forecasting algorithms
    algorithms = []
    if qscat.dockwidget.cb_forecasting_algorithm_1.isChecked():
        algorithms.append(ForecastAlgorithms.KALMAN_FILTER)
    
    # Get forecasting time period
    if qscat.dockwidget.rb_forecasting_time_20y.isChecked():
        forecast_length = ForecastTimePeriods.TWENTY_YEARS
    elif qscat.dockwidget.rb_forecasting_time_10y.isChecked():
        forecast_length = ForecastTimePeriods.TEN_YEARS

    # Load shoreline intersections
    baseline_params = get_baseline_input_params(qscat)
    shorelines_params = get_shorelines_input_params(qscat)
    transects_params = get_transects_input_params(qscat)
    shoreline_change_params = get_shoreline_change_input_params(qscat)

    transects = load_transects(qscat.dockwidget.qmlcb_forecasting_transects_layer.currentLayer())
    shorelines = load_shorelines(shorelines_params)

    globals()['get_transects_intersections_task'] = GetTransectsIntersectionsTask(
        transects,
        shorelines,
        shorelines_params,
        transects_params,
        baseline_params,
        shoreline_change_params,
        qscat.dockwidget.qmlcb_shoreline_change_transects_layer,
    )
    globals()['get_transects_intersections_task'].taskCompleted.connect(
        lambda: get_transects_intersections_task_state_changed(
            qscat,
            forecast_length,
            years_uncs,
            confidence_interval
        )
    )
    QgsApplication.taskManager().addTask(globals()['get_transects_intersections_task'])

    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000
    print(f"Forecast time (s): {elapsed_time:.2f} ms")


def get_transects_intersections_task_state_changed(
    qscat,
    forecast_length,
    years_uncs,
    confidence_interval
):
    task = globals()['get_transects_intersections_task']

    if task.status() == QgsTask.Complete:
        all_years_intersections = load_all_years_intersections(task.transects_intersects)
        globals()['get_forecast_task'] = GetForecastTask(
            forecast_length,
            all_years_intersections,
            years_uncs,
            confidence_interval
        )
        globals()['get_forecast_task'].taskCompleted.connect(
            lambda: get_forecast_task_state_changed(qscat)
        )
        QgsApplication.taskManager().addTask(globals()['get_forecast_task'])


def get_forecast_task_state_changed(qscat):
    task = globals()['get_forecast_task']
    if task.status() == QgsTask.Complete:
        current_datetime = datetime_now()

        # Add layer for forecasted polygon
        # Create the polygon based on unc neg and pos points
        poly_points = task.forecasted_distances_unc_neg \
            + task.forecasted_distances_unc_pos[::-1] \
            + [task.forecasted_distances_unc_neg[0]]

        # Finally, create the polygon out of that line string
        forecasted_unc_polygon = QgsGeometry.fromPolygonXY([poly_points])

        # Forecasted polygon
        unc_fields = [
            {'name': 'period', 'type': QVariant.Int},
            {'name': 'year', 'type': QVariant.Double},
            {'name': 'area', 'type': QVariant.Double}
        ]
        unc_values = [[
            task.forecast_length,
            task.forecasted_year,
            forecasted_unc_polygon.area()
        ]]
        create_add_layer(
            geometry='Polygon',
            geometries=[forecasted_unc_polygon], 
            name="forecast_uncertainty_band",
            fields=unc_fields,
            values=unc_values,
            datetime=current_datetime,
        )

        # Forecasted line
        forecasted_line = QgsGeometry.fromPolylineXY(task.forecasted_points_line)
        line_fields = [
            {'name': 'period', 'type': QVariant.Int},
            {'name': 'year', 'type': QVariant.Double},
            {'name': 'length', 'type': QVariant.Double}
        ]
        line_values = [[
            task.forecast_length,
            task.forecasted_year,
            forecasted_line.length()
        ]]
        
        create_add_layer(
            geometry='LineString',
            geometries=[forecasted_line], 
            name="forecast_line",
            fields=line_fields,
            values=line_values,
            datetime=current_datetime,
        )
        
        # Forecasted points
        point_fields = [
            {'name': 'period', 'type': QVariant.Int},
            {'name': 'year', 'type': QVariant.Double},
            {'name': 'distance', 'type': QVariant.Double},
            {'name': 'uncertainty', 'type': QVariant.Double},
            {'name': 'intersect_x', 'type': QVariant.Double},
            {'name': 'intersect_y', 'type': QVariant.Double},
        ]

        point_values = []
        
        for distance, uncertainty, points_line in zip(
            task.forecasted_distances,
            task.forecasted_distances_uncs,
            task.forecasted_points_line):

            point_values.append([
                task.forecast_length,
                task.forecasted_year,
                distance,
                uncertainty,
                points_line.x(),
                points_line.y(),
            ])

        create_add_layer(
            geometry='Point',
            geometries=task.forecasted_points, 
            name="forecast_points",
            fields=point_fields,
            values=point_values,
            datetime=current_datetime,
        )

        # Summary
        summary = {}
        summary['datetime'] = current_datetime

        report = SummaryReport(qscat, summary)
        report.forecasting()


def get_angle(point1, point2):
    """Calculate the angle between two points.

    Args:
        point1 (QgsPointXY): The first point.
        point2 (QgsPointXY): The second point.

    Returns:
        float: The angle in radians.
    """
    # Calculate the differences in x and y coordinates
    dx = point2.x() - point1.x()
    dy = point2.y() - point1.y()

    # Calculate the angle using the arctangent function
    angle = math.atan2(dy, dx)

    # Convert angle to degrees if desired
    # angle_degrees = math.degrees(angle)

    return angle


def extend_point_by_n_distance(angle, point, distance):
    """Extends a given point by a specified distance in the direction of the given angle.

    Args:
        angle (float): The angle in radians.
        point (QgsPointXY): The point to be extended.
        distance (float): The distance by which the point should be extended.

    Returns:
        QgsPointXY: The extended point.
    """

    # Calculate the change in x and y coordinates using the angle and distance
    dx = distance * math.cos(angle)
    dy = distance * math.sin(angle)

    # Extend the point
    extended_x = point.x() + dx
    extended_y = point.y() + dy

    return QgsPointXY(extended_x, extended_y)


def run_forecasting_single_transect(
    forecast_length,
    years_intersections,
    years_uncs,
    confidence_interval
):
    """Run forecasting for a single transect.

    Args:
        forecast_length (int): The forecast length.
        years_intersections (dict): The years intersections.
        years_uncs (dict): The years uncertainties.
        confidence_interval (float): The confidence interval.

    Returns:
        tuple: The forecasted shoreline year, 
            the forecasted shoreline point, 
            the forecasted shoreline distance, 
            the forecasted shoreline uncertainty negative, 
            the forecasted shoreline uncertainty positive.
    """
    # TODO: Show error if not enough shorelines (atleast 3) to run forecasting
    # TODO: Create cache of LRR shoreline change get sorted years distances, and read that here for forecasting
    years, distances = get_sorted_years_distances(years_intersections)

    uncs = get_sorted_uncs(years_uncs)

    LCI_value = compute_LCI(years, distances, confidence_interval)
    LSE_value = compute_LSE(years, distances)

    slope, intercept = np.polyfit(years, distances, 1) # LRR
    y0 = intercept + slope * years[0]
    x0 = np.round(np.array([y0, slope]), 2)

    Xc, Pc, T = kalman_filter(
        forecast_length,
        years,
        distances,
        uncs,
        LSE_value,
        LCI_value,
        x0,
    )

    n = len(T)

    # Predicted shoreline year added by forecast length
    predicted_shoreline_year = float(T[n-1])

    # Predicted shoreline distance with respect to transect angle/direction
    predicted_shoreline_distance = float(Xc[n-1][0])

    # Predicted uncertainty
    u = Pc[n-1][0][0]
    predicted_uncertainty_1 = float(predicted_shoreline_distance + np.sqrt(u))
    predicted_uncertainty_2 = float(predicted_shoreline_distance - np.sqrt(u))

    # Calculate based on shoreline distance
    # Determine the angle of transect where to put the predicted shoreline distance
    # We can use the 'angle' field value of the transect layer, but
    # I want to use directly from "years_intersections" where I need to compute 
    # the angle where to put the predicted shoreline position

    closest_distance_year = min(
        years_intersections.items(), key=lambda x: x[1]['distance'])[0]
    closest_distance_pt = QgsPointXY(
        years_intersections[closest_distance_year]['intersect_x'],
        years_intersections[closest_distance_year]['intersect_y']
    )
    farthest_distance_year = max(
        years_intersections.items(), key=lambda x: x[1]['distance'])[0]
    farthest_distance_pt = QgsPointXY(
        years_intersections[farthest_distance_year]['intersect_x'],
        years_intersections[farthest_distance_year]['intersect_y']
    )
    angle = get_angle(closest_distance_pt, farthest_distance_pt)

    for value in years_intersections.values():
        if 'transect_origin' in value:
            transect_origin_pt = value['transect_origin'].asPoint()
            break

    predicted_shoreline_point = extend_point_by_n_distance(
        angle,
        transect_origin_pt,
        predicted_shoreline_distance
    )
    predicted_shoreline_point_geom = QgsGeometry.fromPointXY(
        predicted_shoreline_point
    )
    predicted_shoreline_point_unc_neg = extend_point_by_n_distance(
        angle,
        transect_origin_pt,
        predicted_uncertainty_1
    )
    predicted_shoreline_point_unc_neg_geom = predicted_shoreline_point_unc_neg
    
    predicted_shoreline_point_unc_pos = extend_point_by_n_distance(
        angle, 
        transect_origin_pt, 
        predicted_uncertainty_2
    )
    predicted_shoreline_point_unc_pos_geom = predicted_shoreline_point_unc_pos

    return (
        predicted_shoreline_year,
        predicted_shoreline_point_geom,
        predicted_shoreline_distance,
        predicted_shoreline_point_unc_neg_geom,
        predicted_uncertainty_1,
        predicted_shoreline_point_unc_pos_geom,
        predicted_uncertainty_2,
    )


def kalman_filter(
    forecast_length,
    years, 
    distances, 
    uncertainties,
    LSE_value,
    LCI_value,
    x0,
    dt=0.1,
    process_noise=0.1
):    
    """Based from
    https://code.usgs.gov/cch/dsas/-/blob/master/src/DSASv5Addin/Install/usgs_scripts/DSAS_kalmanfilter.py
    """
    now = datetime.datetime.now()
    startT = int(years[0])

    T = np.arange(startT, (now.year+(forecast_length+1)), 0.1)
    T = np.round(T, 1) # fix imprecision error
    A = np.array([[1, dt], [0, 1]])
    Q = np.round(np.array([
        [(process_noise**2)*(dt**3)/3, (process_noise**2)*(dt**2)/2],
        [(process_noise**2)*(dt**2)/2, (process_noise**2)*(dt)]
    ]), 8)
    P = np.array([
        [(LSE_value)**2 + (uncertainties[0])**2, 0],
        [0,(LCI_value)**2],
    ])
    H = np.array([1, 0])
    R = (LSE_value**2) + (uncertainties**2)

    n_time = len(T)
    n_state = len(A[:][:])

    # Initialize matrices for results
    Xp = np.zeros((n_time, n_state)) # Predicted state
    Xc = np.zeros((n_time, n_state)) # Corrected state
    Pp = np.zeros((n_time, n_state, n_state))
    Pp[0] = P
    Pc = np.zeros((n_time, n_state, n_state)) # Corrected covariance
    Pc[0] = P
    K = np.zeros((n_time, n_state)) # Kalman gain
    res = np.zeros(n_time) # Residual
    Xp[0] = x0
    Xc[0] = x0

    for j in range(1, n_time):
        # Compute predicted state
        # Xp = A*Xc
        Xp1 = np.dot(A, Xc[j-1])
        Xp[j] = Xp1
        
        # Compute A PRIORI error covariance
        # Pp = A[j-1] * Pc[j-1] * A[j-1] + Q[j-1]
        Pp1 = np.matmul(A, Pc[j-1])
        Pp2 = np.matmul(Pp1, A.T)
        Pp3 = Q + Pp2
        Pp[j] = Pp3
        
        # Compute Kalman gain if observations are available
        # K = Pp * H' * invert(H * P * H' + R)
        if T[j] in years:
            i = np.where(years==T[j])[0][0]
            K1 = Pp[j] @ H
            K2 = np.dot(H, K1) + R[i]
            K3 = 1/K2
            K4 = K1 * K3
            K[j] = K4
            
            res1 = H * Xp[j]
            res[j] = distances[i] - res1[0]
            
        Xc[j] = Xp[j] + K[j] * res[j]
        
        Pc1 = np.outer(K[j], H)
        Pc2 = np.eye(2) - Pc1
        Pc3 = np.matmul(Pc2, Pp[j])
        Pc[j] = Pc3

    return (Xc, Pc, T)