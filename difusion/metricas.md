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
| 03/08/2026 | `lastmod` en el sitemap: Google puede distinguir qué páginas cambiaron |
