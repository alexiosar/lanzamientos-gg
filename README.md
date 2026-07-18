# LANZAMIENTOS.LAT

Calendario de lanzamientos de videojuegos en español para PS5, PS4, Xbox, Switch y Switch 2.
Sitio 100% estático: HTML, CSS y JavaScript puro, sin frameworks ni proceso de build.

**Dominio:** https://lanzamientos.lat
**Contacto:** contacto@lanzamientos.lat (Email Routing de Cloudflare, reenvía a la casilla personal)

## Estructura del proyecto

```
├── index.html                  Página principal (calendario)
├── css/style.css               Todos los estilos (temas oscuro y claro)
├── js/main.js                  Lógica del calendario: filtros, buscador, fichas, modal
├── datos/juegos.js             Base de datos: array JUEGOS con todos los lanzamientos
├── juegos/{id}.html            Fichas estáticas pre-generadas (una por juego, NO editar
│                               a mano: se regeneran con scripts/generar-fichas.py)
├── juegos/juego.html           Ficha dinámica (?id=) — solo fallback para links viejos
├── scripts/generar-fichas.py   Regenera las fichas estáticas desde juegos.js
├── acerca.html                 Página "Acerca de" (qué es el sitio, fuentes, independencia)
├── privacidad.html             Política de privacidad
├── terminos.html               Términos de uso
├── scripts/generar-sitemap.py  Regenera sitemap.xml a partir de juegos.js
├── sitemap.xml                 Mapa del sitio para Google (generado, no editar a mano)
├── robots.txt                  Permite indexación y declara el sitemap
├── favicon.svg                 Ícono del sitio (pestañas y favoritos)
├── og-image.png                Imagen que aparece al compartir el link en redes (1200x630)
└── wrangler.jsonc              Configuración de deploy en Cloudflare (assets estáticos)
```

## Cómo agregar un juego

Editar `datos/juegos.js` y agregar un objeto al array `JUEGOS`:

```js
{
  id: "nombre-del-juego",        // único, en minúsculas con guiones (se usa en la URL)
  titulo: "NOMBRE DEL JUEGO",    // en mayúsculas
  fecha: "2026-07-15",           // formato AAAA-MM-DD
  relanzamiento: null,           // opcional: para ports/re-lanzamientos, aclara dónde ya
                                 // está el juego, ej: "En PC desde 2024" (se muestra ↺ bajo la fecha)
  duracion: null,                // opcional: horas según HowLongToBeat,
                                 // ej: "28,5 h (historia) · 58,5 h (completo)"
  plataformas: ["PS5", "XBOX", "SWITCH2", "SWITCH", "PS4"],  // las que correspondan
  genero: ["ACCION", "RPG"],     // los filtros de género se generan solos
  desarrollador: "ESTUDIO",
  descripcion: "Texto normal en minúsculas...",
  trailer: "https://youtube.com/embed/XXXXXXX",   // formato /embed/, no /watch — o null:
                                                  // el botón VER TRAILER se oculta solo
  metacritic: null,              // número (ej: 82) o null si no tiene puntaje
  imagen: null,                  // URL de carátula o null (ver abajo)
  noticias: [                    // opcional: se puede omitir el campo entero
    {
      fecha: "2026-07-10",
      titulo: "TÍTULO CORTO EN MAYÚSCULAS",
      texto: "Detalle de la noticia en texto normal."
    }
  ],
  gamepass: false,               // true muestra el badge GAME PASS
  psplus: false,                 // true muestra el badge PS PLUS
  nuevo: true                    // true muestra ★ NUEVO (solo se ve en juegos que aún no salieron)
}
```

Todos los campos opcionales (`metacritic`, `imagen`, `noticias`, `trailer`) se ocultan solos
si están en `null` o ausentes — no rompen nada.

### Fuentes de datos habituales

- **Lista de lanzamientos**: releases.com (bloquea robots: para cargarlo con Claude hace
  falta la extensión de Chrome, o copiar y pegar la lista). Filtrar: solo consolas; sin
  parches de temporada, packs de contenido ni re-lanzamientos semanales de Arcade Archives.
- **Descripción en español, géneros y desarrollador**: API de Steam
  (`store.steampowered.com/api/appdetails?appids=NUMERO&l=spanish`).
- **Carátulas**: CDN de Steam (ver abajo) o, para exclusivos de Nintendo, la API de búsqueda
  de la eShop europea (`searching.nintendo-europe.com`, campo `image_url_sq_s`).
