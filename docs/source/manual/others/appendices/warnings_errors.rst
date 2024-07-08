.. index:: Warning and Errors
.. _appendices_warnings_errors:

Appendix 1: Warning and Errors
==============================

Shorelines
----------

.. list-table:: 
   :header-rows: 1
   :widths: 50 50

   * - Message
     - Description
   * - :bdg-warning:`Warning` The selected shorelines layer (``<shorelines layer name>``) has less than 2 features.
     - QSCAT requires the selected shorelines layer to have at least two shoreline features which equals to two shorelines. Minimum of two shorelines can run the NSM and EPR statistics.
   * - :bdg-warning:`Warning` The selected shorelines layer (``<shorelines layer name>``) has less than 2 fields.
     - QSCAT requires the selected shorelines layer to have the two fields for ``date`` and ``uncertainty`` field.
   * - :bdg-warning:`Warning` The selected shorelines layer (``<shorelines layer name>``) has invalid date inputs: ``<10 or less invalid dates shown>``.
     - QSCAT requires the selected shorelines layer to have valid date inputs in the ``date`` field. The date should be in the format of ``MM/YYYY``, and values of 1-12 for month and 1900-2100 for year.


Transects
---------

.. list-table::
    :header-rows: 1
    :widths: 50 50

    * - Message
      - Description
    * - :bdg-danger:`Error` The selected shorelines layer ``(<shorelines layer name>)`` CRS ``(<shorelines layer crs auth id>)`` doesn't match the project CRS ``(<project crs auth id>)``.
      - QSCAT requires the selected shoreline layer to have the same CRS as the project CRS.
    * - :bdg-danger:`Error` The selected baseline layer ``(<baseline layer name>)`` CRS ``(<baseline layer crs auth id>)`` doesn't match the project CRS ``(<project crs auth id>)``.
      - QSCAT requires the selected baseline layer to have the same CRS as the project CRS.  

Shoreline Change
----------------

.. list-table::
    :header-rows: 1
    :widths: 50 50

    * - Message
      - Description
    * - :bdg-danger:`Error` LRR and WLR requires atleast 3 shorelines.
      - QSCAT requires at least three shorelines to run the LRR and WLR statistics.


 