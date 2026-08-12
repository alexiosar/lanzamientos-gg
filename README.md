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
├── noticias.html               Todas las novedades en una página (generada, NO editar a mano)
├── datos/noticias.js           Noticias que NO cuelgan de un lanzamiento (PS Plus, Directs…)
├── scripts/generar-noticias.py Regenera noticias.html mezclando juegos.js y noticias.js
├── acerca.html                 Página "Acerca de" (qué es el sitio, fuentes, independencia)
├── privacidad.html             Política de privacidad
├── terminos.html               Términos de uso
├── scripts/generar-feeds.py    Regenera rss.xml y la API pública (api/*.json)
├── rss.xml                     Feed de novedades (generado, no editar a mano)
├── api/juegos.json             API pública: calendario completo (generada)
├── api/proximos.json           API pública: próximos 30 días (generada)
├── api/openapi.yaml            Contrato de la API en OpenAPI 3.1. **Se escribe a mano**: si
│                               cambian los campos de juegos.js hay que actualizarlo (ver
│                               difusion/directorios-api.md para el chequeo)
├── _headers                    CORS abierto para /api/* (Cloudflare)
├── api.html                    Documentación de la API pública (enlace canónico: /api)
├── scripts/verificar-enlaces.py  Chequea que las carátulas y trailers cargados sigan vivos
├── scripts/post-diario.py      Arma el texto del posteo diario para X y Bluesky (no publica)
├── scripts/cargar-duraciones.py  Carga el campo `duracion` desde HowLongToBeat
├── scripts/generar-imagenes-redes.py  Regenera el avatar y la portada de los perfiles
├── redes/avatar.png            Avatar de @lanzamientoslat (400x400, generado)
├── redes/portada.png           Portada de los perfiles (1500x500, generada)
├── difusion/                   Material de difusión (PR a directorios, textos). No es del sitio.
├── scripts/generar-sitemap.py  Regenera sitemap.xml a partir de juegos.js
├── sitemap.xml                 Mapa del sitio para Google (generado, no editar a mano)
├── datos/lastmod.json          Huella y fecha de cambio de cada URL. **Commitearlo**: si se
│                               pierde, todas las fechas del sitemap se resetean al día que
│                               se regenere y el sitemap miente hasta que el contenido cambie.
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
  alta: "2026-08-07"             // día que entró al calendario; lo sella actualizar.py solo
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
- **Duración**: HowLongToBeat, con `python3 scripts/cargar-duraciones.py --aplicar`.
  Ya no hace falta cargarla a mano. El buscador de HLTB bloquea peticiones ingenuas, pero
  su propia web usa un protocolo público de dos pasos que el script replica: pide un token
  a `/api/bleed/init` y con él hace un POST a `/api/bleed`. Solo carga el resultado cuando
  el título coincide en un 82% o más, así que no mete la duración de otro juego; lo que
  queda por debajo lo lista como dudoso y no lo toca.
  **Si algún día devuelve 403 en todo**, el endpoint rotó: hay que mirar los chunks de
  `/_next/static/` en howlongtobeat.com, buscar la llamada `fetch` de la búsqueda y
  actualizar `init()` y `buscar()` en el script.
  Solo tiene sentido para juegos ya jugados en alguna plataforma (lanzados o ports); los
  estrenos no tienen datos, y los MMO dan cifras engañosas (Final Fantasy XIV está en la
  lista `EXCLUIDOS` del script por eso).
- **Puntajes**: Metacritic (solo puntajes reales de Metacritic, no OpenCritic). Las páginas
  `metacritic.com/game/SLUG/` responden a peticiones con User-Agent de navegador; el
  Metascore está en el campo `"ratingValue"` del JSON-LD embebido. Los indies chicos suelen
  quedar "TBD" (necesitan al menos 4 reseñas de críticos para tener puntaje).

### Carátulas (campo `imagen`)

**Las carátulas vienen en tres formas y no se pueden unificar** (al 11/08/2026: 146
verticales 2:3 de `library_600x900`, 145 apaisadas 460×215 de `header`, 24 cuadradas de la
eShop). Se probó conseguir la vertical de las 145 apaisadas: **solo 6 la tenían**. Steam
publica el arte vertical recién cuando la ficha de la tienda está completa, así que un indie
sin lanzar no la tiene en ningún lado.

Cómo lo trata el sitio, decidido el 11/08/2026:

- **Grilla, miniaturas y ficha**: se recorta (`object-fit: cover`). Las cuadrículas quedan
  parejas, a costa de que una apaisada muestre solo su franja central.
- **Destacado**: es uno solo por página, así que ahí la caja toma la proporción de la
  imagen y se ve entera. `formaCaratula()` en `js/main.js` deduce la forma por la URL y le
  pone la clase; el CSS tiene una caja por forma. En móvil, si es apaisada el bloque se
  apila (imagen arriba a lo ancho, texto abajo) porque al lado dejaba el título en 93px.

**Buscar SIEMPRE primero la vertical.** El orden es `library_600x900.jpg` → si da 404,
`header_image` de `appdetails`. El 11/08/2026 se cargaron 6 juegos con el header pudiendo
tener la vertical, porque el script tomó `header_image` sin probar la otra:

```
https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/<appid>/library_600x900.jpg
```

Vale la pena reintentarlo cada tanto sobre las que quedaron apaisadas: Steam publica la
vertical recién cuando la ficha de la tienda está completa, así que un juego que hoy no la
tiene puede tenerla cerca de su lanzamiento.


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

### Un juego que sale en varias fechas (regla decidida el 01/08/2026)

Pasa seguido: un juego sale primero en unas consolas y meses después en otras. La regla es
**una entrada por lanzamiento**, no por juego.

- Se crea una **entrada nueva** cuando la segunda fecha trae plataformas que no estaban en la
  primera. El `id` lleva un sufijo que aclara cuál es (`-xbox`, `-switch-2`, `-consolas`).
- La entrada nueva **siempre** lleva `relanzamiento` apuntando a la anterior, con fecha y
  plataformas: *"En PS5 y Switch desde el 23 de julio de 2026 — esta fecha corresponde a la
  edición de Xbox"*.
- La entrada vieja **no** debe listar plataformas que todavía no salieron. Es el error que
  tenía Avatar Legends: figuraba en Xbox desde julio cuando esa versión llegaba en septiembre.
- La `descripcion` de la segunda entrada **no se copia tal cual**: se reescribe explicando qué
  aporta esa edición. Son dos páginas del mismo juego y el contenido duplicado juega en contra
  de la indexación, que es justo el problema que estamos peleando.
- Si el juego original es viejo y **no está en el calendario** (Elden Ring en Switch 2,
  Xenoblade 2), alcanza con una sola entrada y el campo `relanzamiento`. No hace falta inventar
  una entrada para el lanzamiento de 2022.

**Por qué así:** el sitio es un calendario y su eje es la fecha. Si alguien filtra por PS5 y
mira octubre, tiene que encontrar el juego que llega a su consola en octubre. Con una sola
entrada fechada en el primer lanzamiento, ese juego desaparece del mes que le importa.

**Casos ya normalizados con esta regla:** Steins;Gate Re:Boot, Avatar Legends: The Fighting
Game y PAW Patrol: Dino World.

### Después de CUALQUIER cambio en datos/juegos.js

Regenerar las fichas estáticas y el sitemap:

```
python3 scripts/generar-fichas.py
python3 scripts/generar-noticias.py
python3 scripts/generar-sitemap.py
```

Luego commit y deploy. Las fichas estáticas (`juegos/{id}.html`) contienen los datos
renderizados, así que **cualquier** edición de datos (noticias, puntajes, trailers)
requiere regenerarlas. El generador también borra las fichas de juegos eliminados.

`generar-noticias.py` va en la lista porque `noticias.html` también sale de `juegos.js`:
si se agrega una noticia a un juego y no se regenera, la ficha la muestra pero la página
de novedades no. Lo mismo al tocar `datos/noticias.js`. La rutina diaria corre los cuatro
generadores sola, así que esto sólo hace falta en una edición suelta.

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
- **Página de noticias** (`/noticias`): todas las novedades del sitio en una sola página,
  ordenadas por fecha, cada una con enlace al juego del que habla. Mezcla dos fuentes: el
  campo `noticias` de cada juego en `datos/juegos.js` (puntajes de estreno, ediciones,
  retrasos de un título) y `datos/noticias.js` (lo que no cuelga de un lanzamiento). Se
  muestran las 60 más recientes; las anteriores siguen en la ficha de su juego.

  Es la única parte del sitio que da una razón para volver más de una vez por mes, así que
  se genera **estática** y no con JavaScript: sólo sirve si Google la indexa. En el sitemap
  va con `changefreq: daily` y prioridad 0.8, la segunda más alta después de la portada.

  Formato de una entrada de `datos/noticias.js`:

  ```js
  {
    id: "ps-plus-agosto-2026",   // va en la URL; minúsculas y guiones
    fecha: "2026-07-28",         // la del anuncio, NO la del día que se carga
    categoria: "SUSCRIPCIONES",  // SUSCRIPCIONES | RETRASOS | ANUNCIOS | EVENTOS
    titulo: "…",                 // en mayúsculas, como el resto del sitio
    texto: "…",                  // uno o dos párrafos
    fuente: "https://…",         // siempre la oficial si existe; sale como "FUENTE ↗"
    juegos: ["big-walk"]         // opcional: ids de juegos.js, se enlazan solos
  }
  ```

  Los ids de `juegos` tienen que existir en `datos/juegos.js`: si no, el enlace no se dibuja
  y la noticia queda huérfana sin avisar.

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
  Ojo al verificar: el beacon **no aparece con `curl`**, ni siquiera poniendo User-Agent de
  navegador. Cloudflare lo inyecta sólo para peticiones que reconoce como navegador real, así
  que para comprobar que está hay que mirar `document.scripts` desde el navegador. Decidido
  el 01/08/2026 **no** sumar Google Analytics: obligaría a un cartel de cookies (hoy la
  política de privacidad promete que el sitio no usa cookies propias), pesa cientos de KB, y
  responde una pregunta —qué hace quien llega— que todavía no es el problema.
- **Ficha desplegable** al hacer clic en un juego: carátula, datos, Metacritic, descripción,
  tags, trailer en modal y link a la ficha completa.
- **Carátula en caja fija (200x220)** tanto en la ficha desplegable como en la estática, con
  `object-fit: contain`. El alto tiene que estar reservado antes de que la imagen cargue: si
  no, al llegar empuja todo hacia abajo y eso cuenta como CLS, una de las métricas que Google
  usa como señal. Hasta el 01/08/2026 había además una clase `.apaisada` que cambiaba el ancho
  de 160 a 280px **en el `onload`**, o sea que el salto estaba garantizado por diseño y sólo
  se disimulaba con la caché. Se eliminó. No volver a dimensionar carátulas según
  `naturalWidth` después de cargar.
- **Ficha individual** (`juegos/juego.html?id=...`): igual que la desplegable más la sección
  **ÚLTIMAS NOVEDADES** (noticias del juego) y el trailer embebido.
- **Juegos relacionados** al pie de cada ficha: dos bloques de hasta 6 juegos cada uno,
  **JUEGOS RELACIONADOS** (elegidos por géneros compartidos, con bonus por plataforma en
  común y fecha cercana) y **MÁS LANZAMIENTOS DE `<MES>`**. Los arma `generar-fichas.py`
  con las funciones `relacionados()` y `mismo_mes()`. Existe porque hasta julio de 2026
  cada ficha era un callejón sin salida: 247 páginas con cero enlaces entre sí, y la única
  salida era volver al calendario. Ahora cada ficha ofrece 12 caminos.
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
- **★ NUEVO**: marca los juegos que entraron al calendario en los últimos 7 días, y solo si
  todavía no salieron (en los ya disponibles se apaga sola). Sale del campo `alta`, que
  `actualizar.py` sella con la fecha del día en cualquier juego que aparezca sin él.

  Hasta el 07/08/2026 esto era un booleano `nuevo` que se ponía a mano al cargar el juego y
  que nadie apagaba nunca: terminó encendido en 283 de 292 juegos, o sea que la estrella
  estaba en casi todo el calendario y no distinguía nada. Las fechas de alta de los 292
  juegos se recuperaron del historial de git, así que son reales y no una fecha inventada.

  El campo `alta` queda fuera de la huella con la que `generar-sitemap.py` calcula `lastmod`:
  no cambia nada de lo que se ve en la página, y si entrara en la huella el día que se agregó
  el campo Google habría leído que las 304 URLs cambiaron a la vez.

## Difusión: RSS y datos abiertos

Sin redes sociales, la estrategia es que otros encuentren y enlacen el sitio:

- **RSS** (`/rss.xml`): las últimas 40 novedades, mezclando las noticias de cada juego con
  las propias de `datos/noticias.js`, para lectores de feeds,
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
- **`lastmod` por URL** (desde el 03/08/2026): es la señal con la que Google decide a qué
  páginas vale la pena volver. Sin ese dato trata las 302 URLs como igual de estáticas y no se
  entera de que una ficha se actualizó con una noticia nueva. **No se pone la fecha de hoy en
  todo**: eso diría que las 292 fichas cambian a diario, que es falso y le hace perder la
  confianza al dato. `generar-sitemap.py` guarda una huella del contenido de cada URL en
  `datos/lastmod.json` y sólo mueve la fecha cuando esa huella cambia de verdad. La portada y
  las páginas de plataforma dependen de todo el calendario, así que cualquier juego nuevo o
  corregido las marca como modificadas; las fichas, sólo si cambió ese juego.
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

**Los enlaces internos van sin `.html`.** El sitio se sirve en `/ps5` y `/juegos/<id>`;
si un enlace apunta a `ps5.html`, Cloudflare responde con un **307** y Googlebot come una
redirección en vez de llegar a la página. En agosto de 2026 eso puso 188 URLs en "Página con
redirección" de Search Console. El 307 además es temporal, así que Google no consolida las
señales como con una permanente, y no lo podemos cambiar: lo genera Cloudflare.
Vale para `js/main.js`, los dos generadores y la navegación de las páginas estáticas.
Se comprueba con: `grep -oh 'href="[^"]*\.html' juegos/*.html *.html` — tiene que dar vacío.

Por eso la vista previa local usa `scripts/servidor-local.py` y no `python3 -m http.server`:
hace falta un servidor que resuelva `/ps5` a `ps5.html`, como hace Cloudflare.

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
   Las de **un juego** van en su campo `noticias` dentro de `datos/juegos.js`; las que **no
   cuelgan de un lanzamiento** (PS Plus y Game Pass del mes, un Direct, un cierre de estudio)
   van en `datos/noticias.js`. La página `/noticias` mezcla las dos y las ordena por fecha.

   `actualizar.py` recuerda al final cuántas noticias propias hay y hace cuánto se cargó la
   última. Lo que conviene mirar, en este orden: **retrasos** (son lo que más se busca y lo
   que más le importa a un calendario: además de la noticia, hay que corregir la fecha del
   juego), **Directs y State of Play**, y los **juegos del mes** de PS Plus y Game Pass.
   Si no pasó nada que valga la pena, no se fuerza: una entrada floja vale menos que ninguna.
3. `python3 scripts/post-diario.py` — imprime tres opciones de posteo para X y Bluesky
   (lanzamientos del día, lo que viene en la semana, cuenta regresiva) con el conteo de
   caracteres de cada red. No publica nada: se elige una, se copia y se pega. Correrlo
   **después** de cargar las noticias, así el texto sale con los datos del día.
4. Commit y deploy.

**Mensual, además — suscripciones:**

Esto no lo cubre ningún script y es el agujero por el que se escapó Big Walk: durante meses
el calendario tuvo **292 juegos y cero con el badge de PS Plus**, y tres juegos de agosto
entraban a Game Pass el día del estreno sin tenerlo marcado. Los servicios anuncian una vez
por mes y hay que ir a buscarlo:

- **PS Plus**, a fin de mes: [blog.latam.playstation.com](https://blog.latam.playstation.com/).
  Los juegos mensuales se anuncian unos días antes de que empiecen.
- **Game Pass**, dos veces por mes: [news.xbox.com](https://news.xbox.com/es-mx/).

De cada anuncio salen dos cosas: marcar `psplus: true` o `gamepass: true` en los juegos del
calendario que aparezcan (solo los que **se estrenan** en el servicio; el catálogo viejo no
va, porque esto es un calendario de lanzamientos), y una entrada en `datos/noticias.js` con
categoría `SUSCRIPCIONES`.

**Semanal:**
5. Barrido de releases.com de **todos los meses ya cargados en el calendario**, no solo del
   mes en curso y el siguiente.

   **Ya no hace falta la extensión de Chrome**: desde el 10/08/2026 el barrido se hace con el
   navegador de la app. `curl` sigue dando 403, pero el navegador carga bien. Cada página se
   raspa con este selector, que devuelve fecha, título y plataformas de cada juego:

   ```js
   document.querySelectorAll('.RWP-Calendar-Group')          // cada bloque de fecha
   //   dentro: .RWPCC-CalendarItems-CardControl             // cada juego
   //   el nombre: a.RWPCC-CalendarItems-CardControl-Name
   ```

   Conviene acumular en `localStorage` entre navegaciones y volcar todo al final.

   **Dos trampas al comparar con el calendario:**
   - releases.com mezcla **expansiones y DLC** con los juegos. Antes de cargar algo, mirar el
     `type` en la API de Steam: el 10/08 casi entra "Jurassic World Evolution 3: Crocodilia
     Coast", que es una expansión de un juego de 2025.
   - Comparar por **título en inglés falla** con los que tenemos en español: Dragon Quest
     Monsters figuraba como "The Withered World" y nosotros lo teníamos como "El reino
     marchito". Comparar también por `id` antes de dar uno por faltante. releases.com sigue sumando
   juegos a meses futuros después de que los cargamos, así que un mes barrido una vez queda
   desactualizado en pocas semanas. Hay que buscar dos cosas:
   - juegos nuevos que no estén en `datos/juegos.js`;
   - cambios de fecha y de plataformas de los que ya están (las fechas se adelantan y se
     atrasan; ej. Hot Wheels Infinite Rush pasó del 24 al 10 de septiembre).

   URLs del barrido: `https://www.releases.com/calendar/games?at=2026-Sep-01` y variantes
   (`-Sep-09`, `-Sep-18`, `-Sep-26`…). Cada carga muestra ~10 días, así que hacen falta 3 o 4
   por mes. Al final de cada mes aparecen los bloques "Estimated <mes>" y "Estimated Q<n>":
   esos van con `estimado: true` y `fechaEstimada`.
6. Trailers, carátulas y campo `relanzamiento` de lo que se haya agregado.
7. **Backlog de carátulas y trailers:** reintentar los que `actualizar.py` lista bajo
   "Faltantes". Suelen ser juegos que todavía no tenían ficha en Steam ni en la eShop cuando
   se cargaron; a medida que las tiendas publican assets, aparecen. Es un minuto de trabajo.
8. Regenerar todo (`generar-fichas`, `generar-plataformas`, `generar-feeds`, `generar-sitemap`)
   y verificar que las carátulas y los trailers nuevos devuelvan HTTP 200 antes del deploy.

8. **Enlaces vivos:** `python3 scripts/verificar-enlaces.py`. Comprueba que las 315
   carátulas y los 293 trailers cargados sigan respondiendo. Las URLs se rompen solas —Steam
   reorganiza sus CDN, un estudio borra su video— y **no se nota mirando el sitio**: una
   carátula caída muestra el mismo marcador que un juego que todavía no tiene, y un trailer
   roto sólo se ve si alguien entra a esa ficha y le da play. La primera corrida, el
   11/08/2026, encontró tres carátulas en 404 y un id de YouTube truncado a 10 caracteres.
   Reintenta antes de dar algo por roto, así que si marca algo, está roto de verdad.

**Mensual (fin de mes):**
9. Cargar el mes siguiente completo desde releases.com (el que todavía no existe en el
   calendario). A partir de ahí ese mes entra en el barrido semanal del punto 5.
10. Duraciones: `python3 scripts/cargar-duraciones.py --aplicar`. Recorre **todos** los
    ports sin `duracion`, no solo los del mes nuevo, así que cubre el mes recién cargado y
    el backlog de una sola pasada. Tarda unos minutos (consulta de a uno, con pausa).
11. Repasar los "dudosos" que imprima el script: son títulos que coincidieron poco o que
    HLTB todavía no tiene cronometrados. Los que valgan la pena se cargan a mano.
12. **Backlog de noticias:** buscar noticias para los ~10 juegos mejor puntuados que no
    tengan el campo `noticias`. Se prioriza por puntaje porque son los que aparecen en el
    ranking y concentran las visitas. La diaria solo cubre lanzamientos de hoy/mañana, así
    que sin este paso los juegos viejos se quedan en cero para siempre.
12 bis. **Backlog de fechas estimadas:** los "Estimated Q3/Q4" de releases.com que el barrido
    semanal deja afuera. Al 10/08/2026 quedan ~35, casi todos de Q4. Son los más caros de
    cargar porque Steam no los encuentra —son juegos muy chicos o que en PC se llaman
    distinto—, así que hay que ir a la eShop o a la web del estudio de a uno. Van con
    `estimado: true` y su ancla de fin de trimestre. Vale la pena hacerlo de a tandas
    chicas: muchas de esas fechas se van a mover igual antes de confirmarse.
13. Evaluar archivo/limpieza de meses viejos del calendario.
14. Repasar la sección "Pendientes / ideas" de este archivo.

**Cuál usar si falta un juego de un mes ya cargado:** la semanal. La mensual solo estrena
meses nuevos; la semanal es la que vuelve sobre lo ya cargado y tapa los huecos.

**Cobertura por campo — qué rutina mantiene qué**

Regla del proyecto: **todo lo que se desactualiza solo tiene que estar en una rutina.**
Si algo no está en esta tabla, no lo mantiene nadie.

| Qué | Al cargar el juego | Después, quién lo mantiene |
|---|---|---|
| `metacritic` (y con eso el ranking) | — | **Diaria, automática.** Único campo 100% automático: `actualizar.py` barre toda la base cada día buscando puntaje para cualquier juego ya lanzado con `metacritic: null` |
| `noticias` de un juego | Diaria, paso 2 (lanzamientos de hoy y mañana, y debuts con puntaje) | Mensual, paso 12 (los mejor puntuados que sigan sin noticias) |
| `datos/noticias.js` (PS Plus, Game Pass, Directs, retrasos) | Diaria, paso 2 | Diaria: `actualizar.py` avisa hace cuántos días se cargó la última |
| `gamepass` y `psplus` | Al cargar, si ya se sabe | **Mensual, sección "suscripciones"** |
| `fecha` y `plataformas` (cambian solas) | — | Semanal, paso 5 (barrido de releases.com) |
| Juegos nuevos | Semanal, paso 5 | Mensual, paso 9 (estrena el mes siguiente) |
| `estimado` / `fechaEstimada` | Semanal, paso 5 | Mensual, paso 12 bis (backlog de Q3/Q4) |
| `imagen` y `trailer` | Semanal, paso 6 | Semanal, paso 7 (los que faltan) |
| **Que esas URLs sigan vivas** | — | **Semanal, paso 8:** `python3 scripts/verificar-enlaces.py` |
| `duracion` (HLTB) | Mensual, paso 10 | Mensual, paso 10 (recorre todos, no solo los nuevos) |
| `descripcion`, `genero`, `desarrollador` | Semanal / Mensual, al cargar | — (no se desactualizan) |
| `alta` | — | Diaria, automática (`actualizar.py` la sella) |
| `sitemap` y `lastmod` | — | Diaria, automática |

**Lo que NO cubre ninguna rutina, a propósito:** la difusión (posteos, mensajes a feeds y
blogs, directorios de API). Eso vive en `difusion/`, con su propio registro y sus fechas.
El posteo diario sí está en la rutina diaria, paso 3.

## Desarrollo local

Servidor local para previsualizar (cualquiera sirve, es un sitio estático):

```
python3 -m http.server 8080
```

y abrir http://localhost:8080

## Pendientes / ideas

- **Creepshow: ¿va o no va en el calendario?** Está cargado para el 13/08/2026 en PS5, PS4,
  Xbox y Switch, pero al 12/08 toda la prensa (Bloody Disgusting, Gizmodo, Engadget, Games
  Press) anuncia el lanzamiento **solo en PC vía Steam**, y no aparece ni en la PS Store ni
  en la eShop europea. El único rastro de consola es una ficha de PS5 en GameFAQs, que crea
  páginas por plataforma a partir de anuncios y a veces se adelanta. Como esto es un
  calendario de consolas, o se le corrigen las plataformas o sale de la lista. Verificar
  después del 13: si no salió en consolas, borrarlo hasta que haya fecha real.

- **Carátulas faltantes (3)**, con lo ya descartado el 07/08/2026 para no repetir la búsqueda:
  - *BloodRayne: Definitive Collection* — no existe carátula propia. En PS Store solo están los
    tres juegos por separado (es un bundle físico de Strictly Limited, no un producto digital),
    Ziggurat publica un compuesto de las tres carátulas juntas (1900×900) y Strictly Limited
    solo tiene fotos cuadradas de la caja. Nada sirve como carátula única.
  - *Harvest Moon: Echoes of Teradea* — la tienda de Natsume tiene tres imágenes 3000×3000,
    pero las tres son promocionales con el peluche de regalo al lado, no la carátula sola.
    Todavía no está en Steam ni en la eShop pese a tener reservas abiertas.
  - *Flying Fire Shark!!!: Toaplan Arcade Garage* — sale el 29/08 y no está en ninguna tienda
    todavía. El anterior de la serie (Kyukyoku TigerHeli) sí está en la eShop europea, así que
    lo más probable es que aparezca ahí cerca del lanzamiento.

  **Dónde buscar, en este orden:** Steam (`/search/?term=` incluye los "próximamente", que la
  API `storesearch` se saltea) → eShop europea (`searching.nintendo-europe.com`) → ficha de
  PlayStation (`playstation.com/en-us/games/<slug>/`, de donde salen las `image.api.playstation.com`)
  → sitio de la distribuidora.
- Trailers faltantes (2): Dungeon Antiqua y Mamon King (indies sin trailer propio en YouTube).
- Duraciones (HLTB): quedan 23 ports sin cargar, todos porque HLTB todavía no tiene tiempos
  cronometrados (indies muy chicos). Reintentar en las mensuales con el script.
  **La de GTA VI se resolvió el 01/08/2026 buscándola en el sitio oficial de Rockstar**
  (`rockstargames.com/VI/-/opengraph-image.jpg`): cuando un juego sale en tienda propia y no
  aparece en Steam, conviene mirar la web oficial de la editora antes de darlo por perdido.
- Cuando falta la carátula, el sitio muestra un marcador con la marca ▸ y el texto
  "SIN CARÁTULA" (clases `grilla-vacia`, `mini-vacia` y `portada-vacia` en css/style.css).
  Está hecho con pseudo-elementos y no con una imagen para que el color siga al tema. Como los
  pseudo-elementos no funcionan sobre un `<img>`, cuando una URL falla `sinCaratula()` en
  js/main.js reemplaza el elemento por un `<span>`.
- Noticias en más juegos (hoy tienen 66 de 274). El paso 12 de la mensual ya bajó los mejor
  puntuados sin noticias hasta 72; de ahí para abajo son indies chicos con poca cobertura.
- Samson: A Tyndalston Story (estimado septiembre 2026, PS5/Xbox): no está en Steam ni en la
  eShop, así que no hay carátula ni descripción de origen. Queda fuera hasta conseguir assets.
- Bloque "Estimated Q3/Q4" de releases.com: el 10/08/2026 se cargaron 14 (Aniimo, He-Man,
  Endurance Motorsport Series, Woodo, Danger Mouse, Ember and Blade, LIFTED, Super Battle Golf,
  Road Truckers, Case Solved, Whirlight, Nomad Drive, Diablo IV en Switch 2 y Muchi Muchi Pork).
  Quedan ~35 sin cargar, casi todos de Q4, y son los más difíciles: **Steam no los encuentra**
  (juegos muy chicos o con otro nombre en PC), así que hay que buscarlos de a uno en la eShop
  o en la web de su estudio. Lo descartado a propósito, para no repetir el trabajo:
  - **Vampire Survivors: Legacy of the Bloodmoon**, **Dragon Ball Xenoverse 2 - Future Saga
    Chapter 4** y **Banchou Tactics** son DLC, no juegos.
  - **Dragon's Dogma 2** (Switch 2) y **Octopath Traveler 1 y 2** (Switch 2) ya están en el
    calendario como "Dark Arisen" y como el bundle "I + II".
  - **Fallout 76** aparece como Q3 2026 en PS5 y Xbox pero es de 2018: sin confirmar qué es
    esa reedición, no se carga.
- Difusión (idea pendiente del usuario): mails a medios y creadores en español desde
  contacto@lanzamientos.lat, y listados en directorios/GitHub. Sin redes sociales.
- El bloque de novedades en la portada quedó descartado (empuja el calendario hacia abajo).
  La página `/noticias` sí se hizo, el 09/08/2026: ver "Funcionalidades".
- Si algún día se cargan datos desde una API externa: escapar HTML antes de inyectar
  con `innerHTML` (hoy no hace falta porque los datos son propios).