- **Trailers**: búsqueda en YouTube (`youtube.com/results?search_query=NOMBRE+official+trailer`
  responde a peticiones con User-Agent de navegador; el primer resultado está en el JSON
  embebido como `videoRenderer`). Validar siempre que el título del video corresponda al
  juego antes de cargar el ID. Los videos de Steam ya no sirven: son streaming DASH/HLS,
  no reproducibles en un iframe.
- **Duración**: HowLongToBeat (howlongtobeat.com). Su buscador bloquea bots (el endpoint
  interno rota y los buscadores externos limitan las consultas en lote), así que la carga
  es manual: buscar el juego en el sitio, tomar "Main Story" y "Completionist" y cargar el
  campo `duracion`. Las páginas de juego (`howlongtobeat.com/game/ID`) sí responden a
  peticiones con User-Agent de navegador: los datos están en el JSON `__NEXT_DATA__`
  (campos `comp_main` / `comp_100`, en segundos). Solo tiene sentido para juegos ya
  jugados en alguna plataforma (lanzados o ports); los estrenos nuevos no tienen datos.
- **Puntajes**: Metacritic (solo puntajes reales de Metacritic, no OpenCritic). Las páginas
  `metacritic.com/game/SLUG/` responden a peticiones con User-Agent de navegador; el
  Metascore está en el campo `"ratingValue"` del JSON-LD embebido. Los indies chicos suelen
  quedar "TBD" (necesitan al menos 4 reseñas de críticos para tener puntaje).

### Carátulas (campo `imagen`)

- **Juegos en Steam**: buscar el juego en store.steampowered.com, copiar el número de la URL
  (`store.steampowered.com/app/1290760/...` → `1290760`) y usar:
  `https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/NUMERO/library_600x900.jpg`
  (carátula vertical). Si no existe (juegos muy nuevos), en la página del juego en Steam
  se puede copiar la URL del banner horizontal (`header.jpg`).
- **Exclusivos de Nintendo**: usar la imagen cuadrada de la ficha del juego en nintendo.com.
- Sirve cualquier URL de imagen o un archivo local del proyecto.
- El sitio detecta solo la orientación: las verticales se muestran a 120px y las
  horizontales más anchas (230px) para que no queden diminutas.

### Después de CUALQUIER cambio en datos/juegos.js

Regenerar las fichas estáticas y el sitemap:

```
python3 scripts/generar-fichas.py
python3 scripts/generar-sitemap.py
```

Luego commit y deploy. Las fichas estáticas (`juegos/{id}.html`) contienen los datos
renderizados, así que **cualquier** edición de datos (noticias, puntajes, trailers)
requiere regenerarlas. El generador también borra las fichas de juegos eliminados.

## Funcionalidades

- **Calendario agrupado por mes y día**, con desplegables. Se abre solo el mes actual
  y hace scroll automático al día de hoy (o al más próximo).
- **Layout de dos columnas** (desktop): calendario a la izquierda, filtros en una barra
  lateral derecha fija (sticky) que acompaña el scroll. En pantallas de menos de 900px
  vuelve a una columna con los filtros arriba.
- **Miniaturas de carátula** (40px) en todas las listas: calendario, ranking, próximos
  7 días y páginas de plataforma. Con `loading="lazy"` solo cargan las visibles
  (~25 de 160 al abrir), así el peso inicial casi no cambia.
- **Juego destacado** en la portada: banner con el próximo lanzamiento notable (se elige
  solo: el futuro más cercano con noticias; si no hay, el más cercano con carátula), con
  carátula, fecha y cuenta regresiva. Se oculta al filtrar o buscar.
- **Bloque "Próximos 7 días"** arriba del calendario: lista los lanzamientos de la semana
  que viene (respeta los filtros; se oculta si no hay ninguno o en la vista ranking).
- **Indicadores por día**: `[ HOY ]` (amarillo, parpadea), `[ PRÓXIMO ]` (el primer día
  con lanzamientos después de hoy) y `[ YA DISPONIBLE ]` (verde, días pasados).
- **Filtros por plataforma y género** (los de género se generan automáticamente desde los
  datos).
