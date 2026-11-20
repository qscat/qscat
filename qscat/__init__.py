from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qscat.qscat_plugin import QscatPlugin


def classFactory(iface) -> QscatPlugin:
    from qscat.qscat_plugin import QscatPlugin

    return QscatPlugin(iface)
