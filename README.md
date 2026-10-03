# JA Sun para IngeTrazo

**0.1.0 · Julio Angulo · GPL-3.0-or-later**

Panel de sol y sombras para **IngeTrazo 0.5.7, API de extensiones 2**, probado
contra el código del commit `6be29fe`. Interfaz en español, con temas claro y
oscuro y distribución adaptable al ancho del panel.

## Instalación

1. Descomprime `JA_Sun_v0.1.0.zip`.
2. En IngeTrazo abre **Extensiones → Abrir carpeta de plugins**.
3. Copia la carpeta **`ja_sun` completa** dentro de esa carpeta.
4. Reinicia IngeTrazo.
5. Abre **Extensiones → JA Sun · Sol y sombras…**, el botón de sol de su barra,
   o **Ctrl+Alt+S** si el atajo está disponible. En macOS, Qt muestra Ctrl como
   Command.

Es una extensión Python nativa para IngeTrazo; el paquete no se instala como
RBZ en SketchUp. No necesita dependencias adicionales a las del anfitrión.
Para desinstalar, cierra IngeTrazo y retira la carpeta `ja_sun`.

## Sol

- **Mostrar sombras:** activa el motor nativo y sincroniza su control de menú.
- **Recorrido solar:** diagrama del cielo con norte, este, sur y oeste; el
  círculo exterior es el horizonte y el centro es el cenit. Arrastra sobre la
  curva para elegir una hora real, en pasos de 10 minutos. Con el diagrama
  enfocado, las flechas izquierda/derecha cambian la hora en pasos de 5 minutos.
- **Fecha:** calendario, deslizador anual y accesos al 20 de marzo, 21 de junio,
  22 de septiembre y 21 de diciembre. Son fechas de comparación fijas, no una
  predicción del instante de equinoccios o solsticios de todos los años.
- **Hora local:** campo exacto y deslizador de 00:00 a 23:59. Accesos a 09:00,
  16:00 y al máximo de altura solar del día, muestreado cada 10 minutos.
- **Intensidad:** 0 % hace la sombra imperceptible y 100 % la hace negra.
- **Lecturas:** altura, acimut geográfico, salida y puesta aproximadas y longitud
  de la sombra de un poste vertical de 1 m sobre suelo horizontal.
- **Recorrer el día:** rango dentro del mismo día, pasos de 5/15/30/60 minutos y
  bucle opcional. Cada paso ocurre aproximadamente cada 180 ms; el rendimiento
  efectivo depende del modelo y del renderizador.

Los cambios se ven en el modelo inmediatamente. **Un arrastre o una reproducción
completa ocupa un paso de Deshacer.** Pausar o esconder el panel conserva la hora
actual. Usa el Deshacer nativo para recuperar el estado anterior. Durante la
reproducción se modifican los ajustes reales del documento: Guardar conserva la
hora que esté visible en ese momento. Una edición externa, Deshacer, Nuevo o
Abrir interrumpe la reproducción antes de continuar cambiando el documento.

**Guardar escena del modelo** crea una escena nativa con la vista, las sombras
y las demás propiedades de visualización actuales. Usa un nombre nuevo y se
puede deshacer. Estas escenas aparecen también en JA Camera y pueden utilizarse
desde allí con Sheet Composer.

## Ubicación

Latitud, longitud y norte se aplican con un botón explícito. El norte es el giro
horario desde el eje verde (+Y). Se conserva la altitud existente del datum.
Estos valores son los datos geográficos compartidos del modelo: también afectan
al mapa, terreno y referencias geográficas. La edición se puede deshacer.

La entrada de ubicación admite latitudes entre −80° y 84°, y longitudes desde
−180° hasta menos de 180°, por el dominio UTM del anfitrión. Si el modelo no tiene
ubicación, el panel identifica claramente la referencia de Arequipa que utiliza
el motor. No se asigna una ubicación al abrir el panel.

La zona horaria puede ser automática por longitud o un desfase de horas enteras
UTC−12 a UTC+14. La aproximación por longitud no identifica zonas políticas ni
horario de verano: selecciona manualmente el desfase que corresponda.

## Ajustes guardados y ejemplo

La pestaña **Guardados** permite guardar, aplicar y eliminar ajustes con nombre.
Conservan fecha, hora, intensidad, activación y zona horaria. Usan la ubicación
actual del modelo; aplicar un ajuste no cambia el lugar ni el norte. Los nombres
duplicados se rechazan. Guardar/eliminar ajustes también se puede deshacer.

Los ajustes viven en `scene.plugin_data["ja_sun"]` y viajan en el archivo IGZ.
Las sombras activas y las escenas utilizan los datos nativos del anfitrión.

`Ejemplo_JA_Sun.igz` contiene una plataforma, un volumen, un poste de 1 m y tres
escenas/ajustes a las 09:00, 12:00 y 16:00 del 21 de junio, con una ubicación de
referencia en Bogotá y desfase UTC−5.

## Alcance y validación

El panel usa `core.sun`, `ShadowSettings`, `SceneDatum`, `SavedView` y el render
nativo. El cálculo de posiciones usa **el año actual del equipo**, igual que el
viewport de esta versión de IngeTrazo. El año se indica en Ubicación; no existe
un selector de año que prometa un render distinto al que ofrece el anfitrión.

Salida, puesta y mediodía son aproximaciones con muestreo de 10 minutos, sin
refracción ni obstrucciones del relieve. La noche y los días sin salida o puesta
se indican explícitamente. El diagrama es una representación del cielo, no una
superposición 3D dentro del modelo.

La dirección del sol se obtiene del lugar, norte, fecha y hora. La versión
actual no expone un sol libre con altura/acimut arbitrarios, suavidad de borde,
iluminación ambiental, mapas de horas de asoleamiento ni exportación de vídeo.
JA Sun es una implementación independiente inspirada en el flujo de estudios
solares; no contiene código ni recursos de Curic Sun y no reproduce todas sus
funciones.

Validación: descubridor real de extensiones, `MainWindow`, entrada de datos,
historial de Deshacer/Rehacer, interrupción de reproducción, conservación de
geometría, persistencia IGZ y dirección que consume el viewport. Se revisaron
capturas de Qt en claro/oscuro y del render OpenGL nativo del modelo de ejemplo
a las 09:00 y las 16:00. Estas pruebas se realizaron en el anfitrión de desarrollo;
la instalación del usuario todavía requiere cargar el paquete en su versión.

La API 0.x de IngeTrazo es provisional; otras versiones requieren comprobar
compatibilidad. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para reproducir las
pruebas y construir los paquetes.
