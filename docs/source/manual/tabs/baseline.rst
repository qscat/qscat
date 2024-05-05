.. _tab_baseline:

*************
Tab: Baseline
*************

The :guilabel:`Baseline Tab` allows you to configure the baseline by selecting the baseline layer, placement, orientation, and fields.

.. only:: html

   .. contents::
      :local:
      :depth: 2

.. _figure_tab_baseline:

.. figure:: /img/baseline/baseline-tab.png
   :align: center
   :alt: User interface of Baseline Tab

   User interface of Baseline Tab


.. _tab_baseline_layer:
   

Layer
=====

.. figure:: /img/baseline/baseline-tab-layer.png
   :align: center
   :alt: Baseline layer section Baseline Tab

   Baseline layer section in Baseline Tab


The input layer is the baseline created in :ref:`generating_the_baseline_vectors`.

.. _tab_baseline_placement:


Placement
=========

.. figure:: /img/baseline/baseline-tab-placement.png
   :align: center
   :alt: Baseline placement section in Baseline Tab

   Baseline placement section in Baseline Tab

After selecting the baseline layer, the next step is to choose the baseline placement. This selection determines whether the baseline is positioned sea (offshore) or land (onshore). The baseline placement defines the direction of the transects when casting. Additionally, the placement also determines the signs of magnitude values whether it is eroding or accreting. If the selected baseline placement is seaward or offshore (landward or onshore), the transects will be cast from the sea to the land (or land to the sea) as shown in :numref:`figure_baseline_placement`.

.. _figure_baseline_placement:

.. figure:: /img/baseline/baseline-placement.png
   :align: center
   :alt: Guide for determining the appropriate baseline placement
   
   Guide for determining the appropriate baseline placement

.. _tab_baseline_orientation:


Orientation
===========

.. figure:: /img/baseline/baseline-tab-orientation.png
   :align: center
   :alt: Baseline orientation section in Baseline Tab

   Baseline orientation section in Baseline Tab

In addition to baseline placement, another important parameter is baseline orientation, which determines the relative position of the land with respect to the drawn or digitized baseline. It specifies whether the land is on the right or left side of the baseline orientation. To assist in selecting the appropriate orientation, :numref:`figure_baseline_orientation` illustrates different scenarios based on the direction of the baseline vector. In QSCAT, you can enable or disable the :guilabel:`Show baseline orientation` option, which adds arrows, and "L" (left) and "R" (right) letter indicating the direction of the baseline vector.

.. _figure_baseline_orientation:

.. figure:: /img/baseline/baseline-orientation.png
   :align: center
   :alt: Guide for determining the appropriate baseline orientation

   Guide for determining the appropriate baseline orientation

Both the baseline placement and orientation are crucial in determining the direction of transect casting. Additionally, they play a significant role in correctly assigning the sign (+ or -) to the calculated magnitude and rate of shoreline changes. This ensures that the interpretation of shoreline change data accurately represents whether there is erosion (negative value) or accretion (positive value) occurring.


Fields (optional)
=================

.. figure:: /img/baseline/baseline-tab-fields.png
   :align: center
   :alt: Baseline fields section in Baseline Tab

   Baseline fields section in Baseline Tab

Allows you to optionally select fields of multi baseline layer.

.. |checkbox| image:: /img/checkbox.png
   :width: 1.0em