.. _others_sample_workflow:

***************
Sample Workflow
***************

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

-

Casting of transects
====================

-

Computing the shoreline change
==============================

-

Running optional features
=========================

Computing the area change
-------------------------

-

Running the forecasting
-----------------------

-

Visualizing the transects
-------------------------


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
.. |cursorPoint| image:: /img/cursor-point.png
   :width: 1.3em
.. |select| image:: /img/select.png
   :width: 1.3em

.. |checkbox| image:: /img/checkbox.png
   :width: 1.0em
.. |br| raw:: html

    <br />