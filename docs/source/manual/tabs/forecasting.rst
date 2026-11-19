.. _tab_forecasting:

****************
Tab: Forecasting
****************


The :guilabel:`Forecasting Tab` allows you to forecast the shoreline position using the Kalman Filter algorithm.

.. only:: html

   .. contents::
      :local:
      :depth: 2
      
.. _figure_tab_forecasting:

.. figure:: /img/forecasting/forecasting-tab.png
   :align: center
   :alt: User interface of Forecasting Tab

   User interface of Forecasting Tab



Layer
=====

.. _figure_tab_forecasting_layer:

.. figure:: /img/forecasting/forecasting-tab-layer.png
   :align: center
   :alt: Layer section in Forecasting Tab

   Layer section in Forecasting Tab

Allows you to select the transects layer to be used for forecasting. In QSCAT, the requirement for forecasting is a transect layer unlike DSAS. This allows you to run the forecasting algorithm without the need to run the shoreline change statistics.

.. _tab_forecasting_algorithm:

Algorithm
=========

.. _figure_tab_forecasting_algorithm:

.. figure:: /img/forecasting/forecasting-tab-algorithm.png
   :align: center
   :alt: Algorithm section in Forecasting Tab

   Algorithm section in Forecasting Tab

.. _tab_forecasting_kalman_filter:

Kalman Filter
-------------

Based on :cite:`long2012extended`, according to DSAS :cite:`2018:dsasv5`.

.. _tab_forecasting_time_period:

Time period
===========

.. _figure_tab_forecasting_time_period:

.. figure:: /img/forecasting/forecasting-tab-time-period.png
   :align: center
   :alt: Time period section in Forecasting Tab

   Time period section in Forecasting Tab

Allows you to select the forecast period (10 or 20 years) from now. "From now" refers to system date when the forecasting algorithm is executed.


Vector layer output
===================

The :guilabel:`Kalman Filter` forecasting algorithm outputs two vector layers:

#. **Forecasted points:** the forecasted shoreline position on each transect.
#. **Forecasted uncertainty points:** the positive and negative forecasted uncertainty positions on each transect.

Layers
------

.. list-table:: Vector layer output geometry type and name
   :header-rows: 1
   :widths: 30 20 50

   * - Layer
     - Geometry
     - Name
   * - Forecasted points
     - ``Point``
     - ``forecast_points [<datetime>]``
   * - Forecasted uncertainty points
     - ``Point``
     - ``forecast_uncertainty_points [<datetime>]``


Attributes
----------

Forecast points
...............

.. list-table:: Forecast points attribute table
   :header-rows: 1
   :widths: 30 20 50

   * - Field name
     - Data type
     - Description
   * - ``period``
     - ``integer``
     - Selected forecast period in years (10 or 20).
   * - ``year``
     - ``double``
     - Forecasted year (decimal year) calculated based on the period.
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


Forecast uncertainty points
...........................

.. list-table:: Forecast uncertainty points attribute table
   :header-rows: 1
   :widths: 30 20 50

   * - Field name
     - Data type
     - Description
   * - ``period``
     - ``integer``
     - Selected forecast period in years (10 or 20).
   * - ``year``
     - ``double``
     - Forecasted year (decimal year) calculated based on the period.
