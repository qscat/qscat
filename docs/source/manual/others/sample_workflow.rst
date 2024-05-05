.. _others_sample_workflow:

***************
Sample Workflow
***************

.. only:: html

   .. contents::
      :local:
      :depth: 3

This section provides a step-by-step guide on how to run a shoreline change analysis using QSCAT with sample data from Agoo, La Union shorelines. The sample data includes shoreline vectors from 1977, 1988, 2010, and 2022. The process includes generating the baseline vectors, merging the shoreline vectors, and running the shoreline change analysis.

According to the :ref:`plugin_required_inputs` section, the QSCAT requires the two following layers:

   #. Shoreline layer
   #. Baseline layer

Preparing the shoreline vectors
================================

The tracing of shoreline vectors are out of scope in this guide. However, the shoreline vectors are already provided in the sample data. The shoreline vectors are saved as separate shapefile layers for each year. The shoreline vectors are saved as follows:

   #. `Agoo 1977` - shoreline vectors from 1977
   #. `Agoo 1988` - shoreline vectors from 1988
   #. `Agoo 2010` - shoreline vectors from 2010
   #. `Agoo 2022` - shoreline vectors from 2022

You can download the sample data from the following link: <insert link>

Generating the baseline vectors
================================

One of the required inputs for the QSCAT is the baseline vectors. Baseline vectors can be created using the following different strategies:

   #. Creating a buffer of merged shorelines layer.
   #. Creating a buffer of a single shoreline layer.
   #. Manually drawing lines using :guilabel:`Add Line Feature`. 

In this guide, we will choose the first strategy, which is creating a buffer of the merged shorelines layer. Then, we will choose the part of the buffer that best represents the baseline.


Merging the shoreline vectors
-----------------------------
 
Merging the shoreline step is optional. We only apply this if our digitized shorelines are saved as **separate** shapefile layers. However, in this guide, the Agoo, La Union shorelines are shared as separate shapefile layers. Thus, we will demonstrate here on how to merge these layers. 

However, regardless on what strategy you choose for generating the baseline vectors, the QSCAT requires the shoreline layers to be merged into a single layer. Also, if you choose the first strategy, you should first merge the shoreline layers so that we can create a buffer of all shorelines.


#. Open |toolbox| :guilabel:`Processing Toolbox` via :menuselection:`Processing --> Toolbox`.

   .. figure:: /img/workflow/simple_data/merge/opening-processing-toolbox.png
      :align: center
         
   |br|

#. Search |search| ``Merge vector layers`` in the search bar. Then double left-click on |mergeVectorLayers| ``Merge vector layers`` to open the tool.

   .. figure:: /img/workflow/simple_data/merge/searching-merge-vector-layers.png
      :align: center

   |br|

#. In :guilabel:`Input layers`, click :guilabel:`...` then select the all shoreline layers to be merged. In this example, select `Agoo 1977, Agoo 1988, Agoo 2010, and Agoo 2022`. After you are done selecting, click :guilabel:`OK`.

   .. figure:: /img/workflow/simple_data/merge/selecting-input-layers.png
      :align: center

   |br|

#. In :guilabel:`Destination CRS`, select the appropriate ``CRS`` of the shoreline layers for your project. In this example, select ``EPSG:32651``.

   .. figure:: /img/workflow/simple_data/merge/choosing-destination-crs.png
      :align: center

   |br|


#. In :guilabel:`Merged`, it is recommended to permanently save the merged layers. Thus, click :guilabel:`...`, and :guilabel:`Save to file`. Choose a folder (recommended in the same folder of your ``QGIS`` project), pick a file name such as ``Shorelines Merged`` and choose ``SHP files (*.shp)`` as the file type, and click :guilabel:`Save`. Click :guilabel:`Run` to start the merge process, then you can :guilabel:`Close`. 

   .. figure:: /img/workflow/simple_data/merge/opening-save-merge-layers.png
      :align: center

   |br|

   .. figure:: /img/workflow/simple_data/merge/saving-merged-vector-layer.png
      :align: center

   |br|

   .. figure:: /img/workflow/simple_data/merge/running-merge-vector-layers.png
      :align: center

   |br|

   .. figure:: /img/workflow/simple_data/merge/closing-merge-vector-layers.png
      :align: center

   |br|

