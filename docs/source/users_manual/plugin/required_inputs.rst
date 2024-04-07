.. _plugin_required_inputs:

***************
Required Inputs
***************

.. only:: html

   .. contents::
      :local:
      :depth: 3

To use this plugin, you only need these two vector layers:

#. **Shorelines layer:** vectors of shoreline positions for different years; and 
#. **Baseline layer:** vector that serves as a starting point for all transects cast by ``QSCAT`` :cite:p:`2018:dsasv5`.

.. _plugin_required_inputs_shorelines:

Shorelines Layer
================

The first primary data required in ``QSCAT`` is the :menuselection:`Shoreline`, or roughly the boundary between land and water. In practice, the shoreline is not usually taken as the `waterline`, or the boundary between land and sea due to tides. Owing to tidal fluctuation, the shoreline can be anywhere between the low-tide line (LTL) and high-tide line (HTL). In many cases, high water features such as high-tide line (HTL), continuous scarps, or the vegetation line are used as shoreline proxies to minimize the effects of tides and at the same time, take into account the net effect of high-wave energy events such as storms on a coastline.

.. _preparing_the_shoreline_vectors:

Preparing the shoreline vectors
-------------------------------

Shoreline data can be acquired through mapping using a handheld GPS unit, or traced on topographic maps, satellite images, and aerial photographs. The methods for extracting the shoreline on topographic map, and satellite images are discussed in detail in the accompanying **Manual on Shoreline Change Analysis**. The shoreline vectors generated in this step will be the main input dataset to ``QSCAT``.

Merging shoreline layers
------------------------

If shoreline vectors are traced or gathered for each year and stored in separate layers, it is required to merge those shoreline layers into a single layer.

The following are steps to merge multiple shoreline layers into a single layer using ``QGIS``:

#. Open |toolbox| :menuselection:`Processing --> Toolbox`.
#. Search for ``Merge vector layers`` in the search bar.
#. In :guilabel:`Input layers`, click :guilabel:`...` then select the shoreline layers to be merged. After you are done selecting, click :guilabel:`OK` when done.
#. In :guilabel:`Destination CRS`, select the appropriate ``CRS`` of the shoreline layers for your project.
#. In :guilabel:`Merged`, it is recommended to permanently save the merged layers. Thus, click :guilabel:`...`, and :guilabel:`Save to file`. Choose a folder (recommended in the same folder of your ``QGIS`` project), pick a file name such as ``Shorelines Merged`` and choose ``SHP files (*.shp)`` as the file type, and click :guilabel:`Save`.
#. Click :guilabel:`Run` to start the merge process. Once finished, the newly merged layer with your chosen file name will appear in the ``Layers`` panel.

Adding attribute fields and values
----------------------------------

After merging, each feature in the shoreline layer should contain the necessary information for each shoreline, including the shoreline date and uncertainty. The table below illustrates the required attribute table for the shoreline layer and the format of the attribute values:


=========================== ============ =========== ===========
Field                       Name         Data Type   Format
=========================== ============ =========== ===========
``QSCAT`` date field        ``any_name`` ``String``  ``mm/yyyy``
``QSCAT`` uncertainty field ``any_name`` ``Decimal`` ``x.xx``
=========================== ============ =========== ===========

.. note:: **Attribute fields and values**
    
    * You need to add the two fields with proper data type above.
    * The date value should be in the format ``mm/yyyy``. Ensure that the date is valid to avoid errors. Use ``mm`` for ``January`` such as ``01``.
    * The uncertainty field should be of decimal data type and follow the format ``x.xx``. However, if the uncertainty value is an integer, a decimal value is not required.
    * Editing the uncertainty value in the attribute table is optional but recommended. If it is not defined (``0`` or ``None``), the plugin will default to the uncertainty value defined in the :ref:`shorelines_parameters`.

.. tip:: **Automating attribute table**

   You can manually add the attribute table, but you can also automate the addition of the required attribute fields name and data types using the ``QSCAT`` :ref:`tab_automator_shoreline_fields` automator.

.. _plugin_required_inputs_baseline:

Baseline Layer
==============

