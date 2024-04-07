.. _tab_area_change:

***********************
Tab: Area Change (Beta)
***********************

.. only:: html

   .. contents::
      :local:
      :depth: 2

.. note:: This feature is currently in beta and has not undergone extensive testing on other coastal shorelines. While we encourage exploration, be aware that there may be occasional bugs or unexpected outputs. Feel free to provide feedback as you use it! 

An additional functionality of QSCAT is the estimation of area change between two shoreline vectors for a given polygon layer. The polygon layer can be randomly drawn, or based on geographic boundaries (e.g., shapefiles of barangay, municipal boundaries) for which this type of analysis may be more meaningful. Monitoring how much coastal land a barangay or municipality has gained or lost is important for coastal planning and management. Make sure the boundary drawn encompasses all shorelines.

The input layers are:

#. Polygon layer - a shapefile that encompasses the area of interest; may be drawn randomly or based on geographic or administrative boundaries
#. NSM layer - a memory-based layer where the NSM results are temporarily saved. Area change is calculated based on the NSM results.

Results of area change calculation are stored as a memory-based layer, “filename_area [date time of run]”. It can also be accessed in the attribute table of area change results (Table X - sample table). Aside from the area change per shoreline trend, the attribute table also provides estimates of the length of shoreline that is undergoing erosion, accretion or remains stable, respectively, for a given polygon. 
