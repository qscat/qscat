from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QRadioButton
from qgis.core import Qgis

from qgis.core import QgsProject

from qgis.gui import QgsFieldComboBox
from qgis.gui import QgsMapLayerComboBox
from qgis.gui import QgsSpinBox

from qscat.core.projects import load_current_projection
from qscat.core.utils import get_baseline_input_params
from qscat.core.utils import get_project_input_params
from qscat.core.utils import get_shorelines_input_params
from qscat.core.utils import get_transects_input_params
from qscat.core.messages import display_message

def save_project_setting(key, value):
    if value is not None:
        project = QgsProject.instance()
        val_type = type(value)
        if val_type is str or val_type is int:
            project.writeEntry("qscat", key, value)
        elif val_type is float:
            project.writeEntryDouble("qscat", key, value)
        elif val_type is bool:
            project.writeEntryBool("qscat", key, value)
        else:
            #print(val_type, value)
            raise Exception("Saving settings with types of: `str`, `int`, `double` and `int` only.")


def read_project_setting(key, _type=str):
    project = QgsProject.instance()
    if _type is str:
        value, res = project.readEntry("qscat", key)
    elif _type is int:
        value, res = project.readNumEntry("qscat", key)
    elif _type is float:
        value, res = project.readDoubleEntry("qscat", key)
    elif _type is bool:
        value, res = project.readBoolEntry("qscat", key)
    else:
        raise Exception("Reading settings with types of: `str`, `int`, `float` and `int` only.")
    return (value, res)


def load_project_setting(widget, key):
    """Populate the QT widget value given by a QT widget object and project 
    setting `key`"""
    project = QgsProject.instance()
    _type = str
    if isinstance(widget, QgsMapLayerComboBox) or \
       isinstance(widget, QLineEdit) or \
       isinstance(widget, QgsFieldComboBox) or \
       isinstance(widget, QgsSpinBox):
        _type = str
    elif isinstance(widget, QRadioButton) or \
         isinstance(widget, QCheckBox):
        _type = bool

    value, res = read_project_setting(key, _type)
    
    if res:
        if isinstance(widget, QgsMapLayerComboBox):
            widget.setLayer(project.mapLayer(value))
        elif isinstance(widget, QRadioButton) or \
             isinstance(widget, QCheckBox):
            widget.setChecked(value)
        elif isinstance(widget, QLineEdit):
            widget.setText(value)
        elif isinstance(widget, QgsSpinBox):
            widget.setValue(int(value))
        elif isinstance(widget, QgsFieldComboBox):
            widget.setField(value)
        else:
            raise Exception("Changing saved settings is only for: `combo_box` and `line_edit`.")
        
        
def load_project_tab_project_settings(self):
    load_current_projection(self)
    self.dockwidget.qpsw_proj_selected_crs.setCrs(
        QgsProject.instance().crs())
    load_project_setting(self.dockwidget.le_proj_author_full_name,
                        'author_full_name')
    load_project_setting(self.dockwidget.le_proj_author_affiliation,
                        'author_affiliation')
    load_project_setting(self.dockwidget.le_proj_author_email,
                        'author_email')
    

def load_shorelines_tab_project_settings(self):
    load_project_setting(self.dockwidget.qmlcb_shorelines_shorelines_layer,
                         'shorelines_layer_id')
    load_project_setting(self.dockwidget.le_shorelines_default_data_unc,
                        'default_data_uncertainty')
    load_project_setting(self.dockwidget.qfcb_shorelines_date_field,
                        'date_field')
    load_project_setting(self.dockwidget.qfcb_shorelines_uncertainty_field,
                        'uncertainty_field')
   

def load_baseline_tab_project_settings(self):
    load_project_setting(self.dockwidget.qmlcb_baseline_baseline_layer,
                        'baseline_layer_id')
    load_project_setting(self.dockwidget.rb_baseline_placement_sea,
                        'is_baseline_placement_sea')
    load_project_setting(self.dockwidget.rb_baseline_placement_land,
                        'is_baseline_placement_land')
    load_project_setting(self.dockwidget.rb_baseline_orientation_land_right,
                        'is_baseline_orientation_land_right')
    load_project_setting(self.dockwidget.rb_baseline_orientation_land_left,
                        'is_baseline_orientation_land_left')