Another important input data is the :menuselection:`Baseline`, a vector constructed by the user that is parallel to and at a certain distance from the shoreline. Similar to ``DSAS``, the :menuselection:`Baseline` is the starting point for all shoreline change calculations to be made in ``QSCAT``.  It is not part of the ``QSCAT`` plugin but can be generated using ``QGIS`` or any GIS software with the same functionality.

Unlike ``DSAS``, ``QSCAT`` does not currently supports multiple base segments on a single transect casting. It is recommended to run separate transect casting for each baseline segment to increase versatility, allowing for different input parameters for each baseline segment. Thus, ``QSCAT`` does not have any required attribute table for the baseline layer.

.. _generating_the_baseline_vectors:
 
Generating the baseline vectors
-------------------------------

In ``QGIS``, the creation of a baseline line vector involves the use of buffers and conversions. Initially, a buffer (in the form of a ``Polygon``) is generated around the merged shorelines layer. This buffer is then transformed into a ``LineString`` vector. Finally, you can choose which side of the ``LineString`` will serve as the designated baseline.

Creating buffer
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

   You can also create buffers and convert the buffer to a line vector manually from :menuselection:`Processing --> Toolbox`. However, you can automate the process using ``QSCAT`` :ref:`tab_automator_baseline_buffer` automator.

Once the baseline buffer is created, you will need to manually designate the baseline side of the ``LineString`` in the next step.

Choosing baseline side
.......................

#. First, enable the |checkbox| :guilabel:`Advanced Digitizing Toolbar` (if not yet enabled) by going to :menuselection:`View --> Toolbars --> Advanced Digitizing Toolbar`.
#. Right click on the baseline buffer layer and select |toggleEditing| :guilabel:`Toggle Editing`.
#. In the :guilabel:`Advanced Digitizing Toolbar`, click :guilabel:`Split Features`.
#. Use the |splitFeatures| :guilabel:`Split Features` tool to draw two lines that intersects the baseline buffer. First, draw the first line where you want the baseline's starting point to be. Then, draw the second line where you want the baseline's ending point to be. If drawn properly, the baseline buffer will be split into parts.
#. Next, select |selectFeatures| :guilabel:`Select Features by Area or Single Click` tool and select the baseline buffer segments that you want to remove. Selected segments will be highlighted in yellow line and red points (X). Hit :kbd:`Delete` to remove the selected segment. Remove all segments that you do not want until only the baseline segment you want remains.
#. Finally, right click on the baseline buffer layer and select |toggleEditing| :guilabel:`Toggle Editing` to save the changes.
#. If you are happy with final baseline, you can now permanently save it as a file, right click on the layer and select :guilabel:`Export --> Save Features As...`. Choose a folder (recommended in the same folder of your ``QGIS`` project), pick a file name such as ``Baseline``, and choose ``ESRI Shapefile (*.shp *.SHP)`` as the file type, and click :guilabel:`Save`. Choose appropriate ``CRS`` for your project and click :guilabel:`OK`.


.. _optional_multiple_baseline_vectors:

Optional multiple baseline vectors in one layer
-----------------------------------------------

Currently, QSCAT supports an experimental features which allows multiple baseline features in one layer. This feature is not yet fully supported and may not work as expected. To use this feature, you need to add 3 required fields in the attribute table of the baseline layer using :ref:`tab_automator_baseline_fields` automator. The required fields are: baseline placement, baseline orientation and transect length.

Basically, if you want to use multiple baseline features in one layer or you want to cast transects on multiple baselines at once, you are required to define the baseline placement, baseline orientation and transect length in the attribute table of the baseline layer. The addition of attribute table allows QSCAT to know different input parameters for each baseline segment.

The following are the supported values for each fields:

==================== =====================
Field                Values              
==================== =====================
baseline placement   ``sea`` or ``land``
baseline orientation ``left`` or ``right``
transect length      ``<any_number>``
==================== =====================

To know more about these values, please refer to the following: :ref:`tab_baseline_placement`, :ref:`tab_baseline_orientation` and :ref:`tab_transects_parameters_length` sections respectively.

.. warning:: Values such as ``sea``, ``land``, ``left`` and ``right`` are case-sensitive and should be written as is. If the values are not written as is, QSCAT will not recognize the values and will default to the values defined in the baseline parameters tab. Although, these may change in the future.

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