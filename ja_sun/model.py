# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""Native solar math and small commands; no geometry snapshots of our own."""
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
import math

from core import sun
from core.history import Command
from georef.datum import SceneDatum


def year():
    # The viewport uses date.today().year: expose that year, never a fake override.
    return date.today().year


def site(scene):
    datum = getattr(scene, "georef", None)
    if datum is None:
        return sun.DEFAULT_LAT, sun.DEFAULT_LON, 0.0
    return datum.lat, datum.lon, datum.north


def validated(raw):
    """Reject invalid dates and offsets before entering host history."""
    if not isinstance(raw, dict):
        raise ValueError("Ajustes de sombra no válidos.")
    allowed = {"enabled", "month", "day", "hour", "minute", "darkness", "utc_offset"}
    if set(raw) - allowed:
        raise ValueError("Propiedad de sombra desconocida.")
    result = sun.ShadowSettings().to_dict()
    result.update(raw)
    if type(result["enabled"]) is not bool:
        raise ValueError("El estado de sombras debe ser verdadero o falso.")
    for key in ("month", "day", "hour", "minute"):
        if type(result[key]) is not int:
            raise ValueError("La fecha y la hora necesitan números enteros.")
    datetime(year(), result["month"], result["day"], result["hour"], result["minute"])
    dark = result["darkness"]
    if isinstance(dark, bool) or not isinstance(dark, (int, float)) or not math.isfinite(dark) or not 0 <= dark <= 1:
        raise ValueError("La intensidad debe estar entre 0 y 100 %.")
    offset = result.get("utc_offset")
    if offset is not None and (type(offset) is not int or not -12 <= offset <= 14):
        raise ValueError("La zona horaria admite horas enteras entre UTC−12 y UTC+14.")
    if offset is None:
        result.pop("utc_offset", None)
    return result


def apply_shadow(scene, raw):
    # Keep the object identity: the native tray may retain this reference.
    fresh = sun.ShadowSettings.from_dict(raw)
    scene.shadows.__dict__.update(fresh.__dict__)


class SetShadows(Command):
    def __init__(self, raw):
        self.after = validated(raw)
        self.before = None

    def do(self, scene):
        if self.before is None:
            self.before = scene.shadows.to_dict()
        apply_shadow(scene, self.after)
        scene.version += 1

    def undo(self, scene):
        apply_shadow(scene, self.before)
        scene.version += 1


class SetLocation(Command):
    def __init__(self, lat, lon, north):
        if not all(math.isfinite(v) for v in (lat, lon, north)):
            raise ValueError("Escribe coordenadas finitas.")
        if not -80 <= lat <= 84 or not -180 <= lon < 180 or not -180 <= north <= 180:
            raise ValueError("Ubicación fuera del dominio UTM admitido por el panel.")
        self.values = (lat, lon, north)
        self.before = None
        self.captured = False

    def do(self, scene):
        if not self.captured:
            self.before = deepcopy(scene.georef.to_dict()) if scene.georef else None
            self.captured = True
        lat, lon, north = self.values
        altitude = self.before.get("alt", 0.0) if self.before else 0.0
        scene.georef = SceneDatum(lat, lon, altitude, north=north)
        scene.version += 1

    def undo(self, scene):
        scene.georef = SceneDatum.from_dict(self.before) if self.before else None
        scene.version += 1


class AddScene(Command):
    def __init__(self, view):
        self.view = view

    def do(self, scene):
        if self.view not in scene.saved_views:
            scene.saved_views.append(self.view)
        scene.version += 1

    def undo(self, scene):
        if self.view in scene.saved_views:
            scene.saved_views.remove(self.view)
        scene.version += 1


def offset_for(raw, lon):
    value = raw.get("utc_offset")
    return sun.default_utc_offset(lon) if value is None else value


@lru_cache(maxsize=48)
def path_for(lat, lon, month, day, offset, current_year):
    """Ten-minute samples, with the exact midnight endpoint for chart continuity."""
    tz = timezone(timedelta(hours=offset))
    start = datetime(current_year, month, day, tzinfo=tz)
    return tuple((minute, *sun.solar_position(lat, lon, (start + timedelta(minutes=minute)).astimezone(timezone.utc)))
                 for minute in range(0, 1441, 10))


def solar_details(scene):
    raw = validated(scene.shadows.to_dict())
    lat, lon, north = site(scene)
    offset = offset_for(raw, lon)
    when = scene.shadows.when_utc(lon, year=year())
    elevation, azimuth = sun.solar_position(lat, lon, when)
    path = path_for(lat, lon, raw["month"], raw["day"], offset, year())
    daylight = [p for p in path[:-1] if p[1] > 0]
    # None/polar day remain explicit; a wraparound daylight interval is not
    # incorrectly labelled as a single sunrise/sunset pair.
    rising = [b[0] for a, b in zip(path, path[1:]) if a[1] <= 0 < b[1]]
    setting = [b[0] for a, b in zip(path, path[1:]) if a[1] > 0 >= b[1]]
    return dict(elevation=elevation, azimuth=azimuth, north=north, path=path,
                sunrise=rising[0] if rising else None,
                sunset=setting[0] if setting else None,
                daylight=bool(daylight), all_day=len(daylight) == 144,
                noon=max(path[:-1], key=lambda p: p[1])[0], offset=offset,
                ratio=1 / math.tan(math.radians(elevation)) if elevation > 0 else None)


def clock_text(minute):
    return f"{minute // 60:02d}:{minute % 60:02d}"
