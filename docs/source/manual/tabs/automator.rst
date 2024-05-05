.. _tab_automator:

**************
Tab: Automator
**************

The :guilabel:`Automator Tab` allows you to automate repetitive tasks directly from the plugin such as adding fields to the shoreline layer and baseline layer.

.. only:: html

   .. contents::
      :local:
      :depth: 2

.. _figure_tab_automator:

.. figure:: /img/automator/automator-tab.png
   :align: center
   :alt: User interface of Automator Tab

   User interface of Automator Tab

Shorelines
==========

.. _tab_automator_shorelines_fields:

Shorelines fields
-----------------

.. figure:: /img/automator/automator-tab-shorelines-fields.png
   :align: center
   :alt: Shorelines fields section in Automator Tab

   Shorelines fields section in Automator Tab

The :guilabel:`Shorelines fields` automator simplifies the process of adding attributes by automatically assigning pre-defined data types and custom field names. By simply defining the desired field name, the plugin takes care of the necessary data type assignments for each field. This requires the following input:

#. **Input layer:** vector layer containing the merged shorelines.
#. **Date field name:** field name that represents the date of the source of shoreline data, following the format ``mm/yyyy``.
#. **Uncertainty field name:** field name that captures the uncertainty associated with the measurement and/or positional accuracy inherent in the source of shoreline data.

The automator adds the following fields to the input layer:

============================ ==========
Field name                   Data type
============================ ==========
``<date_field_name>``        ``String``
``<uncertainty_field_name>`` ``Double``
============================ ==========

Without the automator, the ``date`` and ``uncertainty`` fields can be manually added on the :menuselection:`Attribute Table` of the shoreline input layer. Basically, this means that you are responsible for selecting the attribute data type. To check full details about shorelines layer, please refer to the :ref:`preparing_the_shoreline_vectors`.

Baseline
========

.. _tab_automator_baseline_fields:

Baseline fields
---------------

.. figure:: /img/automator/automator-tab-baseline-fields.png
   :align: center
   :alt: Baseline fields section in Automator Tab

   Baseline fields section in Automator Tab


The :guilabel:`Baseline fields` automator simplifies the process of adding attributes by automatically assigning pre-defined data types and custom field names. By simply defining the desired field name, the plugin takes care of the necessary data type assignments for each field. This requires the following input:

#. **Input layer:** vector layer containing the merged baseline.
#. **Placement field name:** field name that represents placement of baseline.
#. **Orientation field name:** field name that captures the orientation of the baseline.
#. **Transect length name:** field name that captures the length of the transect.

The automator adds the following fields to the input layer:

============================ ===========
Field name                   Data type
============================ ===========
``<placement_field_name>``   ``String``
``<orientation_field_name>`` ``String``
``<transect_length_name>``   ``Integer``
============================ ===========

For more information about these fields, please refer to :ref:`optional_multiple_baseline_vectors`.

.. _tab_automator_baseline_buffer:

Baseline buffer
---------------

.. figure:: /img/automator/automator-tab-baseline-buffer.png
   :align: center
   :alt: Baseline buffer section in Automator Tab

   Baseline buffer section in Automator Tab

The :guilabel:`Baseline buffer` automator simplifies the process of creating a buffer around the baseline. This requires the following input:

#. **Input layer:** vector layer containing the merged shorelines.
#. **Buffer distance:** distance in meters to create the buffer around the baseline.

The automator uses processing algorithm :guilabel:`Buffer` with pre-defined inputs to create the buffer around the merged shorelines layer. The output is then converted to ``LineString``. To read more about input baseline layer, please refer to :ref:`generating_the_baseline_vectors`. 

The following are the pre-defined inputs for the :guilabel:`Buffer` algorithm:

======================================= ====================
Parameter                               Value
======================================= ====================
:guilabel:`Distance`                    ``<input_distance>``
:guilabel:`Segments`                    5
:guilabel:`End cap style`               Flat
:guilabel:`Join style`                  Round
|checkbox| :guilabel:`Dissolve results` Checked
======================================= ====================

.. |checkbox| image:: /img/checkbox.png
   :width: 1.0em