def load_transects_tab_project_settings(self):
    load_project_setting(self.dockwidget.le_transects_layer_output_name,
                        'layer_output_name')
    load_project_setting(self.dockwidget.rb_transects_by_transect_spacing,
                        'is_by_transect_spacing')
    load_project_setting(self.dockwidget.rb_transects_by_number_of_transects,
                        'is_by_number_of_transects')
    load_project_setting(self.dockwidget.qsb_transects_by_transect_spacing,
                        'by_transect_spacing')
    load_project_setting(self.dockwidget.qsb_transects_by_number_of_transects,
                        'by_number_of_transects')
    load_project_setting(self.dockwidget.qsb_transects_length,
                        'length')
    load_project_setting(self.dockwidget.qsb_transects_smoothing_distance,
                        'smoothing_distance')
    load_project_setting(self.dockwidget.rb_choose_by_distance,
                        'is_choose_by_distance')
    load_project_setting(self.dockwidget.rb_choose_by_distance_farthest,
                        'is_choose_by_distance_farthest')
    load_project_setting(self.dockwidget.rb_choose_by_distance_closest,
                        'is_choose_by_distance_closest')
    load_project_setting(self.dockwidget.rb_choose_by_placement,
                        'is_choose_by_placement')
    load_project_setting(self.dockwidget.rb_choose_by_placement_seaward,
                        'is_choose_by_placement_seaward')
    load_project_setting(self.dockwidget.rb_choose_by_placement_landward,
                        'is_choose_by_placement_landward')
    # Can't put on load_plugin_widget_properties because it should be called after
    # project settings are loaded
    if self.dockwidget.rb_choose_by_distance.isChecked():
        self.dockwidget.gb_choose_by_placement.setEnabled(False)
    elif self.dockwidget.rb_choose_by_placement.isChecked():
        self.dockwidget.gb_choose_by_distance.setEnabled(False)

    # load_project_setting(self.dockwidget.chb_transects_clip_transects,
    #                     'is_clip_transects')
    # load_project_setting(self.dockwidget.chb_transects_include_intersections,
    #                     'is_include_intersections')

    

def load_plugin_project_settings(self):
    load_project_tab_project_settings(self)
    load_shorelines_tab_project_settings(self)
    load_baseline_tab_project_settings(self)
    load_transects_tab_project_settings(self)


def save_project_tab_project_settings(self):
    QgsProject.instance().setCrs(
        self.dockwidget.qpsw_proj_selected_crs.crs())
    load_current_projection(self)

    project = get_project_input_params(self)
    save_project_setting('author_full_name',
                        project['author_full_name'])
    save_project_setting('author_affiliation',
                        project['author_affiliation'])
    save_project_setting('author_email',
                        project['author_email'])

    display_message('Inputs saved!', Qgis.Info)


def save_shorelines_tab_project_settings(self):
    shorelines = get_shorelines_input_params(self)
    save_project_setting('shorelines_layer_id',
                    shorelines['shorelines_layer'].id())
    save_project_setting('default_data_uncertainty',
                    shorelines['default_data_uncertainty'])
    save_project_setting('date_field',
                    shorelines['date_field'])
    save_project_setting('uncertainty_field',
                    shorelines['uncertainty_field'])

    display_message('Inputs saved!', Qgis.Info)
   

def save_baseline_tab_project_settings(self):
    baseline = get_baseline_input_params(self)
    save_project_setting('baseline_layer_id',
                    baseline['baseline_layer'].id())
    save_project_setting('is_baseline_placement_sea',
                    baseline['is_baseline_placement_sea'])
    save_project_setting('is_baseline_placement_land',
                    baseline['is_baseline_placement_land'])
    save_project_setting('is_baseline_orientation_land_right',
                    baseline['is_baseline_orientation_land_right'])
    save_project_setting('is_baseline_orientation_land_left',
                    baseline['is_baseline_orientation_land_left'])
                    
    display_message('Inputs saved!', Qgis.Info)


def save_transects_tab_project_settings(self):
    transects = get_transects_input_params(self)
    save_project_setting('layer_output_name',
                    transects['layer_output_name'])
    save_project_setting('is_by_transect_spacing',
                    transects['is_by_transect_spacing'])
    save_project_setting('is_by_number_of_transects',
                    transects['is_by_number_of_transects'])
    save_project_setting('by_transect_spacing',
                    transects['by_transect_spacing'])
    save_project_setting('by_number_of_transects',
                    transects['by_number_of_transects'])
    save_project_setting('length',
                    transects['length'])
    save_project_setting('smoothing_distance',
                    transects['smoothing_distance'])
    
    save_project_setting('is_choose_by_distance',
                    transects['is_choose_by_distance'])
    save_project_setting('is_choose_by_distance_farthest',
                    transects['is_choose_by_distance_farthest'])
    save_project_setting('is_choose_by_distance_closest',
                    transects['is_choose_by_distance'])
    save_project_setting('is_choose_by_placement',
                    transects['is_choose_by_placement'])
    save_project_setting('is_choose_by_placement_seaward',
                    transects['is_choose_by_placement_seaward'])
    save_project_setting('is_choose_by_placement_landward',
                    transects['is_choose_by_placement_landward'])
    
    save_project_setting('is_clip_transects',
                    transects['is_clip_transects'])
    save_project_setting('is_include_intersections',
                    transects['is_include_intersections'])

    display_message('Inputs saved!', Qgis.Info)

def save_statistics_tab_project_settings(self):
    display_message('Inputs saved!', Qgis.Info)