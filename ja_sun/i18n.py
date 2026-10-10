# SPDX-License-Identifier: GPL-3.0-or-later
"""Plugin-local translations and a persistent interface language preference."""
from dataclasses import dataclass

from PySide6.QtCore import QLocale, QObject, QSettings, Signal


ENGLISH = {
    "SOL Y SOMBRAS": "SUN AND SHADOWS",
    "Mostrar sombras en el modelo": "Show shadows in the model",
    "Sol": "Sun",
    "Fecha": "Date",
    "Día del año": "Day of year",
    "20 mar": "20 Mar",
    "21 jun": "21 Jun",
    "22 sep": "22 Sep",
    "21 dic": "21 Dec",
    "Hora local": "Local time",
    "Hora local en minutos": "Local time in minutes",
    "Mediodía solar": "Solar noon",
    "Intensidad de sombra": "Shadow intensity",
    "Intensidad de sombra, de cero a cien por ciento": "Shadow intensity, from zero to one hundred percent",
    "0 %: sombra imperceptible. 100 %: sombra negra.": "0%: invisible shadow. 100%: black shadow.",
    "Recorrer el día": "Animate the day",
    "▶ Reproducir": "▶ Play",
    "Ⅱ Pausar": "Ⅱ Pause",
    "Bucle": "Loop",
    "Pausa conserva la hora · un paso de Deshacer.": "Pausing keeps the time · one Undo step.",
    "Guardar escena del modelo": "Save model scene",
    "Ubicación": "Location",
    "Lugar y orientación": "Location and orientation",
    "Latitud": "Latitude",
    "Longitud": "Longitude",
    "Norte desde +Y": "North from +Y",
    "Norte: giro horario desde el eje verde (+Y). La ubicación y el norte son compartidos con el mapa y el terreno del modelo.": "North: clockwise rotation from the green axis (+Y). Location and north are shared with the model's map and terrain.",
    "Aplicar ubicación y norte": "Apply location and north",
    "Zona horaria": "Time zone",
    "Automática por longitud": "Automatic by longitude",
    "La zona automática es una aproximación. Ajusta el desfase local y el horario de verano manualmente. Este motor admite horas enteras.": "The automatic time zone is approximate. Set the local UTC offset and daylight saving time manually. This engine supports whole-hour offsets.",
    "El sol se calcula a partir de lugar, fecha y hora. La suavidad del borde y la luz ambiental dependen del renderizador y no son controles de este panel.": "The sun is calculated from the location, date and time. Shadow edge softness and ambient light depend on the renderer and cannot be adjusted in this panel.",
    "Guardados": "Presets",
    "Tus ajustes solares": "Your sun presets",
    "Guarda fecha, hora, intensidad y zona horaria dentro del archivo IGZ. Los ajustes usan la ubicación actual del modelo.": "Save the date, time, intensity and time zone in the IGZ file. Presets use the model's current location.",
    "Guardar ajuste actual…": "Save current preset…",
    "Aplicar": "Apply",
    "Eliminar": "Delete",
    "Eliminar un ajuste se puede deshacer desde el historial del modelo.": "Deleting a preset can be undone through the model's history.",
    "Sol sobre el horizonte durante todo el día": "Sun above the horizon all day",
    "Sol bajo el horizonte durante todo el día": "Sun below the horizon all day",
    "Horizonte geométrico plano. Muestreo cada diez minutos; no considera relieve ni refracción.": "Flat geometric horizon. Sampled every ten minutes; terrain and refraction are not taken into account.",
    "Fecha o zona horaria no válida": "Invalid date or time zone",
    "Modelo sin ubicación: el motor utiliza Arequipa. Define el lugar real para estudiar el asoleamiento.": "The model has no location: the engine uses Arequipa. Set the actual location to study sun exposure.",
    "JA Sun · Sol y sombras…": "JA Sun · Sun and shadows…",
    "Controlar el sol, las sombras y el recorrido del día.": "Control the sun, shadows and daily sun path.",
    "La hora final debe ser posterior a la inicial, dentro del mismo día.": "The end time must be later than the start time, within the same day.",
    "La hora final debe ser posterior a la inicial.": "The end time must be later than the start time.",
    "Guardar ajuste solar": "Save sun preset",
    "Nombre del ajuste:": "Preset name:",
    "Escribe un nombre de 1 a 80 caracteres.": "Enter a name between 1 and 80 characters long.",
    "Ya existe un ajuste con ese nombre. Usa otro nombre.": "A preset with that name already exists. Choose another name.",
    "Selecciona un ajuste guardado.": "Select a saved preset.",
    "Ajustes de sombra no válidos.": "Invalid shadow settings.",
    "Propiedad de sombra desconocida.": "Unknown shadow property.",
    "El estado de sombras debe ser verdadero o falso.": "The shadow state must be true or false.",
    "La fecha y la hora necesitan números enteros.": "The date and time require whole numbers.",
    "La intensidad debe estar entre 0 y 100 %.": "Intensity must be between 0 and 100%.",
    "La zona horaria admite horas enteras entre UTC−12 y UTC+14.": "The time zone supports whole-hour offsets between UTC−12 and UTC+14.",
    "Escribe coordenadas finitas.": "Enter finite coordinates.",
    "Ubicación fuera del dominio UTM admitido por el panel.": "Location outside the UTM range supported by this panel.",
    "JA Sun requiere la API de extensiones 2 de IngeTrazo.": "JA Sun requires IngeTrazo extension API 2.",
    "Recorrido solar. Arrastra sobre la curva para elegir hora; flechas para pasos de cinco minutos.": "Sun path. Drag along the curve to choose a time; use the arrow keys for five-minute steps.",
    "Arrastra sobre el recorrido para cambiar la hora. El centro es el cenit; el círculo exterior es el horizonte.": "Drag along the sun path to change the time. The center is the zenith; the outer circle is the horizon.",
    "Idioma": "Language",
    "O": "W",
    "E": "E",
    "{minute} min/paso": "{minute} min/step",
    "Año utilizado por el motor: {year}. La fecha sigue el año del equipo.": "Year used by the engine: {year}. The date follows the computer's year.",
    "Altura {elevation:.1f}°   ·   Acimut {azimuth:.1f}°": "Elevation {elevation:.1f}°   ·   Azimuth {azimuth:.1f}°",
    "Sombra de un poste de 1 m: {ratio:.2f} m": "Shadow of a 1 m post: {ratio:.2f} m",
    "Sol bajo el horizonte · sin sombra solar": "Sun below the horizon · no sun shadow",
    "Sombras desactivadas": "Shadows disabled",
    "Salida ≈ {rise}   ·   Puesta ≈ {setting}": "Sunrise ≈ {rise}   ·   Sunset ≈ {setting}",
    "Ubicación del modelo": "Model location",
    "Sol {day:02d}-{month:02d} · {time}": "Sun {day:02d}-{month:02d} · {time}",
    "Escena creada: {name}": "Scene created: {name}",
    "Revisa la fecha o zona horaria del modelo: {error}": "Check the model's date or time zone: {error}",
    "Aceptar": "OK",
    "Cancelar": "Cancel"
}


