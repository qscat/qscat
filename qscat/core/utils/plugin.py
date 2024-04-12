import configparser
import os
from pathlib import Path

from qgis.core import QgsApplication
from qgis.core import QgsProject


def get_project_dir():
    project_path = QgsProject.instance().absoluteFilePath()
    project_dir = os.path.dirname(project_path)
    return project_dir


def get_plugin_dir():
    profiles_default_dir = QgsApplication.qgisSettingsDirPath()
    plugin_dir = os.path.join(
        profiles_default_dir,
        'python', 
        'plugins', 
        'qscat',
    )
    return plugin_dir


def get_plugins_dir():
    profiles_default_dir = QgsApplication.qgisSettingsDirPath()
    plugins_dir = os.path.join(
        profiles_default_dir,
        'python', 
        'plugins',
    )
    return plugins_dir


def get_metadata_version():
    """Get the version from local QGIS plugin metadata.txt.
    Returns:
        str: The string version from local metadata.txt
    """
    plugin_dir = get_plugin_dir()
    config = configparser.ConfigParser()
    config.read(Path(plugin_dir) / "metadata.txt")
    version = config.get('general', 'version')
    return version