#. Once finished, the newly merged layer with your chosen file name will appear in the ``Layers`` panel.

   .. figure:: /img/workflow/simple_data/merge/showing-saved-merge-vector-layer.png
      :align: center

   |br|


Creating a buffer using QSCAT
-----------------------------

Here, we can start using the QSCAT plugin. The QSCAT plugin has a feature that automates the creation of the :ref:`tab_automator_baseline_buffer`.

#. Open QSCAT if not yet opened. The QSCAT plugin can be open by clicking the |qscat| icon at the top toolbar area near the |python| :guilabel:`Python Console` icon.
  
#. In the QSCAT interface, navigate to :guilabel:`Automator Tab`. Then, in the :guilabel:`Baseline Buffer` section, select the merged shoreline layer from :guilabel:`Input shorelines layer`. Next, enter ``400`` in the :guilabel:`Distance (m)`, click :guilabel:`Buffer`. The buffer will be created and displayed in the map canvas. The buffer will be saved as a temporary layer. 

   .. figure:: /img/workflow/simple_data/buffer/creating-baseline-buffer.png
      :align: center

      Creating baseline buffer in Automator Tab
      
      |br|

   .. figure:: /img/workflow/simple_data/buffer/created-buffer-on-merged-shoreline.png
      :align: center

      Created buffer on merged shoreline with 400 meters distance

      |br|

Converting the buffer to baseline vector
----------------------------------------   

#. First, enable the |checkbox| :guilabel:`Advanced Digitizing Toolbar` (if not yet enabled) by going to :menuselection:`View --> Toolbars --> Advanced Digitizing Toolbar`.

   .. figure:: /img/workflow/simple_data/buffer/enabling-advanced-digitizing-toolbar.png
      :align: center

      Enabling Advanced Digitizing Toolbar

      |br|

   .. figure:: /img/workflow/simple_data/buffer/advanced-digitizing-toolbar.png
      :align: center

      Advanced Digitizing Toolbar

      |br|
      
#. Right click on the baseline buffer layer and select |toggleEditing| :guilabel:`Toggle Editing`. The baseline buffer layer will be editable if there is a |toggleEditing| icon on the layer.

   .. figure:: /img/workflow/simple_data/buffer/toggling-editing.png
      :align: center
      :class: img-border

      Toggling Editing

      |br|

#. In the :guilabel:`Advanced Digitizing Toolbar`, |splitFeatures| click :guilabel:`Split Features`.

   .. figure:: /img/workflow/simple_data/buffer/clicking-split-features.png
      :align: center

      Clicking Split Features

      |br|

#. Use the |splitFeatures| :guilabel:`Split Features` tool to draw two lines that intersects the baseline buffer. First, |cursorPoint| draw the first line where you want the first split. Then, |cursorPoint| draw the second line where you want the second split. If drawn properly, the baseline buffer will be split into parts.

   .. figure:: /img/workflow/simple_data/buffer/splitting-features.png
      :align: center

      Splitting features using Split Features

      |br|

#. Next, select |selectFeatures| :guilabel:`Select Features` tool and |select| select the baseline buffer segments that you want to remove. Selected segment will be highlighted in yellow line and red points (X). Hit :kbd:`Delete` on your keyboard to remove the selected segment. Remove all segments that you do not want until only the baseline segment you want remains.

   .. figure:: /img/workflow/simple_data/buffer/clicking-select-features.png
      :align: center

      Clicking Select Features

      |br|

   .. figure:: /img/workflow/simple_data/buffer/selecting-deleting-features.png
      :align: center

      Selecting and deleting a feature

      |br|