- **URLs compartibles**: todos los filtros se reflejan en la URL y se pueden combinar —
  `?plat=PS5&gen=RPG&q=texto&vista=ranking`. Al cambiar un filtro la URL se actualiza sola
  (sin recargar), así cualquier vista se comparte copiando la barra de direcciones. Los
  parámetros inválidos se ignoran sin romper nada.
- **Buscador**: filtra en vivo por título, desarrollador o género (es texto libre, no hay
  botones por estudio), y abre todos los meses mientras se busca.
- **Páginas por plataforma** (`ps5.html`, `ps4.html`, `xbox.html`, `switch-2.html`,
  `switch.html`): listados estáticos pre-renderizados por plataforma, indexables por Google
  para búsquedas tipo "lanzamientos PS5". El menú del sitio apunta a ellas; cada una linkea
  al calendario interactivo. Se regeneran con `scripts/generar-plataformas.py` (la rutina
  diaria lo hace sola).
- **Filtros conscientes del archivo**: los botones de género solo se generan con juegos
  visibles en la portada; si un filtro/búsqueda no tiene resultados próximos pero sí
  archivados, el mensaje ofrece "BUSCAR EN EL ARCHIVO →" conservando el filtro.
- **Archivo automático** (`archivo.html`): la portada muestra solo el mes actual en
  adelante; los meses pasados se mueven solos al archivo (link punteado arriba del
  calendario). No requiere mantenimiento: es un filtro por fecha, no hay que mover datos.
  El ranking sigue considerando todos los juegos, archivados incluidos.
- **Botón ⇗ COMPARTIR** en todas las fichas: menú nativo del celular (WhatsApp, X, etc.)
  o copia del link en desktop, siempre apuntando a la ficha estática (con su carátula
  en la tarjeta social).
- **Vista ★ RANKING**: selector "VISTA" arriba de los filtros; lista los juegos con puntaje
  de Metacritic ordenados de mejor a peor. Respeta los filtros de plataforma/género y el
  buscador. Crece solo a medida que se cargan puntajes.
- **Cuenta regresiva**: en las fichas de juegos futuros, debajo de la fecha
  (`▸ FALTAN X DÍAS`, `▸ FALTA 1 DÍA`, `▸ ¡SALE HOY!` parpadeante). Se oculta en los
  ya lanzados. Funciona en la ficha desplegable y en la página +INFO.
- **Botón ◷ AGENDAR**: en juegos futuros, descarga un archivo .ics (evento de día completo)
  para agendar el lanzamiento en Google Calendar / Apple Calendar / Outlook. Se genera
  en el navegador, sin backend. Desaparece cuando el juego ya salió.
- **PWA instalable**: `manifest.json` + íconos (192/512). En el celular se puede "Agregar
  a la pantalla de inicio" y el sitio abre como app, a pantalla completa y con su ícono.
- **Accesibilidad**: tipografía en unidades relativas (base 14px, mínimo 11px — escala si
  el usuario agranda la letra del navegador); navegación completa por teclado (Tab llega a
  filas de juegos y meses, Enter/Espacio los abre, Escape cierra el modal, foco visible);
  se respeta "reducir movimiento" del sistema (sin parpadeos); botones más grandes en móvil.
- **Analytics**: Cloudflare Web Analytics activado desde el panel (inyección automática,
  sin cookies). Métricas de visitas en Cloudflare → Analytics & Logs → Web Analytics.
- **Ficha desplegable** al hacer clic en un juego: carátula, datos, Metacritic, descripción,
  tags, trailer en modal y link a la ficha completa.
- **Ficha individual** (`juegos/juego.html?id=...`): igual que la desplegable más la sección
  **ÚLTIMAS NOVEDADES** (noticias del juego) y el trailer embebido.
- **Badge de Metacritic** con color según puntaje: verde ≥ 75, amarillo 50–74, rojo < 50.
- **Tema oscuro/claro**: botón ☾/☀ en la esquina superior derecha. Si el usuario nunca tocó
  el botón, el sitio sigue el modo del sistema operativo (como X: cambia solo de día/noche
  si el sistema tiene apariencia automática); al tocar el botón, esa elección se guarda en
  localStorage y manda sobre el sistema. El tema claro es blanco puro con su propia paleta
  de acentos oscurecidos para mantener el contraste.
- **★ NUEVO**: marca juegos recién agregados al calendario, pero solo se muestra si el juego
  todavía no salió (en los ya disponibles se apaga sola).

## SEO y redes

