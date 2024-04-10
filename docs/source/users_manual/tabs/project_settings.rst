.. _tab_project_settings:

*********************
Tab: Project Settings
*********************

.. only:: html

   .. contents::
      :local:
      :depth: 2

The :guilabel:`Project Settings Tab` is the first tab in the plugin interface. This tab contains settings that are used to configure the plugin for the QGIS project. The settings in this tab are used to set the coordinate reference system (CRS) and metadata for the project.

.. _figure_tab_project_settings:

.. figure:: /img/project_settings/project-settings-tab.png
   :align: center

   User interface of Project Settings tab.

Coordinate Reference System
===========================

.. _figure_tab_project_settings_crs:

.. figure:: /img/project_settings/project-settings-tab-crs.png
   :align: center

   Coordinate Reference System (CRS) section in Project Settings tab.

The :guilabel:`Coordinate Reference System` or CRS setting in this plugin enables users to directly set the CRS from the plugin. This setting ensures that both input Shoreline and Baseline layers to the plugin match the current project CRS before casting transects in :ref:`tab_transects`. If the CRS of the input layers does not match, the plugin will generate an error to notify the user as shown in :numref:`figure_tab_project_settings_crs_error`.

.. _figure_tab_project_settings_crs_error:

.. figure:: /img/project_settings/project-settings-tab-crs-error.png
   :align: center

   Example error message when the CRS of the input layers does not match the project CRS.

Metadata
========

The metadata contains customizable information written in every :ref:`summary_report` file. Currently, the first version of QSCAT defines only author information in the metadata section.

Author
------

The author metadata allows you to specify the full name, position, and email address. 