#. Finally, right click on the baseline buffer layer and select |toggleEditing| :guilabel:`Toggle Editing` and it will prompt to save the changes.

   .. warning:: There will be a case when the baseline buffer are split unexpectedly. As you can see in :numref:`figure_unexpected_split`, you can verify that there are two resulting segments even though we did not draw a line there. 
   
   .. _figure_unexpected_split:

   .. figure:: /img/workflow/simple_data/buffer/unexpected-split.png
      :align: center

      Unexpected split of baseline buffer

      |br|

   To fix this, go back to the editing mode (|toggleEditing| :guilabel:`Toggle Editing`). Select the two segments by clicking |select| left click on each segment while holding :kbd:`Shift` key. Then, in :guilabel:`Advanced Digitizing Toolbar`, click |mergeFeatures| :guilabel:`Merge Selected Features`, and click :guilabel:`OK`. The two segments will be merged into one, you can verify by selecting the features. You can |toggleEditing| :guilabel:`Toggle Editing` again to save.
   

   .. figure:: /img/workflow/simple_data/buffer/clicking-merge-features.png
      :align: center

      Clicking Merge Selected Features

      |br|


   .. figure:: /img/workflow/simple_data/buffer/merging-features.png
      :align: center

      Merging Selected Features

      |br|


#. If you are okay with the final baseline, you can now permanently save it as a file, right click on the layer and select :guilabel:`Export --> Save Features As...`. Choose a folder (recommended in the same folder of your QGIS project), pick a file name such as ``Baseline``, and choose ``ESRI Shapefile (*.shp *.SHP)`` as the file type, and click :guilabel:`Save`. Choose appropriate ``CRS`` for your project and click :guilabel:`OK`.

   .. figure:: /img/workflow/simple_data/buffer/opening-saving-feature.png
      :align: center

      Accessing Save Feature As...

      |br|

   .. figure:: /img/workflow/simple_data/buffer/saving-vector-layer-as.png
      :align: center

      Saving Vector Layer As...

      |br|

   .. figure:: /img/workflow/simple_data/buffer/saving-layer-as.png
      :align: center

      Saving Layer As...

      |br|

   .. figure:: /img/workflow/simple_data/buffer/saving-vector-layer-as-final.png
      :align: center

      Finalizing Saving Vector Layer As...

      |br|


Configuring the shoreline and baseline layer attributes
========================================================

Shorelines
----------

Next, we need to add details of each shoreline such as its date and its uncertainty value of the images. We can use :guilabel:`Shoreline Fields Automator` to add the required fields for these.

#. Navigate to :guilabel:`Automator Tab`. Then, in the :guilabel:`Fields - Shoreline`, select the merged shoreline layer from :guilabel:`Shoreline layer`. Make sure |checkbox|:guilabel:`Date field name` and |checkbox| :guilabel:`Uncertainty field name` is both checked. Type the appropriate date field name and uncertainty field name or leave as is. In this example, we choose ``qs_date`` and ``qs_unc`` as the field names. Click :guilabel:`Add Fields`.

   .. figure:: /img/workflow/simple_data/attributes/automating-shoreline-fields.png
      :align: center

      Automating adding of shoreline fields using Shoreline Fields Automator

      |br|

#. Then, we need to fill in the details of each shoreline. Right click on the merged shoreline layer and select |openTable| :guilabel:`Open Attribute Table`. But first, enable the |toggleEditing| :guilabel:`Toggle Editing` if not yet enabled. In the attribute table, fill in the details of each shoreline such as its date and its uncertainty value. In our sample data, input the following details:

   .. list-table:: Shoreline date and uncertainty of Agoo, La Union shorelines
      :align: center
      :header-rows: 1
      :widths: 30 20 50

      * - Shoreline
        - Date
        - Uncertainty
      * - Agoo 1977
        - 01/1977
        - 25
      * - Agoo 1988
        - 03/1988
        - 15
      * - Agoo 2010
        - 05/2010
        - 15
      * - Agoo 2022
        - 04/2022
        - 15

   According to :ref:`tab_automator_shorelines_fields`, date is in the format of ``MM/YYYY`` and uncertainty is in meters. Also, make sure that details aligns based on the shoreline layer.

   .. figure:: /img/workflow/simple_data/attributes/opening-attribute-table.png
      :align: center
      :class: img-border

      Opening attribute table of shoreline layer.

      |br|

   .. figure:: /img/workflow/simple_data/attributes/editing-attribute-table.png
      :align: center

      Editing attribute table of shoreline layer.

      |br|

   .. figure:: /img/workflow/simple_data/attributes/saving-attribute-table.png
      :align: center

      Saving attribute table of shoreline layer.

      |br|