GERMAN = {
    "SOL Y SOMBRAS": "SONNE UND SCHATTEN",
    "Mostrar sombras en el modelo": "Schatten im Modell anzeigen",
    "Sol": "Sonne",
    "Fecha": "Datum",
    "Día del año": "Tag des Jahres",
    "20 mar": "20. März",
    "21 jun": "21. Juni",
    "22 sep": "22. Sept.",
    "21 dic": "21. Dez.",
    "Hora local": "Ortszeit",
    "Hora local en minutos": "Ortszeit in Minuten",
    "Mediodía solar": "Sonnenhöchststand",
    "Intensidad de sombra": "Schattenstärke",
    "Intensidad de sombra, de cero a cien por ciento": "Schattenstärke von null bis hundert Prozent",
    "0 %: sombra imperceptible. 100 %: sombra negra.": "0 %: unsichtbarer Schatten. 100 %: schwarzer Schatten.",
    "Recorrer el día": "Tagesverlauf abspielen",
    "▶ Reproducir": "▶ Abspielen",
    "Ⅱ Pausar": "Ⅱ Pause",
    "Bucle": "Wiederholen",
    "Pausa conserva la hora · un paso de Deshacer.": "Pause behält die Uhrzeit bei · ein Rückgängig-Schritt.",
    "Guardar escena del modelo": "Modellszene speichern",
    "Ubicación": "Standort",
    "Lugar y orientación": "Standort und Ausrichtung",
    "Latitud": "Breitengrad",
    "Longitud": "Längengrad",
    "Norte desde +Y": "Norden relativ zu +Y",
    "Norte: giro horario desde el eje verde (+Y). La ubicación y el norte son compartidos con el mapa y el terreno del modelo.": "Norden: Drehung im Uhrzeigersinn ausgehend von der grünen Achse (+Y). Standort und Nordrichtung gelten auch für die Karte und das Gelände des Modells.",
    "Aplicar ubicación y norte": "Standort und Nordrichtung übernehmen",
    "Zona horaria": "Zeitzone",
    "Automática por longitud": "Automatisch nach Längengrad",
    "La zona automática es una aproximación. Ajusta el desfase local y el horario de verano manualmente. Este motor admite horas enteras.": "Die automatische Zeitzone ist eine Näherung. UTC-Abweichung und Sommerzeit müssen manuell eingestellt werden. Die Berechnung unterstützt nur Abweichungen in ganzen Stunden.",
    "El sol se calcula a partir de lugar, fecha y hora. La suavidad del borde y la luz ambiental dependen del renderizador y no son controles de este panel.": "Der Sonnenstand wird aus Standort, Datum und Uhrzeit berechnet. Weiche Schattenkanten und Umgebungslicht hängen vom Renderer ab und lassen sich in diesem Panel nicht einstellen.",
    "Guardados": "Vorlagen",
    "Tus ajustes solares": "Gespeicherte Sonneneinstellungen",
    "Guarda fecha, hora, intensidad y zona horaria dentro del archivo IGZ. Los ajustes usan la ubicación actual del modelo.": "Datum, Uhrzeit, Schattenstärke und Zeitzone werden in der IGZ-Datei gespeichert. Die Vorlagen verwenden den aktuellen Standort des Modells.",
    "Guardar ajuste actual…": "Aktuelle Einstellungen speichern…",
    "Aplicar": "Übernehmen",
    "Eliminar": "Löschen",
    "Eliminar un ajuste se puede deshacer desde el historial del modelo.": "Das Löschen einer Vorlage lässt sich über den Verlauf des Modells rückgängig machen.",
    "Sol sobre el horizonte durante todo el día": "Sonne den ganzen Tag über dem Horizont",
    "Sol bajo el horizonte durante todo el día": "Sonne den ganzen Tag unter dem Horizont",
    "Horizonte geométrico plano. Muestreo cada diez minutos; no considera relieve ni refracción.": "Ebener geometrischer Horizont. Berechnung im Abstand von zehn Minuten; Gelände und Lichtbrechung werden nicht berücksichtigt.",
    "Fecha o zona horaria no válida": "Ungültiges Datum oder ungültige Zeitzone",
    "Modelo sin ubicación: el motor utiliza Arequipa. Define el lugar real para estudiar el asoleamiento.": "Das Modell hat keinen Standort: Die Berechnung verwendet Arequipa. Für die Untersuchung der Besonnung den tatsächlichen Standort festlegen.",
    "JA Sun · Sol y sombras…": "JA Sun · Sonne und Schatten…",
    "Controlar el sol, las sombras y el recorrido del día.": "Sonnenstand, Schatten und Tagesverlauf steuern.",
    "La hora final debe ser posterior a la inicial, dentro del mismo día.": "Die Endzeit muss nach der Startzeit und am selben Tag liegen.",
    "La hora final debe ser posterior a la inicial.": "Die Endzeit muss nach der Startzeit liegen.",
    "Guardar ajuste solar": "Sonneneinstellungen speichern",
    "Nombre del ajuste:": "Name der Vorlage:",
    "Escribe un nombre de 1 a 80 caracteres.": "Einen Namen mit 1 bis 80 Zeichen eingeben.",
    "Ya existe un ajuste con ese nombre. Usa otro nombre.": "Eine Vorlage mit diesem Namen ist bereits vorhanden. Einen anderen Namen wählen.",
    "Selecciona un ajuste guardado.": "Eine gespeicherte Vorlage auswählen.",
    "Ajustes de sombra no válidos.": "Ungültige Schatteneinstellungen.",
    "Propiedad de sombra desconocida.": "Unbekannte Schatteneigenschaft.",
    "El estado de sombras debe ser verdadero o falso.": "Der Schattenstatus muss wahr oder falsch sein.",
    "La fecha y la hora necesitan números enteros.": "Datum und Uhrzeit müssen als ganze Zahlen angegeben werden.",
    "La intensidad debe estar entre 0 y 100 %.": "Die Schattenstärke muss zwischen 0 und 100 % liegen.",
    "La zona horaria admite horas enteras entre UTC−12 y UTC+14.": "Die Zeitzone unterstützt ganze Stunden zwischen UTC−12 und UTC+14.",
    "Escribe coordenadas finitas.": "Endliche Koordinatenwerte eingeben.",
    "Ubicación fuera del dominio UTM admitido por el panel.": "Der Standort liegt außerhalb des vom Panel unterstützten UTM-Bereichs.",
    "JA Sun requiere la API de extensiones 2 de IngeTrazo.": "JA Sun benötigt die Erweiterungs-API 2 von IngeTrazo.",
    "Recorrido solar. Arrastra sobre la curva para elegir hora; flechas para pasos de cinco minutos.": "Sonnenbahn. Zum Wählen der Uhrzeit entlang der Kurve ziehen; Pfeiltasten ändern die Uhrzeit in Schritten von fünf Minuten.",
    "Arrastra sobre el recorrido para cambiar la hora. El centro es el cenit; el círculo exterior es el horizonte.": "Entlang der Sonnenbahn ziehen, um die Uhrzeit zu ändern. Die Mitte ist der Zenit; der äußere Kreis ist der Horizont.",
    "Idioma": "Sprache",
    "O": "W",
    "E": "O",
    "{minute} min/paso": "{minute} Min./Schritt",
    "Año utilizado por el motor: {year}. La fecha sigue el año del equipo.": "Verwendetes Berechnungsjahr: {year}. Das Datum richtet sich nach dem Jahr des Computers.",
    "Altura {elevation:.1f}°   ·   Acimut {azimuth:.1f}°": "Sonnenhöhe {elevation:.1f}°   ·   Azimut {azimuth:.1f}°",
    "Sombra de un poste de 1 m: {ratio:.2f} m": "Schatten eines 1 m hohen Pfostens: {ratio:.2f} m",
    "Sol bajo el horizonte · sin sombra solar": "Sonne unter dem Horizont · kein Sonnenschatten",
    "Sombras desactivadas": "Schatten deaktiviert",
    "Salida ≈ {rise}   ·   Puesta ≈ {setting}": "Sonnenaufgang ≈ {rise}   ·   Sonnenuntergang ≈ {setting}",
    "Ubicación del modelo": "Modellstandort",
    "Sol {day:02d}-{month:02d} · {time}": "Sonne {day:02d}-{month:02d} · {time}",
    "Escena creada: {name}": "Szene erstellt: {name}",
    "Revisa la fecha o zona horaria del modelo: {error}": "Datum oder Zeitzone des Modells prüfen: {error}",
    "Aceptar": "OK",
    "Cancelar": "Abbrechen"
}


