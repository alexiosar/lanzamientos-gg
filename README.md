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
└── robots.txt                  Permite indexación y declara el sitemap
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
  trailer: "https://youtube.com/embed/XXXXXXX",   // formato /embed/, no /watch
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

Todos los campos opcionales (`metacritic`, `imagen`, `noticias`) se ocultan solos si están
en `null` o ausentes — no rompen nada.

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

## SEO

- Meta de verificación de Google Search Console en el `<head>` de `index.html`.
- `sitemap.xml` con la portada + una URL por juego (regenerar con el script, ver arriba).
- `robots.txt` que permite indexar todo y apunta al sitemap.
- Tras un deploy con juegos nuevos: Search Console → Sitemaps → enviar `sitemap.xml`.

## Desarrollo local

Servidor local para previsualizar (cualquiera sirve, es un sitio estático):

```
python3 -m http.server 8080
```

y abrir http://localhost:8080

## Pendientes / ideas

- Noticias en más juegos (hoy tienen 12 de 37).
- Bloque destacado "Próximos 7 días" arriba del calendario.
- Filtros combinables en la URL (`?plat=PS5&gen=RPG`) para links compartibles.
- Accesibilidad: tamaño de fuente base, objetivos táctiles, `prefers-reduced-motion`.
- Sección de noticias general (`/noticias.html`) agregando las noticias de todos los juegos.
- Si algún día se cargan datos desde una API externa: escapar HTML antes de inyectar
  con `innerHTML` (hoy no hace falta porque los datos son propios).
