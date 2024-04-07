.. index:: Example Summary Report
.. _appendices_example_summary_report:

Appendix 1: Example Summmary Report
===================================

Shoreline Change Statistic
--------------------------

.. code-block:: 

    [Author]
    Name: Last name, First name Middle Name
    Affiliation: xx
    Email: xx

    [System]
    Time generated: dd/mm/yyyy hh:mm:ss
    QGIS version: 3.22.6
    QSCAT version: v1.0.0beta

    [Input]
    [Shorelines]
    Layer: xxx
    Default uncertainty: xx
    Date field: xxx
    Dates: 01/2018, 01/2022, 01/2022
    Uncertainty field: xxx
    Uncertainty: 25.0, 25.0, 15.0

    [Baseline]
    Layer: xxx
    Placement: (sea or offshore|land or onshore)
    Orientation: (land is to the R|land is to the L)

    [Transects]
    Name: xxx
    Total number of transects
    Number of transects with negative distance
    By (transect spacing|number of transects): xx meters
    Search distance: xx meters
    Smoothing distance: xx meters
    Intersection by (distance/placement): (farthest|closest|seaward|landward)
    Clip transects: yes
    Include intersections layer: yes

    [Statistics]
    Layer: xx
    Statistics: SCE, NSM, EPR
    Newest date: mm/yyyy
    Oldest date: mm/yyy

    Area layer: xxx
    Area NSM layer: xxx

    [Visualization-not included?]

    [Results]
    Total number of transects: xxx
    ………………..
    SCE:


Area Change Statistic
---------------------

.. code-block:: 
    
  [PROJECT DETAILS]

    GENERAL:
    Time generated: 04-07-24 01-20-12
    Project location: /home/louis/Desktop

    PROJECTION:
    CRS auth id: EPSG:32651

    AUTHOR:
    Full name: Louis Facun
    Affiliation: Science Research Assistant
    Email: louisfacun@gmail.com

    [SYSTEM DETAILS]

    OS version: Linux 6.5.0-18-generic
    QGIS version: 3.22.16-Białowieża
    QSCAT version: 1.0.0

    [INPUT PARAMETERS]

    AREA:
    NSM layer: EPR (2023.0-1977.0) [04-07-24 01-19-01]
    Polygon area layer: area

    [SUMMARY OF RESULTS]

    AREA:

    Total area: 1691336.08

    Erosion:
    Total of areas: 739196.44
    (%) of areas: 43.70%
    No. of areas: 2
    (%) of no. of areas: 25.00%
    Avg. value: 92399.56
    Max. value: 730310.57
    Min. value: 8885.87

    Accretion:
    Total of areas: 952095.96
    (%) of areas: 56.29%
    No. of areas: 4
    (%) of no. of areas: 50.00%
    Avg. value: 119012.0
    Max. value: 362910.93
    Min. value: 34011.15

    Stable:
    Total of areas: 43.67
    (%) of areas: 0.00%
    No. of areas: 2
    (%) of no. of areas: 25.00%
    Avg. value: 5.46
    Max. value: 36.13
    Min. value: 7.54

    SHORELINE (LENGTH):

    Total shoreline (length): 5841.48

    Erosion:
    Total of lengths: 2087.88
    (%) of lengths: 35.74%
    No. of lengths: 2
    (%) of no. of lengths: 25.00%
    Avg. value: 260.98
    Max. value: 1960.68
    Min. value: 127.19

    Accretion:
    Total of lengths: 3611.35
    (%) of lengths: 61.82%
    No. of lengths: 4
    (%) of no. of lengths: 50.00%
    Avg. value: 451.42
    Max. value: 1608.24
    Min. value: 486.16

    Stable:
    Total of lengths: 142.25
    (%) of lengths: 2.44%
    No. of lengths: 2
    (%) of no. of lengths: 25.00%
    Avg. value: 17.78
    Max. value: 106.12
    Min. value: 36.13


Forecasting
-----------