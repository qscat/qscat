.. _tab_forecasting:

****************
Tab: Forecasting
****************

.. only:: html

   .. contents::
      :local:
      :depth: 2
      
.. _figure_tab_forecasting:

.. figure:: /img/forecasting/forecasting-tab.png
   :align: center

   User interface of Forecasting Tab.

.. _tab_forecasting_algorithm:

Algorithm
=========

*Content for this section will be added soon.*


.. _tab_forecasting_kalman_filter:

Kalman Filter
-------------

*Content for this section will be added soon.*

.. _tab_forecasting_time_period:

Time Period
===========

Allows user to select the forecast period (10 or 20 years) from now.


Vector layer output
===================

The :guilabel:`Kalman Filter` forecasting algorithm output three vector layers:

#. **Forecasted Points** is the forecasted points for each transect.
#. **Forecasted Line** is a line string geometry connected by forecasted points.
#. **Forecasted Polygon** is a polygon geometry connected by positive and negative forecasted uncertainty points.

Layers
------

.. list-table:: 
   :header-rows: 1
   :widths: 30 20 50

   * - Layer
     - Geometry
     - Name
   * - Forecasted Points
     - ``Point``
     - ``forecast_points [<datetime>]``
   * - Forecasted Line
     - ``LineString``
     - ``forecast_line [<datetime>]``
   * - Forecasted Polygon
     - ``Polygon``
     - ``forecast_polygon [<datetime>]`` 


Attributes
----------


Forecast Point
..............

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``period``
     - ``integer``
     - Selected forecast year period (10 or 20).
   * - ``year``
     - ``integer``
     - Forecasted year calculated based from period.
   * - ``distance``
     - ``double``
     - Magnitude value of forecasted distance.
   * - ``uncertainty``
     - ``double``
     - Value of forecasted uncertainty.
   * - ``intersect_x``
     - ``double``
     - X coordinate of the forecasted point.
   * - ``intersect_y``
     - ``double``
     - Y coordinate of the forecasted point.


Forecast Shoreline
...................

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``period``
     - ``integer``
     - Selected forecast year period (10 or 20).
   * - ``year``
     - ``integer``
     - Forecasted year calculated based from period.
   * - ``length``
     - ``double``
     - Line length of connected forecasted points.


Forecast Polygon
................

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``period``
     - ``integer``
     - Selected forecast year period (10 or 20).
   * - ``year``
     - ``integer``
     - Forecasted year calculated based from period.
   * - ``area``
     - ``double``
     - Polygon area of connected forecasted uncertainty.

