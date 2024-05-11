# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from PyQt5.QtGui import QColor
from qgis.core import (
    QgsApplication,
    QgsLineSymbol,
    QgsMarkerLineSymbolLayer,
    QgsNullSymbolRenderer,
    QgsSimpleLineSymbolLayer,
    QgsSingleSymbolRenderer,
    QgsSvgMarkerSymbolLayer,
)

from qscat.core.utils.plugin import get_plugin_dir


def show_hide_baseline_orientation(qscat):
    """Update baseline layer symbology to show and hide orientation.

    Args:
        qscat (QscatPlugin): QscatPlugin instance.

    Notes:
        Line (QgsLineSymbol)
        -Marker Line (QgsMarkerLineSymbolLayer)
        --Marker (QgsMarkerSymbol)
        ---SVG Marker (QgsSvgMarkerSymbolLayer)
    """
    layer = qscat.dockwidget.qmlcb_baseline_layer.currentLayer()

    if not layer:
        return

    registry = QgsApplication.symbolLayerRegistry()

    # QgisLineSymbol
    if isinstance(layer.renderer(), QgsNullSymbolRenderer):
        # Create a default line symbol if there are no symbols
        symbol = QgsLineSymbol()
        layer.setRenderer(QgsSingleSymbolRenderer(symbol))
    else:
        symbol = layer.renderer().symbol()

    # Change stroke color to black
    for layer in symbol.symbolLayers():
        if isinstance(layer, QgsSimpleLineSymbolLayer):
            layer.setColor(QColor(0, 0, 0))

    if qscat.dockwidget.cb_baseline_show_orientation.isChecked():
        # QgsSymbolLayerAbstractMetadata
        marker_meta = registry.symbolLayerMetadata("MarkerLine")

        # QgsMarkerLineSymbolLayer
        marker_layer = marker_meta.createSymbolLayer(
            {
                "width": "0.26",
                "color": "0,0,0",
                "interval": "3",
                "rotate": "1",
                "placement": "interval",
                "offset": "0.0",
            }
        )

        # QgsMarkerSymbol
        marker_layer_sub_symbol = marker_layer.subSymbol()

        # Remove existing SimpleMarker
        marker_layer_sub_symbol.deleteSymbolLayer(0)

        # QgsSvgMarkerSymbolLayer
        custom_marker = QgsSvgMarkerSymbolLayer(
            path=f"{get_plugin_dir()}/gui/icons/orientation.svg", size=10
        )
        marker_layer_sub_symbol.appendSymbolLayer(custom_marker)

        # Append the symbol layer to the symbol
        symbol.appendSymbolLayer(marker_layer)
    else:
        # Get the indices of all QgsMarkerLineSymbolLayer
        marker_indices = [
            i
            for i, layer in enumerate(symbol.symbolLayers())
            if isinstance(layer, QgsMarkerLineSymbolLayer)
        ]

        for index in reversed(marker_indices):
            symbol.deleteSymbolLayer(index)

    layer.triggerRepaint()