- Meta de verificación de Google Search Console en el `<head>` de `index.html`.
- `sitemap.xml` con la portada + una URL por juego (regenerar con el script, ver arriba).
- `robots.txt` que permite indexar todo y apunta al sitemap.
- **Open Graph**: al compartir la portada aparece la tarjeta con `og-image.png`; al
  compartir una ficha (`/juegos/{id}.html`) aparece **la carátula y datos de ese juego**
  (las fichas son HTML estático pre-generado, los scrapers no necesitan ejecutar JS).
- **Datos estructurados (JSON-LD)**: la portada declara `WebSite` y cada ficha inyecta
  `VideoGame` (nombre, fecha, plataformas, desarrollador, imagen) para que Google entienda
  el contenido. Ojo: el test de rich results de Google muestra "0 elementos" porque
  `VideoGame` no genera resultados enriquecidos específicos — es normal, no es un error.
  Para ver los datos detectados usar validator.schema.org con la URL de la portada.
- Tras un deploy con juegos nuevos: Search Console → Sitemaps → enviar `sitemap.xml`.

## URLs limpias (importante)

Cloudflare redirige automáticamente las URLs `.html` a versiones sin extensión
(`/ps5.html` → 307 → `/ps5`). Por eso **todo lo que ve Google usa URLs limpias**:
sitemap, canonicals, og:url, JSON-LD y los links de compartir/agendar. Los links
internos relativos del sitio sí usan `.html` (para que funcionen en el servidor de
desarrollo local, que no redirige); en producción Cloudflare los resuelve con una
redirección invisible. No volver a poner URLs `.html` en el sitemap ni en canonicals:
generan el aviso "Página con redirección" en Search Console.

## Deploy

Cloudflare (Wrangler) con `wrangler.jsonc`: sube toda la carpeta como assets estáticos.
Pendiente evaluar un `.assetsignore` para excluir del deploy los archivos que no son del
sitio (`scripts/`, `README.md`, el propio `wrangler.jsonc`).

## Mantenimiento

El sitio se mantiene con tres rutinas. En una sesión de Claude alcanza con decir
"rutina diaria", "rutina semanal" o "rutina mensual" — los métodos están documentados
en este archivo y en la sección "Fuentes de datos habituales".

**Diaria (o día por medio, ~10 min):**
1. `python3 scripts/actualizar.py` — refresca puntajes de Metacritic, regenera fichas y
   sitemap, y reporta: debuts con puntaje, lanzamientos de hoy/mañana (candidatos a
   noticias) y faltantes. Este paso no necesita a Claude.
2. Cargar noticias de los lanzamientos del día y eventos (debuts, Game Pass, betas).
3. Commit y deploy.

**Semanal:**
4. Barrido de releases.com del mes en curso y el siguiente (con Claude + extensión de
   Chrome): juegos nuevos Y verificación de fechas ya cargadas (las fechas cambian).
5. Trailers, carátulas y campo `relanzamiento` de lo que se haya agregado.

**Mensual (fin de mes):**
6. Cargar el mes siguiente completo desde releases.com.
7. Duraciones (HLTB) de los ports del mes nuevo.
8. Evaluar archivo/limpieza de meses viejos del calendario.
9. Repasar la sección "Pendientes / ideas" de este archivo.

## Desarrollo local

Servidor local para previsualizar (cualquiera sirve, es un sitio estático):

```
python3 -m http.server 8080
```

y abrir http://localhost:8080

## Pendientes / ideas

- Trailers faltantes en 7 juegos chicos del 16 de julio (Viking Frontiers, Rhapsody,
  Geppy-X, K-pop Idol Stories, Farlands, Looking For Fael, MAVRIX).
- eBaseball PRO SPIRIT 2026 (16 jul, PS5) quedó sin cargar: no tiene ficha en Steam.
- Cargar la semana del 20 de julio: Splatoon Raiders (23), Halo: Campaign Evolved (28),
  Mistfall Hunter (29), Xenoblade Chronicles 2 Switch 2 (30), The Relic: First Guardian (31).
- Noticias en más juegos (hoy tienen 22 de 126).
- Noticias en portada: descartado el bloque (empuja el calendario hacia abajo — decisión
  jul 2026). La página `/noticias.html` completa + RSS quedan para si el sitio crece.
- Si algún día se cargan datos desde una API externa: escapar HTML antes de inyectar
  con `innerHTML` (hoy no hace falta porque los datos son propios).
