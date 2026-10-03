# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""JA Sun: a native, reversible solar study panel for IngeTrazo."""
from pathlib import Path

__version__ = "0.1.0"
__author__ = "Julio Angulo"
__license__ = "GPL-3.0-or-later"
ICON_DIR = Path(__file__).resolve().parent / "icons"


def setup(app):
    if getattr(app, "api_version", 0) < 2:
        raise RuntimeError("JA Sun requiere la API de extensiones 2 de IngeTrazo.")
    controllers = getattr(app.window, "_ja_sun_controllers", None)
    if controllers is None:
        controllers = app.window._ja_sun_controllers = {}
    if app.key not in controllers:
        from .controller import Controller
        controller = Controller(app)
        controller.install()
        controllers[app.key] = controller
    return controllers[app.key]
