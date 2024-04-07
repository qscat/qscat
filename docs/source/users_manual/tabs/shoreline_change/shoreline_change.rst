.. index:: Shoreline Change Statistics

Shoreline Change Statistics
===========================

.. only:: html

   .. contents::
      :local:

The four shoreline change statistics available in QSCAT and the resulting sample attribute table (Table X) are described below. 

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

The shoreline change envelope (SCE) is the maximum distance, in meters (m), among all the shorelines that intersect a given transect :cite:p:`2018:dsasv5`. If there are multiple shoreline vectors, one can easily identify the greatest magnitude of shoreline movement (``SCE_value`` column) and when it occurred (``SCE_closest`` year and ``SCE_farthest`` year columns) in the resulting attribute table of shoreline change statistics (Table X). Since SCE is a distance, all values are positive. The shoreline trends can be inferred from the ``SCE_trend`` column, whether SCE represents erosion, accretion or stability. 

.. math::
   
   SCE = farthest\_year\_distance - closest\_year\_distance

Net Shoreline Movement (NSM)
----------------------------

The net shoreline movement (NSM) represents the magnitude of shoreline change between the oldest and youngest shorelines in meters (m), and is calculated as:

.. math::

   NSM = oldest\_year\_distance - newest\_year\_distance

The uncertainty is based on the shoreline with largest uncertainty values in the attribute table of the input layer. 

End-Point Rate (EPR)
--------------------

The end-point rate (``EPR``) is the rate of change based on ``NSM``, in meters/year (m/y), and is calculated as:

.. math::
   EPR = \frac{NSM}{newest\_shoreline\_year - oldest\_shoreline\_year}

Both ``NSM`` and ``EPR`` require only two shoreline vectors, i.e., the youngest and oldest shoreline vectors. QSCAT will ignore any shoreline vector/s between the youngest and oldest years. As such, it provides no information about shoreline movement during the intervening years even if there are multiple shoreline positions in the input layer. Additional information may be inferred from the ``SCE``, which can at least identify the greatest magnitude of change and the corresponding time period for a given set of shoreline vectors.      

Linear Regression Rate (LRR)
----------------------------
For multiple shoreline positions, a more appropriate rate-of-change statistic to use is the Linear Regression Rate-of-change (LRR) since it takes into consideration all shoreline positions in the calculation, not just the endpoints like what NSM and EPR do. In fact, LRR requires at least three (3) shoreline vectors, or intersection points to calculate the rate of change, in m/y, for a given transect. LRR is determined from the slope of a least-squares regression line fitted to all shoreline intersection points for each transect. 

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

xx

.. math::
   LR2\ or\ WR2 = 1 - \sqrt{\frac{\sum_{i=1}^{n} (y_i-\hat{y}_i)^2}{\sum_{i=1}^{n} (y_i-\bar{y})^2}}

where:

- :math:`n` - length of years and distances
- :math:`\hat{y}` - predicted i\ :sup:`th` distance (:math:`LRR\ or\ WLR*x_i + intercept`)
- :math:`\bar{y}` - mean of distances
- :math:`y_i` - actual i\ :sup:`th` distance

Standard Error of Estimate of Linear Regression (LSE or WSE)
............................................................

xx

.. math::
   LSE\ or\ WSE  = \sqrt{\frac{\sum_{i=1}^{n} (y_i-\hat{y}_i)^2}{n-2}}

where:

- :math:`n` - length of years and distances
- :math:`\hat{y}` - predicted i\ :sup:`th` distance (:math:`LRR\ or\ WLR*x_i + intercept`)
- :math:`y_i` - actual i\ :sup:`th` distance

Confidence Interval of Linear Regression (LCI or WCI)
......................................................

xx

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

Output Layer Names
------------------

.. list-table:: 
   :header-rows: 1
   :widths: 20 80

   * - Statistic
     - Name
   * - :menuselection:`ALL`
     - ``<baseline layer name>_Stats [<datetime>]``
   * - ``SCE``
     - ``<baseline layer name>_SCE [<datetime>]``
   * - ``NSM``
     - ``<baseline layer name>_NSM (newest_year - oldest_year) [<datetime>]``
   * - ``EPR, EPR_unc``
     - ``<baseline layer name>_EPR (newest_year - oldest_year) [<datetime>]``
   * - ``LRR, LSE, LCI``
     - ``<baseline layer name>_LRR [<datetime>]``
   * - ``WLR, WSE, WCI``
     - ``<baseline layer name>_WLR [<datetime>]``