.. TODO: Update `Shoreline layer` and `Input shorelines layer` (not consistent)

Baseline
--------

Baseline also optionally includes fields such as placement, transect length, and orientation. However for this sample data, we will not add any fields because it is only applicable for multi baseline. For more information, refer to :ref:`tab_automator_baseline_fields`.


Configuring the selections of layer and fields
==============================================

#. For shorelines, go to :guilabel:`Shorelines Tab`. 

   In :guilabel:`Layer` section, select the merged shoreline layer as the :guilabel:`Input layer`. Leave :guilabel:`Default data uncertainty` as is; this value is used when no uncertainty value is provided in a shoreline uncertainty field (:ref:`shorelines_parameters`).
   
   In :guilabel:`Fields` section, select the added date (:guilabel:`Year`) and uncertainty (:guilabel:`Uncertainty`) field names, and click :guilabel:`Save`.

   .. figure:: /img/workflow/simple_data/attributes/configuring-shorelines.png
      :align: center

      Configuring shorelines in Shorelines Tab

      |br|


#. For baseline, go to :guilabel:`Baseline Tab`.

   In :guilabel:`Layer` section, select the baseline layer as the :guilabel:`Input layer`.

   In :guilabel:`Placement` section, select |radiobutton| :guilabel:`Sea or offshore` (see :ref:`tab_baseline_placement`).

   In :guilabel:`Orientation` section, select |radiobutton| :guilabel:`Land is to the RIGHT (R)` (see :ref:`tab_baseline_orientation`), and click :guilabel:`Save`.

   .. figure:: /img/workflow/simple_data/attributes/configuring-baseline.png
      :align: center

      Configuring baseline in Baseline Tab

      |br|

Casting of transects
====================

We can now start the process of running shoreline change analysis. The first step is to cast transects. The transects are lines that are perpendicular to the baseline. The transects are used to measure the shoreline change statistics.

