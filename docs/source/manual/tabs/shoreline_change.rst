.. _tab_shoreline_change:

*********************
Tab: Shoreline Change
*********************

The :guilabel:`Shoreline Change Tab` allows you to calculate the following shoreline change statistics: (a) Shoreline Change Envelope (SCE), (b) Net Shoreline Movement (NSM), (c) End-Point Rate (EPR), and (d) Linear Regression Rate (LRR). The first three statistics (SCE, NSM, and EPR) require only two shoreline vectors, while LRR requires at least three (3) shoreline vectors to compute the rate of change. SCE and NSM refer to magnitude or distance in meters (m), while EPR and LRR are rate-of-change statistics in meters/year (m/y).

.. only:: html

   .. contents::
      :local:
      :depth: 3

.. _figure_tab_shoreline_change:

.. figure:: /img/shoreline_change/shoreline-change-tab.png
   :align: center
   :alt: User interface of Shoreline Change Tab

   User interface of Shoreline Change Tab

General
=======

.. _figure_tab_shoreline_change_general:

.. figure:: /img/shoreline_change/shoreline-change-tab-general.png
   :align: center
   :alt: General section in Shoreline Change Tab

   General section in Shoreline Change Tab

Transects layer
---------------

This run requires a transect layer to calculate the selected statistics in the :guilabel:`Shoreline Change Statistics` section. The output statistics will be tabulated in the Attribute Table, which can then be exported as a worksheet file and/or viewed in map format.

Clip transects
--------------

By default, the transects are not clipped to the farthest shoreline extent. However, you have the power to choose whether to clip the shorelines by checking this box. The clipping has no effects on the statistics, but it will make seeing statistics' transects easier.

.. _tab_shoreline_change_tsi:

Transect-shoreline intersections
================================

.. _figure_tab_shoreline_change_transect_shorelines_intersections:

.. figure:: /img/shoreline_change/shoreline-change-tab-transect-shorelines-intersections.png
   :align: center
   :alt: Transects-shoreline intersections in Shoreline Change Tab

   Transect-shoreline intersections section in Shoreline Change Tab

.. _figure_transects_shoreline_intersections:

.. figure:: /img/shoreline_change/transects-shorelines-intersections.png
   :align: center
   :alt: Guide on determining the intersection point of transects and shorelines

   Guide on determining the intersection point of transects and shorelines
  
Sometimes, a transect intersects the shoreline vector at more than one point, particularly on curved segments (:numref:`figure_transects_shoreline_intersections`). To handle shoreline vector/s with multiple intersections, QSCAT allows you to choose the intersection point by distance (i.e., farthest or closest to the baseline) or by placement (seaward or landward, similar to DSAS). As it will affect the distance between the intersection points at the baseline and the shoreline, it is recommended that the selected option be applied to all shorelines for analysis.

.. _tab_shoreline_change_scs:

Shoreline change statistics
===========================

.. _figure_tab_shoreline_change_statistics:

.. figure:: /img/shoreline_change/shoreline-change-tab-shoreline-change-statistics.png
   :align: center
   :alt: Shoreline change statistics in Shoreline Change Tab

   Shoreline change statistics section in Shoreline Change Tab

The shoreline change statistics in QSCAT and the resulting sample attribute table (:numref:`table_shoreline_change_statistics`) are described below. 

.. _table_shoreline_change_statistics:

.. list-table:: Shoreline change statistics acronyms
   :header-rows: 1
   :widths: 20 80

   * - Statistics
     - Description
   * - ``SCE``
     - Shoreline Change Envelope
   * - ``NSM``
     - Net Shoreline Movement
   * - ``EPR``
     - End-Point Rate
   * - ``EPR_unc``
     - Uncertainty of End-Point Rate
   * - ``LRR``
     - Linear Regression Rate
   * - ``LR2``
     - R-Squared of Linear Regression
   * - ``LSE``
     - Standard Error of Linear Regression
   * - ``LCI``
     - Confidence Interval of Linear Regression
   * - ``WLR``
     - Weighted Linear Regression Rate
   * - ``WR2``
     - R-Squared of Weighted Linear Regression 
   * - ``WSE``
     - Standard Error of Weighted Linear Regression
   * - ``WCI``
     - Confidence Interval of Weighted Linear Regression


Shoreline Change Envelope (SCE)
-------------------------------

The shoreline change envelope (SCE) is the maximum distance, in meters (m), among all the shorelines intersecting a given transect :cite:p:`2018:dsasv5`. If there are multiple shoreline vectors, one can quickly identify the most significant magnitude of shoreline movement (``SCE_value`` column) and when it occurred (``SCE_closest`` year and ``SCE_farthest`` year columns) in the resulting attribute table of shoreline change statistics (:numref:`table_shoreline_change_statistics`). Since SCE is a distance, all values are positive. The shoreline trends can be inferred from the ``SCE_trend`` column, depending on whether SCE represents erosion, accretion, or stability. 

.. math::
   
   SCE = farthest\_year\_distance - closest\_year\_distance


