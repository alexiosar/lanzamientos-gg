# LANZAMIENTOS.LAT

Calendario de lanzamientos de videojuegos en español para PS5, PS4, Xbox, Switch y Switch 2.
Sitio 100% estático: HTML, CSS y JavaScript puro, sin frameworks ni proceso de build.

**Dominio:** https://lanzamientos.lat
**Contacto:** contacto@lanzamientos.lat (Email Routing de Cloudflare, reenvía a la casilla personal)

## Índice

<!-- Se mantiene a mano: no lo genera ningún script. Al agregar o renombrar un `##` o un
     `###` hay que sumar o corregir su línea acá.

     Las anclas son las que arma GitHub solo: minúsculas, sin puntuación, los espacios pasan
     a guiones y **los acentos se conservan**. Ojo con dos casos que parecen erratas y no lo
     son: lo que se borra deja su espacio, así que "Pendientes / ideas" da
     `pendientes--ideas` y "con `${...}` en" da `con--en`, los dos con guión doble.

     Para comprobarlas sin adivinar, se le pasan los encabezados a la API de GitHub y se leen
     los id que devuelve:
         grep -E '^#{2,3} ' README.md | grep -v '^## Índice' > /tmp/t.md
         python3 -c "import json;print(json.dumps({'text':open('/tmp/t.md').read()}))" > /tmp/p.json
         curl -s -X POST https://api.github.com/markdown --data @/tmp/p.json \
           | grep -o 'id="user-content-[^"]*"'
-->

