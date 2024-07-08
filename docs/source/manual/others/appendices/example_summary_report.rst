.. index:: Example Summary Reports
.. _appendices_example_summary_reports:

Appendix 2: Example Summary Reports
===================================

Shoreline Change
----------------

.. code-block:: 

  [PROJECT DETAILS]

  GENERAL:
  Time generated: 05-06-24 14-40-40
  Project location: /home/louis/Desktop/sca workspace/Agoo, La Union

  PROJECTION:
  CRS auth id: EPSG:32651

  AUTHOR:
  Full name: Louis Philippe Facun
  Affiliation: UP-MSI
  Email: louisfacun@gmail.com

  [SYSTEM DETAILS]

  OS version: Linux 6.5.0-18-generic
  QGIS version: 3.34.5-Prizren
  QSCAT version: 0.4.0

  [INPUT PARAMETERS]

  SHORELINES TAB:
  Layer: Shorelines Merged
  Default data uncertainty: 15
  Date field: qs_date
  Uncertainty field: qs_unc
  Dates: 01/1977, 03/1988, 05/2010, 04/2022
  Uncertainties: 25.00, 15.00, 15.00, 15.00

  BASELINE TAB:
  Layer: Baseline
  Placement: Sea or Offshore
  Orientation: Land is to the RIGHT

  TRANSECTS TAB:
  Layer output name: transects
  Transect count: By transect spacing
  Transect spacing: 50 meters
  Transect length: 2000 meters
  Smoothing distance: 500 meters

  SHORELINE CHANGE TAB:
  Transects layer: transects [05-06-24 14-40-37]
  Clip transects: Yes
  Intersections: Choose by distance
  By distance: Farthest
  Selected statistics: SCE, NSM, EPR, LRR, WLR
  Newest date: 04/2022
  Oldest date: 01/1977
  Newest year: 2022.25
  Oldest year: 1977.0
  Confidence interval: 99.7

  [SUMMARY OF RESULTS]

  Total no. of transects: 114

  SHORELINE CHANGE ENVELOPE (SCE):
  Avg. value: 123.74
  Max. value: 287.23
  Min. value: 75.06

  NET SHORELINE MOVEMENT (NSM):
  Avg. distance: -99.95:

  Eroding:
  No. of transects: 101
  (%) transects: 95.28 %
  Avg. value: -110.72
  Max. value: -41.98
  Min. value: -185.53

  Accreting:
  No. of transects: 4
  (%) transects: 3.77 %
  Avg. value: 148.9
  Max. value: 231.59
  Min. value: 50.06

  Stable:
  No. of transects: 1
  (%) transects: 0.94 %
  Avg. value: -7.46
  Max. value: -7.46
  Min. value: -7.46

  END POINT RATE (EPR):
  Avg. rate: -2.21

  Eroding:
  No. of transects: 101
  (%) transects: 95.28 %
  Avg. value: -2.45
  Max. value: -0.93
  Min. value: -4.1

  Accreting:
  No. of transects: 4
  (%) transects: 3.77 %
  Avg. value: 3.29
  Max. value: 5.12
  Min. value: 1.11

  Stable:
  No. of transects: 1
  (%) transects: 0.94 %
  Avg. value: -0.16
  Max. value: -0.16
  Min. value: -0.16

  LINEAR REGRESSION RATE (LRR):
  Eroding:
  No. of transects: 102
  (%) transects: 96.23 %
  Avg. value: -2.49
  Max. value: -0.32
  Min. value: -4.75

  Accreting:
  No. of transects: 4
  (%) transects: 3.77 %
  Avg. value: 3.64
  Max. value: 5.86
  Min. value: 1.05

  WEIGHTED LINEAR REGRESSION (WLR):
  Eroding:
  No. of transects: 101
  (%) transects: 95.28 %
  Avg. value: -2.26
  Max. value: -0.38
  Min. value: -5.02

  Accreting:
  No. of transects: 5
  (%) transects: 4.72 %
  Avg. value: 3.64
  Max. value: 6.87
  Min. value: 0.23



Area Change
-----------

.. code-block:: 
    
  [PROJECT DETAILS]

  GENERAL:
  Time generated: 05-06-24 14-40-45
  Project location: /home/louis/Desktop/sca workspace/Agoo, La Union

  PROJECTION:
  CRS auth id: EPSG:32651

  AUTHOR:
  Full name: Louis Philippe Facun
  Affiliation: UP-MSI
  Email: louisfacun@gmail.com

  [SYSTEM DETAILS]

  OS version: Linux 6.5.0-18-generic
  QGIS version: 3.34.5-Prizren
  QSCAT version: 0.4.0

  [INPUT PARAMETERS]

  AREA:
  Polygon layer: whole area
  Shoreline change statistic layer: NSM (2022.25-1977.0) [05-06-24 14-40-40]

  [SUMMARY OF RESULTS]

  AREA CHANGE:

  Total area: 591620.2

  Eroding:
  Total of areas: 558994.2
  (%) of areas: 94.49%
  No. of areas: 2
  (%) of no. of areas: 50.00%
  Avg. value: 139748.55
  Max. value: 548267.16
  Min. value: 10727.04

  Accreting:
  Total of areas: 31953.47
  (%) of areas: 5.40%
  No. of areas: 1
  (%) of no. of areas: 25.00%
  Avg. value: 7988.37
  Max. value: 31953.47
  Min. value: 31953.47

  Stable:
  Total of areas: 672.53
  (%) of areas: 0.11%
  No. of areas: 1
  (%) of no. of areas: 25.00%
  Avg. value: 168.13
  Max. value: 672.53
  Min. value: 672.53

  NEWEST SHORELINE (LENGTH):

  Total shoreline (length): 5382.12

  Eroding:
  Total of lengths: 5041.11
  (%) of lengths: 93.66%
  No. of lengths: 2
  (%) of no. of lengths: 50.00%
  Avg. value: 1260.28
  Max. value: 4887.51
  Min. value: 153.6

  Accreting:
  Total of lengths: 250.38
  (%) of lengths: 4.65%
  No. of lengths: 1
  (%) of no. of lengths: 25.00%
  Avg. value: 62.59
  Max. value: 250.38
  Min. value: 250.38

  Stable:
  Total of lengths: 90.63
  (%) of lengths: 1.68%
  No. of lengths: 1
  (%) of no. of lengths: 25.00%
  Avg. value: 22.66
  Max. value: 90.63
  Min. value: 90.63

  OLDEST SHORELINE (LENGTH):

  Total shoreline (length): 5382.56

  Eroding:
  Total of lengths: 4985.92
  (%) of lengths: 92.63%
  No. of lengths: 2
  (%) of no. of lengths: 50.00%
  Avg. value: 1246.48
  Max. value: 4846.75
  Min. value: 139.18

  Accreting:
  Total of lengths: 301.75
  (%) of lengths: 5.61%
  No. of lengths: 1
  (%) of no. of lengths: 25.00%
  Avg. value: 75.44
  Max. value: 301.75
  Min. value: 301.75

  Stable:
  Total of lengths: 94.89
  (%) of lengths: 1.76%
  No. of lengths: 1
  (%) of no. of lengths: 25.00%
  Avg. value: 23.72
  Max. value: 94.89
  Min. value: 94.89

  MEAN SHORELINE DISPLACEMENT:
  Avg. value: 77.23
  Max. value: 115.75
  Min. value: 7.25

Forecasting
-----------

*The Forecasting summary report is not yet available.*