Net Shoreline Movement (NSM)
----------------------------

The net shoreline movement (NSM) represents the magnitude of shoreline change between the oldest and youngest shorelines in meters (m) and is calculated as:

.. math::

   NSM = oldest\_year\_distance - newest\_year\_distance

The uncertainty is based on the shoreline with the largest uncertainty values in the attribute table of the input layer.


End-Point Rate (EPR)
--------------------

The end-point rate (``EPR``) is the rate of change based on ``NSM``, in meters/year (m/y), and is calculated as:

.. math::
   EPR = \frac{NSM}{newest\_shoreline\_year - oldest\_shoreline\_year}

Both ``NSM`` and ``EPR`` require only two shoreline vectors, the youngest and oldest. QSCAT will ignore any shoreline vector/s between the youngest and oldest years. As such, it provides no information about shoreline movement during the intervening years, even if there are multiple shoreline positions in the input layer. Additional information may be inferred from the ``SCE``, which can at least identify the greatest magnitude of change and the corresponding period for a given set of shoreline vectors.          


Linear Regression Rate (LRR)
----------------------------
For multiple shoreline positions, a more appropriate rate-of-change statistic to use is the linear regression rate-of-change (LRR) since it takes into consideration all shoreline positions in the calculation, not just the endpoints like NSM and EPR do. In fact, LRR requires at least three (3) shoreline vectors or intersection points to calculate the rate of change, in m/y, for a given transect. LRR is determined from the slope of a least-squares regression line fitted to all shoreline intersection points for each transect.

.. math::
   LRR = \frac{\sum_{i=1}^{n} (x_i - \bar{x})*(y_i - \bar{y})}{\sum_{i=1}^{n} (x_i - \bar{x})*(x_i - \bar{x})}

where:

- :math:`n` - length of years and distances
- :math:`\bar{x}` - mean of years
- :math:`\bar{y}` - mean of distances
- :math:`x_i` - i\ :sup:`th` year
- :math:`y_i` - i\ :sup:`th` distance


Weighted Linear Regression (WLR)
--------------------------------

In WLR, uncertainty values are converted to weights:

.. math::
   weight = \frac{1}{e^2}

where:

- :math:`e` - uncertainty value of a shoreline

Then, a weighted linear regression is performed using the weights. The resulting slope is the WLR:

.. math::
   WLR = \frac{\sum_{i=1}^{n} (x_i - \bar{x}_w)*(y_i - \bar{y}_w)*weight_i}{\sum_{i=1}^{n} (x_i - \bar{x}_w)^2 * weight_i}

where:

- :math:`n` - length of years and distances
- :math:`\bar{x}_w` - weighted mean of years
- :math:`\bar{y}_w` - weighted mean of distances
- :math:`x_i` - i\ :sup:`th` year
- :math:`y_i` - i\ :sup:`th` distance
- :math:`weight_i` - i\ :sup:`th` weight


Supplementary Statistics
------------------------

Uncertainty of End-Point Rate (EPR_unc)
........................................

The uncertainty of EPR (``EPR_unc``) is based on the following formula, after DSAS :cite:p:`2018:dsasv5`:

.. math::
   EPR\_unc = \frac{{\sqrt{{(uncyA)^2 + (uncyB)^2}}}}{yearA - yearB}

where:

- :math:`uncyA` - uncertainty of the youngest shoreline A
- :math:`uncyB` - uncertainty of the oldest shoreline B
- :math:`yearA` - year of youngest shoreline A
- :math:`yearB` - year of oldest shoreline B

.. _supplementary_statistics:


R-Squared of Linear Regression (LR2 or WR2)
...........................................

.. math::
   LR2\ or\ WR2 = 1 - \sqrt{\frac{\sum_{i=1}^{n} (y_i-\hat{y}_i)^2}{\sum_{i=1}^{n} (y_i-\bar{y})^2}}

where:

- :math:`n` - length of years and distances
- :math:`\hat{y}` - predicted i\ :sup:`th` distance (:math:`LRR\ or\ WLR*x_i + intercept`)
- :math:`\bar{y}` - mean of distances
- :math:`y_i` - actual i\ :sup:`th` distance


Standard Error of Estimate of Linear Regression (LSE or WSE)
............................................................

.. math::
   LSE\ or\ WSE  = \sqrt{\frac{\sum_{i=1}^{n} (y_i-\hat{y}_i)^2}{n-2}}

where:

- :math:`n` - length of years and distances
- :math:`\hat{y}` - predicted i\ :sup:`th` distance (:math:`LRR\ or\ WLR*x_i + intercept`)
- :math:`y_i` - actual i\ :sup:`th` distance


Confidence Interval of Linear Regression (LCI or WCI)
......................................................

.. math::
   LCI\ or\ WCI  = t\_inv(n-2,\ 1-\alpha/2) *  \sqrt{\frac{LSE^2\ or\ WSE^2}{\sum_{i=1}^{n}(x_i-\bar{x})^2}}

where:

