# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""A compact Qt panel, following the host palette in light and dark mode."""
import math

from PySide6.QtCore import QDate, QLocale, QPointF, QRectF, Qt, QTime
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPalette, QPen
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDateEdit, QDoubleSpinBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QScrollArea,
    QSlider, QTabWidget, QTimeEdit, QVBoxLayout, QWidget,
)
from .model import clock_text, site, year


STYLE = """
QWidget#jaSun { background: palette(window); color: palette(window-text); }
QWidget#jaSun QLabel { background: transparent; }
QWidget#jaSun QTabWidget::pane { border: 0; }
QWidget#jaSun QTabBar::tab { padding: 8px 11px; }
QWidget#jaSun QFrame[card="true"] { background: palette(base); border: 1px solid palette(midlight); border-radius: 9px; }
QWidget#jaSun QPushButton { padding: 6px 8px; min-height: 17px; }
QWidget#jaSun QPushButton[primary="true"] { background: palette(highlight); color: palette(highlighted-text); border: none; border-radius: 6px; }
QWidget#jaSun QLineEdit, QWidget#jaSun QAbstractSpinBox, QWidget#jaSun QComboBox { min-height: 23px; }
QWidget#jaSun QScrollArea { border: none; background: palette(window); }
"""


def label(text, bold=False):
    widget = QLabel(text)
    widget.setWordWrap(True)
    if bold:
        widget.setStyleSheet("font-weight:600;")
    return widget


class SunPath(QWidget):
    """Polar sky chart; clicks choose a real time on the solar path."""
    def __init__(self, controller):
        super().__init__()
        self.c = controller
        self.details = None
        self.dragging = False
        self.setMinimumHeight(218)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAccessibleName("Recorrido solar. Arrastra sobre la curva para elegir hora; flechas para pasos de cinco minutos.")
        self.setToolTip("Arrastra sobre el recorrido para cambiar la hora. El centro es el cenit; el círculo exterior es el horizonte.")

    def geometry_data(self):
        return QPointF(self.width() / 2, self.height() / 2), min(self.width() / 2 - 32, self.height() / 2 - 27)

    def point(self, elevation, azimuth):
        center, radius = self.geometry_data()
        angle = math.radians(azimuth + self.details["north"])
        r = radius * (90 - elevation) / 90
        return center + QPointF(r * math.sin(angle), -r * math.cos(angle))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        center, radius = self.geometry_data()
        palette = self.palette()
        p.setBrush(palette.brush(QPalette.ColorRole.Base))
        p.setPen(QPen(palette.color(QPalette.ColorRole.Midlight), 1))
        p.drawEllipse(center, radius, radius)
        p.setBrush(Qt.BrushStyle.NoBrush)
        for factor in (1 / 3, 2 / 3):
            p.drawEllipse(center, radius * factor, radius * factor)
        p.drawLine(center + QPointF(-radius, 0), center + QPointF(radius, 0))
        p.drawLine(center + QPointF(0, -radius), center + QPointF(0, radius))
        if self.details is None:
            p.end()
            return
        p.setPen(palette.color(QPalette.ColorRole.Text))
        for az, text in ((0, "N"), (90, "E"), (180, "S"), (270, "O")):
            angle = math.radians(az + self.details["north"])
            pos = center + QPointF((radius + 15) * math.sin(angle), -(radius + 15) * math.cos(angle))
            p.drawText(QRectF(pos.x() - 10, pos.y() - 9, 20, 18), Qt.AlignmentFlag.AlignCenter, text)
        path = QPainterPath()
        connected = False
        for minute, elevation, azimuth in self.details["path"]:
            if elevation <= 0:
                connected = False
                continue
            pos = self.point(elevation, azimuth)
            if connected:
                path.lineTo(pos)
            else:
                path.moveTo(pos)
            connected = True
            if minute in (480, 720, 960):
                p.setPen(palette.color(QPalette.ColorRole.Text))
                text = clock_text(minute)
                width = p.fontMetrics().horizontalAdvance(text)
                x = min(self.width() - width - 5, max(5, pos.x() + 6))
                p.drawText(QPointF(x, pos.y() - 6), text)
        accent = QColor("#dc9b25") if palette.color(QPalette.ColorRole.Window).lightness() < 128 else QColor("#a96808")
        p.setPen(QPen(accent, 2.5))
        p.drawPath(path)
        if self.details["elevation"] > 0:
            pos = self.point(self.details["elevation"], self.details["azimuth"])
            p.setPen(QPen(accent, 1, Qt.PenStyle.DashLine))
            p.drawLine(center, pos)
            p.setPen(QPen(accent, 2))
            p.setBrush(QColor("#f8c55a"))
            p.drawEllipse(pos, 6, 6)
        p.end()

    def choose(self, pos):
        if not self.details:
            return
        samples = [v for v in self.details["path"] if v[1] > 0 and v[0] < 1440]
        if not samples:
            return
        nearest = min(samples, key=lambda v: (self.point(v[1], v[2]) - pos).manhattanLength())
        self.c.run(self.c.set_minute, nearest[0])

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.c.begin_group()
            self.choose(event.position())
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.choose(event.position())

    def mouseReleaseEvent(self, event):
        if self.dragging and event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.c.end_group()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right):
            sh = self.c.scene.shadows
            step = -5 if event.key() == Qt.Key.Key_Left else 5
            self.c.run(self.c.set_minute, max(0, min(1439, sh.hour * 60 + sh.minute + step)))
            event.accept()
        else:
            super().keyPressEvent(event)


