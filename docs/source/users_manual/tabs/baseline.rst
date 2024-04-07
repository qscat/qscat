.. _tab_baseline:

*************
Tab: Baseline
*************

.. only:: html

   .. contents::
      :local:
      :depth: 2

.. _tab_baseline_parameters:
   
Baseline Parameters
===================

The input layer is the ``Baseline`` created in :ref:`generating_the_baseline_vectors`.

.. _tab_baseline_placement:

Baseline Placement
==================

After selecting the baseline layer, the next step is to choose the baseline placement. This selection determines whether the baseline is positioned sea (offshore) or land (onshore). The baseline placement defines the direction of the transects when casting. Additionally, the placement also determines the signs of magnitude values whether it is eroding or accreting. If the selected baseline placement is seaward or offshore (landward or onshore), the transects will be cast from the sea to the land (or land to the sea) as shown in :numref:`figure_baseline_placement`.

.. _figure_baseline_placement:

.. figure:: /img/baseline/baseline-placement.png
   :align: center
   
   Baseline placement.

.. _tab_baseline_orientation:

Baseline Orientation
====================

In addition to baseline placement, another important parameter is baseline orientation, which determines the relative position of the land with respect to the drawn or digitized baseline. It specifies whether the land is on the right or left side of the baseline orientation. To assist in selecting the appropriate orientation, :numref:`figure_baseline_orientation` illustrates different scenarios based on the direction of the baseline vector. In ``QSCAT``, users can enable the |checkbox| :guilabel:`Show baseline orientation` option, which adds arrows indicating the direction of the baseline vector.

.. _figure_baseline_orientation:

.. figure:: /img/baseline/baseline-orientation.png
   :align: center
   
   Guide for determining the appropriate baseline orientation.

Both the baseline placement and orientation are crucial in determining the direction of transect casting. Additionally, they play a significant role in correctly assigning the sign (+ or -) to the calculated magnitude and rate of shoreline changes. This ensures that the interpretation of shoreline change data accurately represents whether there is erosion (negative value) or accretion (positive value) occurring.


.. |checkbox| image:: /img/checkbox.png
   :width: 1.0em