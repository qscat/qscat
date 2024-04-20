# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

from PyQt5.QtGui import QColor

from qgis.core import QgsCategorizedSymbolRenderer
from qgis.core import QgsClassificationEqualInterval
from qgis.core import QgsClassificationJenks
from qgis.core import QgsClassificationPrettyBreaks
from qgis.core import QgsClassificationQuantile
from qgis.core import QgsFillSymbol
from qgis.core import QgsGradientStop
from qgis.core import QgsGraduatedSymbolRenderer
from qgis.core import QgsLineSymbol
from qgis.core import QgsRendererCategory
from qgis.core import QgsRendererRange
from qgis.core import QgsStyle
from qgis.core import QgsSymbol

from qscat.core.utils.input import get_highest_unc_from_input
from qscat.core.utils.input import get_epr_unc_from_input
from qscat.core.utils.layer import is_field_in_layer

from qscat.core.constants import Statistic
from qscat.core.constants import Trend


def apply_area_colors(layer):
    """Apply colors to the layer output of the area change feature based 
       on `area_type` field.

    Args:
        layer (QgsVectorLayer): The layer to apply the colors to.
    """
    field_name = 'area_type'

    accretion_symbol = QgsFillSymbol.createSimple(
        {'color': QColor(34,101,188,255), 'style': 'solid'}
    )
    erosion_symbol = QgsFillSymbol.createSimple(
        {'color': QColor(173,29,42,255), 'style': 'solid'}
    )
    stable_symbol = QgsFillSymbol.createSimple(
        {'color': QColor(229,228,218,255), 'style': 'solid'}
    )
    accretion_symbol.setOpacity(0.5)
    erosion_symbol.setOpacity(0.5)
    stable_symbol.setOpacity(0.5)

    categories = [
        QgsRendererCategory(
            value=Trend.ACCRETING,
            symbol=accretion_symbol,
            label=Trend.ACCRETING,
        ),
        QgsRendererCategory(
            value=Trend.ERODING,
            symbol=erosion_symbol,
            label=Trend.ERODING,
        ),
        QgsRendererCategory(
            value=Trend.STABLE,
            symbol=stable_symbol,
            label=Trend.STABLE,
        ),
    ]
    renderer = QgsCategorizedSymbolRenderer(field_name, categories)
    layer.setRenderer(renderer)
    layer.triggerRepaint()


def apply_color_ramp(self):
    """Apply color ramp to the layer based on the selected stat layer in the GUI.
    """
    layer = self.dockwidget.qmlcb_vis_stat_layer.currentLayer()
    mode = self.dockwidget.cb_vis_mode.currentIndex()

    pos_classes = int(self.dockwidget.qsb_vis_pos_classes.text())
    neg_classes = int(self.dockwidget.qsb_vis_neg_classes.text())

    if is_field_in_layer(Statistic.SCE, layer):
        stat = Statistic.SCE
        uncertainty = get_highest_unc_from_input(self) # TODO: get from layer custom property
    elif is_field_in_layer(Statistic.NSM, layer):
        stat = Statistic.NSM
        uncertainty = get_highest_unc_from_input(self) # TODO: get from layer custom property
    elif is_field_in_layer(Statistic.EPR, layer):
        stat = Statistic.EPR
        uncertainty = get_epr_unc_from_input(self) # TODO: get from layer custom property
    elif is_field_in_layer(Statistic.LRR, layer):
        stat = Statistic.LRR
        uncertainty = None
    elif is_field_in_layer(Statistic.WLR, layer):
        stat = Statistic.WLR
        uncertainty = None

    feats = layer.getFeatures()
    values = [f[stat] for f in feats]

    default_style = QgsStyle().defaultStyle()
    color_ramp = default_style.colorRamp("Greys")
   
    if stat == Statistic.SCE:
        # grey - start color
        color_ramp.setColor1(QColor(229,228,218))

        # blue - end color
        color_ramp.setColor2(QColor(34,101,188))
   
    elif stat in [Statistic.NSM, Statistic.EPR, Statistic.LRR, Statistic.WLR]:
        # red - start color
        color_ramp.setColor1(QColor(173,29,42))

        # blue - end color
        color_ramp.setColor2(QColor(34,101,188))

        # grey mid color
        color_ramp.setStops([QgsGradientStop(0.5, QColor(229,228,218))])

    classification_methods = [
        QgsClassificationQuantile(),
        QgsClassificationEqualInterval(),
        QgsClassificationJenks(),
        QgsClassificationPrettyBreaks()
    ]
    classification_method = classification_methods[mode]
    classification_method.setLabelFormat("%1 – %2")
    classification_method.setLabelPrecision(2)
    classification_method.setLabelTrimTrailingZeroes(True)
    
    # Determine if color ramp has uncertainty value
    if stat == Statistic.NSM or stat == Statistic.EPR:
        neg_minimum = min(values)
        neg_maximum = -uncertainty
        #neg_classes = 4

        pos_minimum = uncertainty
        pos_maximum = max(values)
        #pos_classes = 4

        # Specific modes need list of values, and max and min
        if mode == 0 or mode == 2:
            neg_values = sorted(i for i in values if i <= uncertainty)
            pos_values = sorted(i for i in values if i >= uncertainty)
            neg_ranges = classification_method.classes(
                neg_values, 
                neg_classes
            )
            pos_ranges = classification_method.classes(
                pos_values,
                pos_classes
            )

        elif mode == 1 or mode == 3:
            neg_ranges = classification_method.classes(
                neg_minimum, neg_maximum, neg_classes
            )
            pos_ranges = classification_method.classes(
                pos_minimum, pos_maximum, pos_classes
            )
        
        # For stable values
        classification_method_unc = QgsClassificationEqualInterval()
        classification_method_unc.setLabelFormat("%1 – %2")
        classification_method_unc.setLabelPrecision(2)
        classification_method_unc.setLabelTrimTrailingZeroes(True)
        
        unc_range = classification_method_unc.classes(
            -uncertainty, uncertainty, 1
        )
        ranges = neg_ranges + unc_range + pos_ranges
    
    elif stat == Statistic.SCE:
        pos_maximum = max(values)
        if mode == 0 or mode == 2:
            ranges = classification_method.classes(
                values,
                pos_classes
            )
        elif mode == 1 or mode == 3:
            ranges = classification_method.classes(
                0.0,
                pos_maximum,
                pos_classes
            )

    elif stat == Statistic.LRR or stat == Statistic.WLR:
        if mode == 0 or mode == 2:
            ranges = classification_method.classes(
                values,
                pos_classes*2
            )
        elif mode == 1 or mode == 3:
            ranges = classification_method.classes(
                min(values),
                max(values),
                pos_classes*2
            )

    symbol = QgsLineSymbol.createSimple({'capstyle': 'round'})
    symbol.setWidth(1.5)
    
    render_ranges = [
        QgsRendererRange(
            r, QgsSymbol.defaultSymbol(layer.geometryType())
        ) for r in ranges
    ]
    renderer = QgsGraduatedSymbolRenderer(stat, render_ranges)
    renderer.updateColorRamp(color_ramp)
    renderer.updateSymbols(symbol)
    layer.setRenderer(renderer)
    layer.triggerRepaint()