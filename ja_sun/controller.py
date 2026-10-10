# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""Host integration and grouped, document-safe live edits."""
from copy import deepcopy
import json

from PySide6.QtCore import QObject, QSignalBlocker, QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QInputDialog, QToolBar
from core.saved_views import SavedView

from . import ICON_DIR
from .model import (AddScene, SetLocation, SetShadows, apply_shadow,
                    clock_text, site, solar_details, validated)
from .i18n import language, tr


class Controller(QObject):
    def __init__(self, app):
        super().__init__(app.window)
        self.app = app
        self.grouping = False
        self.record = None
        self.expected = None
        self.internal = False
        self.last_stamp = None
        self.playback = QTimer(self)
        self.playback.setInterval(180)
        self.playback.timeout.connect(lambda: self.run(self.tick))
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.poll)

    @property
    def scene(self):
        return self.app.scene

    def install(self):
        from .ui import Panel
        self.panel = Panel(self)
        self.dock = self.app.add_panel("JA Sun", self.panel)
        self.action = self.app.add_menu_action(tr('JA Sun · Sol y sombras…'), self.show,
                                             "Ctrl+Alt+S", tip=tr('Controlar el sol, las sombras y el recorrido del día.'))
        if self.action is not None:
            self.action.setIcon(QIcon(str(ICON_DIR / "sun.svg")))
            self.action.setIconVisibleInMenu(True)
            self.toolbar = QToolBar("JA Sun", self.app.window)
            self.toolbar.setObjectName("ja_sun_toolbar")
            self.toolbar.setIconSize(QSize(24, 24))
            self.toolbar.addAction(self.action)
            self.app.window.addToolBar(self.toolbar)
        language().changed.connect(self.retranslate)
        self.app.on_document_changed(self.document_changed)
        self.timer.start()
        self.retranslate()

    def retranslate(self):
        self.panel.retranslate()
        if self.action is not None:
            self.action.setText(tr("JA Sun · Sol y sombras…"))
            tip = tr("Controlar el sol, las sombras y el recorrido del día.")
            self.action.setToolTip(tip)
            self.action.setStatusTip(tip)
        self.panel.status.clear()
        self.refresh()

    def show(self):
        self.app.show_panel(self.dock)
        self.refresh()

    def run(self, fn, *args):
        try:
            result = fn(*args)
            self.panel.status.setText("")
            return result
        except (ValueError, TypeError, RuntimeError, KeyError) as exc:
            self.stop()
            self.panel.status.setText(str(exc))
            return None

    def stamp(self):
        sc = self.scene
        return (id(sc), id(sc.shadows), id(self.app.viewport.history),
                sc.content_version, json.dumps(sc.shadows.to_dict(), sort_keys=True),
                site(sc), id(sc.georef),
                id(self.app.viewport.history.undo_stack[-1]) if self.app.viewport.history.undo_stack else None)

    def document_changed(self):
        if not self.internal:
            self.poll()

    def poll(self):
        stamp = self.stamp()
        if self.record is not None and stamp != self.expected:
            self.stop()
        if stamp != self.last_stamp:
            self.refresh()

    def notify(self):
        self.internal = True
        try:
            native = getattr(self.app.window, "shadows_panel", None)
            if native:
                native.refresh()
            action = getattr(self.app.window, "_act_shadows", None)
            if action is not None:
                blocker = QSignalBlocker(action)
                action.setChecked(self.scene.shadows.enabled)
                del blocker
            self.app.viewport.notify_scene_changed()
            self.app.viewport.update()
        finally:
            self.internal = False
        self.expected = self.stamp()
        self.refresh()

    def execute(self, command):
        self.app.viewport.history.execute(command)
        error = self.app.viewport.history.last_error
        if error:
            raise RuntimeError(error)
        self.notify()

    def begin_group(self):
        self.stop()
        self.grouping = True

    def stop(self):
        self.playback.stop()
        self.grouping = False
        self.record = None
        self.expected = None
        if hasattr(self, "panel"):
            self.panel.play.setText(tr('▶ Reproducir'))

    def end_group(self):
        self.grouping = False
        self.record = None
        self.expected = None

    def change(self, patch):
        raw = self.scene.shadows.to_dict()
        raw.update(patch)
        chosen = validated(raw)
        if chosen == self.scene.shadows.to_dict():
            return
        # Only extend a command while it is still the top undo entry and the
        # document is exactly the one we last touched. New/Open/Undo, native
        # shadow edits, and other commands terminate a running gesture.
        if self.record is not None and self.stamp() != self.expected:
            self.stop()
        if self.grouping and self.record is not None:
            self.record.after = deepcopy(chosen)
            apply_shadow(self.scene, chosen)
            self.scene.version += 1
            self.notify()
        else:
            command = SetShadows(chosen)
            self.execute(command)
            if self.grouping:
                self.record = command
                self.expected = self.stamp()

    def manual_change(self, patch):
        if self.playback.isActive():
            self.stop()
        self.change(patch)

    def set_minute(self, minute):
        self.manual_change({"hour": int(minute) // 60, "minute": int(minute) % 60})

    def toggle_play(self):
        if self.playback.isActive():
            self.stop()
            return
        start, end = self.panel.play_range()
        if start >= end:
            raise ValueError(tr('La hora final debe ser posterior a la inicial, dentro del mismo día.'))
        self.begin_group()
        minute = self.scene.shadows.hour * 60 + self.scene.shadows.minute
        if not start <= minute < end:
            minute = start
        self.change({"enabled": True, "hour": minute // 60, "minute": minute % 60})
        # Start with an expected stamp even when enabling was a no-op.
        self.expected = self.stamp()
        self.playback.start()
        self.panel.play.setText(tr('Ⅱ Pausar'))

    def tick(self):
        if self.stamp() != self.expected:
            self.stop()
            self.refresh()
            return
        start, end = self.panel.play_range()
        if start >= end:
            raise ValueError(tr('La hora final debe ser posterior a la inicial.'))
        minute = self.scene.shadows.hour * 60 + self.scene.shadows.minute
        step = self.panel.speed.currentData()
        if minute >= end:
            if not self.panel.loop.isChecked():
                self.stop()
                return
            minute = start
        else:
            minute = min(end, minute + step)
        self.change({"hour": minute // 60, "minute": minute % 60})

    def location(self):
        self.stop()
        values = (self.panel.lat.value(), self.panel.lon.value(), self.panel.north.value())
        if self.scene.georef is not None and values == site(self.scene):
            return
        self.execute(SetLocation(*values))

    def presets(self):
        data = self.app.document_data({})
        if not isinstance(data, dict):
            return {}
        raw = data.get("presets", {})
        if not isinstance(raw, dict):
            return {}
        return {name: value for name, value in raw.items() if isinstance(name, str) and isinstance(value, dict)}

    def save_preset(self, name=None):
        self.stop()
        if name is None:
            dialog = QInputDialog(self.panel)
            dialog.setWindowTitle(tr("Guardar ajuste solar"))
            dialog.setLabelText(tr("Nombre del ajuste:"))
            dialog.setOkButtonText(tr("Aceptar"))
            dialog.setCancelButtonText(tr("Cancelar"))
            accepted = dialog.exec()
            name = dialog.textValue()
            dialog.deleteLater()
            if not accepted:
                return
        name = str(name).strip()
        if not 1 <= len(name) <= 80:
            raise ValueError(tr('Escribe un nombre de 1 a 80 caracteres.'))
        presets = self.presets()
        if any(key.casefold() == name.casefold() for key in presets):
            raise ValueError(tr('Ya existe un ajuste con ese nombre. Usa otro nombre.'))
        presets[name] = validated(self.scene.shadows.to_dict())
        data = self.app.document_data({})
        data = data if isinstance(data, dict) else {}
        data["presets"] = presets
        self.app.set_document_data(data)
        self.refresh()

    def load_preset(self, name):
        self.stop()
        presets = self.presets()
        if name not in presets:
            raise ValueError(tr('Selecciona un ajuste guardado.'))
        # A missing UTC offset in an automatic preset must replace an explicit
        # offset in the current document, not inherit it through a dict update.
        raw = validated(presets[name])
        raw.setdefault("utc_offset", None)
        self.change(raw)

    def delete_preset(self, name):
        self.stop()
        data = self.app.document_data({})
        if not isinstance(data, dict) or name not in self.presets():
            return
        data["presets"].pop(name)
        self.app.set_document_data(data)
        self.refresh()

    def save_scene(self):
        self.stop()
        sh = self.scene.shadows
        base = tr("Sol {day:02d}-{month:02d} · {time}",
                  day=sh.day, month=sh.month, time=clock_text(sh.hour * 60 + sh.minute))
        name, index = base, 2
        names = {v.name.casefold() for v in self.scene.saved_views}
        while name.casefold() in names:
            name = f"{base} ({index})"
            index += 1
        view = SavedView.capture(name, self.scene, self.app.viewport.camera)
        self.execute(AddScene(view))
        self.app.viewport.flash_status(tr("Escena creada: {name}", name=name), 4000)

    def refresh(self):
        self.last_stamp = self.stamp()
        try:
            details = solar_details(self.scene)
        except (ValueError, TypeError, OverflowError) as exc:
            details = None
            self.panel.status.setText(tr("Revisa la fecha o zona horaria del modelo: {error}", error=exc))
        self.panel.refresh(self.scene, details, self.presets())
