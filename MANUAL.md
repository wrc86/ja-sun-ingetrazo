# JA Sun · Manual de usuario / User manual

**Versión / Version 0.1.0 · IngeTrazo 0.5.7 (API de extensiones 2) · Julio Angulo · GPL-3.0-or-later**

[Español](#español) · [English](#english)

---

## Español

### 1. ¿Qué es JA Sun?

JA Sun es un panel de **estudio solar** para IngeTrazo. Permite ver cómo caen las
sombras sobre tu modelo en cualquier fecha y hora del año, en la ubicación real
del proyecto. Sirve para:

- estudiar el asoleamiento de fachadas, patios y terrazas;
- comparar mañana y tarde, o verano e invierno;
- animar el recorrido del sol a lo largo de un día;
- guardar estudios con nombre y convertirlos en escenas para láminas.

Usa el motor de sombras nativo de IngeTrazo: no añade geometría al modelo.

### 2. Instalación

1. Descarga `ja_sun-0.1.0.zip` desde el catálogo de IngeTrazo o desde
   [las versiones del repositorio](https://github.com/wrc86/ja-ingetrazo-extensions/releases).
2. Descomprímelo. Obtendrás una carpeta llamada **`ja_sun`**.
3. En IngeTrazo abre **Extensiones → Abrir carpeta de plugins**.
4. Copia allí la carpeta `ja_sun` completa.
5. Reinicia IngeTrazo.

**Desinstalar:** cierra IngeTrazo y borra la carpeta `ja_sun` de la carpeta de plugins.

### 3. Abrir el panel

Cualquiera de estas opciones:

- Menú **Extensiones → JA Sun · Sol y sombras…**
- El botón con el **icono de sol** en la barra de herramientas.
- Atajo **Ctrl+Alt+S** (en macOS: **Cmd+Alt+S**), si no lo usa otra extensión.

El panel tiene tres pestañas: **Sol**, **Ubicación** y **Guardados**.

> **Primer paso recomendado:** antes de estudiar sombras, define la ubicación del
> proyecto (sección 5). Si el modelo no tiene ubicación, el motor usa Arequipa
> (Perú) como referencia y el panel te lo avisa.

### 4. Pestaña «Sol»

| Control | Qué hace |
|---|---|
| **Mostrar sombras en el modelo** | Activa o desactiva las sombras del modelo (es el mismo ajuste del menú de IngeTrazo). |
| **Recorrido solar** (diagrama) | Vista del cielo: el círculo exterior es el horizonte, el centro es el cenit, con N, E, S y O marcados. La curva es el recorrido del sol en la fecha elegida. **Arrastra sobre la curva** para elegir la hora (pasos de 10 min). Con el diagrama seleccionado, las **flechas ← →** mueven la hora de 5 en 5 minutos. |
| **Fecha** | Calendario y deslizador de día del año. Botones rápidos: **20 mar**, **21 jun**, **22 sep**, **21 dic** (fechas de referencia aproximadas a equinoccios y solsticios). |
| **Hora local** | Campo exacto (HH:mm) y deslizador de 00:00 a 23:59. Botones rápidos: **09:00**, **16:00** y **Mediodía solar** (la hora de mayor altura del sol ese día). |
| **Intensidad de sombra** | 0 % = sombra casi invisible · 100 % = sombra negra. |

**Lecturas** (debajo de los controles):

- **Altura** del sol sobre el horizonte y **acimut** geográfico, en grados.
- **Salida ≈** y **Puesta ≈** aproximadas.
- **Sombra de un poste de 1 m:** largo de la sombra que proyecta un poste vertical
  de 1 m sobre suelo plano. Útil para estimar sombras rápidamente
  (un edificio de 10 m proyecta 10 veces ese valor).
- Avisos como «Sol bajo el horizonte · sin sombra solar» o «Sombras desactivadas».

#### Recorrer el día (animación)

1. En **Recorrer el día** elige la hora inicial y la final (mismo día; la final debe ser posterior).
2. Elige el paso: **5, 15, 30 o 60 min/paso**.
3. Marca **Bucle** si quieres que se repita.
4. Pulsa **▶ Reproducir**. El botón cambia a **Ⅱ Pausar**.

Al pausar, el modelo se queda en la hora alcanzada. Cada paso dura unos 180 ms
(puede ir más lento en modelos pesados). Abrir otro archivo, deshacer o editar el
modelo detiene la reproducción.

#### Guardar escena del modelo

El botón **Guardar escena del modelo** crea una **escena nativa** de IngeTrazo con
la vista actual y la configuración de sombras. Se nombra automáticamente, por
ejemplo «Sol 21-06 · 09:00». Estas escenas también aparecen en **JA Camera** y se
pueden usar en **Sheet Composer** para armar láminas de asoleamiento.

### 5. Pestaña «Ubicación»

1. Escribe **Latitud** y **Longitud** en grados decimales
   (ejemplo Bogotá: 4.711, −74.072). Latitudes admitidas: −80° a 84°.
2. **Norte desde +Y:** giro del norte, en sentido horario, desde el eje verde (+Y).
   Si tu planta está dibujada con el norte hacia arriba en +Y, deja 0°.
3. Pulsa **Aplicar ubicación y norte**. Los cambios no se aplican hasta pulsar este botón.
4. **Zona horaria:** «Automática por longitud» o un desfase fijo de **UTC−12 a UTC+14**.
   La automática es solo una aproximación: para Colombia elige **UTC−05:00**.
   El horario de verano no se calcula; ajústalo manualmente donde aplique.

> **Importante:** la ubicación y el norte son datos compartidos del modelo. También
> afectan el mapa, el terreno y las referencias geográficas de IngeTrazo.

El panel indica el **año** que usa el motor: es el año actual del computador
(no hay selector de año).

### 6. Pestaña «Guardados»

Guarda configuraciones solares con nombre para volver a ellas rápidamente.

- **Guardar ajuste actual…** pide un nombre (1 a 80 caracteres, sin repetir)
  y guarda fecha, hora, intensidad, sombras activas y zona horaria.
- **Aplicar** recupera el ajuste seleccionado.
- **Eliminar** lo borra.

Los ajustes **no** guardan la ubicación: siempre usan la ubicación actual del modelo.
Se guardan dentro del archivo **.igz**, así que viajan con el modelo.

### 7. Deshacer y guardar

- Cada cambio se puede deshacer con el **Deshacer** normal de IngeTrazo.
- Un arrastre completo o una reproducción completa cuentan como **un solo paso** de Deshacer.
- Guarda el modelo como **.igz** para conservar ubicación, sombras, ajustes y escenas.
  Si guardas durante una animación, se guarda la hora visible en ese momento.

### 8. Flujo de trabajo sugerido

1. Abre el modelo y define **Ubicación**, **Norte** y **Zona horaria**.
2. En **Sol**, activa **Mostrar sombras en el modelo**.
3. Pulsa **21 jun** y recorre el día; repite con **21 dic** para comparar extremos.
4. Para cada momento clave pulsa **Guardar escena del modelo**.
5. Monta las escenas en una lámina con JA Camera / Sheet Composer.

Abre `Ejemplo_JA_Sun.igz` (incluido en el repositorio) para ver un caso listo:
una plataforma, un volumen y un poste de 1 m en Bogotá (UTC−5) con escenas
a las 09:00, 12:00 y 16:00 del 21 de junio.

### 9. Limitaciones

- Salida, puesta y mediodía son aproximaciones (muestreo cada 10 min, horizonte
  plano, sin refracción ni relieve).
- No hay sol libre (altura/acimut arbitrarios), mapas de horas de sol ni exportación de video.
- La suavidad del borde de la sombra y la luz ambiental dependen del renderizador de IngeTrazo.
- La interfaz está en español.

### 10. Problemas frecuentes

| Problema | Solución |
|---|---|
| No veo sombras | Activa **Mostrar sombras en el modelo** y revisa que el sol no esté bajo el horizonte. |
| Las sombras no coinciden con la realidad | Revisa latitud/longitud, **norte** y **zona horaria**, y pulsa **Aplicar ubicación y norte**. |
| «La hora final debe ser posterior a la inicial» | En Recorrer el día, la hora final debe ser mayor, dentro del mismo día. |
| «Ya existe un ajuste con ese nombre» | Usa otro nombre al guardar. |
| No aparece en el menú | Verifica que la carpeta copiada se llame `ja_sun` y contenga `__init__.py`; reinicia IngeTrazo. |

### Autor

**Julio Eduardo Angulo** — arquitecto colombiano, fundador y director de diseño de
**[Línea Prima](https://lineaprima.co)**, estudio de arquitectura, diseño y construcción
en Bogotá. Desde 2009 proyecta y construye, con 77 proyectos en Colombia, Puerto Rico
y Estados Unidos, bajo un modelo *Design & Build*: un mismo equipo del concepto a la obra
terminada. Línea Prima hace «arquitectura para durar»: atmósfera, materia honesta y
precisión. Estas extensiones nacen de su práctica diaria con BIM y herramientas digitales.

- Web: [lineaprima.co](https://lineaprima.co) · Perfil: [lineaprima.co/julio-eduardo-angulo](https://lineaprima.co/julio-eduardo-angulo/)
- Correo: info@lineaprima.co · Instagram: [@buskua.co](https://instagram.com/buskua.co)
- Código y reportes de errores: [github.com/wrc86/ja-ingetrazo-extensions](https://github.com/wrc86/ja-ingetrazo-extensions/issues)

---

## English

### 1. What is JA Sun?

JA Sun is a **sun-study panel** for IngeTrazo. It shows how shadows fall on your
model at any date and time of the year, at the project's real location. Use it to:

- study sunlight on façades, courtyards and terraces;
- compare morning vs. afternoon, or summer vs. winter;
- animate the sun across a day;
- save named studies and turn them into scenes for drawing sheets.

It uses IngeTrazo's native shadow engine and adds no geometry to the model.

> **Note:** the panel's interface is in Spanish. Spanish labels are shown in
> parentheses below.

### 2. Installation

1. Download `ja_sun-0.1.0.zip` from the IngeTrazo catalog or from the
   [repository releases](https://github.com/wrc86/ja-ingetrazo-extensions/releases).
2. Unzip it. You get a folder named **`ja_sun`**.
3. In IngeTrazo open **Extensions → Open plugins folder**.
4. Copy the whole `ja_sun` folder there.
5. Restart IngeTrazo.

**Uninstall:** close IngeTrazo and delete the `ja_sun` folder from the plugins folder.

### 3. Opening the panel

- Menu **Extensions → JA Sun · Sol y sombras…**
- The **sun icon** button on the toolbar.
- Shortcut **Ctrl+Alt+S** (macOS: **Cmd+Alt+S**), if no other extension uses it.

The panel has three tabs: **Sun** (*Sol*), **Location** (*Ubicación*) and **Saved** (*Guardados*).

> **Recommended first step:** set the project location (section 5). If the model
> has no location, the engine uses Arequipa (Peru) and the panel says so.

### 4. «Sun» tab (*Sol*)

| Control | What it does |
|---|---|
| **Show shadows in the model** (*Mostrar sombras en el modelo*) | Turns model shadows on/off (same setting as IngeTrazo's menu). |
| **Sun path** chart (*Recorrido solar*) | Sky view: outer circle = horizon, centre = zenith, N/E/S/W marked. The curve is the sun's path on the chosen date. **Drag along the curve** to pick a time (10-min steps). With the chart focused, **← →** move 5 minutes. |
| **Date** (*Fecha*) | Calendar and day-of-year slider. Quick buttons: **20 Mar, 21 Jun, 22 Sep, 21 Dec** (fixed reference dates near equinoxes/solstices). |
| **Local time** (*Hora local*) | Exact HH:mm field and 00:00–23:59 slider. Quick buttons: **09:00**, **16:00** and **Solar noon** (*Mediodía solar*). |
| **Shadow intensity** (*Intensidad de sombra*) | 0 % = barely visible, 100 % = black. |

**Readouts:** sun **altitude** and geographic **azimuth**; approximate **sunrise**
(*Salida*) and **sunset** (*Puesta*); and **shadow of a 1 m post** — the shadow
length of a 1 m vertical post on flat ground (a 10 m building casts 10× that).

#### Play the day (*Recorrer el día*)

1. Set start and end times (same day; end after start).
2. Choose the step: **5, 15, 30 or 60 min**.
3. Tick **Loop** (*Bucle*) to repeat.
4. Press **▶ Play** (*Reproducir*); it becomes **Ⅱ Pause** (*Pausar*).

Pausing keeps the current time. Each step takes about 180 ms (slower on heavy
models). Opening a file, undoing or editing the model stops playback.

#### Save model scene (*Guardar escena del modelo*)

Creates a **native IngeTrazo scene** with the current view and shadow settings,
named e.g. «Sol 21-06 · 09:00». These scenes also appear in **JA Camera** and can
be used in **Sheet Composer** for sun-study sheets.

### 5. «Location» tab (*Ubicación*)

1. Enter **Latitude** and **Longitude** in decimal degrees (supported latitudes −80° to 84°).
2. **North from +Y** (*Norte desde +Y*): clockwise rotation of north from the green
   (+Y) axis. Leave 0° if your plan has north pointing to +Y.
3. Press **Apply location and north** (*Aplicar ubicación y norte*). Nothing changes until you do.
4. **Time zone** (*Zona horaria*): automatic by longitude or a fixed offset
   **UTC−12 to UTC+14**. The automatic option is only an approximation; daylight
   saving time is not computed — set the offset manually.

> **Important:** location and north are shared model data; they also affect
> IngeTrazo's map, terrain and geographic references.

The engine uses the computer's **current year** (there is no year selector).

### 6. «Saved» tab (*Guardados*)

- **Save current setting…** (*Guardar ajuste actual…*): asks for a unique name
  (1–80 characters) and stores date, time, intensity, shadows on/off and time zone.
- **Apply** (*Aplicar*) restores it. **Delete** (*Eliminar*) removes it.

Saved settings do **not** store the location; they use the model's current one.
They are saved inside the **.igz** file.

### 7. Undo and saving

- Every change can be undone with IngeTrazo's normal **Undo**.
- A full drag or a full playback counts as **one** undo step.
- Save as **.igz** to keep location, shadows, settings and scenes.

### 8. Suggested workflow

1. Set **Location**, **North** and **Time zone**.
2. In **Sun**, turn on shadows.
3. Press **21 Jun** and play the day; repeat with **21 Dec**.
4. Press **Save model scene** at each key moment.
5. Lay the scenes out on a sheet with JA Camera / Sheet Composer.

Open `Ejemplo_JA_Sun.igz` (in the repository) for a ready-made example in Bogotá
(UTC−5) with scenes at 09:00, 12:00 and 16:00 on 21 June.

### 9. Limitations

- Sunrise, sunset and solar noon are approximations (10-min sampling, flat
  horizon, no refraction or terrain).
- No free sun (arbitrary altitude/azimuth), sun-hour maps or video export.
- Shadow softness and ambient light depend on IngeTrazo's renderer.

### 10. Troubleshooting

| Problem | Fix |
|---|---|
| No shadows | Turn on **Show shadows in the model**; check the sun is above the horizon. |
| Shadows look wrong | Check latitude/longitude, **north** and **time zone**, then press **Apply location and north**. |
| "End time must be after start time" | In Play the day, the end time must be later, same day. |
| Not in the menu | Make sure the copied folder is named `ja_sun` and contains `__init__.py`; restart IngeTrazo. |

### Author

**Julio Eduardo Angulo** — Colombian architect, founder and design director of
**[Línea Prima](https://lineaprima.co)**, an architecture, design and construction studio
in Bogotá. Designing and building since 2009, with 77 projects in Colombia, Puerto Rico
and the United States under a *Design & Build* model: one team from concept to finished
building. Línea Prima makes "architecture to last": atmosphere, honest materials and
precision. These extensions come from his daily practice with BIM and digital tools.

- Web: [lineaprima.co](https://lineaprima.co) · Profile: [lineaprima.co/julio-eduardo-angulo](https://lineaprima.co/julio-eduardo-angulo/)
- Email: info@lineaprima.co · Instagram: [@buskua.co](https://instagram.com/buskua.co)
- Code and bug reports: [github.com/wrc86/ja-ingetrazo-extensions](https://github.com/wrc86/ja-ingetrazo-extensions/issues)
