.. _tab_forecasting:

****************
Tab: Forecasting
****************

.. only:: html

   .. contents::
      :local:
      :depth: 2
      
Forecasting Parameters
======================

*Content for this section will be added soon.*

Forecasting Algorithm
=====================

*Content for this section will be added soon.*

Kalman Filter
-------------

*Content for this section will be added soon.*

Forecasting Period
==================

Allows user to select the forecast period (10 or 20 years) from now.

Forecasting Output Layers
=========================

Kalman Filter
-------------

The :menuselection:`Kalman Filter` forecasting algorithm output three vector layers:

#. ``Point`` layer is the forecasted point starting from transect origin point and inline with the transect line angle
#. ``LineString`` layer is the forecasted points connected as a linestring
#. ``Polygon`` layer is the forecasted uncertainty points + and - connected that formed a polygon.


.. list-table:: Forecasted point layer attributes
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``period``
     - ``integer``
     - the selected forecast year period (10 or 20)
   * - ``year``
     - ``integer``
     - the forecasted year calculated based from period
   * - ``distance``
     - ``double``
     - the magnitude value of forecasted distance
   * - ``uncertainty``
     - ``double``
     - the value of forecasted uncertainty
   * - ``intersect_x``
     - ``double``
     - the x coordinate of the forecasted point
   * - ``intersect_y``
     - ``double``
     - the y coordinate of the forecasted point

.. list-table:: Forecasted line layer attributes
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``period``
     - ``integer``
     - the selected forecast year period (10 or 20)
   * - ``year``
     - ``integer``
     - the forecasted year calculated based from period
   * - ``length``
     - ``double``
     - the line length of connected forecasted points

.. list-table:: Forecasted polygon layer attributes
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``period``
     - ``integer``
     - the selected forecast year period (10 or 20)
   * - ``year``
     - ``integer``
     - the forecasted year calculated based from period
   * - ``area``
     - ``double``
     - the polygon area of connected forecasted uncertainty

Output Layer Names
..................

.. list-table:: 
   :header-rows: 1
   :widths: 20 80

   * - Type
     - Name
   * - ``Point``
     - ``forecast_points [<datetime>]``
   * - ``LineString``
     - ``forecast_line [<datetime>]``
   * - ``Polygon``
     - ``forecast_polygon [<datetime>]``    