@dataclass(frozen=True)
class LanguageSpec:
    """Native display name, Qt locale, and Spanish-source translations."""

    name: str
    locale: str
    translations: dict[str, str]


# Register new languages here; no UI or preference-handling changes are needed.
# Missing translations fall back to English, then to the original source text.
DEFAULT_LANGUAGE = "en"
LANGUAGES = {
    "de": LanguageSpec("Deutsch", "de_DE", GERMAN),
    "en": LanguageSpec("English", "en_GB", ENGLISH),
    "es": LanguageSpec("Español", "es_CO", {source: source for source in ENGLISH}),
}


def default_language(locale=None):
    """Prefer an exact system locale, then its language, then English."""
    locale = QLocale.system() if locale is None else locale
    for code, spec in LANGUAGES.items():
        if QLocale(spec.locale).name() == locale.name():
            return code
    for code, spec in LANGUAGES.items():
        if QLocale(spec.locale).language() == locale.language():
            return code
    return DEFAULT_LANGUAGE


class Language(QObject):
    changed = Signal()

    def __init__(self):
        super().__init__()
        self.settings = QSettings("IngeTrazo", "JA Sun")
        default = default_language()
        saved = self.settings.value("interface/language", default)
        self.code = saved if saved in LANGUAGES else default

    @property
    def locale(self):
        return QLocale(LANGUAGES[self.code].locale)

    def set(self, code):
        if code not in LANGUAGES or code == self.code:
            return
        self.code = code
        self.settings.setValue("interface/language", code)
        self.changed.emit()


_language = None


def language():
    global _language
    if _language is None:
        _language = Language()
    return _language


def tr(source, **values):
    translations = LANGUAGES[language().code].translations
    fallback = LANGUAGES[DEFAULT_LANGUAGE].translations
    text = translations.get(source, fallback.get(source, source))
    return text.format(**values) if values else text
