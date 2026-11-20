from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qgis.core import QgsVectorLayer


def is_field_in_layer(field: str, layer: QgsVectorLayer) -> bool:
    """Check if field exists in the layer.

    Args:
        field: The field name to check.
        layer: The layer to check the field in.

    Returns:
        True if field exists, False otherwise.
    """
    if layer.fields().indexFromName(field) == -1:
        return False
    return True
