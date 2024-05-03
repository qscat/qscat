.. _tab_summary_reports:

********************
Tab: Summary Reports
********************

.. only:: html

   .. contents::
      :local:
      :depth: 2

The :guilabel:`Summary Reports Tab` allows the user to configure the save location of the summary reports and enable or disable the generation of summary reports. The summary reports are text files that contain the base information and the summary of results of the shoreline change, area change, and forecasting. The summary reports are saved in the folder specified by the user.

.. _figure_tab_summary_reports:

.. figure:: /img/summary_reports/summary-reports-tab.png
   :align: center
   :alt: User interface of Summary Reports Tab

   User interface of Summary Reports Tab

General
=======

Reports save location
---------------------

Allows users to choose the folder in which to save the summary reports. Defaults to ``QSCATSummaryReports`` under user home directory. Additionally, each results type (shoreline change, area change, and forecasting) will be saved inside another folder within the specified folder. The filename of the report will be in the format ``qscat_<version>_<result_type>_<datetime>.txt``, where the datetime is in the format ``MM-DD-YY HH-MM-SS``. The following table shows the folder structure and the filename format of the summary reports.

.. list-table:: 
   :header-rows: 1
   :widths: 20 30 50

   * - Result
     - Folder
     - File name
   * - Shoreline Change
     - ``shoreline_change``
     - ``qscat_<version>_shoreline_change_<datetime>.txt``
   * - Area Change
     - ``area_change``
     - ``qscat_<version>_area_change_<datetime>.txt``
   * - Forecasting
     - ``forecasting``
     - ``qscat_<version>_forecasting_<datetime>.txt``


Example of the folder structure and file name
.............................................

.. code-block::

   ── QSCATSummaryReports/
      ├── shoreline_change/
      │   ├── qscat_0.3.1_shoreline_change_04-29-24_15-15-28.txt
      │   ├── qscat_0.3.1_shoreline_change_05-01-24_10-30-12.txt
      │   └── ...
      │
      ├── area_change/
      │   ├── qscat_0.3.1_area_change_04-30-24_20-45-33.txt
      │   ├── qscat_0.3.1_area_change_05-02-24_14-25-46.txt
      │   └── ...
      │
      └── forecasting/
          ├── qscat_0.3.1_forecasting_04-28-24_18-55-21.txt
          ├── qscat_0.3.1_forecasting_05-03-24_09-10-58.txt
          └── ...

Enable reports generation
-------------------------

A convenient way to enable or disable the generation of summary reports. Users can also enable or disable the generation of individual reports: Shoreline Change, Area Change, and Forecasting.


Content of summary reports
==========================

Base information
----------------

Regardless of the type of result (shoreline change, area change, or forecasting), the base information is always written at the top of the text file. The base information contains standard details such as general info, projection, metadata, and system details. The following are information that are included in the base information:

**Project details**

- **Time generated:** date and time the report was generated (format ``MM-DD-YYYY HH-MM-SS``).
- **Project location:** folder location of the QGIS project :file:`.qgz`.
- **Projection:** CRS auth id of the QGIS project (e.g ``EPSG:32651``).

**Metadata**

- **Author full name:** metadata of the QGIS project.
- **Author affiliation:** metadata of the QGIS project.
- **Author email:** metadata of the QGIS project.

**System details**

- **OS version:** operating system name and version.
- **QGIS version:** QGIS version and name.
- **QSCAT version:** QSCAT version.

Shoreline Change
----------------

Input parameters
................

**Shorelines Tab**

- **Layer:** layer name of the selected shoreline.
- **Default data uncertainty:** default data uncertainty value.
- **Date field:** field name of the selected shoreline date.
 
Summary of results
..................

Area Change
-----------

Input parameters
................

- **NSM layer:** layer name of the selected stat NSM layer.
- **Polygon:** layer name of the selected area's polygon layer.
  
Summary of results
..................

**Area change**

Erosion, accretion, stable:

* Total areas
* (%) of areas
* No. of areas
* (%) of no. areas
* Avg. value
* Min. value
* Max. value

**Shoreline**

Erosion, accretion, stable:

* Length of shoreline
* (%) of length
* No. of shoreline
* (%) of number of shoreline
* Avg. value
* Min. value
* Max. value

Forecasting
-----------

Input parameters
................

Summary of results
..................

**Forecast points**

*Content for this section will be added soon.*

**Forecast line**

*Content for this section will be added soon.*

**Forecast area**

*Content for this section will be added soon.*