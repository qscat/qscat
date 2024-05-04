.. _tab_project_settings:

*********************
Tab: Project Settings
*********************

The :guilabel:`Project Settings Tab` allows you to configure the plugin for the QGIS project.

.. only:: html

   .. contents::
      :local:
      :depth: 2

.. _figure_tab_project_settings:

.. figure:: /img/project_settings/project-settings-tab.png
   :align: center
   :alt: User interface of Project Settings Tab

   User interface of Project Settings Tab


Coordinate Reference System
===========================

.. _figure_tab_project_settings_crs:

.. figure:: /img/project_settings/project-settings-tab-crs.png
   :align: center

   Coordinate Reference System (CRS) section in Project Settings tab.

The :guilabel:`Coordinate Reference System` or CRS setting in this plugin enables you to directly set the CRS from the plugin. This setting ensures that both input Shoreline and Baseline layers to the plugin match the current project CRS before casting transects in :ref:`tab_transects`. If the CRS of the input layers does not match, the plugin will generate an error to notify you as shown in :numref:`figure_tab_project_settings_crs_error`.

.. _figure_tab_project_settings_crs_error:

.. figure:: /img/project_settings/project-settings-tab-crs-error.png
   :align: center
   :alt: Example error message when the CRS of the input layers does not match the project CRS

   Example error message when the CRS of the input layers does not match the project CRS


Metadata
========

The metadata contains customizable information written in every :ref:`tab_summary_reports` file. Currently, the first version of QSCAT defines only author information in the metadata section.

Author
------

The author metadata allows you to specify the full name, position, and email address. 