- :math:`\alpha` - :math:`1 - (confidence\_interval*.01)` (confidence interval in percent)
- :math:`t\_inv()` - student's t-distribution function
- :math:`LSE` - standard error of estimate of linear regression
- :math:`WSE` - standard error of estimate of weighted linear regression
- :math:`n` - length of years and distances
- :math:`\bar{x}` - mean of years
- :math:`x_i` - i\ :sup:`th` year

.. _tab_shoreline_change_pcs:

Pairwise comparison of shorelines
=================================

.. figure:: /img/shoreline_change/shoreline-change-tab-pairwise-comparison-of-shorelines.png
   :align: center
   :alt: Pairwise comparison of shorelines in Shoreline Change Tab

   Pairwise comparison of shorelines in Shoreline Change Tab

By default, NSM and EPR calculate the magnitude and rate of shoreline changes between the oldest and most recent shorelines, even if multiple shorelines are available. In QSCAT, the algorithm for calculating NSM and EPR can be applied to any two shorelines from the selected shoreline layer by specifying the dates of the two shorelines for comparison. While LRR can estimate the net rate of change among multiple shorelines, the pairwise comparison can better understand how the shoreline has evolved over different periods, as well as the possible causes of the observed trends.


.. _tab_shoreline_change_additional_parameters:

Additional parameters
=====================

.. figure:: /img/shoreline_change/shoreline-change-tab-additional-parameters.png
   :align: center
   :alt: Additional parameters in Shoreline Change Tab

   Additional parameters section in Shoreline Change Tab

Currently, additional parameters include a field that defines the confidence interval value for calculating LCI and WCI. The default value is 99.7%, based on DSAS :cite:p:`2018:dsasv5`.


.. _tab_shoreline_change_vector_layer_output_name:

Vector layer output
===================

Layers
------

.. list-table:: 
   :header-rows: 1
   :widths: 30 20 50

   * - Layer
     - Geometry
     - Name
   * - ``SCE``
     - ``LineString``
     - ``SCE [<datetime>]``
   * - ``NSM``
     - ``LineString``
     - ``NSM (newest_year - oldest_year) [<datetime>]``
   * - ``EPR, EPR_unc``
     - ``LineString``
     - ``EPR (newest_year - oldest_year) [<datetime>]``
   * - ``LRR, LR2, LSE, LCI``
     - ``LineString``
     - ``LRR [<datetime>]``
   * - ``WLR, WR2, WSE, WCI``
     - ``LineString``
     - ``WLR [<datetime>]``


Attributes
----------

Shoreline Change Envelope (SCE)
...............................

.. list-table:: 
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``SCE``
     - ``double``
     - Shoreline Change Envelope (SCE) value in meters.
   * - ``SCE_highest_unc``
     - ``double``
     - The highest uncertainty value used in the calculation of SCE.
   * - ``SCE_trend``
     - ``string``
     - Trends (stable, erosion, or accretion) based on SCE and uncertainty value. 
   * - ``SCE_closest_year``
     - ``integer``
     - Shoreline year closest to the baseline.
   * - ``SCE_farthest_year``
     - ``integer``
     - Shoreline year farthest from the baseline.


Net Shoreline Movement (NSM)
............................

.. list-table:: 
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``NSM``
     - ``double``
     - Net Shoreline Movement (NSM) value in meters.
   * - ``NSM_highest_unc``
     - ``double``
     - The highest uncertainty value used in the calculation of NSM.
   * - ``NSM_trend``
     - ``string``
     - Trends (stable, erosion, or accretion) based on NSM and uncertainty value.


End-Point Rate (EPR)
....................

.. list-table:: 
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``EPR``
     - ``double``
     - End-Point Rate (EPR) value in meters/year.
   * - ``EPR_unc``
     - ``double``
     - Uncertainty of End-Point Rate (EPR) value in meters/year.
   * - ``EPR_trend``
     - ``string``
     - Trends (stable, erosion, or accretion) based on EPR and uncertainty value.


Linear Regression Rate (LRR)
............................

.. list-table:: 
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``LRR``
     - ``double``
     - Linear Regression Rate (LRR) value in meters/year.
   * - ``LR2``
     - ``double``
     - R-Squared of Linear Regression (LR2) value.
   * - ``LSE``
     - ``double``
     - Standard Error of Linear Regression (LSE) value.
   * - ``LCI``
     - ``double``
     - Confidence Interval of Linear Regression (LCI) value.


Weighted Linear Regression (WLR)
................................

.. list-table:: 
   :header-rows: 1
   :widths: 15 15 70

   * - Field name
     - Data type
     - Description
   * - ``WLR``
     - ``double``
     - Weighted Linear Regression Rate (WLR) value in meters/year.
   * - ``WR2``
     - ``double``
     - R-Squared of Weighted Linear Regression (WR2) value.
   * - ``WSE``
     - ``double``
     - Standard Error of Weighted Linear Regression (WSE) value.
   * - ``WCI``
     - ``double``
     - Confidence Interval of Weighted Linear Regression (WCI) value.