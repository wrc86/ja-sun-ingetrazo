# Desarrollo de JA Sun

**Alcance de esta separación:** este repositorio contiene el plugin, su documentación y el ZIP instalable. Los comandos de pruebas y empaquetado descritos abajo pertenecen al entorno o paquete de fuentes original; sus carpetas `tests/`, `scripts/` y `.reference/` no se incluyen aquí. No se presentan como comandos ejecutables desde esta copia.


Copyright © 2026 Julio Angulo. GPL-3.0-or-later; véase LICENSE.

1. Obtén el código de https://github.com/ingelibre/ingetrazo en `.reference/ingetrazo`.
   La revisión comprobada es `6be29fe` (0.5.7, API 2).
2. Crea un entorno `dev-env` con las dependencias del anfitrión y pytest.
3. Desde la raíz de este espacio o de la distribución fuente:

```sh
dev-env/bin/python -m pytest tests/test_ja_sun.py -q
dev-env/bin/python scripts/preview_ja_sun.py
dev-env/bin/python scripts/build_ja_sun_release.py
dev-env/bin/python scripts/verify_ja_sun_release.py
```

Para comprobar el viewport real en macOS, en una sesión gráfica:

```sh
QT_QPA_PLATFORM=cocoa dev-env/bin/python scripts/preview_ja_sun.py --render
```

El script usa preferencias y autoguardado aislados. Abre temporalmente una
ventana de desarrollo, genera `previews/ja_sun/modelo_09.png` y `modelo_16.png`,
y la cierra. El modo predeterminado offscreen comprueba solamente la interfaz
Qt y crea el modelo de ejemplo. El render OpenGL necesita una sesión gráfica.

Los cambios de documento deben pasar por comandos reversibles. No cambies
directamente geometría desde el panel. Al añadir controles de render, comprueba
primero su soporte en el viewport, las escenas y la serialización IGZ.

## Adding an interface language

Define a translation dictionary in `i18n.py`, using the same Spanish keys as
`ENGLISH`, and add one entry to `LANGUAGES`. For example:

```python
FRENCH = {
    "Idioma": "Langue",
    "Sol": "Soleil",
    "{minute} min/paso": "{minute} min/pas",
    # Add the remaining entries from ENGLISH here.
}

# Inside LANGUAGES:
"fr": LanguageSpec("Français", "fr_FR", FRENCH),
```

The registry controls the selector, accepted saved preferences, system-language
detection and Qt date/number formatting. No changes to `ui.py` or the controller
are needed. Restart IngeTrazo after adding an entry. This example is a partial
catalogue, not a bundled French translation.

Keep format placeholders and their specifications unchanged, such as `{minute}`
and `{elevation:.1f}`. Missing entries fall back to English, then to the Spanish
source text if no English translation exists. Spanish uses the original source
text. Unknown saved language codes fall back to the system language when it is
registered, or English otherwise.
