.. _tab_visualization:

******************
Tab: Visualization
******************

.. only:: html

   .. contents::
      :local:
      :depth: 2

.. _figure_tab_visualization:

.. figure:: /img/visualization/visualization-tab.png
   :align: center

   User interface of Visualization Tab.

Layer
=====

Stat layer
----------

Accept layers:

* SCE
* NSM 
* EPR
* LRR
* WLR

Color Ramp
==========

Color ramp visualization uses PyQGIS to generate classification values based on mode and input stat layer.

Accept inputs:

#. # of Negative Classes (erosion values)
#. # of Positive Classes (accretion values)
#. Mode of classification

Generate outputs:

* SCE - stable, positive
* NSM, EPR - negative, stable, positive
* LRR, WLR - negative, positive


Modes
-----

*Content for this section will be added soon.*

Quantile
........

*Content for this section will be added soon.*

Equal Interval
...............

*Content for this section will be added soon.*

Natural Breaks (Jenks)
......................

*Content for this section will be added soon.*

Prettry Breaks
................

*Content for this section will be added soon.*