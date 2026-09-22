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
| 01/09/2026 | 361 | 602 | 27 | 4.870 | 32 | 240 | 590 | 369 |

## Objetivos para el 01/10/2026 (escritos el 22/09/2026)

Anotados antes de ver los números, para no acomodar la vara después. Son objetivos, no
pronósticos: buena parte de esto no se controla desde el sitio.

**Agosto fue el mes de la indexación y septiembre fue un mes de contenido.** Entraron 89
juegos, se reescribieron unas 140 descripciones y se sumaron noticias y crítica en muchas
fichas, más las páginas de mes y 2027. Eso no se ve en "indexadas": se ve en posición y en
clics. Este mes el número que importa deja de ser las impresiones y pasa a ser el clic.

| Métrica | 01/09 | Bien | Muy bien | Mala señal |
|---|---|---|---|---|
| Indexadas | 361 | 420 | 450+ | menos de 380 |
| Impresiones (28 d) | 4.870 | 9.000 | 15.000+ | menos de 6.000 |
| Clics (28 d) | 32 | 100 | 200+ | menos de 60 |
| CTR | 0,65% | ~1% | 1,5% | que baje mientras suben las impresiones |
| Visitas (30 d) | 240 | 500 | 800+ | menos de 350 |
| Páginas vistas | 590 | 1.300 | 2.000+ | que caiga la relación con las visitas |

Las 420 indexadas no son crecimiento puro: el calendario pasó de 369 a 458 juegos, así que
hay 89 fichas nuevas haciendo cola. Quedarse en 361 con 89 páginas más sí sería un problema.

**Tres cosas a mirar aparte de la tabla:**

1. **Páginas por visita.** El 01/09 eran 2,46. Si sube, el enlazado interno y las páginas de
   mes están funcionando. Si baja mientras crecen las visitas, es tráfico que entra a una
   ficha y se va.
2. **`/octubre-2026` sola, no dentro del total.** Es la primera página de mes que llega
   estrenada al mes que le toca, y "juegos que salen en octubre" se busca a fin de septiembre
   y en los primeros días del mes.
3. **"Descubierta sin indexar".** Estaba en 27. Con 89 fichas nuevas puede subir a 50 o 60 sin
   que pase nada; si se dispara a 150, ahí hay que mirar.

**Los votos todavía no se miden.** Se publicaron el 15/09 y en la primera semana juntaron tres
en diez fichas; los dos posteos diarios existen recién desde el 18. Octubre es el primer mes
con datos reales: se anotan como columna nueva desde el 01/10, sin objetivo, para tener contra
qué comparar en noviembre.

**Si los clics no llegan, no es motivo para tocar nada.** Son lo más difícil de mover y lo que
más depende de cosas ajenas: qué juegos grandes salen, si alguien enlaza el sitio, cómo
reparte Google. Si octubre da 60 clics pero las impresiones y la posición siguieron subiendo,
el mes fue bueno igual.

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
| 01/09/2026 | **Una página por mes** (`/septiembre-2026` y las demás), en el sitemap. Son las primeras URLs pensadas para búsquedas del tipo "juegos que salen en octubre" |
| 02/09/2026 | Mis juegos: favoritos guardados en el navegador, con la estrella en todas las páginas |
| 06/09/2026 | El sitio aclara hasta dónde llega el calendario, y los redirects cubren también la variante `.html` |
| 07/09/2026 | **Gameplay en español** en las fichas (campo `gameplay`), empezando por los recomendados |
| 08/09/2026 | `/mejores-juegos-agosto-2026`: primera página de recomendados de un mes cerrado. Mismo día, se sacaron de todos los textos las frases que hablaban del sitio en vez de los juegos |
| 08/09/2026 | La grilla del calendario pasó a agruparse por día |
| 09/09/2026 | **2027 entra al calendario**, con filtro por año, tras el Nintendo Direct. Se suman páginas de mes de enero a abril de 2027 |
| 14/09/2026 | **Unas 140 descripciones reescritas.** Estaban copiadas de Steam o la eShop, con tú, vosotros y signos de exclamación. Es contenido propio donde antes había texto repetido en otras webs |
| 15/09/2026 | **Votos "¿Lo vas a jugar?"** en todas las fichas, con un Worker de Cloudflare. El bloque carga después de la página y no debería mover la velocidad, pero si cambia algo en Core Web Vitals, empezar a buscar por acá |

Además, a lo largo de septiembre la rutina diaria sumó críticas y noticias a los estrenos del
día. Al 31/08 había 131 fichas con noticias y 103 con resumen de crítica; al 16/09 son 174 y
138. No tiene una fecha única, pero es la otra parte del contenido propio del mes.

## Agosto de 2026: el mes en que el sitio entró a Google

Es el primer salto real desde que existe el registro, y conviene dejar dicho de qué está
hecho antes de que el número se lea solo:

| | 01/08 | 01/09 | |
|---|---|---|---|
| Indexadas | 31 | **361** | de un 12% del calendario a prácticamente todo |
| Impresiones (28 d) | 140 | **4.870** | 35 veces más |
| Clics (28 d) | 0 | **32** | |
| Visitas (30 d) | 100 | 240 | |
| Páginas vistas | 300 | 590 | |

**El "602 sin indexar" asusta y casi todo es correcto.** Queda desarmado acá para no tener
que investigarlo de nuevo cada mes:

| Motivo | Páginas | Qué es |
|---|---|---|
| Página con redirección | 282 | Las variantes `.html` y con barra final de cada URL. Cloudflare las manda solas a la URL limpia. No salen de nuestro sitemap, que no tiene ninguna de las dos formas |
| Excluida por `noindex` | 273 | El esquema viejo `/juegos/juego?id=X`. Esa plantilla lleva `noindex` a propósito desde que existen las fichas estáticas: Google está obedeciendo, no fallando |
| Descubierta sin indexar | 27 | Cola normal de rastreo |
| Rastreada sin indexar | 10 | Ídem |
| No encontrada (404) | 5 | Las cinco fichas borradas en junio sin redirect. **Ya tienen 301 desde el 27/08**; el "Error" de validación es de la tanda vieja |
| Error de redirección | 5 | No son nuestras: los doce redirects propios dan un solo salto y terminan en 200 (verificado el 01/09/2026) |

**Lo único mejorable de esa lista** son los 282: Cloudflare responde esas redirecciones con
**307, que es temporal**. Para canonicalizar, Google prefiere 301, y ante un 307 sigue
volviendo a pedir la URL vieja — que es probablemente por qué ese número sube en vez de
estabilizarse. No está claro que se pueda cambiar sin sacarle a Cloudflare el manejo
automático de URLs limpias, así que queda como pendiente a evaluar y no como algo roto.

**De dónde salieron estos números.** `search.google.com` está bloqueado para el navegador de
la app, así que los pasó el usuario a mano desde el suyo. Por Gmail llegan los avisos de
Search Console pero no las cifras.
