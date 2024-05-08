.. _plugin_required_inputs:

***************
Required Inputs
***************

.. only:: html

   .. contents::
      :local:
      :depth: 3

To use this plugin, you only need these two vector layers:

#. **Shorelines layer:** Vectors of shoreline positions for different years; and 
#. **Baseline layer:** Vector that serves as a starting point for all transects cast by QSCAT :cite:p:`2018:dsasv5`.

.. _plugin_required_inputs_shorelines:

Shorelines layer
================

The first primary data required in QSCAT is the shoreline, or roughly the boundary between land and water. In practice, the shoreline is not usually taken as the waterline, or the boundary between land and sea due to tides. Owing to tidal fluctuation, the shoreline can be anywhere between the low-tide line (LTL) and high-tide line (HTL). In many cases, high water features such as high-tide line (HTL), continuous scarps, or the vegetation line are used as shoreline proxies to minimize the effects of tides and at the same time, take into account the net effect of high-wave energy events such as storms on a coastline.

.. _preparing_the_shoreline_vectors:

Shoreline vectors preparation
-----------------------------

Shoreline data can be acquired through mapping using a handheld GPS unit, or traced on topographic maps, satellite images, and aerial photographs. The methods for extracting the shoreline on topographic map, and satellite images are discussed in detail in the accompanying **Manual on Shoreline Change Analysis** (to be shared soon). The shoreline vectors generated in this step will be the main input dataset to QSCAT.

Merged shoreline layers
-----------------------

If shoreline vectors are traced or gathered for each year and stored in separate layers, it is required to merge those shoreline layers into a single layer. See :ref:`others_sample_workflow_mergin_shorelines` in the :ref:`others_sample_workflow` for the steps on how to merge multiple shoreline layers into a single layer using QGIS.


Attribute fields and values
---------------------------

After merging, each feature in the shoreline layer should contain the necessary information for each shoreline, including the shoreline date and uncertainty. The table below illustrates the required attribute table for the shoreline layer and the format of the attribute values:


======================= ============ =========== ===========
Field                   Name         Data Type   Format
======================= ============ =========== ===========
QSCAT date field        ``any_name`` ``String``  ``mm/yyyy``
QSCAT uncertainty field ``any_name`` ``Decimal`` ``x.xx``
======================= ============ =========== ===========

.. note:: **Attribute fields and values**
    
    * You need to add the two fields with proper data type above.
    * The date value should be in the format ``mm/yyyy``. Ensure that the date is valid to avoid errors. Use ``mm`` for ``January`` such as ``01``.
    * The uncertainty field should be of decimal data type and follow the format ``x.xx``. However, if the uncertainty value is an integer, a decimal value is not required.
    * Editing the uncertainty value in the attribute table is optional but recommended. If it is not defined (``0`` or ``None``), the plugin will default to the uncertainty value defined in the :ref:`shorelines_parameters`.

.. tip:: **Automating attribute table**

   You can manually add the attribute table, but you can also automate the addition of the required attribute fields name and data types using the QSCAT :ref:`tab_automator_shorelines_fields` automator.

.. _plugin_required_inputs_baseline:

Baseline layer
==============

Another important input data is the baseline, a vector constructed that is parallel to and at a certain distance from the shoreline. Similar to DSAS, the baseline is the starting point for all shoreline change calculations to be made in QSCAT. It is not part of the QSCAT plugin but can be generated using QGIS or any GIS software with the same functionality.

.. _generating_the_baseline_vectors:
 
Baseline vectors creation
-------------------------

In QGIS, the creation of a baseline line vector involves the use of buffers and conversions. Initially, a buffer (in the form of a ``Polygon``) is generated around the merged shorelines layer. This buffer is then transformed into a ``LineString`` vector. Finally, you can choose which side of the ``LineString`` will serve as the designated baseline.

Buffer creation
...............

For creating buffer geometry, the following inputs are recommended:

======================================= ====================
Parameter                               Value
======================================= ====================
:guilabel:`Distance`                    ``<input_distance>``
:guilabel:`Segments`                    5
:guilabel:`End cap style`               Flat
:guilabel:`Join style`                  Round
|checkbox| :guilabel:`Dissolve results` Checked
======================================= ====================

.. tip:: **Automating baseline buffer and conversion**

   You can create buffers and convert the buffer to a line vector manually from :menuselection:`Processing --> Toolbox`. However, you can automate the process using QSCAT :ref:`tab_automator_baseline_buffer` automator.

Once the baseline buffer is created, you will need to manually designate the baseline side of the ``LineString`` in the next step. See :ref:`others_sample_workflow_converting_buffer_to_baseline` in the :ref:`others_sample_workflow` for the steps on how to convert the buffer to a line vector and designate the baseline side using QGIS.

.. _optional_multiple_baseline_vectors:

Optional multiple baseline vectors in one layer
-----------------------------------------------

This feature allows you to cast transects on single run with multiple baseline vector in one layer with different baseline placement and orientation, and transect length values. To use this feature, you need to add any of the fields you want to have a different value other than the values defined in Baseline Tab in the attribute table of the baseline layer using :ref:`tab_automator_baseline_fields` automator (or manually using QGIS).

Then, you should edit the field values with the following:

==================== =====================
Field                Values              
==================== =====================
baseline placement   ``sea`` or ``land``
baseline orientation ``left`` or ``right``
transect length      ``<any_number>``
==================== =====================

To know more about these values, please refer to the following: :ref:`tab_baseline_placement`, :ref:`tab_baseline_orientation` and :ref:`tab_transects_parameters_length` sections respectively.

.. warning:: Values such as ``sea``, ``land``, ``left`` and ``right`` are case-sensitive and should be written as is. If the values are not written as is, QSCAT will not recognize the values and will default to the values defined in the Baseline Tab.

.. |selectFeatures| image:: /img/action-select-features.png
   :width: 1.5em
.. |toggleEditing| image:: /img/action-toggle-editing.png
   :width: 1.5em
.. |splitFeatures| image:: /img/action-split-features.png
   :width: 1.5em

.. |checkbox| image:: /img/checkbox.png
   :width: 1.0em
.. |toolbox| image:: /img/toolbox.png
   :width: 1.3em