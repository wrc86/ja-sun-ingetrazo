# Desarrollo de JA Sun

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