#. Go to :guilabel:`Transects Tab`.


   In :guilabel:`Layer` section, select a name for the transect layer in :guilabel:`Layer output name`. In this example, we leave ``transects`` as is (see :ref:`tab_transects_vector_layer_output_name` how is the output name used).

   In :guilabel:`Count` section, select how would you want the number of transects to be determined. In this example, we choose |radiobutton| :guilabel:`By transect spacing` and leave ``50`` meters as is` (see :ref:`tab_transects_count`).

   In :guilabel:`Parameters` section, leave :guilabel:`Transect length` and :guilabel:`Smoothing distance` as is (see :ref:`tab_transects_parameters`).

   Click :guilabel:`Cast Transect` to start the process of casting transects. The transects will be created and displayed in the map canvas. The transects will be saved as a temporary layer. You can optionally :guilabel:`Save` the selections such that it will be retain when you close QSCAT or QGIS.

   .. figure:: /img/workflow/simple_data/transects/casting-transects.png
      :align: center

      Casting transects using Transect Tab.

      |br|

   .. figure:: /img/workflow/simple_data/transects/transects.png
      :align: center
      :class: img-border

      Transects with 2000 meters length, and 500 meters smoothing distance together with baseline (baseline orientation shown) and shorelines.

      |br|

   .. figure:: /img/workflow/simple_data/transects/layer-with-transects.png
      :align: center
      :class: img-border

      Current layers with transects.

      |br|


Computing the shoreline change
==============================

#. Go to :guilabel:`Shoreline Change Tab`.

   In :guilabel:`General` section, select the created transect layer (note that after every cast the transects layer will be automatically selected here). You can optionally |checkbox| :guilabel:`Clip transects` if you want, this is only for visualization purposes and does not affect statistics. Choose where you want the summary reports to be saved in :guilabel:`Summary reports location` (see :ref:`tab_summary_reports`).

   In :guilabel:`Transect-Shoreline Intersections`, leave |radiobutton| :guilabel:`Distance` and :guilabel:`Farthest` as is (see :ref:`tab_shoreline_change_tsi`).

   In :guilabel:`Shoreline Change Statistics`, select statistics you want to calculate, select all via :guilabel:`Select / Deselect All` (see :ref:`tab_shoreline_change_scs`).

   In :guilabel:`Pairwise Comparison Shorelines`, always click :guilabel:`Update` when selections are empty in :guilabel:`Newest date` and :guilabel:`Oldest date`. The :guilabel:`Update` button is also used when you changed the values of date field in shorelines layer then you want to update the selection of dates. Make sure to select ``04/2022`` in :guilabel:`Newest date` and ``01/1977`` in :guilabel:`Oldest date` (see :ref:`tab_shoreline_change_pcs`).

   In :guilabel:`Additional Parameters`, leave :guilabel:`Confidence interval (%)` as is (see :ref:`tab_shoreline_change_additional_parameters`).

   Click :guilabel:`Compute Shoreline Change` to start the process of computing shoreline change. The shoreline change statistics will be calculated and the transects will be displayed in the map canvas. The statistics will be saved as a temporary layer. You can optionally :guilabel:`Save` the selections such that it will be retain when you close QSCAT or QGIS (see :ref:`tab_shoreline_change_vector_layer_output_name`) for layer outputs.

   .. figure:: /img/workflow/simple_data/shoreline_change/computing-shoreline-change.png
      :align: center
      :class: img-border

      Current layers with shoreline change statistics.

      |br|

   .. figure:: /img/workflow/simple_data/shoreline_change/statistics.png
      :align: center
      :class: img-border

      Current layers with shoreline change statistics.

      |br|

   .. figure:: /img/workflow/simple_data/shoreline_change/nsm.png
      :align: center
      :class: img-border

      Example NSM statistic transect layer when clip transect intersections applied.

      |br|

   .. figure:: /img/workflow/simple_data/shoreline_change/nsm-table.png
      :align: center
      :class: img-border

      Example NSM statistic table field and values.

      |br|


Running optional features
=========================

Computing the area change
-------------------------

This feature requires a polygon area to encompass which would you like to get the area change. Usually, we designed this for a specific area of interest like municipality or barangay boundaries. If you want to get the area change on whole area at once then you can draw a polygon that encompasses the whole area. For this sample data, we will get the area change on the whole area.

Creating the polygon using QGIS
...............................

#. In the top part of QGIS, click |newVectorLayer| :guilabel:`New Shapefile Layer`.

   .. figure:: /img/workflow/simple_data/area_change/opening-new-shapefile-layer.png
      :align: center
      :class: img-border

      Opening New Shapefile Layer.

      |br|

#. In the :guilabel:`File name` click :guilabel:`...`, select a folder location, type a file name such as ``whole area.shp`` and :guilabel:`Save`.

   .. figure:: /img/workflow/simple_data/area_change/saving-shapefile-layer.png
      :align: center

      Saving New Shapefile Layer.

      |br|

#. Select ``Polygon`` as the :guilabel:`Geometry type`. Select ``ESPG:32651`` and click :guilabel:`OK`.

   .. figure:: /img/workflow/simple_data/area_change/final-saving-shapefile-layer.png
      :align: center

      Final Saving New Shapefile Layer.

      |br|


#. Change the symbology for better visualization. Double left click the square from left of the layer name. Then, select ``outline red`` click :guilabel:`Apply` and :guilabel:`OK`.

   .. figure:: /img/workflow/simple_data/area_change/opening-symbology.png
      :align: center
      :class: img-border

      Opening symbology in layer properties.

      |br|

   .. figure:: /img/workflow/simple_data/area_change/changing-symbology.png
      :align: center

      Changing symbology in layer properties.

      |br|

#. Draw the polygon. Toggle the layer to be editable by |toggleEditing| :guilabel:`Toggle Editing`. Then, click |addPolygon| :guilabel:`Add Polygon Feature` and draw the polygon that encompasses the whole area. You can draw the polygon with just 4 points enough to cover the whole area. |cursorPoint| draw 4 points, then right click anywhere to end drawing, and click :guilabel:`OK`. Of course, you do not need to follow the points on the figure just make sure the polygon will encompass the area of interest. Select |toggleEditing| :guilabel:`Toggle Editing` to save the changes.

   .. figure:: /img/workflow/simple_data/area_change/opening-add-polygon-feature.png
         :align: center
         :class: img-border

         Opening Add Polygon Feature.

         |br|

   .. figure:: /img/workflow/simple_data/area_change/drawing-polygon.png
         :align: center

         Drawing Polygon using Add Polygon Feature.

         |br|

   .. figure:: /img/workflow/simple_data/area_change/polygon-feature.png
         :align: center

         Example drawn polygon feature.

         |br|

#. Go to :guilabel:`Area Change Tab`.

   In :guilabel:`General` section, select the created polygon layer as the :guilabel:`Polygon boundary`, and in :guilabel:`Stat`, select the NSM layer. Only NSM and EPR statistics are available for area change for now (see :ref:`tab_area_change`).

   .. figure:: /img/workflow/simple_data/area_change/computing-area-change.png
         :align: center

         Computing area change in Area Change Tab.

         |br|

   .. figure:: /img/workflow/simple_data/area_change/example-area-change.png
         :align: center

         Example area change in the top part.

         |br|

Running the forecasting
-----------------------

#. Go to :guilabel:`Forecasting Tab`

   In :guilabel:`Algorithm`, the current available algorithm is :guilabel:`Kalman Filter` (see :ref:`tab_forecasting_algorithm`).

   In :guilabel:`Time Period`, select |radiobutton| :guilabel:`10 years` (see :ref:`tab_forecasting_time_period`) and click :guilabel:`Forecast`.

   .. figure:: /img/workflow/simple_data/forecasting/example-forecasting.png
      :align: center
      :class: img-border

      Example forecasting in Forecasting Tab.

      |br|

   .. figure:: /img/workflow/simple_data/forecasting/example-forecasting.png
      :align: center
      :class: img-border

      Example forecasting in Forecasting Tab.

      |br|
      
Visualizing the statistics transects
------------------------------------

#. Go to :guilabel:`Visualization Tab`

   In :guilabel:`Layer`, select a statistic layer to apply visualization. In this example, we choose the NSM statistic layer.

   In :guilabel:`Color Ramp`, leave the number of :guilabel:`Negative classes` and :guilabel:`Positive classes` as is. Select ``Equal Interval`` as the :guilabel:`Mode` and click :guilabel:`Visualize`.

   .. figure:: /img/workflow/simple_data/visualization/visualizing-nsm-statistic.png
      :align: center

      Visualizing statistics in Visualization Tab.

      |br|

   .. figure:: /img/workflow/simple_data/visualization/visualized-nsm-statistic.png
      :align: center

      Visualized NSM statistic.

      |br|

   .. figure:: /img/workflow/simple_data/visualization/visualized-nsm-statistic-color-ramp-values.png
      :align: center
      :class: img-border

      Visualized NSM statistic color ramp with equal interval range values.

      |br|


.. Icons
.. |qscat| image:: /img/qscat.png
   :width: 1.3em
.. |python| image:: /img/python.png
   :width: 1.3em
.. |toolbox| image:: /img/toolbox.png
   :width: 1.3em
.. |search| image:: /img/search.png
   :width: 1.0em
.. |mergeVectorLayers| image:: /img/merge-vector-layers.png
   :width: 1.0em
.. |selectFeatures| image:: /img/action-select-features.png
   :width: 1.5em
.. |mergeFeatures| image:: /img/ action-merge-features.png
   :width: 1.5em
.. |toggleEditing| image:: /img/action-toggle-editing.png
   :width: 1.5em
.. |splitFeatures| image:: /img/action-split-features.png
   :width: 1.5em
.. |openTable| image:: /img/action-open-table.png
   :width: 1.5em
.. |newVectorLayer| image:: /img/action-new-vector-layer.png
   :width: 1.5em
.. |addPolygon| image:: /img/action-add-polygon.png
   :width: 1.5em
.. |cursorPoint| image:: /img/cursor-point.png
   :width: 1.3em
.. |select| image:: /img/select.png
   :width: 1.3em

.. |checkbox| image:: /img/checkbox.png
   :width: 1.0em
.. |radiobutton| image:: /img/radiobutton.png
   :width: 1.0em
.. |br| raw:: html

    <br />