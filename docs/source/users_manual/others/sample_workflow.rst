.. _others_sample_workflow:

***************
Sample Workflow
***************

This section provides a step-by-step guide on how to run a shoreline change analysis using QSCAT with sample data from Agoo, La Union shorelines. The sample data includes shoreline vectors from 1977, 1988, 2010, and 2022. The process includes generating the baseline vectors, merging the shoreline vectors, and running the shoreline change analysis.


Generating the baseline vectors
================================

According to the section :ref:`plugin_required_inputs_baseline`, one of the required inputs for the QSCAT is the baseline vectors. Baseline vectors can be created using a buffer of merged shorelines or manually drawing them. In this step-by-step guide, we will choose the former: we will create the baseline based on the shorelines.

Merging the shoreline vectors
-----------------------------
 
In practice, this step is optional. We only apply this if our digitized shorelines are saved as **separate** shapefile layers. However, in this guide, the Agoo, La Union shorelines are shared as separate shapefile layers. Thus, we will demonstrate here on how to merge these layers.

#. Open |toolbox| :guilabel:`Processing Toolbox` via :menuselection:`Processing --> Toolbox`.

   .. figure:: /img/workflow/simple_data/opening-processing-toolbox.png
      :align: center
         
   |br|

#. Search |search| ``Merge vector layers`` in the search bar. Then double left-click on |merge-vector-layers| ``Merge vector layers`` to open the tool.

   .. figure:: /img/workflow/simple_data/searching-merge-vector-layers.png
      :align: center

   |br|

#. In :guilabel:`Input layers`, click :guilabel:`...` then select the all shoreline layers to be merged. In this example, select `Agoo 1977, Agoo 1988, Agoo 2010, and Agoo 2022`. After you are done selecting, click :guilabel:`OK`.

   .. figure:: /img/workflow/simple_data/selecting-input-layers.png
      :align: center

   |br|

#. In :guilabel:`Destination CRS`, select the appropriate ``CRS`` of the shoreline layers for your project. In this example, select ``EPSG:32651``.

   .. figure:: /img/workflow/simple_data/choosing-destination-crs.png
      :align: center

   |br|


#. In :guilabel:`Merged`, it is recommended to permanently save the merged layers. Thus, click :guilabel:`...`, and :guilabel:`Save to file`. Choose a folder (recommended in the same folder of your ``QGIS`` project), pick a file name such as ``Shorelines Merged`` and choose ``SHP files (*.shp)`` as the file type, and click :guilabel:`Save`. Click :guilabel:`Run` to start the merge process, then you can :guilabel:`Close`. 

   .. figure:: /img/workflow/simple_data/opening-save-merge-layers.png
      :align: center

   |br|

   .. figure:: /img/workflow/simple_data/saving-merged-vector-layer.png
      :align: center

   |br|

   .. figure:: /img/workflow/simple_data/running-merge-vector-layers.png
      :align: center

   |br|

   .. figure:: /img/workflow/simple_data/closing-merge-vector-layers.png
      :align: center

   |br|

#. Once finished, the newly merged layer with your chosen file name will appear in the ``Layers`` panel.

   .. figure:: /img/workflow/simple_data/showing-saved-merge-vector-layer.png
      :align: center

   |br|


.. Icons
.. |toolbox| image:: /img/toolbox.png
   :width: 1.3em
.. |search| image:: /img/search.png
   :width: 1.0em
.. |merge-vector-layers| image:: /img/merge-vector-layers.png
   :width: 1.0em

.. |br| raw:: html

    <br />