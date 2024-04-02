from qgis.core import QgsApplication

def show_baseline_orientation(self):
    # TODO: dont overlap
    # TODO: Add L and R
    layer = self.dockwidget.qmlcb_baseline_baseline_layer.currentLayer()
    registry = QgsApplication.symbolLayerRegistry()
    symbol = layer.renderer().symbol()
    marker_meta = registry.symbolLayerMetadata("MarkerLine")
    marker_layer = marker_meta.createSymbolLayer(
        {'width': '0.26', 'color': '0,0,0', 'interval': '3', 
        'rotate': '1', 'placement': 'interval', 'offset': '0.0'})
    marker_layer_sub_symbol = marker_layer.subSymbol()
    marker_layer_sub_symbol.deleteSymbolLayer(0)
    custom_marker = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer(
        {'name': 'filled_arrowhead', 'color': '0,0,0', 'color_border': '0,0,0', 
        'offset': '0,0', 'size': '3.0', 'angle': '0'})
    marker_layer_sub_symbol.appendSymbolLayer(custom_marker)
    #symbol.deleteSymbolLayer(0)
    symbol.appendSymbolLayer(marker_layer)
    layer.triggerRepaint()