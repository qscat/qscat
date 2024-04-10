.. _tab_transects:

***************
Tab: Transects
***************

.. only:: html

   .. contents::
      :local:
      :depth: 2

The :menuselection:`Transects Tab` allows the user to cast transects based on the baseline.

.. _figure_tab_transects:

.. figure:: /img/transects/transects-tab.png
   :align: center

   User interface of Transects tab.

* Transects will be cast perpendicular to the baseline.
* Shoreline change statistics are calculated on each transect within each shoreline intersection point.
* Transects are numbered following the baseline orientation; if the baseline is oriented from north to south, the transect number also starts from the north.
* The following subsections describe several parameters needed for transect casting, such as transect count, length, and smoothing distance value. 

Layer
=====

.. figure:: /img/transects/transects-tab-layer.png
   :align: center

   Layer section in Transects tab.

Layer output name
-----------------

This is the name that will be prefixed on the name of vector layer.


.. _tab_transects_count:

Count
=====

.. figure:: /img/transects/transects-tab-count.png
   :align: center

   Count section in Transects tab.

This section allows the user to determine the number of transects for casting by transect spacing or the number of transects.

By transect spacing
-------------------

.. _figure_transect_spacing:

.. figure:: /img/transects/transects-spacing.png
  :align: center
   
  Transect spacing.

Based on a user-defined spacing or interval between transects, in meters, this automatically calculates the number of transects to be cast.

By number of transects
----------------------

.. _figure_transects_count:

.. figure:: /img/transects/transects-count.png
  :align: center
   
  Number of transects.

Based on the user-defined number of transects, QSCAT estimates the appropriate spacing between transects for a particular baseline.

In DSAS, the number of transects to be cast depends on the scale of the data and the intended scale of output rate information :cite:p:`2018:dsasv5`. It has been observed that the casting of transects in DSAS takes more time as the transect spacing becomes smaller. In QSCAT, the speed at which transects are cast does not differ significantly with varying transect spacing. A 10-m transect spacing applied to a nearly linear 94-km coastline of La Union took about 5-10 minutes in QSCAT and about 30-45 minutes in DSAS.   


.. _tab_transects_parameters:

Parameters
==========

.. figure:: /img/transects/transects-tab-parameters.png
   :align: center

   Parameters section in Transects tab.

Other important parameters are the transect length and smoothing distance value to ensure the transects are oriented perpendicular to the baseline.

.. _tab_transects_parameters_length:

Transect length
---------------

.. _figure_transect_length:

.. figure:: /img/transects/transects-length.png
  :align: center
   
  Transects length.

DSAS uses the term search distance, which is the distance (in meters) that DSAS uses to search for intersection points from the baseline to the shoreline vectors along a transect. The baseline will be the starting point for calculating distances. As depicted in :numref:`figure_transect_length`, the concept of search distance is similar to transect length. Thus, in QSCAT, search distance is referred to as transect length. 

Intuitively, the transect length should be long enough to intersect all shoreline vectors to be analyzed. To approximate this length, a user can estimate the distance between the baseline and the shoreline farthest from it and use the maximum value as the transect length. As such, a single transect length may not apply to the entire coastline due to varying magnitudes of change and the curvature of the coast itself. On embayed coasts, the longer the transect, the greater the possibility of transects intersecting one another, particularly on curved coastal segments. In such cases, a variable transect length should be implemented. Where a variable transect length is more suitable, it is advisable to segmentize the shoreline and baseline (**see Section 3.1**) before running QSCAT.

Smoothing distance
------------------

Smoothing distance is applied to the baseline to ensure that the cast transects will be oriented perpendicular to the baseline. Smoothing is needed, particularly on curvy or embayed shorelines, to prevent the transects from intersecting one another along the curved section of the coast :cite:p:`2018:dsasv5`. In the DSAS v5 manual :cite:p:`2018:dsasv5`, the following guidelines were provided:

#. For a curvy or sinuous coastline, the smoothing distance should be longer than the width of the bends in the shoreline. 
#. The smoothing distance should not be too large to produce a nearly linear (or overly smoothed) baseline and generate transects that are oriented almost parallel to the baseline.
#. The recommended smoothing distance is 500 m but should be at most 2500 m. 
#. However, It is recommended that the user experiment using different smoothing distances until the transects become oriented perpendicular to the baseline. Figure 19 in the DSAS v5 manual demonstrates several smoothing examples to guide the user in selecting the appropriate smoothing distance :cite:p:`2018:dsasv5`. :numref:`figure_transects_smoothing_distance` shows how the smoothing procedure is being implemented in both QSCAT and DSAS.

.. _figure_transects_smoothing_distance:

.. figure:: /img/transects/transects-smoothing-distance.png
   :align: center
  
   Smoothing distance calculation.

   A smoothing applied to a single transect with 200 meters distance. First, the baseline traverses half the distance on both left and right. Second, the two points are connected, which will be the baseline where the smooth transect will be cast perpendicularly.


.. _tab_transects_vector_layer_output_name:

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
   * - Transects
     - ``LineString``
     - ``<baseline layer name>_transects [<datetime>]``