class Panel(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.c = controller
        self.updating = True
        self.site_stamp = None
        self.preset_stamp = None
        self.setObjectName("jaSun")
        self.setLocale(QLocale("es_CO"))
        self.setStyleSheet(STYLE)
        self.setMinimumWidth(270)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 8)
        layout.setSpacing(7)
        heading = QHBoxLayout()
        brand = label("JA Sun", True)
        brand.setStyleSheet("font-size:22px; font-weight:700;")
        heading.addWidget(brand)
        heading.addStretch()
        heading.addWidget(label("SOL Y SOMBRAS"))
        layout.addLayout(heading)
        self.enabled = QCheckBox("Mostrar sombras en el modelo")
        self.enabled.toggled.connect(lambda value: self.change({"enabled": value}))
        layout.addWidget(self.enabled)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs, 1)
        self.build_sun()
        self.build_location()
        self.build_presets()
        self.status = label("")
        layout.addWidget(self.status)
        self.updating = False

    def page(self, title):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        box = QVBoxLayout(content)
        box.setContentsMargins(2, 7, 2, 4)
        box.setSpacing(9)
        scroll.setWidget(content)
        self.tabs.addTab(scroll, title)
        return box

    def button(self, text, callback, primary=False):
        button = QPushButton(text)
        button.setProperty("primary", primary)
        button.clicked.connect(lambda _checked=False: self.c.run(callback))
        return button

    def change(self, patch):
        if not self.updating:
            self.c.run(self.c.manual_change, patch)

    def slider(self, minimum, maximum, callback):
        widget = QSlider(Qt.Orientation.Horizontal)
        widget.setRange(minimum, maximum)
        widget.sliderPressed.connect(self.c.begin_group)
        widget.sliderReleased.connect(self.c.end_group)
        widget.valueChanged.connect(lambda value: None if self.updating else self.c.run(callback, value))
        return widget

    def build_sun(self):
        box = self.page("Sol")
        self.chart = SunPath(self.c)
        box.addWidget(self.chart)
        self.metrics = label("")
        self.metrics.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box.addWidget(self.metrics)
        self.daylight = label("")
        self.daylight.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box.addWidget(self.daylight)

        row = QHBoxLayout()
        row.addWidget(label("Fecha", True))
        row.addStretch()
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDisplayFormat("dd MMM")
        self.date.setDateRange(QDate(year(), 1, 1), QDate(year(), 12, 31))
        self.date.setKeyboardTracking(False)
        self.date.dateChanged.connect(lambda value: self.change({"month": value.month(), "day": value.day()}))
        row.addWidget(self.date)
        box.addLayout(row)
        self.doy = self.slider(1, QDate(year(), 12, 31).dayOfYear(), self.set_day)
        self.doy.setAccessibleName("Día del año")
        box.addWidget(self.doy)
        dates = self.dates_grid = QGridLayout()
        self.date_buttons = []
        for index, (month, day, text) in enumerate(((3, 20, "20 mar"), (6, 21, "21 jun"), (9, 22, "22 sep"), (12, 21, "21 dic"))):
            button = self.button(text, lambda m=month, d=day: self.change({"month": m, "day": d}))
            self.date_buttons.append(button)
            dates.addWidget(button, index // 2, index % 2)
        box.addLayout(dates)

        row = QHBoxLayout()
        row.addWidget(label("Hora local", True))
        row.addStretch()
        self.time = QTimeEdit()
        self.time.setDisplayFormat("HH:mm")
        self.time.setKeyboardTracking(False)
        self.time.timeChanged.connect(lambda value: self.change({"hour": value.hour(), "minute": value.minute()}))
        row.addWidget(self.time)
        box.addLayout(row)
        self.time_slider = self.slider(0, 1439, self.c.set_minute)
        self.time_slider.setSingleStep(5)
        self.time_slider.setAccessibleName("Hora local en minutos")
        box.addWidget(self.time_slider)
        quick = self.quick_grid = QGridLayout()
        self.quick_buttons = []
        for text, minute in (("09:00", 540), ("16:00", 960)):
            button = self.button(text, lambda v=minute: self.c.set_minute(v))
            self.quick_buttons.append(button)
            quick.addWidget(button, 0, len(self.quick_buttons) - 1)
        box.addLayout(quick)
        self.noon = self.button("Mediodía solar", lambda: self.c.set_minute(self.chart.details["noon"]))
        quick.addWidget(self.noon, 1, 0, 1, 2)

        row = QHBoxLayout()
        row.addWidget(label("Intensidad de sombra", True))
        row.addStretch()
        self.intensity_text = label("")
        row.addWidget(self.intensity_text)
        box.addLayout(row)
        self.intensity = self.slider(0, 100, lambda v: self.c.manual_change({"darkness": 1 - v / 100}))
        self.intensity.setAccessibleName("Intensidad de sombra, de cero a cien por ciento")
        self.intensity.setToolTip("0 %: sombra imperceptible. 100 %: sombra negra.")
        box.addWidget(self.intensity)

        card = QFrame()
        card.setProperty("card", True)
        inner = QVBoxLayout(card)
        inner.setContentsMargins(9, 9, 9, 9)
        inner.addWidget(label("Recorrer el día", True))
        row = self.range_grid = QGridLayout()
        self.start = QTimeEdit(QTime(6, 0))
        self.end = QTimeEdit(QTime(18, 0))
        for control in (self.start, self.end):
            control.setDisplayFormat("HH:mm")
            control.setKeyboardTracking(False)
            control.timeChanged.connect(lambda _: self.c.stop())
        row.addWidget(self.start, 0, 0)
        row.addWidget(label("→"), 0, 1)
        row.addWidget(self.end, 0, 2)
        self.speed = QComboBox()
        for minute in (5, 15, 30, 60):
            self.speed.addItem(f"{minute} min/paso", minute)
        self.speed.setCurrentIndex(1)
        inner.addLayout(row)
        row.addWidget(self.speed, 1, 0, 1, 3)
        row = QHBoxLayout()
        self.play = self.button("▶ Reproducir", self.c.toggle_play, True)
        row.addWidget(self.play, 1)
        self.loop = QCheckBox("Bucle")
        row.addWidget(self.loop)
        inner.addLayout(row)
        inner.addWidget(label("Pausa conserva la hora · un paso de Deshacer."))
        box.addWidget(card)
        box.addWidget(self.button("Guardar escena del modelo", self.c.save_scene))
        box.addStretch()

    def set_day(self, doy):
        day = QDate(year(), 1, 1).addDays(doy - 1)
        self.c.manual_change({"month": day.month(), "day": day.day()})

    def build_location(self):
        box = self.page("Ubicación")
        self.site_label = label("")
        box.addWidget(self.site_label)
        box.addWidget(label("Lugar y orientación", True))
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        self.lat = QDoubleSpinBox()
        self.lon = QDoubleSpinBox()
        self.north = QDoubleSpinBox()
        for widget, lo, hi, digits in ((self.lat, -80, 84, 6), (self.lon, -180, 179.999999, 6), (self.north, -180, 180, 1)):
            widget.setRange(lo, hi)
            widget.setDecimals(digits)
            widget.setSuffix("°")
            widget.setKeyboardTracking(False)
        self.north.setSingleStep(5)
        form.addRow("Latitud", self.lat)
        form.addRow("Longitud", self.lon)
        form.addRow("Norte desde +Y", self.north)
        box.addLayout(form)
        box.addWidget(label("Norte: giro horario desde el eje verde (+Y). La ubicación y el norte son compartidos con el mapa y el terreno del modelo."))
        box.addWidget(self.button("Aplicar ubicación y norte", self.c.location, True))
        box.addWidget(label("Zona horaria", True))
        self.zone = QComboBox()
        self.zone.addItem("Automática por longitud", None)
        for value in range(-12, 15):
            self.zone.addItem(f"UTC{value:+03d}:00", value)
        self.zone.currentIndexChanged.connect(lambda _: self.change({"utc_offset": self.zone.currentData()}))
        box.addWidget(self.zone)
        box.addWidget(label("La zona automática es una aproximación. Ajusta el desfase local y el horario de verano manualmente. Este motor admite horas enteras."))
        self.year_label = label(f"Año utilizado por el motor: {year()}. La fecha sigue el año del equipo.")
        box.addWidget(self.year_label)
        box.addWidget(label("El sol se calcula a partir de lugar, fecha y hora. La suavidad del borde y la luz ambiental dependen del renderizador y no son controles de este panel."))
        box.addStretch()

    def build_presets(self):
        box = self.page("Guardados")
        box.addWidget(label("Tus ajustes solares", True))
        box.addWidget(label("Guarda fecha, hora, intensidad y zona horaria dentro del archivo IGZ. Los ajustes usan la ubicación actual del modelo."))
        self.saved = QListWidget()
        self.saved.setMinimumHeight(180)
        self.saved.itemDoubleClicked.connect(lambda item: self.c.run(self.c.load_preset, item.text()))
        box.addWidget(self.saved)
        box.addWidget(self.button("Guardar ajuste actual…", self.c.save_preset, True))
        row = QHBoxLayout()
        self.load = self.button("Aplicar", lambda: self.c.load_preset(self.selected_preset()))
        self.delete = self.button("Eliminar", lambda: self.c.delete_preset(self.selected_preset()))
        row.addWidget(self.load)
        row.addWidget(self.delete)
        box.addLayout(row)
        self.saved.itemSelectionChanged.connect(self.preset_selection)
        self.preset_selection()
        box.addWidget(label("Eliminar un ajuste se puede deshacer desde el historial del modelo."))
        box.addStretch()

    def selected_preset(self):
        item = self.saved.currentItem()
        return item.text() if item else ""

    def preset_selection(self):
        selected = self.saved.currentItem() is not None
        self.load.setEnabled(selected)
        self.delete.setEnabled(selected)

    def play_range(self):
        def minute(control):
            return control.time().hour() * 60 + control.time().minute()
        return minute(self.start), minute(self.end)

    def refresh(self, scene, details, presets):
        self.updating = True
        try:
            sh = scene.shadows
            self.enabled.setChecked(sh.enabled)
            day = QDate(year(), sh.month, sh.day)
            if day.isValid():
                self.date.setDate(day)
                self.doy.setValue(day.dayOfYear())
            self.time.setTime(QTime(sh.hour, sh.minute))
            self.time_slider.setValue(sh.hour * 60 + sh.minute)
            intensity = round((1 - sh.darkness) * 100)
            self.intensity.setValue(intensity)
            self.intensity_text.setText(f"{intensity} %")
            index = self.zone.findData(sh.utc_offset)
            self.zone.setCurrentIndex(max(0, index))
            self.chart.details = details
            self.noon.setEnabled(details is not None)
            self.play.setEnabled(details is not None)
            self.chart.update()
            if details:
                elevation, azimuth = details["elevation"], details["azimuth"]
                metrics = f"Altura {elevation:.1f}°   ·   Acimut {azimuth:.1f}°"
                if elevation <= 0:
                    metrics += "\nSol bajo el horizonte · sin sombra solar"
                elif not sh.enabled:
                    metrics += "\nSombras desactivadas"
                elif details["ratio"] is not None:
                    metrics += f"\nSombra de un poste de 1 m: {details['ratio']:.2f} m"
                self.metrics.setText(metrics)
                if details["all_day"]:
                    daylight = "Sol sobre el horizonte durante todo el día"
                elif not details["daylight"]:
                    daylight = "Sol bajo el horizonte durante todo el día"
                else:
                    rise, setting = details["sunrise"], details["sunset"]
                    daylight = f"Salida ≈ {clock_text(rise) if rise is not None else '—'}   ·   Puesta ≈ {clock_text(setting) if setting is not None else '—'}"
                self.daylight.setText(daylight)
                self.daylight.setToolTip("Horizonte geométrico plano. Muestreo cada diez minutos; no considera relieve ni refracción.")
            else:
                self.metrics.setText("Fecha o zona horaria no válida")
                self.daylight.clear()
            stamp = (id(scene), id(scene.shadows), site(scene))
            if stamp != self.site_stamp:
                self.site_stamp = stamp
                lat, lon, north = site(scene)
                self.lat.setValue(lat)
                self.lon.setValue(lon)
                self.north.setValue(north)
            if scene.georef is None:
                self.site_label.setText("Modelo sin ubicación: el motor utiliza Arequipa. Define el lugar real para estudiar el asoleamiento.")
            else:
                self.site_label.setText(f"Ubicación del modelo\n{scene.georef.lat:.5f}°, {scene.georef.lon:.5f}°")
            names = tuple(sorted(presets, key=str.casefold))
            if (id(scene), id(scene.shadows), names) != self.preset_stamp:
                selected = self.selected_preset()
                self.preset_stamp = (id(scene), id(scene.shadows), names)
                self.saved.clear()
                self.saved.addItems(names)
                matches = self.saved.findItems(selected, Qt.MatchFlag.MatchExactly)
                if matches:
                    self.saved.setCurrentItem(matches[0])
            self.preset_selection()
        finally:
            self.updating = False

    def hideEvent(self, event):
        self.c.stop()
        super().hideEvent(event)

    def resizeEvent(self, event):
        wide = self.width() >= 360
        if hasattr(self, "range_grid") and getattr(self, "wide", None) != wide:
            self.wide = wide
            for index, button in enumerate(self.date_buttons):
                self.dates_grid.removeWidget(button)
                self.dates_grid.addWidget(button, 0 if wide else index // 2, index if wide else index % 2)
            for button in (*self.quick_buttons, self.noon):
                self.quick_grid.removeWidget(button)
            self.quick_grid.addWidget(self.quick_buttons[0], 0, 0)
            self.quick_grid.addWidget(self.quick_buttons[1], 0, 2 if wide else 1)
            self.quick_grid.addWidget(self.noon, 0 if wide else 1, 1 if wide else 0, 1, 1 if wide else 2)
            self.range_grid.removeWidget(self.speed)
            self.range_grid.addWidget(self.speed, 0 if wide else 1, 3 if wide else 0, 1, 1 if wide else 3)
        super().resizeEvent(event)
