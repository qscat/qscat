.. _tab_transects:

***************
Tab: Transects
***************

.. only:: html

   .. contents::
      :local:
      :depth: 2

The next step is the casting of transects, which is described below:

#. Transects should be cast perpendicular to the baseline.
#. Transects will be cast only if there are no gaps in the baseline and/or shoreline vectors. Any gap in the baseline will result in processing error. 
#. The calculation of shoreline change statistics is carried out on each transect at the intersection points with the baseline and shorelines. 
#. Transects are numbered following the baseline orientation; if the baseline is oriented from north to south, the transect number also starts from the north.
#. Several parameters are needed for transect casting such as transect count, transect length and smoothing parameters, which are  described in the following subsections. 

Transects Storage Parameters
============================

Layer output name
-----------------

*Content for this section will be added soon.*

Transect Count
==============

This step allows the user to determine the number of transects for casting, in terms of:

Transect spacing
----------------

.. _figure_transect_spacing:

.. figure:: /img/transects/transects-spacing.png
  :align: center
   
  Transect Spacing.

Based on user-defined spacing or interval between transects, in meters. This automatically calculates the number of transects to be cast.

Number of transects
-------------------

.. _figure_transects_count:

.. figure:: /img/transects/transects-count.png
  :align: center
   
  Number of transects.

Based on the user-defined number of transects while ``QSCAT`` estimates the appropriate spacing between transects for a particular baseline.

In ``DSAS``, the number of transects to be cast depends on the scale of the data, and the intended scale of output rate information :cite:p:`2018:dsasv5`. It has been observed that casting of transects in ``DSAS`` takes more time as the transect spacing becomes smaller. In ``QSCAT``, the speed at which transects are cast do not differ significantly with varying transect spacing. A 10-m transect spacing applied to a nearly linear 94-km coastline of La Union took about 5-10 minutes in ``QSCAT`` while it took about 30-45 minutes in ``DSAS``.   

Transect Parameters
===================

Other important parameters are the transect length and smoothing distance to ensure that the transects are oriented perpendicular  to the baseline.

.. _tab_transects_parameters_length:

Transect length
---------------

.. _figure_transect_length:

.. figure:: /img/transects/transects-length.png
  :align: center
   
  Transects length.

``DSAS`` uses the term search distance, which is the distance (in meters) that ``DSAS`` uses to search for intersections points from the baseline to the shoreline vectors along a transect (Fig. X). The baseline will be the starting point for the calculation of distances.  As depicted in :numref:`figure_transect_length`, the concept of search distance is similar to transect length. Thus, in ``QSCAT``,  search distance is simply referred to as transect length. 

Intuitively, the transect length should be long enough to intersect all shoreline vectors to be analyzed. To approximate this length, a user can estimate the  distance between the baseline and the shoreline farthest from it, and use the maximum value as the transect length. As such, a single transect length may not be applicable to the entire coastline due to varying magnitudes of change, and the curvature of the coast itself. On embayed coasts, the longer the transect, the greater is the possibility of transects intersecting one another particularly on  curved coastal segments. In such cases, a variable transect length should be implemented. Where a variable transect length is more suitable, it is advisable to segmentize the shoreline and baseline (**see Section 3.1**) prior to running ``QSCAT``.

Smoothing distance
------------------

The next step is to specify the smoothing distance to be applied to the baseline to ensure that the cast transects will be oriented perpendicular to the baseline. Smoothing is needed particularly on curvy or embayed shorelines to prevent the transects from intersecting one another along the curved section of the coast :cite:p:`2018:dsasv5`. In the ``DSAS`` v5 manual :cite:p:`2018:dsasv5`, the following guidelines were provided:

#. For curvy or sinuous coastline, the smoothing distance should be longer than the width of the bends in the shoreline. 
#. The smoothing distance should not be too large to produce a nearly linear (or overly smoothed) baseline and generate transects that are oriented almost parallel to the baseline (Fig. X). 
#. The recommended smoothing distance is 500 m but should not be more than 2500 m. 
#. It is recommended, however, that the user experiment on using different smoothing distances until the transects become oriented perpendicular to the baseline. ``Figure 19`` in the ``DSAS`` v5 manual demonstrates several smoothing examples to guide the user in selecting the appropriate smoothing distance :cite:p:`2018:dsasv5`. :numref:`figure_transects_smoothing_distance` shows how the smoothing procedure is being implemented in both ``QSCAT`` and ``DSAS``.

.. _figure_transects_smoothing_distance:

.. figure:: /img/transects/transects-smoothing-distance.png
   :align: center
  
   Transects-Shoreline Intersections.

   A smoothing applied to a single transect with 200 meters distance. First, the baseline is traversed half the distance both left and right. Second, the two points are connected that will be the baseline where the smooth transect will be cast perpendicularly.
  

Transect-Shoreline Intersections
================================

.. _figure_transects_shoreline_intersections:

.. figure:: /img/transects/transects-shorelines-intersections.png
   :align: center
  
   Transects-Shoreline Intersections.
  
In some cases, a transect intersects the shoreline vector at more than one point particularly on curved segments (:numref:`figure_transects_shoreline_intersections`). To handle shoreline vector/s with multiple intersections, ``QSCAT`` allows the user to choose the intersection point by distance (i.e., farthest or closest to the baseline) or by placement (seaward or landward, similar to ``DSAS``). As it will affect the distance between the intersection points at the baseline and the shoreline, it is recommended that the selected option be applied to all shorelines for analysis.

Transect Output
===============

By default, the transects are clipped to the farthest shoreline extent, and the shoreline intersections are shown on the transects. The user can choose not to view these by unclicking the selection on the transect output.

Clip transects to shoreline extent
----------------------------------

*Content for this section will be added soon.*

Include intersections layers
----------------------------

*Content for this section will be added soon.*

.. _tab_transects_output_layer_names:

Output Layer Names
------------------

.. list-table:: 
   :header-rows: 1
   :widths: 20 80

   * - Type
     - Name
   * - Transects
     - ``<baseline layer name>_transects [<datetime>]``
   * - Intersections
     - ``<baseline layer name>_intersections [<datetime>]``