# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from unittest.mock import patch

from qgis.testing import start_app

from qgis.core import QgsProject
from qgis.core import QgsVectorLayer

from qscat.core.automator import automate_baseline_buffer
from qscat.core.automator import automate_baseline_field
from qscat.core.automator import automate_shoreline_field

start_app()


class TestAutomator:
    """Test automator functions."""
    layer = QgsVectorLayer('LineString', 'test_layer', 'memory')
    
    def test_automate_shoreline_field(self):
        """Test automate shoreline field function."""
        with patch('qscat.core.automator.display_message', return_value=None):
            automate_shoreline_field(self.layer, 'date', 'unc', True, True)

            assert 'date' in [field.name() for field in self.layer.fields()]
            assert 'unc' in [field.name() for field in self.layer.fields()]


    def test_automate_baseline_field(self):
        """Test automate baseline field function."""
        with patch('qscat.core.automator.display_message', return_value=None):
            automate_baseline_field(
                self.layer, 
                'placement', 'orientation', 'length', 
                True, True, True,
            )

            assert 'placement' in [field.name() for field in self.layer.fields()]
            assert 'orientation' in [field.name() for field in self.layer.fields()]
            assert 'length' in [field.name() for field in self.layer.fields()]


    def test_baseline_buffer(self):
        """Test create baseline buffer function."""
        project = QgsProject.instance()
        initial_layer_count = len(project.mapLayers())
        buffer_layer = automate_baseline_buffer(self.layer, 10)

        assert len(project.mapLayers()) == initial_layer_count + 1
        assert 'Baseline Buffer' in buffer_layer.name()
