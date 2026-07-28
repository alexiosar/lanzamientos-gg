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
├── scripts/generar-feeds.py    Regenera rss.xml y la API pública (api/*.json)
├── rss.xml                     Feed de novedades (generado, no editar a mano)
├── api/juegos.json             API pública: calendario completo (generada)
├── api/proximos.json           API pública: próximos 30 días (generada)
├── _headers                    CORS abierto para /api/* (Cloudflare)
├── scripts/generar-sitemap.py  Regenera sitemap.xml a partir de juegos.js
├── sitemap.xml                 Mapa del sitio para Google (generado, no editar a mano)
├── robots.txt                  Permite indexación y declara el sitemap
├── 404.html                    Página de error propia (sugiere juegos parecidos al slug).
│                               Requiere "not_found_handling": "404-page" en wrangler.jsonc:
│                               sin eso Cloudflare devuelve un 404 vacío.
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
  estimado: true,                // opcional: juego anunciado sin día confirmado.
  fechaEstimada: "OCTUBRE 2026", // `fecha` debe ser el ÚLTIMO día del mes (ancla de orden);
                                 // se muestra en un bloque "SIN FECHA CONFIRMADA" al final
                                 // del mes, sin cuenta regresiva ni botón de agendar.
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
- **Preferir siempre `library_600x900`.** Hoy 114 juegos la tienen, 107 usan la cápsula
  horizontal de Steam y 19 la cuadrada de la eShop. La vertical es la única que llena el
  marco 3/4 de la vista grilla sin recorte. Ojo: para los juegos que hoy usan `header.jpg`
  la vertical directamente no existe (probadas las 107, dan 404), así que no vale la pena
  reintentarlas en masa — sí conviene chequearla al cargar un juego nuevo.
- En la vista grilla las carátulas horizontales y cuadradas quedan recortadas al centro por
  el `object-fit: cover` del marco 3/4. Se probó mostrarlas enteras sobre un fondo difuminado
  (julio 2026) y **se descartó**: no gustó el resultado. La grilla queda con recorte.

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
- **Juegos sin fecha confirmada**: los anunciados para un mes o trimestre sin día exacto
  aparecen en un bloque "SIN FECHA CONFIRMADA" al final de su mes (borde punteado), con la
  ventana anunciada. No aparecen en "Próximos 7 días" ni como destacado, y sus fichas no
  ofrecen cuenta regresiva ni agendar. Cuando se confirme la fecha: poner el día real en
  `fecha` y borrar `estimado`/`fechaEstimada`.
- **Bloque "Próximos 7 días"** arriba del calendario: lista los lanzamientos de la semana
  que viene (respeta los filtros; se oculta si no hay ninguno o en la vista ranking).
- **Indicadores por día**: `[ HOY ]` (amarillo, parpadea), `[ PRÓXIMO ]` (el primer día
  con lanzamientos después de hoy) y `[ YA DISPONIBLE ]` (verde, días pasados).
- **Filtros por plataforma y género** (los de género se generan automáticamente desde los
  datos).
- **URLs compartibles**: todos los filtros se reflejan en la URL y se pueden combinar —
  `?plat=PS5&gen=RPG&q=texto&vista=grilla|ranking`. Al cambiar un filtro la URL se actualiza sola
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
- **Vista ⊞ GRILLA**: mosaico de carátulas grandes ordenado por fecha, con el puntaje de
  Metacritic sobre la portada y una franja "HOY" en los que salen hoy. Respeta filtros,
  búsqueda y el archivo (mismo conjunto que el calendario). Columnas automáticas: ~5 en
  desktop, 2 en móvil.
- **Vista ★ RANKING**: selector "VISTA" arriba de los filtros; lista los juegos con puntaje
  de Metacritic ordenados de mejor a peor. Respeta los filtros de plataforma/género y el
  buscador, y tiene su propio selector de período (TODO EL CALENDARIO / ESTE MES /
  ÚLTIMOS 30 DÍAS). Crece solo a medida que se cargan puntajes.
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
- **Tipografía**: Space Mono (monoespaciada con negrita real). La negrita (700) jerarquiza
  nombres de juego, encabezados de mes y títulos; la metadata (fechas, plataformas, labels)
  va en peso normal (400). Toda la jerarquía vive en css/style.css, así que las fichas y
  páginas generadas la heredan sin regenerar.
- **Tema oscuro/claro**: botón ☾/☀ en la esquina superior derecha. Si el usuario nunca tocó
  el botón, el sitio sigue el modo del sistema operativo (como X: cambia solo de día/noche
  si el sistema tiene apariencia automática); al tocar el botón, esa elección se guarda en
  localStorage y manda sobre el sistema. El tema claro es blanco puro con su propia paleta
  de acentos oscurecidos para mantener el contraste.
- **★ NUEVO**: marca juegos recién agregados al calendario, pero solo se muestra si el juego
  todavía no salió (en los ya disponibles se apaga sola).

## Difusión: RSS y datos abiertos

Sin redes sociales, la estrategia es que otros encuentren y enlacen el sitio:

- **RSS** (`/rss.xml`): las últimas 40 noticias del calendario, para lectores de feeds,
  agregadores y bots. Enlazado con autodiscovery en el `<head>` de todas las páginas y
  desde el footer.
- **API pública** (`/api/juegos.json` y `/api/proximos.json`): el calendario en JSON, con
  CORS abierto, sin registro ni clave. Documentada en "Acerca de" con licencia de uso libre
  citando la fuente. La apuesta: si alguien construye algo con estos datos, enlaza al sitio,
  y esos enlaces son lo que falta para ganar autoridad en Google.
- Ambos se regeneran con `scripts/generar-feeds.py` (incluido en la rutina diaria).

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

## Nunca dejar URLs con `${...}` en el JavaScript

Googlebot escanea el código JS en busca de enlaces y **rastrea literales sin evaluar**.
Un `href="/juegos/${j.id}"` dentro de una plantilla, o un `"https://lanzamientos.lat/juegos/${id}"`
en una función, termina generando 404 reales en Search Console
(pasó en julio 2026 con `/juegos/$%7BplataformaSlug(j.plataformas[0])%7D`).
Regla: construir las URLs por concatenación (`location.origin + "/juegos/" + id`) o dentro
de una interpolación completa (`${"/juegos/" + j.id}`), nunca como texto plano con `${}` adentro.

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
4. Barrido de releases.com de **todos los meses ya cargados en el calendario** (con Claude +
   extensión de Chrome), no solo del mes en curso y el siguiente. releases.com sigue sumando
   juegos a meses futuros después de que los cargamos, así que un mes barrido una vez queda
   desactualizado en pocas semanas. Hay que buscar dos cosas:
   - juegos nuevos que no estén en `datos/juegos.js`;
   - cambios de fecha y de plataformas de los que ya están (las fechas se adelantan y se
     atrasan; ej. Hot Wheels Infinite Rush pasó del 24 al 10 de septiembre).

   URLs del barrido: `https://www.releases.com/calendar/games?at=2026-Sep-01` y variantes
   (`-Sep-09`, `-Sep-18`, `-Sep-26`…). Cada carga muestra ~10 días, así que hacen falta 3 o 4
   por mes. Al final de cada mes aparecen los bloques "Estimated <mes>" y "Estimated Q<n>":
   esos van con `estimado: true` y `fechaEstimada`.
5. Trailers, carátulas y campo `relanzamiento` de lo que se haya agregado.
6. **Backlog de carátulas y trailers:** reintentar los que `actualizar.py` lista bajo
   "Faltantes". Suelen ser juegos que todavía no tenían ficha en Steam ni en la eShop cuando
   se cargaron; a medida que las tiendas publican assets, aparecen. Es un minuto de trabajo.
7. Regenerar todo (`generar-fichas`, `generar-plataformas`, `generar-feeds`, `generar-sitemap`)
   y verificar que las carátulas y los trailers nuevos devuelvan HTTP 200 antes del deploy.

**Mensual (fin de mes):**
8. Cargar el mes siguiente completo desde releases.com (el que todavía no existe en el
   calendario). A partir de ahí ese mes entra en el barrido semanal del punto 4.
9. Duraciones (HLTB) de los ports del mes nuevo.
10. **Backlog de duraciones:** cargar HLTB de ~15 ports viejos que no tengan `duracion`.
    `actualizar.py` los cuenta al final del reporte. Sin este paso el backlog no lo toca
    ninguna rutina: el punto 9 solo cubre el mes que se acaba de cargar.
11. **Backlog de noticias:** buscar noticias para los ~10 juegos mejor puntuados que no
    tengan el campo `noticias`. Se prioriza por puntaje porque son los que aparecen en el
    ranking y concentran las visitas. La diaria solo cubre lanzamientos de hoy/mañana, así
    que sin este paso los juegos viejos se quedan en cero para siempre.
12. Evaluar archivo/limpieza de meses viejos del calendario.
13. Repasar la sección "Pendientes / ideas" de este archivo.

**Cuál usar si falta un juego de un mes ya cargado:** la semanal. La mensual solo estrena
meses nuevos; la semanal es la que vuelve sobre lo ya cargado y tapa los huecos.

**Cobertura por campo — qué rutina mantiene qué:**

| Campo | Juegos nuevos | Backlog |
|---|---|---|
| Metacritic / ranking | Diaria (automática) | Diaria (automática) |
| Carátulas y trailers | Semanal, paso 5 | Semanal, paso 6 |
| Duración (HLTB) | Mensual, paso 9 | Mensual, paso 10 |
| Noticias | Diaria, paso 2 | Mensual, paso 11 |
| Descripciones | Semanal / Mensual, al cargar | — (se revisan solo si se detecta algo raro) |

Metacritic es el único campo 100% automático: `actualizar.py` barre toda la base cada día
buscando puntaje para cualquier juego ya lanzado con `metacritic: null`. Los demás dependen
de que las rutinas se corran.

## Desarrollo local

Servidor local para previsualizar (cualquiera sirve, es un sitio estático):

```
python3 -m http.server 8080
```

y abrir http://localhost:8080

## Pendientes / ideas

- Carátulas faltantes (5): GTA VI (no está en Steam ni eShop), Marvel's Wolverine, Halloween,
  Harvest Moon: Echoes of Teradea, BloodRayne, Flying Fire Shark. Reintentar en las semanales
  a medida que las tiendas publiquen assets.
- Trailers faltantes (2): Dungeon Antiqua y Mamon King (indies sin trailer propio en YouTube).
- Duraciones (HLTB): ~75 ports sin cargar. Se van sumando de a poco en las mensuales.
- Noticias en más juegos (hoy tienen 47 de 246).
- Samson: A Tyndalston Story (estimado septiembre 2026, PS5/Xbox): no está en Steam ni en la
  eShop, así que no hay carátula ni descripción de origen. Queda fuera hasta conseguir assets.
- Bloque "Estimated Q3" de releases.com: quedan ~25 juegos de consola sin cargar (Aniimo,
  He-Man, Endurance Motorsport Series, Woodo, Vampire Survivors: Legacy of the Bloodmoon,
  Danger Mouse, Ember & Blade, LIFTED, Super Battle Golf, Banchou Tactics…). Son fechas sin
  confirmar; cargarlos con `estimado: true` cuando haya tiempo.
- Difusión (idea pendiente del usuario): mails a medios y creadores en español desde
  contacto@lanzamientos.lat, y listados en directorios/GitHub. Sin redes sociales.
- Página `/noticias.html` completa: solo si el sitio crece y las noticias se cargan seguido.
  El bloque de novedades en portada quedó descartado (empuja el calendario hacia abajo).
- Si algún día se cargan datos desde una API externa: escapar HTML antes de inyectar
  con `innerHTML` (hoy no hace falta porque los datos son propios).
