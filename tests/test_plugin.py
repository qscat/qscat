import configparser
import re

from pathlib import Path

from qgis.testing.mocked import get_iface

from qscat.qscat_plugin import QscatPlugin


def test_plugin():
    """Test the plugin class."""
    plugin = QscatPlugin(get_iface())
    plugin.initGui()
    plugin.run(test=True)


def test_metadata():
    """Test the content of metadata.txt of the plugin."""
    # https://github.com/qgis/qgis-django/blob/master/qgis-app/plugins/validator.py
    REQUIRED_METADATA = [
        "name",
        "description",
        "version",
        "qgisMinimumVersion",
        "author",
        "email",
        "about",
        "tracker",
        "repository",
    ]
    # BOOLEAN_METADATA = ["experimental", "deprecated", "server"]

    file_path = Path(__file__).parent.parent / "qscat" / "metadata.txt"

    print(file_path)
    parser = configparser.ConfigParser()
    parser.read(file_path)

    # Check if `general` section exists
    assert parser.has_section("general"), "Missing general section in metadata."

    # Check if all required metadata is present
    for metadata in REQUIRED_METADATA:
        assert parser.has_option(
            "general", metadata
        ), f"Missing required {metadata} in general section of metadata."

    # Check if version follows format x.y.z only
    version = parser.get("general", "version")
    assert re.match(
        r"^[0-9]+\.[0-9]+\.[0-9]+$", version
    ), f"Version {version} does not follow x.y.z format."
