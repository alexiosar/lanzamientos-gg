# LANZAMIENTOS.LAT

Calendario de lanzamientos de videojuegos en español para PS5, PS4, Xbox, Switch y Switch 2.
Sitio 100% estático: HTML, CSS y JavaScript puro, sin frameworks ni proceso de build.

**Dominio:** https://lanzamientos.lat

## Estructura del proyecto

```
├── index.html                  Página principal (calendario)
├── css/style.css               Todos los estilos (temas oscuro y claro)
├── js/main.js                  Lógica del calendario: filtros, buscador, fichas, modal
├── datos/juegos.js             Base de datos: array JUEGOS con todos los lanzamientos
├── juegos/juego.html           Plantilla de ficha individual (+INFO), lee ?id= de la URL
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

### Después de agregar o quitar juegos

Regenerar el sitemap (necesario para el SEO):

```
python3 scripts/generar-sitemap.py
```

Luego commit y deploy. No hace falta si solo se editan campos de juegos existentes.

## Funcionalidades

- **Calendario agrupado por mes y día**, con desplegables. Se abre solo el mes actual
  y hace scroll automático al día de hoy (o al más próximo).
- **Indicadores por día**: `[ HOY ]` (amarillo, parpadea), `[ PRÓXIMO ]` (el primer día
  con lanzamientos después de hoy) y `[ YA DISPONIBLE ]` (verde, días pasados).
- **Filtros por plataforma y género** (los de género se generan automáticamente desde los
  datos). La plataforma también se puede fijar por URL: `index.html?plat=PS5`.
- **Buscador por nombre**: filtra en vivo y abre todos los meses mientras se busca.
- **Vista ★ RANKING**: selector "VISTA" arriba de los filtros; lista los juegos con puntaje
  de Metacritic ordenados de mejor a peor. Respeta los filtros de plataforma/género y el
  buscador. Crece solo a medida que se cargan puntajes.
- **Cuenta regresiva**: en las fichas de juegos futuros, debajo de la fecha
  (`▸ FALTAN X DÍAS`, `▸ FALTA 1 DÍA`, `▸ ¡SALE HOY!` parpadeante). Se oculta en los
  ya lanzados. Funciona en la ficha desplegable y en la página +INFO.
- **Ficha desplegable** al hacer clic en un juego: carátula, datos, Metacritic, descripción,
  tags, trailer en modal y link a la ficha completa.
- **Ficha individual** (`juegos/juego.html?id=...`): igual que la desplegable más la sección
  **ÚLTIMAS NOVEDADES** (noticias del juego) y el trailer embebido.
- **Badge de Metacritic** con color según puntaje: verde ≥ 75, amarillo 50–74, rojo < 50.
- **Tema oscuro/claro**: botón ☾/☀ en la esquina superior derecha. La preferencia se guarda
  en localStorage y aplica en todas las páginas. El tema claro tiene su propia paleta de
  acentos (colores oscurecidos para que se lean sobre fondo claro).
- **★ NUEVO**: marca juegos recién agregados al calendario, pero solo se muestra si el juego
  todavía no salió (en los ya disponibles se apaga sola).

## SEO y redes

- Meta de verificación de Google Search Console en el `<head>` de `index.html`.
- `sitemap.xml` con la portada + una URL por juego (regenerar con el script, ver arriba).
- `robots.txt` que permite indexar todo y apunta al sitemap.
- **Open Graph**: al compartir el link en WhatsApp/X/Discord aparece la tarjeta con
  `og-image.png`. Limitación: los links a fichas individuales muestran la tarjeta genérica
  del sitio (los scrapers de redes no ejecutan JavaScript); tarjetas por juego requerirían
  un Worker de Cloudflare.
- **Datos estructurados (JSON-LD)**: la portada declara `WebSite` y cada ficha inyecta
  `VideoGame` (nombre, fecha, plataformas, desarrollador, imagen) para que Google entienda
  el contenido. Ojo: el test de rich results de Google muestra "0 elementos" porque
  `VideoGame` no genera resultados enriquecidos específicos — es normal, no es un error.
  Para ver los datos detectados usar validator.schema.org con la URL de la portada.
- Tras un deploy con juegos nuevos: Search Console → Sitemaps → enviar `sitemap.xml`.

## Deploy

Cloudflare (Wrangler) con `wrangler.jsonc`: sube toda la carpeta como assets estáticos.
Pendiente evaluar un `.assetsignore` para excluir del deploy los archivos que no son del
sitio (`scripts/`, `README.md`, el propio `wrangler.jsonc`).

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
- Noticias en más juegos (hoy tienen ~13 de 57).
- Botón "agendar" (.ics) por juego y cuenta regresiva en las fichas.
- Bloque destacado "Próximos 7 días" arriba del calendario.
- Filtros combinables en la URL (`?plat=PS5&gen=RPG`) para links compartibles.
- Accesibilidad: tamaño de fuente base, objetivos táctiles, `prefers-reduced-motion`.
- Sección de noticias general (`/noticias.html`) agregando las noticias de todos los juegos.
- Analytics de Cloudflare (gratis, sin cookies) y PWA instalable (manifest.json).
- Si algún día se cargan datos desde una API externa: escapar HTML antes de inyectar
  con `innerHTML` (hoy no hace falta porque los datos son propios).