- [Estructura del proyecto](#estructura-del-proyecto)
- [Cómo agregar un juego](#cómo-agregar-un-juego)
  - [Fuentes de datos habituales](#fuentes-de-datos-habituales)
  - [El resumen de la crítica (campo `critica`)](#el-resumen-de-la-crítica-campo-critica)
  - [Carátulas (campo `imagen`)](#carátulas-campo-imagen)
  - [Qué entra al calendario y qué no (regla decidida el 13/08/2026)](#qué-entra-al-calendario-y-qué-no-regla-decidida-el-13082026)
  - [Un juego que sale en varias fechas (regla decidida el 01/08/2026)](#un-juego-que-sale-en-varias-fechas-regla-decidida-el-01082026)
  - [Y el mismo juego cargado dos veces (regla decidida el 26/08/2026)](#y-el-mismo-juego-cargado-dos-veces-regla-decidida-el-26082026)
  - [Si se borra o se renombra un juego, va un redirect](#si-se-borra-o-se-renombra-un-juego-va-un-redirect)
  - [Después de CUALQUIER cambio en datos/juegos.js](#después-de-cualquier-cambio-en-datosjuegosjs)
- [Funcionalidades](#funcionalidades)
  - [Una página por mes (`/septiembre-2026`, desde el 01/09/2026)](#una-página-por-mes-septiembre-2026-desde-el-01092026)
  - [Recomendados del mes (`/recomendados`, desde el 31/08/2026)](#recomendados-del-mes-recomendados-desde-el-31082026)
  - [Mis juegos (`/mis-juegos`, desde el 02/09/2026)](#mis-juegos-mis-juegos-desde-el-02092026)
- [Difusión: RSS y datos abiertos](#difusión-rss-y-datos-abiertos)
- [SEO y redes](#seo-y-redes)
  - [Los títulos de las fichas apuntan a la cola larga (decidido el 17/08/2026)](#los-títulos-de-las-fichas-apuntan-a-la-cola-larga-decidido-el-17082026)
- [Leer datos/juegos.js se hace en un solo lugar (desde el 02/09/2026)](#leer-datosjuegosjs-se-hace-en-un-solo-lugar-desde-el-02092026)
- [El menú y el pie se tocan en un solo lugar (desde el 02/09/2026)](#el-menú-y-el-pie-se-tocan-en-un-solo-lugar-desde-el-02092026)
- [Nunca dejar URLs con `${...}` en el JavaScript](#nunca-dejar-urls-con--en-el-javascript)
- [URLs limpias (importante)](#urls-limpias-importante)
- [Deploy](#deploy)
- [Mantenimiento](#mantenimiento)
- [Desarrollo local](#desarrollo-local)
- [Pendientes / ideas](#pendientes--ideas)
  - [Ideas del usuario del 27/08/2026 (sin empezar)](#ideas-del-usuario-del-27082026-sin-empezar)

## Estructura del proyecto

```
├── index.html                  Página principal (calendario)
├── css/style.css               Todos los estilos (temas oscuro y claro)
├── js/main.js                  Lógica del calendario: filtros, buscador, fichas, modal
├── js/favoritos.js             La estrella y la lista guardada en el navegador (sin cuentas)
├── mis-juegos.html             Los juegos que guardó quien visita (noindex: es de cada uno)
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
├── scripts/cargar-meta-trailers.py  Fecha de subida de cada trailer (para el marcado de video)
├── datos/trailers-meta.json    Caché de esas fechas. **Commitearla**: si se pierde hay que
│                               volver a bajar ~1 MB por trailer
├── scripts/comun.py           Lo que comparten varios scripts: leer juegos.js y noticias.js,
│                               y pasar títulos de MAYÚSCULAS a minúsculas respetando siglas
│                               y números romanos. **cargar_juegos() se importa de acá**
├── scripts/plantilla.py        Cabecera, menú, pie y script de tema de los 5 generadores.
│                               **Al tocar el menú va acá**, y también en las 9 páginas
│                               sueltas, que siguen con su copia a mano
├── scripts/novedades-steam.py  Lo que anuncian los estudios en Steam (juegos chicos)
├── scripts/verificar-lanzados.py  Juegos dados por lanzados que capaz no salieron
├── scripts/verificar-enlaces.py  Chequea que las carátulas y trailers cargados sigan vivos
├── scripts/verificar-duplicados.py  Juegos cargados dos veces con id distinto
├── scripts/verificar-estimados.py  Fechas estimadas vencidas (corre en la diaria)
├── scripts/verificar-favoritos.py  Que la estrella siga enchufada (corre en la diaria)
├── datos/recomendados.js       La selección del mes, elegida a mano
├── scripts/generar-recomendados.py  Genera recomendados.html
├── scripts/generar-meses.py    Genera una página por mes (/septiembre-2026…)
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
  metacritic: null,              // número (ej: 82) o null; lo baja y lo refresca actualizar.py
  metacriticUsuarios: null,      // puntaje de los usuarios, de 0 a 10 (ej: 2.6); ídem
  metacriticVotos: null,         // sobre cuántos votos se calculó ese puntaje; ídem
  critica: "...",                // opcional: resumen propio de lo que dijo la prensa
  // metacriticSlug: "..."       // sólo si el id NO es el slug de Metacritic (ver abajo)
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
  parches de temporada ni packs de contenido.

  **Las reediciones retro sí entran** (decidido el 25/08/2026). Arcade Archives, Console
  Archives, EGGCONSOLE y las líneas parecidas sacan un juego casi todas las semanas, y durante
  un tiempo se las dejó afuera por volumen. Se cambió de opinión con los datos de Search
  Console en la mano: son juegos de consola, con fecha y precio, sobre los que **nadie escribe
  en español**, que es exactamente donde el sitio convierte. Son unas cincuenta páginas al año
  sin competencia. Se cargan como cualquier otro juego, con `relanzamiento` aclarando de qué
  año es el original.
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

  **El puntaje de usuarios** (campo `metacriticUsuarios`, de 0 a 10) sale de la misma página,
  del `data-testid="global-score-value"` que viene después del encabezado `User score`.
  Ojo con dos trampas, las dos ya resueltas en `actualizar.py` pero fáciles de volver a pisar:

  1. **Los dos puntajes usan el mismo `data-testid`**, primero el de crítica y después el de
     usuarios. Hay que anclarse en el encabezado y buscar sólo en la ventana que le sigue: si
     un juego no tiene votos, en su bloque no hay ningún valor y la búsqueda sigue de largo
     hasta el Metascore de más abajo. Así The Sinking City 2 devolvía 79, su nota de prensa.
  2. **El slug puede ser de otro juego.** `final-fantasy-xiv-online` es el lanzamiento fallido
     de 2010 (49 de crítica, 3.9 de usuarios), no A Realm Reborn, que es lo que llega a
     Switch 2. Antes de creerle a una página se compara su Metascore con el que ya tenemos
     guardado: si difieren en más de 15 puntos es otro juego y se descarta con un aviso. Para
     esos casos está el campo opcional **`metacriticSlug`**, que apunta al slug correcto
     (FFXIV usa `final-fantasy-xiv-online-a-realm-reborn`).

  **Con pocos votos, el puntaje de usuarios no se muestra** (desde el 18/08/2026). Metacritic
  publica el número sin decir sobre cuántos votos se calculó, y un 6.8 sacado de nueve votos al
  lado de un 73 de la prensa aparenta una controversia que no existe: cualquiera lo mueve. Por
  eso se guarda también `metacriticVotos` —del texto "Based on N User Ratings" de la misma
  página— y `generar-fichas.py` oculta el badge por debajo de `MIN_VOTOS` (hoy 20). Al 18/08/2026
  eso deja 41 puntajes a la vista y esconde 23. Cuando se muestra, el conteo va en el `title`
  del badge.

  **Ojo con confundir votos con reseñas escritas**: el endpoint de reseñas devuelve sólo las
  que tienen texto —Voidtrain tenía 5— mientras que el puntaje se calcula sobre todos los votos
  —21 en ese mismo caso—. El número que vale para decidir si un puntaje significa algo es el
  segundo.

  **Los puntajes se refrescan, no se congelan** (desde el 18/08/2026). Hasta ese día el de
  crítica se bajaba una sola vez y quedaba fijo para siempre; al agregar el de usuarios se vio
  que 39 de 82 se habían movido, algunos mucho: Palworld estaba en 86 y hoy es 78, Deltarune
  Chapter 5 estaba en 86 y hoy es 96. Un puntaje viejo en un sitio que se vende por exacto es
  igual de malo que una fecha vieja. Como la página ya se pide para el puntaje de usuarios, el
  refresco no cuesta ni un pedido más. Se sigue refrescando hasta 90 días después del
  lanzamiento (`DIAS_REFRESCO`): el de crítica se planta a los pocos días, pero el de usuarios
  se mueve durante semanas, que es justo cuando pasan las review bombs.

  Las noticias que dicen "debuta con 87" **no se corrigen** cuando el puntaje se mueve: eran
  ciertas el día que se escribieron y así se leen.

### El resumen de la crítica (campo `critica`)

Dos o tres frases en español contando qué elogia y qué le reprocha la prensa a un juego,
escritas **leyendo las reseñas**, no copiándolas. Sale en la ficha, arriba de las novedades.

**Por qué escrito y no copiado** (decidido el 18/08/2026): copiar los extractos de Metacritic
o las reseñas de sus usuarios tiene tres problemas. Los extractos los redacta Metacritic y las
reseñas de usuarios las escriben personas, y sus términos prohíben reproducirlas: hoy les
tomamos un número, que es un dato, y copiar texto sería republicar su contenido. Nadie lo
mantendría, porque son 337 juegos a mano. Y sobre todo haría daño donde más duele: el problema
del sitio es autoridad —posición media 27,7—, y texto copiado de otro lado en cientos de fichas
es exactamente el patrón que Google clasifica como contenido raspado. Un resumen propio en
español, en cambio, no existe en ningún otro lado.

**Cómo se escribe uno.** Las reseñas se leen del backend de Metacritic, que devuelve JSON
limpio con medio, nota y extracto, de a 10 por pedido:

```
https://backend.metacritic.com/reviews/metacritic/critic/games/SLUG/web
  ?offset=0&limit=10&filterBySentiment=all
  &componentName=x&componentDisplayName=x&componentType=ReviewList
```

Cambiando `critic` por `user` salen las de los jugadores, que son las que explican una brecha
como la de EA Sports College Football 27 (77 de prensa contra 2.6 de jugadores). Hay que
paginar con `offset`: la página ordena por nota descendente, así que las primeras diez son
siempre las mejores y sin paginar el resumen sale falseado hacia lo bueno.

Reglas del texto: nada de citas textuales ni de nombres de medios salvo que agreguen algo;
se cuenta el consenso, y **siempre el reparo además del elogio**, que es lo que lo hace útil.
Cuando la brecha con los jugadores es grande, se explica de dónde sale. No se ponen números de
puntaje adentro del texto: se mueven solos y dejarían el resumen viejo.

Si algún día se quiere una cita textual, que sea de crítica y nunca de usuarios, de una línea,
entre comillas, con el nombre del medio y enlace a **su** reseña, no a Metacritic.

**Un juego partido en varias entradas lleva el mismo resumen en todas**, aunque alguna no tenga
puntaje todavía: The Relic: First Guardian está tres veces en el calendario —PS5, Xbox y
Switch 2— y las reseñas son del mismo juego. Si más adelante alguna edición se reseña aparte y
sale distinta, ahí se separan los textos.

### Carátulas (campo `imagen`)

**La forma que queremos es 2:3 vertical**, que es la de las cajas y la que usa releases.com,
que normaliza todo a 200×300 en su propio CDN. Con tres formas distintas —vertical, apaisada
de 460×215 y cuadrada de Nintendo— las tarjetas quedan disparejas por más que el CSS ayude.

**Antes de ir a los bancos de arte, probar la tienda donde el juego sale.** Se pasó por alto
hasta el 02/09/2026: si Steam no tiene vertical se saltaba directo a SteamGridDB, que necesita
clave, y sin la clave a mano el juego se quedaba con la apaisada. Pero **Xbox publica arte 2:3
propio y no pide autenticación**:

```
https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds=<STORE_ID>&market=US&languages=en-us&MS-CV=x.1
```

El `<STORE_ID>` es el código de la URL de la tienda (`.../games/store/shelldiver/9N51NR4GX891`).
En la respuesta, dentro de `LocalizedProperties[0].Images`, la que sirve es la de
`ImagePurpose: "Poster"`: viene en 1440×2160 o 720×1080, o sea 2:3 exacto. El servicio
redimensiona por query, así que conviene pedirla del tamaño del resto del sitio:

```
<uri>?w=600&h=900&format=jpg
```

Ojo con el `market`/`languages`: con `market=AR&languages=es-AR` la API devuelve un JSON sin
la clave `Products`. Con `market=US&languages=en-us` responde bien.

Esa misma respuesta trae `CMSVideos` con el tráiler, pero en DASH y HLS: el sitio embebe
YouTube o mp4 de Steam, así que no sirve tal cual.

**La PS Store no siempre ayuda:** en un juego anunciado y todavía sin salir sube capturas y
arte 16:9, y la caja recién cuando se acerca el lanzamiento. Aerial_Knight's Mr Freezy el
02/09/2026 tenía 41 imágenes en su ficha y las 41 eran 16:9.

Cuando la tienda no tiene vertical, la busca `scripts/caratulas-verticales.py` en SteamGridDB,
un banco de portadas subidas por la comunidad. **La clave va en `SGDB_API_KEY`, nunca en el
repo, que es público.** El 26/08/2026 esa pasada llevó las verticales de 168 a 251 de 361.

Dos reglas del buscador que salieron de revisar las primeras 118 a ojo, y conviene no
aflojarlas:

- **El nombre tiene que parecerse de verdad** (coincidencia exacta o 90% de similitud). La
  primera versión aceptaba que un nombre estuviera contenido en el otro, y The Caribou Trail
  se llevó la portada de un juego llamado «'the», porque "the" está adentro de
  "thecariboutrail".
- **Y el año tiene que cuadrar** con nuestra fecha o con lo que diga `relanzamiento`. Hay dos
  Star Fox en el banco, el de 1993 y el de 2026: sin mirar el año, el remake de Switch 2 se
  llevaba la caja original de Super Nintendo.

Con esas dos reglas quedan afuera los que tienen nombre de expansión o de edición —DOOM: The
Dark Ages Revelations, Disney Dreamlight Valley: Honeyglow Woods— porque el banco sólo tiene
el juego base. Está bien que queden afuera: se conserva la apaisada, que es del juego correcto.

**Antes de aplicar en masa, mirar las imágenes.** El script tiene `--json` para volcar lo que
encontró y armar una hoja de contacto; así aparecieron los dos errores de arriba.

Lo que SteamGridDB no encuentra lo busca `scripts/caratulas-igdb.py` en IGDB, que es una base
de datos y no un banco de arte: ahí cada expansión y cada edición tiene su ficha con su tapa,
que es justo lo que faltaba. Se autentica con una aplicación de Twitch —IGDB es de Twitch— y
las credenciales van en `IGDB_CLIENT_ID` e `IGDB_CLIENT_SECRET`, **nunca en el repo**. El
26/08/2026 cubrió 96 de los 110 que quedaban y las verticales llegaron a 347 de 361.

Hereda las dos reglas de nombre y año, con una diferencia: el año se compara contra todas las
fechas de la ficha y no contra la primera, porque IGDB guarda una por plataforma y en un port
la primera es la de PC de hace años.

Y suma una tercera regla propia: **la tapa tiene que ser más alta que ancha.** IGDB acepta
cualquier imagen en ese campo y algunas son iconos cuadrados, que recortados a 2:3 pierden un
tercio del alto y quedan peor que la apaisada que venían a reemplazar.

Ojo con la proporción, que no es idéntica: IGDB entrega 528x704, o sea 3:4, contra el 2:3 de
Steam. Se le recorta un 11% de ancho y en un arte de tapa no se nota, pero no es lo mismo.

**Los 8 que quedaban al 02/09/2026 no tienen arte en ningún lado, y está chequeado.** Vale la
pena dejarlo escrito porque desde afuera parece que falta correr algo:

| Juego | SteamGridDB | IGDB |
|---|---|---|
| route16r, flying-fire-shark-toaplan-arcade-garage, marupoyo-the-round-chicks-adventure, danger-mouse, power-racing-bundle-4, aerial-knights-mr-freezy | la ficha existe, **0 grids** en cualquier medida | sin resultados o icono cuadrado |
| spooky-spirit-shooting-gallery, sesame-street-amigos-y-risas | el banco devuelve **otro juego** (Spooky's Jump Scare Mansion, Sesame Street Sports) y el matcher lo rechaza bien | ídem |

Dos cosas que se descartaron ahí y conviene no volver a intentar:

- **No es el filtro de tamaño.** `mejor_grid()` pide `dimensions=600x900` y SteamGridDB también
  sirve 342x482 y 660x930, así que parecía que aflojando eso aparecían. No: se consultó sin
  filtro de medida y los seis primeros tienen **cero** grids de cualquier tamaño.
- **No es el matcher.** Los dos que sí tienen arte son homónimos, y rechazarlos es justo para
  lo que existe la regla del nombre.

Queda esperar a que la tienda publique la caja. Mr Freezy es el caso típico: PS5 sin salir, la
PS Store todavía con puras capturas 16:9 y Steam sin `library_600x900`.

Los que ni siquiera así aparecen se buscan a mano, y casi siempre es porque el nombre no
coincide: nosotros escribimos el título en castellano y la base lo tiene en inglés («El
Profesor Layton y el Nuevo Mundo a Vapor» es «Professor Layton and the New World of Steam»,
«Dragon Quest Monsters: El Reino Marchito» es «The Withered World»), o el editor le agrega un
subtítulo que nosotros no ponemos («Let's Sing ABBA» está como «Let's Sing Presents: Abba»).
Buscando el nombre en inglés aparecen enseguida. No conviene aflojar el matcher para cubrir
esto: la búsqueda a mano es de una vez y las reglas flojas meten portadas equivocadas.

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
- **Exclusivos de PlayStation**: la ficha del juego en store.playstation.com trae varias imágenes
  de `image.api.playstation.com`. La que sirve es la **vertical de 2:3** —se reconoce midiéndolas:
  la buena da 764×1146 con `?w=600&thumb=false`, y las demás son 764×430 apaisadas—. Es fácil
  agarrar la apaisada sin darse cuenta, porque es la primera que aparece en la página.
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

### Qué entra al calendario y qué no (regla decidida el 13/08/2026)

El sitio es un **calendario de lanzamientos de juegos para consolas**. Dos cosas quedan afuera,
y las dos se colaron alguna vez:

**1. Lo que sale solo en PC.** Aunque la prensa lo cubra y tenga fecha firme. Creepshow estuvo
cargado con fecha en PS5, PS4, Xbox y Switch hasta que salió, el 13/08/2026, únicamente en
Steam. Antes de cargar un juego con plataformas de consola, que aparezca en la PS Store o en
la eShop; si no está en ninguna, no hay versión de consola todavía.

**2. El contenido descargable.** La vara: **si Metacritic lo evalúa como producto propio, es
un juego; si no, es DLC.** Con eso, Deltarune: Chapter 5 se queda (tiene su propio 86) y
Mafia: The Old Country - Man of Honor se fue (es una expansión de 10 dólares que necesita el
juego base). En el barrido semanal ya se descartan por esto Vampire Survivors: Legacy of the
Bloodmoon, Dragon Ball Xenoverse 2 - Future Saga Chapter 4 y similares.

**Si hay que borrar un juego ya cargado:** además de sacarlo de `datos/juegos.js`, agregar su
URL a `_redirects` apuntando a la portada. `generar-fichas.py` borra la ficha sola, pero Google
ya tiene esa URL indexada y sin la redirección queda un 404.

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

### Y el mismo juego cargado dos veces (regla decidida el 26/08/2026)

El reverso del caso anterior. El 26/08/2026 apareció SESAME STREET: AMIGOS Y RISAS por
duplicado: mismo título, misma fecha, mismas plataformas y el mismo appid de Steam, con dos
ids distintos —uno armado con el nombre en castellano y otro con el nombre en inglés—. El
barrido semanal del 10/08 lo cargó de nuevo dieciséis días después del primero y no se dio
cuenta **porque compara por id, y el id era distinto**. En el sitio se veía como dos juegos,
con dos fichas y dos URLs en el sitemap compitiendo entre sí.

Es de los errores que no se notan mirando: las dos fichas están bien hechas, el problema es
que existan las dos. Y no se detecta mirando el id, que es justo lo que falló.

Lo busca `scripts/verificar-duplicados.py`, que corre solo en la rutina diaria. **Para acusar
a alguien exige las dos cosas a la vez:**

| Que sea el mismo producto | Y que ocupe el mismo lugar |
|---|---|
| El título normalizado, o el appid de Steam de la carátula | La misma fecha, o plataformas que se pisan |

La segunda columna es la que hace que sirva. Con el título repetido solo saltan los cinco
ports legítimos de la sección anterior —The Relic: First Guardian está tres veces a propósito,
en PS5, Xbox y Switch 2— y una alarma que grita todos los días por algo correcto se termina
ignorando. Con las dos condiciones juntas, al 26/08/2026 el único grupo que sale es el que
había que encontrar.

El trailer repetido tampoco alcanza, aunque lo parezca: Toy Story 3: Complete Edition y
Disney/Pixar Toy Story: Retro Roundup salen el mismo día y comparten video, y son dos juegos
distintos. El video es el anuncio conjunto de Atari, que presenta los dos a la vez.

**Cuando aparece uno:** se verifica en la tienda que sean el mismo producto y no dos
ediciones, se queda **el de `alta` más vieja** —que es el que Google pudo llegar a indexar—,
se borra la ficha del otro en `juegos/` y se le agrega un 301 en `_redirects`.

### Si se borra o se renombra un juego, va un redirect

`generar-fichas.py` borra las fichas de los juegos que ya no están en `datos/juegos.js`, así
que su URL empieza a devolver 404. Si Google la tenía indexada —y las tiene: descubre las
fichas por el sitemap— lo reporta como error de indexación. Pasó el 23/08/2026: la validación
de "No se ha encontrado (404)" falló por dos ids viejos.

La regla, en `_redirects`:

- **Juego que se sacó del calendario** (era sólo de PC, era DLC): redirect a la portada.
- **Juego que cambió de id** y sigue en el calendario: redirect **a su ficha nueva**, no a la
  portada. `doom-dark-ages` → `doom-the-dark-ages-revelations`, `granblue-fantasy-relink` →
  `granblue-fantasy-relink-endless-ragnarok`.

**Desde el 27/08/2026 el generador avisa solo.** Cuando borra una ficha, mira si `_redirects`
la cubre, y si no, lo dice en el reporte diario. No puede no borrarla —el juego ya no está—
pero puede no callarse, que es lo que fallaba: el borrado era silencioso.

Ese silencio costó dos meses. El 23/06/2026, antes de que existiera esta regla, se sacaron
del calendario cinco juegos de 2025 y sus fichas desaparecieron sin más: `gta-vi`,
`mario-kart-world`, `metroid-prime-4`, `split-fiction` y `elden-ring-nightreign`. Google ya
las tenía indexadas y las siguió pidiendo. **Las tres validaciones de "No se ha encontrado
(404)" que se pidieron en agosto —el 7, el 16 y el 23— fallaron por esas cinco URLs**, y no
había forma de darse cuenta mirando el sitio: las páginas que sí existen respondían bien.

`gta-vi` era el caso caro: no se había ido del calendario, sólo cambió de id a
`grand-theft-auto-vi`. Dos meses de 404 en la URL del juego más buscado que tiene el sitio.

Para auditar el pasado, que es como se encontraron: comparar todos los ids que existieron
alguna vez en el historial de `datos/juegos.js` contra las fichas de hoy y contra `_redirects`.
`git log --diff-filter=D --name-only --pretty=format: -- 'juegos/*.html'` sirve para lo mismo
si las fichas se borraron en un commit propio.

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
    categoria: "SUSCRIPCIONES",  // SUSCRIPCIONES | RETRASOS | ANUNCIOS | EVENTOS | RUMORES
    titulo: "…",                 // en mayúsculas, como el resto del sitio
    texto: "…",                  // uno o dos párrafos
    fuente: "https://…",         // siempre la oficial si existe; sale como "FUENTE ↗"
    juegos: ["big-walk"],        // opcional: ids de juegos.js, se enlazan solos
    imagen: "https://…"          // opcional: sólo si `juegos` está vacío (ver abajo)
  }
  ```

  Los ids de `juegos` tienen que existir en `datos/juegos.js`: si no, el enlace no se dibuja
  y la noticia queda huérfana sin avisar.

  **Una noticia con `juegos` también sale en la ficha de cada uno** (desde el 18/08/2026), no
  sólo en `/noticias`. El que busca "marvel tokon" en Google cae en la ficha, y ahí es donde
  tiene que encontrar lo último que se dijo del juego. En la ficha van mezcladas con las
  novedades propias y ordenadas por fecha, pero con su categoría al lado del título —y los
  rumores, con el borde punteado— para que se vea que son de otra clase. Siguen sin tocar
  ningún dato del juego.

  **Toda noticia lleva una imagen en la tarjeta.** Si cita un juego del calendario se usa
  su carátula sola —no hay que cargar nada— y la miniatura enlaza a la ficha. El campo
  `imagen` es para las que no citan ninguno, y se elige lo relacionado, en este orden:

  1. **La carátula del juego del que trata**, aunque no esté en el calendario: "Netflix
     cierra el estudio de Oxenfree" lleva la de Oxenfree; el catálogo de PS Plus, la de su
     juego más fuerte. Se saca de Steam igual que las demás (`library_600x900.jpg`), así
     que es estable, gratis y encaja con el resto del sitio.
  2. **Un evento con video** (un Direct, un State of Play): la miniatura de YouTube del
     video, `https://i.ytimg.com/vi/<id>/hqdefault.jpg`, el mismo mecanismo que ya usan los
     trailers. Sirve más que un logo genérico, porque es la portada de ese Direct concreto.
  3. Si no hay nada de eso, se deja sin imagen. Mejor una tarjeta sin foto que una foto que
     no dice nada. Los logos sueltos de plataformas o estudios no se usan: son de terceros
     y no se pueden servir desde una URL estable como las carátulas.

  La miniatura de una `imagen` propia va sin enlace (`<span>`, no `<a>`): no hay ficha
  adonde mandar al lector.

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

### Una página por mes (`/septiembre-2026`, desde el 01/09/2026)

**Por qué existen.** Al 01/09/2026 el sitio tenía 361 páginas indexadas y 4.870 impresiones,
pero 32 clics: posición media 28, o sea que aparece en la página 3 de resultados. Eso no se
arregla con funciones nuevas sino con páginas que apunten a búsquedas donde la competencia
sea flaca. *"Juegos que salen en septiembre de 2026"* es una de esas: existe, se repite doce
veces por año y tenemos el dato verificado para contestarla. El sitio no tenía dónde
recibirla.

**No suman mantenimiento.** Salen enteras de `datos/juegos.js` y se regeneran con la rutina
diaria: ningún campo nuevo que alguien tenga que llenar. Es la diferencia con la idea de los
precios, que serían datos nuevos y envejecen en horas.

Los meses pasados también se generan, y ese es el otro motivo: los juegos lanzados salen de
la portada con sus puntajes y sus resúmenes de crítica, y hasta ahora nadie los miraba.

**El enlace interno importa más que el sitemap.** Cada mes del calendario termina con *"ver
todos los juegos de…"*. Sin eso Google las encontraría sólo por el sitemap, que es la forma
más débil de descubrir una página.

**Cuidado con el "mejor puntuado" del subtítulo:** se calcula sólo entre los ya lanzados. Un
port trae el puntaje del original, así que sin ese filtro un mes futuro anunciaba un mejor
puntuado que todavía no había salido — septiembre decía "Maestro con 93" el día que se
generó. Es el mismo cuidado que ya tenían el ranking y el destacado.

### Recomendados del mes (`/recomendados`, desde el 31/08/2026)

**La lista también manda el "PRÓXIMO DESTACADO" de la portada** (desde el 01/09/2026). Antes
el destacado era *el próximo lanzamiento que tuviera noticias*, y eso no medía lo que
parecía: tener noticias habla de cobertura previa, no de que el juego valga la pena. El
01/09 el destacado era Avatar Legends en Xbox —el port de un juego de julio, que arrastra la
noticia de aquel lanzamiento— por delante de cuatro recomendados que salían antes. Un banner
que dice "PRÓXIMO DESTACADO" está afirmando algo, y ahora lo afirma la lista elegida a mano.

Por eso `index.html` carga `datos/recomendados.js`. Si la lista no está cargada, o si los
recomendados del mes ya salieron todos, se cae a la regla vieja.

La selección de lo que vale la pena de cada mes, **elegida a mano**. Vive en
`datos/recomendados.js` y la arma `scripts/generar-recomendados.py`.

**Por qué no la calcula un script:** el ranking ordena por puntaje de Metacritic y sólo
muestra juegos ya lanzados, así que del mes que arranca no puede decir nada — y es justo del
mes que arranca de lo que la gente quiere que le digan algo. Con 106 juegos en septiembre de
2026, una lista por fecha no ayuda a decidir qué mirar. Si se pudiera calcular, ya lo haría
el ranking.

**Lo único que justifica la página es el texto.** Sin la línea de por qué está cada juego, son
doce carátulas que ya están en el calendario. Los datos duros —carátula, fecha, plataformas—
se leen de `datos/juegos.js`, así que no hay nada duplicado y un retraso se refleja solo.

**Al cambiar de mes** se arma la lista nueva y se actualiza el campo `mes`. Va en la rutina
mensual. Dos avisos que imprime el generador y conviene mirar:

- si un recomendado ya no sale en el mes de la lista (se retrasó), lo dice — y eso **no se ve
  mirando la página**, porque la tarjeta sigue igual de prolija con la fecha nueva;
- si la selección quedó vieja, la página lo dice en vez de hacerla pasar por actual.
  Adelantarse **no** es un problema: a fin de agosto la de septiembre ya tiene que estar.

### Mis juegos (`/mis-juegos`, desde el 02/09/2026)

Una lista de favoritos que cada visitante guarda con la estrella. Vive en
`js/favoritos.js` y la página es `mis-juegos.html`.

**Sin cuentas, y es a propósito.** La idea original era "que la gente pueda crear una cuenta
y agregar sus juegos favoritos", pero ahí hay dos cosas distintas pegadas y sólo una es la
interesante. Los favoritos no necesitan cuentas: van en `localStorage`, igual que la
preferencia de tema. Las cuentas sí romperían lo que hace que este sitio se pueda mantener
solo — el sitio es estático y todo se regenera desde `datos/juegos.js`; una base de datos
sería la única parte que no, y si se rompe la gente pierde sus listas. Además obliga a
reescribir `/privacidad`, que hoy dice que no hay cuentas ni datos personales, y deja la
función atrás de un registro que la mayoría no completa. Con 32 clics en agosto, eso la
usaría nadie.

**Lo que se pierde** es la sincronización entre dispositivos y la lista se va si limpian los
datos de navegación. Lo primero se tapa con el botón *copiar link de la lista*, que arma
`/mis-juegos?lista=id,id,id`; al abrirlo en el otro aparato se **une** con lo que ya haya
(unir nunca destruye nada). Sólo entran ids que existan en el calendario: el link lo escribe
cualquiera.

**Lo que las cuentas darían de verdad** —avisar por mail cuando sale el juego— ya estaba
resuelto sin cuentas: el `.ics` de cada ficha, y ahora *agendar todos* en un solo archivo.
El recordatorio lo da el calendario que la persona ya usa.

Detalles que se pagan si se olvidan:

- **La estrella no va dentro de un `<a>`.** Un `<button>` adentro de un enlace es contenido
  interactivo anidado y el navegador parte el DOM. Por eso está en las filas del calendario
  (que son `div`), en la ficha desplegable y en la página del juego, pero **no** en la grilla
  ni en las filas de `/ps5` y `/septiembre-2026`, que son enlaces enteros. En `/mis-juegos`
  el enlace envuelve sólo carátula y nombre, y la estrella queda afuera.
- **La ficha de juego sale siempre "sin guardar"**, y `favPintar()` la corrige al cargar. Es
  un archivo estático y cacheable: al revés, una página cacheada mentiría.
- **En móvil `.juego-fila` es una grilla** con las posiciones puestas a mano. Un hijo sin
  ubicar cae en la primera celda libre — la columna de la miniatura, 64px. La estrella tiene
  su propia columna.
- **Un id huérfano no se borra.** Si `datos/juegos.js` no cargó, `JUEGOS` no existe y podar
  le vaciaría la lista a alguien por un problema de red. Se filtra al mostrar (`favIds()`),
  que es lo que mantiene el contador del menú de acuerdo con la página.
- **`/mis-juegos` va con `noindex`**: el contenido lo pone cada visitante, así que para
  Google está siempre vacía.

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

### Los títulos de las fichas apuntan a la cola larga (decidido el 17/08/2026)

Los datos de Search Console a 3 meses fueron concluyentes: **los 13 clics vinieron todos de
búsquedas de un juego puntual**, casi siempre con la consola adentro — `grounded 2 ps5 cuando
sale`, `he-man ps5`, `yet another zombie survivors ps5` — y varias con 1 impresión y 1 clic,
o sea 100% de acierto. Las dos búsquedas amplias (`próximos lanzamientos videojuegos`,
`juegos lanzamientos`) sumaron 254 impresiones y **cero** clics: ahí el sitio está en la
posición 28, peleando contra medios grandes.

Conclusión: en Google el producto no es el calendario, son las fichas. Por eso el `<title>`
de cada ficha es `{Nombre} en {consolas}: fecha de salida`, con el nombre del sitio sólo si
entra. Antes era `NOMBRE — LANZAMIENTOS.LAT`: ni la consola ni la intención aparecían.

- **Va en minúsculas** (`comun.titulo`): en una lista de resultados, un título todo en
  mayúsculas se lee como si gritara. El H1 de la página sigue en mayúsculas, que es el diseño.
- **Máximo dos consolas y "salida" en vez de "lanzamiento"**, porque Google corta cerca de los
  60 caracteres. Medido sobre los 331 juegos, esa fórmula deja la mediana en 56 y baja de 316
  a 76 los títulos que se pasan. Lo único que nunca se recorta es el nombre del juego: es el
  término por el que la gente busca.
- **La portada y las páginas de plataforma no se tocaron.** Compiten por las búsquedas
  amplias, esa pelea está perdida por ahora y cambiarles el título no mueve nada.


- Meta de verificación de Google Search Console en el `<head>` de `index.html`.
- `sitemap.xml` con la portada + una URL por juego (regenerar con el script, ver arriba).
- **`lastmod` por URL** (desde el 03/08/2026): es la señal con la que Google decide a qué
  páginas vale la pena volver. Sin ese dato trata las 302 URLs como igual de estáticas y no se
  entera de que una ficha se actualizó con una noticia nueva. **No se pone la fecha de hoy en
  todo**: eso diría que las 292 fichas cambian a diario, que es falso y le hace perder la
  confianza al dato. `generar-sitemap.py` guarda una huella del contenido de cada URL en
  `datos/lastmod.json` y sólo mueve la fecha cuando esa huella cambia de verdad. La portada y
  las páginas de plataforma dependen de todo el calendario, así que cualquier juego nuevo o
  corregido las marca como modificadas; las fichas, sólo si cambió esa ficha.

  La huella de una ficha es **su HTML generado**, no su bloque en `datos/juegos.js`. Hasta el
  18/08/2026 era el bloque, que alcanzaba porque la ficha no dependía de nada más; desde que
  muestra las noticias de `datos/noticias.js` que la citan, un rumor nuevo cambia la página
  sin tocar el bloque, y con el bloque como huella ese cambio no llegaba nunca al sitemap.
  Al cambiar la base de la huella hubo que resembrar `datos/lastmod.json` con la huella del
  HTML tal como estaba en el commit anterior: si no, las 337 fichas habrían saltado a la
  fecha de hoy de una y el sitemap le habría mentido a Google sobre todas.
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

## Leer datos/juegos.js se hace en un solo lugar (desde el 02/09/2026)

`cargar_juegos()` estaba copiado en doce scripts, **en tres variantes distintas**. Con el
archivo de hoy las tres daban lo mismo, pero no son equivalentes: nueve cortaban el array con
`.rstrip(";")` y dos en el último `]`. O sea que el día que el formato cambie —por ejemplo si
se le agrega un `module.exports` al final, como ya tiene `datos/recomendados.js`— se rompe la
mitad de los scripts y la otra mitad no, en silencio.

Ahora está una sola vez en `scripts/comun.py`, en una versión más firme que las tres: se
ancla en la declaración `const JUEGOS` (así no la confunde un `=` que aparezca antes en un
comentario) y corta en el último `]` (así no la molesta lo que venga después).

**Cómo verificar un cambio acá.** Antes de tocar, cargar los doce módulos y hashear lo que
devuelve cada `cargar_juegos()`; después de tocar, repetir y comparar. Eso es lo que atrapó
que al limpiar imports se había borrado el `import sys` que necesitaba `sys.path.insert` en
cinco scripts. Después, regenerar todo y hacer `diff` contra una copia previa: las 386
páginas y el sitemap tienen que salir byte a byte iguales, y lo único que puede cambiar son
las marcas de tiempo de `api/*.json` y el `lastBuildDate` del RSS.

## El menú y el pie se tocan en un solo lugar (desde el 02/09/2026)

Vivían en catorce copias —cinco generadores más nueve páginas sueltas— y siempre fallaban
igual: se cambia en trece lugares y el catorceavo queda distinto. Pasó tres veces en dos
días: `/noticias` salió sin el enlace a RECOMENDADOS (el reemplazo no coincidió porque ahí
ese enlace llevaba `class="activo"`), `/recomendados` salió con el "volver" sin estilo, y el
enlace de Cafecito hubo que ponerlo catorce veces.

Ahora los cinco generadores lo sacan de `scripts/plantilla.py`: `cabecera(activo)`, `pie(rss)`
y `script_tema()`. **Para agregar algo al menú se toca `NAV` y listo.**

Consolidar encontró dos errores que ya estaban y nadie había visto:

- **Las cinco páginas de plataforma tenían el menú en otro orden.** Iteraban su propia lista
  `PLATAFORMAS`, así que mostraban PS5 · PS4 · XBOX · SWITCH 2 · SWITCH, mientras las otras
  396 páginas del sitio mostraban PS5 · XBOX · SWITCH 2 · SWITCH · PS4. Ahora todas iguales.
- **`generar-fichas.py` tenía el año del copyright escrito a mano** (`&copy; 2026`). El 1 de
  enero, las 371 fichas iban a decir el año pasado hasta que alguien lo notara. Ahora se
  calcula, como en los otros cuatro.

**Lo que NO cubre, y hay que tener presente:** las nueve páginas escritas a mano (`index`,
`archivo`, `acerca`, `api`, `widget`, `privacidad`, `terminos`, `404`, `mis-juegos`) siguen
con su copia. No hay dónde meterles esto sin proceso de build. Si algún día molesta, el
camino es generarlas también — **no** resolverlo con JavaScript, que deja el menú fuera del
HTML y por lo tanto fuera de Google.

Cómo verificar un cambio acá: guardar una copia de las páginas generadas antes de tocar,
regenerar y hacer `diff`. Es lo que dejó ver que las 371 fichas sólo cambiaban en dos
detalles cosméticos, y que las de plataforma cambiaban en el orden del menú.

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

   **Mirar los tres chequeos del medio**, que reportan fuerte pero no frenan el deploy:
   duplicados, fechas estimadas y favoritos. Los tres cubren el mismo tipo de error —**el que
   no se ve mirando el sitio**— y por eso corren todos los días: ninguno toca la red.

   El de estimados salió del 02/09/2026, cuando el usuario encontró a ojo tres juegos que
   decían "AGOSTO 2026" con agosto terminado. **Un estimado vencido no se ve roto:** la fila
   sale prolija, en su bloque "SIN FECHA CONFIRMADA", afirmando que algo sale en un mes que ya
   pasó, y cuanto más viejo es el dato más convincente parece. Cuando salte uno, **no asumir
   que se retrasó**: de aquellos tres, uno ya había salido, otro había salido ocho meses
   ANTES de lo que decíamos y el tercero nunca tuvo esa fecha. Hay que ir a la tienda.

   **Mirar el final.** Si dice `⚠⚠ N PASO(S) FALLARON`, no subir. Son dos cosas distintas:
   un **generador** que falla deja su página como estaba —se ve bien y está vieja, que es
   por qué nadie lo nota—, y `verificar-favoritos.py` avisa de algo peor: que la estrella
   de favoritos se desenchufó y **la portada puede quedar en blanco**. `js/main.js` llama a
   `favBotonHtml()` en medio del render y esa función vive en `js/favoritos.js`; si se
   renombra o el script deja de cargarse, el calendario no se dibuja. Ese chequeo no toca
   la red, así que corre todos los días.
2. Cargar noticias de los lanzamientos del día y eventos (debuts, Game Pass, betas).
   Las de **un juego** van en su campo `noticias` dentro de `datos/juegos.js`; las que **no
   cuelgan de un lanzamiento** (PS Plus y Game Pass del mes, un Direct, un cierre de estudio)
   van en `datos/noticias.js`. La página `/noticias` mezcla las dos y las ordena por fecha.

   `actualizar.py` recuerda al final cuántas noticias propias hay y hace cuánto se cargó la
   última. Lo que conviene mirar, en este orden: **retrasos** (son lo que más se busca y lo
   que más le importa a un calendario: además de la noticia, hay que corregir la fecha del
   juego), **Directs y State of Play**, y los **juegos del mes** de PS Plus y Game Pass.
   Si no pasó nada que valga la pena, no se fuerza: una entrada floja vale menos que ninguna.

   **Las fuentes que hay que abrir.** Sin esta lista el paso es reactivo: `actualizar.py`
   dice qué juegos salen y cuáles debutaron con puntaje, y se busca cada uno por su nombre.
   Eso encuentra lo que le pasa a los juegos **ya cargados** y se pierde todo lo de afuera —
   así se nos pasó el catálogo de PS Plus de agosto hasta el 13/08/2026, y así faltaba Ghost
   of Yōtei: Edición Completa, anunciada el día anterior en el blog de PlayStation.

   | Fuente | Qué buscar ahí |
   |---|---|
   | [blog.latam.playstation.com](https://blog.latam.playstation.com/) | PS Plus, fechas nuevas de PS5, informes de jugabilidad. Es oficial y está en español. |
   | [news.xbox.com](https://news.xbox.com/es-mx/) | Game Pass y anuncios de Xbox. |
   | [Gematsu](https://www.gematsu.com/) | **Retrasos y fechas nuevas de consola.** Es el que primero los levanta, y son justo el material que le falta a `datos/noticias.js`. **Usar el feed, no la página:** `https://www.gematsu.com/feed` con `curl`. La portada está detrás de una verificación anti-bot que el 27 y el 28/08/2026 no dejó pasar al navegador, y esa no se saltea. El feed responde 200, trae las 20 últimas con fecha y es más cómodo de leer. |
   | [nintendo.com/us/nintendo-direct](https://www.nintendo.com/us/nintendo-direct/) | Directs y sus anuncios. |
   | [Vandal](https://vandal.elespanol.com/) y [3DJuegos](https://www.3djuegos.com/) | **Radar, no fuente de verdad.** Cubren mucho más que las anteriores, en español y con el criterio de qué le importa al público hispanohablante: rumores, ediciones, coberturas que Gematsu no toca por su sesgo japonés. |

   **Descubrir no es verificar.** Cualquiera de estas fuentes sirve para enterarse de que
   algo pasó, pero antes de tocar una fecha o una plataforma hay que verlo en la tienda.
   Esa doble pasada es la que atrapó que Creepshow salía solo en PC y que Nioh 3: Hell
   Rising era DLC. **Vale para todo: fechas, plataformas y juegos nuevos.** El 19/08/2026,
   de 31 datos que traían las fuentes, 14 no los respaldaba ninguna tienda.

   **Cómo verificar rápido, y en este orden:**

   1. **Nintendo primero, porque tiene API y responde diez juegos de una.** Buscando por
      nombre, o preguntando qué sale en un rango de fechas —esto último es lo que descarta
      un lanzamiento inventado—:

      ```
      https://searching.nintendo-europe.com/en/select?q=NOMBRE&fq=type:GAME&wt=json&rows=5
        &fl=title,dates_released_dts,system_names_txt,image_url_sq_s,publisher
      ```

      Devuelve una fila por plataforma, así que sirve igual para confirmar una fecha que
      para saber si un juego sale en Switch, en Switch 2 o en las dos.

   2. **Steam para lo demás que exista en PC**: `appdetails` da fecha, descripción en
      español, géneros y desarrollador. Su campo `type` es el que separa un juego de una
      expansión.

   3. **PS Store y Xbox al final, de a uno.** Sus buscadores se arman con JavaScript, así
      que hay que **navegar de verdad** a cada búsqueda: pedir la página con `fetch` devuelve
      una cáscara vacía y parece que el juego no existe. En la PS Store el estado "Announced"
      con fecha ya es confirmación suficiente.

   **Si ninguna tienda lo tiene, no se carga y no se corrige.** Un dato sin respaldo es
   exactamente lo que este calendario no puede permitirse.

   Tres cosas salen de ahí, y conviene no quedarse solo con la primera:
   - una **noticia** (de un juego o propia);
   - a veces un **juego que falta** en el calendario;
   - a veces una **corrección de fecha o de plataformas** de uno que ya está.

   Ojo con el catálogo de PS Plus: los planes Extra y Deluxe suman juegos viejos, que **no
   son estrenos**. Van como noticia, pero no llevan `psplus: true`, que está reservado para
   los que debutan en el servicio el día que salen.

   **Los rumores van con categoría `RUMORES` y no tocan los datos.** Nunca modifican `fecha`,
   `plataformas` ni ningún campo del juego: viven dentro de la noticia, nombrando quién lo
   reportó y en condicional. La regla completa, con el motivo, está en la cabecera de
   `datos/noticias.js`. En la página se distinguen solas: la etiqueta va con borde punteado.
2 bis. `python3 scripts/novedades-steam.py` — **lo que anuncian los propios estudios.**

   Trae las novedades de la página de Steam de cada juego que está por salir o salió hace
   menos de 30 días. Es fuente primaria: no es un medio contando lo que dijo el estudio, es
   el estudio. El appid sale de la URL de la carátula, así que no hay nada que cargar: 316
   de los 349 juegos lo tienen.

   **Para qué sirve, con números.** El 20/08/2026 los juegos chicos eran los que mejor
   rendían en Google —"sombras: negative frames" tenía 20% de CTR contra 0,6% del sitio
   entero— y son justo los que las webs grandes no cubren. En su primera corrida encontró
   cuatro fechas que ninguna otra fuente nos había dado, las cuatro de juegos que teníamos
   como estimados: Crimson Moon (1 de septiembre), TOEM 2 (29), Woodo (16) y Hunting
   Simulator 3 (29 de octubre).

   El script guarda lo que ya mostró en `datos/novedades-steam.json`, así cada día aparece
   sólo lo nuevo. Cuando un anuncio de fecha nombra un día distinto al que tenemos, lo avisa
   al final con ⚠.

   **La mayoría de lo que publica un estudio no es noticia para un calendario**: notas de
   parche, concursos, descuentos, un vinilo. El filtro mira sólo el título y descarta eso; se
   puede ver todo con `--todos`. Si algo se cuela y no aporta, no se carga: una entrada floja
   vale menos que ninguna.

   **Sólo cubre Steam.** Los exclusivos de Nintendo y PlayStation quedan afuera y siguen
   dependiendo de las fuentes de arriba.
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
   navegador de la app. `curl` sigue dando 403, pero el navegador carga bien.

   **El panel del navegador tiene que tener tamaño real** (`resize_window` a 1280×1600 antes
   de empezar). Si `window.innerHeight` es 0, releases.com renderiza apenas los primeros
   juegos y el resto nunca carga: el 19/08/2026 una página devolvió 8 juegos con el panel sin
   tamaño y 47 con el panel dimensionado. Un barrido hecho así parece completo y no lo está.
   Después de cargar hay que hacer scroll al fondo en un bucle hasta que deje de crecer.

   `fetch()` desde la página no sirve: devuelve el HTML inicial, sin lo que carga después.

   Cada página se raspa con este selector, que devuelve fecha, título y plataformas de cada
   juego:

   ```js
   document.querySelectorAll('.RWP-Calendar-Group')          // cada bloque de fecha
   //   dentro: .RWPCC-CalendarItems-CardControl             // cada juego
   //   el nombre: a.RWPCC-CalendarItems-CardControl-Name
   ```

   Conviene acumular en `localStorage` entre navegaciones y volcar todo al final.

   **Al cruzar los resultados, "Switch 2" contiene "Switch".** Si se busca la etiqueta
   `Switch` sin sacar antes `Switch 2`, todo juego de Switch 2 aparece como si también saliera
   en Switch: el 19/08/2026 eso infló la lista de diferencias de plataforma de 49 a 107, todas
   falsas. Hay que quitar `Switch 2` de la cadena y recién entonces buscar `Switch`.

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

   **releases.com también inventa lanzamientos que no existen.** El 19/08/2026 listaba Super
   Mario Sunshine para Switch 2 el 13/08 y Minecraft para Switch 2 el 27/10, y ninguno de los
   dos aparece en la eShop en esas fechas: son juegos que llegan por Nintendo Classics o por
   una actualización gratuita, no lanzamientos. La eShop europea sirve para verificarlo de una,
   preguntando qué sale en un rango de fechas:

   ```
   https://searching.nintendo-europe.com/en/select?q=*&wt=json&rows=40
     &fq=type:GAME AND dates_released_dts:[2026-10-25T00:00:00Z TO 2026-10-29T00:00:00Z]
     &fl=title,dates_released_dts,system_names_txt,image_url_sq_s,publisher
   ```

   Si un juego que releases.com anuncia para una fecha no está en esa lista, no se carga.

   **Y no inventar la URL de la carátula.** Con el appid a mano da tentación armar
   `.../apps/<appid>/library_600x900.jpg` de memoria, pero muchos juegos no tienen la
   vertical y esa URL da 404. El 28/08/2026 cayeron así cuatro de ocho juegos nuevos
   —Flamecraft, Train Sim World 7, Graveyard Keeper 2 y Transport Fever 3—. Las agarró
   `verificar-enlaces.py` antes del deploy, pero el camino corto es dejar `imagen: null`
   y correr `caratulas-igdb.py`, que las busca donde sí existen.

   **Y parte lanzamientos en dos.** Octopath Traveler y Octopath Traveler II figuraban como dos
   juegos distintos el 1 de octubre; la eShop muestra un solo producto, el bundle de los dos,
   que ya teníamos cargado. Lo mismo con Dragon's Dogma 2, que es Dragon's Dogma 2: Dark Arisen.

   **Cotejar por id, no por nombre.** Al cruzar lo que devuelve releases.com contra
   `datos/juegos.js`, la comparación por título genera **falsos faltantes**: releases.com
   escribe "Diablo 4" y nosotros "DIABLO IV" (arábigo contra romano), o lista "Dragon Quest
   Monsters: The Withered World" mientras nosotros tenemos el título en español ("El Reino
   Marchito"). Las dos veces el juego ya estaba cargado. El costo es tiempo revisando de
   más, nunca datos duplicados, porque el chequeo por id lo frena antes de escribir. Si un
   juego "falta" y es de una saga conocida, buscarlo también por su nombre en el otro idioma
   y por el número en la otra grafía antes de darlo por nuevo.

   **releases.com no sirve para los meses lejanos.** El 25/08/2026 tenía diez juegos de consola
   en todo noviembre y diciembre, y los diez ya estaban cargados: el problema no era nuestro
   barrido, era la fuente. Para esos meses conviene preguntarle a la eShop por rango de fechas,
   que devuelve el catálogo de Nintendo completo:

   ```
   https://searching.nintendo-europe.com/en/select?q=*&wt=json&rows=200
     &fq=type:GAME AND dates_released_dts:[2026-11-01T00:00:00Z TO 2026-11-30T00:00:00Z]
     &fl=title,dates_released_dts,system_names_txt,publisher,image_url_sq_s,nsuid_txt
     &sort=dates_released_dts asc
   ```

   Ojo con dos cosas: devuelve **una fila por plataforma**, hay que juntar por título; y la
   fecha **31 de diciembre es un comodín** que significa "en 2026, sin día". Esos van con
   `estimado: true`. Un `nsuid_txt` propio confirma que es un producto de la tienda y no una
   incorporación al catálogo de Nintendo Switch Online.

   URLs del barrido: `https://www.releases.com/calendar/games?at=2026-Sep-01` y variantes
   (`-Sep-09`, `-Sep-18`, `-Sep-26`…). Cada carga muestra ~10 días, así que hacen falta 3 o 4
   por mes. Al final de cada mes aparecen los bloques "Estimated <mes>" y "Estimated Q<n>":
   esos van con `estimado: true` y `fechaEstimada`.
5 bis. **Verificar antes de escribir.** Todo lo que devuelve el barrido —juegos nuevos,
   fechas y plataformas— pasa por la misma comprobación en tienda que la rutina diaria, con
   el orden y las trampas que están explicadas ahí (paso 2, "Descubrir no es verificar").
   Vale la pena agrupar por tienda: Nintendo se resuelve en una consulta para diez juegos y
   PS Store y Xbox hay que caminarlas de a una.

   La proporción del 19/08/2026 da una idea de por qué: de 13 juegos "faltantes", 9 no
   existían como lanzamiento; de 18 diferencias de plataforma verificadas, 6 no las respaldaba
   ninguna tienda.
6. Trailers, carátulas y campo `relanzamiento` de lo que se haya agregado.
7. **Backlog de carátulas y trailers:** reintentar los que `actualizar.py` lista bajo
   "Faltantes". Suelen ser juegos que todavía no tenían ficha en Steam ni en la eShop cuando
   se cargaron; a medida que las tiendas publican assets, aparecen. Es un minuto de trabajo.
8. Regenerar todo (`generar-fichas`, `generar-plataformas`, `generar-feeds`, `generar-sitemap`)
   y verificar que las carátulas y los trailers nuevos devuelvan HTTP 200 antes del deploy.

8 bis. **Juegos dados por lanzados que capaz nunca salieron:**
   `python3 scripts/verificar-lanzados.py`.

   Es el error más caro que puede cometer un calendario y **no se ve mirando el sitio**: la
   ficha queda igual de prolija con la fecha equivocada. En agosto de 2026 aparecieron tres,
   cada uno por casualidad y por un camino distinto: Rivage figuraba salido el 13/08 y la
   PlayStation Store decía 22/09; Ratatan figuraba salido el 16/07 y no estaba en ninguna
   tienda; BloodRayne figuraba salido el 29/07 y su editor decía octubre.

   Hace dos pasadas:

   - **La confiable**: si Steam devuelve `coming_soon: true` para un juego que damos por
     lanzado, la fecha está mal. Ojo con una trampa que ya está resuelta en el script: si el
     juego **ya tiene puntaje**, salió, y ese `coming_soon` es de la versión de PC, que a
     veces llega después que la de consola. Culdcept Begins tiene 76 desde julio y en Steam
     figura para el cuarto trimestre.
   - **La de revisar a mano**: juegos lanzados hace más de tres semanas sin puntaje de
     crítica, sin puntaje de usuarios, sin noticias y sin duración. La mayoría son indies que
     no miró nadie —Flesh Made Fear está en la PS Store a 19,99 y es de esos— pero es la única
     forma de agarrar a los que no están en Steam, que es el caso de Ratatan y BloodRayne. Se
     verifica en la tienda de su plataforma; si no aparece en ninguna, la fecha está mal.
9. **Enlaces vivos:** `python3 scripts/verificar-enlaces.py`. Comprueba que las 315
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
| `metacritic` (y con eso el ranking) | — | **Diaria, automática.** `actualizar.py` busca puntaje para cualquier juego ya lanzado con `metacritic: null`, y **refresca el de los que ya lo tienen**: no queda congelado |
| `metacriticUsuarios` y `metacriticVotos` | — | **Diaria, automática.** Misma pasada, misma página: sin pedidos de más |
| `critica` (resumen de la prensa) | Diaria, paso 2, cuando el juego debuta con puntaje | Mensual, con el backlog que lista `actualizar.py`. Al 18/08/2026 están los 86 con puntaje: el backlog vuelve a llenarse solo cada vez que un juego debuta |
| `noticias` de un juego | Diaria, paso 2 (lanzamientos de hoy y mañana, y debuts con puntaje) | Mensual, paso 12 (los mejor puntuados que sigan sin noticias) |
| `datos/noticias.js` (PS Plus, Game Pass, Directs, retrasos) | Diaria, paso 2 | Diaria: `actualizar.py` avisa hace cuántos días se cargó la última |
| Noticias y fechas de los juegos chicos | Diaria, paso 2 bis | Diaria: `novedades-steam.py`, con lo que anuncia el propio estudio |
| `gamepass` y `psplus` | Al cargar, si ya se sabe | **Mensual, sección "suscripciones"** |
| `fecha` y `plataformas` (cambian solas) | — | Semanal, paso 5 (barrido de releases.com) |
| Juegos nuevos | Semanal, paso 5 | Mensual, paso 9 (estrena el mes siguiente) |
| `estimado` / `fechaEstimada` | Semanal, paso 5 | Mensual, paso 12 bis (backlog de Q3/Q4) |
| `imagen` y `trailer` | Semanal, paso 6 | Semanal, paso 7 (los que faltan) |
| **Que esas URLs sigan vivas** | — | **Semanal, paso 9:** `python3 scripts/verificar-enlaces.py` |
| **Que un juego dado por lanzado haya salido** | — | **Semanal, paso 8 bis:** `python3 scripts/verificar-lanzados.py` |
| **Que un juego no esté cargado dos veces** | — | **Diaria, automática** (`verificar-duplicados.py` dentro de `actualizar.py`) |
| **Recomendados del mes** (`datos/recomendados.js`) | — | **Mensual:** armar la lista del mes que entra |
| `duracion` (HLTB) | Mensual, paso 10 | Mensual, paso 10 (recorre todos, no solo los nuevos) |
| `descripcion`, `genero`, `desarrollador` | Semanal / Mensual, al cargar | — (no se desactualizan) |
| Datos estructurados del trailer | — | Diaria, automática (`cargar-meta-trailers.py`) |
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

### Ideas del usuario del 27/08/2026 (sin empezar)

- **Vapor World: Over the Mind — qué fecha va.** Entró a Game Pass el 19/08/2026 en formato
  Game Preview, "available on day one", según el propio anuncio de Xbox Wire. Nosotros lo
  tenemos para el 30/09, que sería la versión terminada. La pregunta es cuál de las dos es
  "el lanzamiento" para este calendario. Hay precedente para las dos respuestas: Grounded 2
  también entró en Game Preview y su ficha usa la fecha del debut en PS5, o sea que el Game
  Preview no cuenta; pero si no cuenta, entonces el 30/09 sí es un estreno en el servicio y
  le faltaría `gamepass: true`. Hoy está sin distintivo y con fecha 30/09, que es la
  combinación que no cierra con ninguna de las dos lecturas.

- **2027 todavía no aprieta.** Al 31/08/2026 la eShop tiene **un** juego en enero de 2027 y
  ninguno en febrero ni marzo, así que el paso 9 de la mensual —estrenar el mes siguiente—
  no tiene con qué. En el calendario hay un solo juego de 2027 (Trine 6, 04/03) y no tiene
  puntaje, así que tampoco toca el ranking. La decisión sobre filtros y ranking sigue
  pendiente pero no está bloqueando nada: cuando las fuentes empiecen a poblar 2027 va a
  haber tiempo de sobra, y conviene tomarla antes de cargar la primera tanda.

- **Repensar el ranking para 2027.** Hoy el ranking es una lista por puntaje de Metacritic
  sobre todo el calendario, que son 360 juegos de un solo año. Cuando entre 2027 empiezan a
  convivir dos años y la lista deja de significar nada sin decir *de qué*. Hace falta al
  menos un filtro de año, y probablemente que el ranking pase a ser "lo mejor de 2026" como
  página propia, que además es contenido que se busca. Va con la pregunta más grande de
  **cómo se ordenan los filtros cuando haya dos años cargados**: hoy hay plataforma y
  género, y sumar año a la misma fila puede volverla ilegible en el teléfono. Conviene
  resolverlo antes de cargar el primer juego de 2027, no después.

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
- **Bloque "Estimated" de releases.com: prácticamente vaciado (18/08/2026).** De los ~35 que
  quedaban a principios de agosto, los barridos semanales fueron absorbiendo casi todos: al
  18/08 quedaban **dos**, y se cargaron (Samson y Vapor World: Over the Mind). El resto de lo
  que sigue en esos bloques es PC, DLC, o cosas que no son lanzamientos. Lo descartado a
  propósito, para no volver a mirarlo:
  - **Fallout 76** en PS5 y Xbox no es un lanzamiento: es la actualización gratuita a versión
    nativa para quien ya tiene el juego. Mismo criterio que la versión de Switch 2 de
    Gobliiins Collection.
  - **Vampire Survivors: Legacy of the Bloodmoon**, **Dragon Ball Xenoverse 2 Chapter 4** y
    **Banchou Tactics** son DLC.
  - **Silent Planet** y **Ari Buktu and the Anytime Elevator**: no se pudo confirmar el juego.
    Steam devuelve otro título ("Silent Shark") o directamente nada.
  - **Another Eden: The Cat Beyond Time and Space**: no está claro si es el mismo producto que
    "Another Eden Begins", que ya está cargado para el 17/09.

- Difusión (idea pendiente del usuario): mails a medios y creadores en español desde
  contacto@lanzamientos.lat, y listados en directorios/GitHub. Sin redes sociales.
- El bloque de novedades en la portada quedó descartado (empuja el calendario hacia abajo).
  La página `/noticias` sí se hizo, el 09/08/2026: ver "Funcionalidades".
- Si algún día se cargan datos desde una API externa: escapar HTML antes de inyectar
  con `innerHTML` (hoy no hace falta porque los datos son propios).
