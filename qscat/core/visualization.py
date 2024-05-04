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

from qscat.core.constants import AreaChangeField
from qscat.core.constants import Statistic
from qscat.core.constants import Trend


def apply_area_colors(layer):
    """Apply colors to the layer output of the area change feature based
       on `AreaChangeField.TREND`.

    Args:
        layer (QgsVectorLayer): The layer to apply the colors to.
    """
    accreting_symbol = QgsFillSymbol.createSimple(
        {"color": QColor(34, 101, 188, 255), "style": "solid"}
    )
    eroding_symbol = QgsFillSymbol.createSimple(
        {"color": QColor(173, 29, 42, 255), "style": "solid"}
    )
    stable_symbol = QgsFillSymbol.createSimple(
        {"color": QColor(229, 228, 218, 255), "style": "solid"}
    )
    accreting_symbol.setOpacity(0.5)
    eroding_symbol.setOpacity(0.5)
    stable_symbol.setOpacity(0.5)

    categories = [
        QgsRendererCategory(
            Trend.ERODING,
            eroding_symbol,
            Trend.ERODING,
        ),
        QgsRendererCategory(
            Trend.STABLE,
            stable_symbol,
            Trend.STABLE,
        ),
        QgsRendererCategory(
            Trend.ACCRETING,
            accreting_symbol,
            Trend.ACCRETING,
        ),
    ]
    renderer = QgsCategorizedSymbolRenderer(AreaChangeField.TREND, categories)
    layer.setRenderer(renderer)
    layer.triggerRepaint()


def apply_color_ramp_button_clicked(qscat):
    """Apply custom graduated symbology values on the selected shoreline change
    statistic layer (on button clicked).

    Args:
        qscat (QscatPlugin): QscatPlugin instance.
    """
    layer = qscat.dockwidget.qmlcb_vis_stat_layer.currentLayer()
    mode = qscat.dockwidget.cb_vis_mode.currentIndex()

    num_of_pos_classes = int(qscat.dockwidget.qsb_vis_pos_classes.text())
    num_of_neg_classes = int(qscat.dockwidget.qsb_vis_neg_classes.text())

    unc = None
    if layer.customProperty("stat") in (Statistic.EPR, Statistic.SCE, Statistic.NSM):
        unc = layer.customProperty("unc")

    apply_color_ramp(layer, mode, num_of_pos_classes, num_of_neg_classes, unc)


def apply_color_ramp(
    layer,
    mode,
    num_of_pos_classes,
    num_of_neg_classes,
    unc,
):
    """Apply custom graduated symbology values on the selected shoreline change
    statistic layer.

    Args:
        layer (QgsVectorLayer): The layer to apply the colors to.
        mode (int): The mode of classification.
        num_of_pos_classes (int): The number of positive classes.
        num_of_neg_classes (int): The number of negative classes.
        unc (float): The highest uncertainty or EPR uncertainty value.
    """
    stat = layer.customProperty("stat")

    feats = layer.getFeatures()
    vals = [f[stat] for f in feats]

    default_style = QgsStyle().defaultStyle()
    color_ramp = default_style.colorRamp("Greys")

    # Colors
    if stat == Statistic.SCE:
        color_ramp.setColor1(QColor(229, 228, 218))  # greyish
        color_ramp.setColor2(QColor(34, 101, 188))  # bluish

    elif stat in (Statistic.NSM, Statistic.EPR, Statistic.LRR, Statistic.WLR):
        color_ramp.setColor1(QColor(173, 29, 42))  # reddish
        color_ramp.setColor2(QColor(34, 101, 188))  # bluish

        # For LRR and WLR, also sets middle color to greyish
        color_ramp.setStops(
            [QgsGradientStop(0.5, QColor(229, 228, 218))]
        )  # greyish - middle

    classification_methods = [
        QgsClassificationQuantile(),
        QgsClassificationEqualInterval(),
        QgsClassificationJenks(),
        QgsClassificationPrettyBreaks(),
    ]
    classification_method = classification_methods[mode]
    classification_method.setLabelFormat("%1 – %2")
    classification_method.setLabelPrecision(2)
    classification_method.setLabelTrimTrailingZeroes(True)

    # For stable value we use equal interval classification
    classification_method_unc = QgsClassificationEqualInterval()
    classification_method_unc.setLabelFormat("%1 – %2")
    classification_method_unc.setLabelPrecision(2)
    classification_method_unc.setLabelTrimTrailingZeroes(True)

    # Negative, Stable, Positive class
    if stat in (Statistic.NSM, Statistic.EPR):
        neg_min = min(vals)
        neg_max = -unc
        pos_min = unc
        pos_max = max(vals)

        if mode in (0, 2):
            neg_vals = sorted(i for i in vals if i <= -unc)
            pos_vals = sorted(i for i in vals if i >= unc)
            neg_ranges = classification_method.classes(
                values=neg_vals, nclasses=num_of_neg_classes
            )
            pos_ranges = classification_method.classes(
                values=pos_vals, nclasses=num_of_pos_classes
            )

        elif mode in (1, 3):
            neg_ranges = classification_method.classes(
                minimum=neg_min, maximum=neg_max, nclasses=num_of_neg_classes
            )
            pos_ranges = classification_method.classes(
                minimum=pos_min, maximum=pos_max, nclasses=num_of_pos_classes
            )

        # Stable value
        unc_range = classification_method_unc.classes(
            minimum=-unc, maximum=unc, nclasses=1
        )
        ranges = neg_ranges + unc_range + pos_ranges

    # Stable, Positive class
    elif stat == Statistic.SCE:
        pos_min = unc
        pos_max = max(vals)

        if mode in (0, 2):
            pos_vals = sorted(i for i in vals if i >= unc)
            pos_ranges = classification_method.classes(
                values=pos_vals, nclasses=num_of_pos_classes
            )

        elif mode in (1, 3):
            pos_ranges = classification_method.classes(
                minimum=pos_min, maximum=pos_max, nclasses=num_of_pos_classes
            )

        # Stable value
        unc_range = classification_method_unc.classes(
            minimum=0, maximum=unc, nclasses=1
        )
        ranges = unc_range + pos_ranges

    # Negative, Positive class in one range
    elif stat in (Statistic.LRR, Statistic.WLR):
        if mode in (0, 2):
            ranges = classification_method.classes(
                values=vals, nclasses=num_of_pos_classes * 2
            )
        elif mode in (1, 3):
            ranges = classification_method.classes(
                minimum=min(vals),
                maximum=max(vals),
                nclasses=num_of_pos_classes * 2,
            )

    symbol = QgsLineSymbol.createSimple({"capstyle": "round"})
    symbol.setWidth(1.5)

    render_ranges = [
        QgsRendererRange(r, QgsSymbol.defaultSymbol(layer.geometryType()))
        for r in ranges
    ]
    renderer = QgsGraduatedSymbolRenderer(stat, render_ranges)
    renderer.updateColorRamp(color_ramp)
    renderer.updateSymbols(symbol)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
