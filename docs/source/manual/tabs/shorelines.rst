.. _tab_shorelines:

***************
Tab: Shorelines
***************

The :guilabel:`Shorelines Tab` allows you to configure shoreline by selecting the shorelines layer and fields.

.. only:: html

   .. contents::
      :local:
      :depth: 2

.. _figure_tab_shorelines:

.. figure:: /img/shorelines/shorelines-tab.png
   :align: center
   :alt: User interface of Shorelines Tab

   User interface of Shorelines Tab

.. _shorelines_parameters:

Layer
=====

.. figure:: /img/shorelines/shorelines-tab-layer.png
   :align: center
   :alt: Layer section in Shorelines Tab

   Layer section in Shorelines Tab

#. **The input layer:** Should be the merged shorelines, created in :ref:`plugin_required_inputs_shorelines`; and

#. **Default data uncertainty:** If the uncertainty value for each shoreline data in the attribute table is set to ``0`` or ``None``, the plugin will automatically assign this defined value (defaults to 15 meters). This value represents the uncertainty inherent in the resolution of Landsat images, which are the readily available sources of shoreline data in the country. This default value may underestimate or overestimate the uncertainty inherent in different types of digital images. Thus, it is recommended for you to provide the uncertainty value in the attribute table of the selected shoreline layer.

For the input layer merged shorelines, the uncertainty value should be based on the map or digital image with the lowest resolution. Hence, QSCAT automatically selects the highest or maximum uncertainty value in the attribute table of the merged shorelines.


Fields
======

.. figure:: /img/shorelines/shorelines-tab-fields.png
   :align: center
   :alt: Fields section in Shorelines Tab

   Fields section in Shorelines Tab

Under the :menuselection:`Shorelines fields`, select the ``date`` and ``uncertainty`` fields of the currently selected shoreline layer to be used. These are the fields that are automatically created in :ref:`tab_automator_shorelines_fields` automator or manually created.