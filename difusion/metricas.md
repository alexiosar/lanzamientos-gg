# Registro de métricas

Una fila por mes. La idea es tener contra qué comparar: en un sitio nuevo los números de
una semana son ruido, los de un mes ya dicen algo.

**Cuándo anotar:** el primer día de cada mes, junto con la rutina mensual.

**Dónde salen los datos:**

- Search Console → *Indexación de páginas* (indexadas, no indexadas, "descubierta")
- Search Console → *Rendimiento* → últimos 28 días (impresiones, clics)
- Cloudflare → *Analytics & Logs* → *Web Analytics* → últimos 30 días (visitas, páginas vistas)

| Fecha | Indexadas | No indexadas | "Descubierta" | Impresiones | Clics | Visitas | Páginas vistas | Juegos |
|---|---|---|---|---|---|---|---|---|
| 29/07/2026 | 31 | 183 | 176 | 63 | 0 | — | — | 246 |
| 01/08/2026 | 31 | 183 | 176 | 140 | 0 | 100 | 300 | 291 |
| 01/09/2026 | — | — | — | — | 30 | — | — | 369 |

## Cómo leerlo

**El orden en que mejoran las cosas es siempre el mismo:** primero suben las impresiones,
después bajan las "descubiertas sin indexar", después suben las indexadas y **al final**
aparecen los clics. Si las impresiones suben y los clics siguen en cero, vamos bien.

Entre el 29/07 y el 01/08 las impresiones pasaron de 63 a 140 con las mismas 31 páginas
indexadas: las mismas páginas se están mostrando más veces, que es exactamente la primera
señal que se espera.

**Contexto para no asustarse:** el sitio se publicó alrededor del 9 de julio de 2026. Para un
dominio nuevo, que Google conozca las URLs y todavía no las rastree es el estado normal, no un
error. Lo que destraba eso son los enlaces externos, no más cambios en el sitio.

## Qué esperar de los cambios del 03/08

Ninguno de los dos hace que Google indexe más páginas de golpe.

- El **`lastmod`** no consigue rastreos nuevos: consigue que los rastreos que ya hace se
  gasten en las páginas que cambiaron. Si sirve, se ve primero como más páginas *rastreadas*,
  no como más *indexadas*, y en semanas.
- **Desbloquear la IA** no toca a Google Search. Su efecto, si aparece, es que el sitio pueda
  citarse en respuestas de ChatGPT, Claude o los resúmenes de IA de Google. Eso no se mide en
  Search Console: se comprueba preguntándole a esas herramientas "cuándo sale tal juego" dentro
  de unos meses y viendo si aparece lanzamientos.lat entre las fuentes.

## Qué NO hacer

- No mirarlo todas las semanas. Siete días de datos en un sitio de un mes es ruido, y sólo
  sirve para desanimarse.
- No medir el éxito por los clics todavía.
- No tocar el sitio "para mejorar el SEO" cada vez que un número no sube. Lo técnico ya está
  verificado y limpio (canonical, JSON-LD, h1, sitemap, robots.txt).

## Cambios que pueden explicar saltos futuros

| Fecha | Cambio |
|---|---|
| 30/07/2026 | Enlazado interno: cada ficha pasó de 0 a 12 enlaces a otras fichas |
| 30/07/2026 | Página `/api` publicada y sumada al sitemap |
| 31/07/2026 | El calendario pasó de 246 a 275 juegos |
| 01/08/2026 | Julio se archivó: la portada arranca en agosto |
| 03/08/2026 | `lastmod` real por URL en el sitemap: Google puede distinguir qué páginas cambiaron de verdad en vez de tratar las 302 como iguales |
| 03/08/2026 | **Rastreadores de IA desbloqueados.** Cloudflare inyectaba un `robots.txt` propio que bloqueaba GPTBot, ClaudeBot, Google-Extended, CCBot y otros. Se desactivó *Managed robots.txt* en Security → Settings → AI Crawl Control. No afectaba la indexación normal de Google, pero impedía que el sitio fuera fuente en respuestas de IA, incluidas las de Google |
| 01/09/2026 | `/recomendados` publicada: la selección del mes elegida a mano, en el sitemap y en la navegación |

**01/09/2026 — fila incompleta a propósito.** Los clics salen del mail de Search Console
("30 clics en 28 días", recibido el 31/08) y los juegos, del calendario. Las impresiones y
los números de indexación **no se pudieron leer**: `search.google.com` está bloqueado para
el navegador de la app, así que Search Console se consulta desde Gmail y por ahí sólo llegan
los avisos, no los números. Completar esas celdas a mano entrando desde el navegador propio.