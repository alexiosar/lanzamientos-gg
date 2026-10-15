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
| 01/10/2026 | 425 | 672 | — | 12.900 | 108 | 500 | 1.090 | 481 |

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
| 24/09/2026 | **Caída de Google**: las impresiones pasan de ~600 a ~30 por día y los clics desde Google a cero. Coincide con el día en que empezó el **September 2026 spam update** de Google (24/09, despliegue de hasta dos semanas). Google no dijo qué castiga: que sean las páginas de plantilla con poco contenido propio es una deducción nuestra a partir de sus políticas de spam (corregido el 07/10). Algorítmico: Acciones manuales y Problemas de seguridad, vacíos |
| 29/09/2026 | **Páginas por consola y mes** (`/ps5-octubre-2026` y las demás) y estructura de PS Plus / Game Pass del mes |
| 30/09/2026 | `/ps-plus-octubre-2026`, enlazada desde la noticia, la portada y el RSS |
| 05/10/2026 | **`noindex, follow` y fuera del sitemap para 134 fichas flacas y las 22 páginas por consola y mes.** El sitemap pasa de 549 a 393 URLs. Las fichas vuelven solas al índice cuando suman noticia, crítica, gameplay o una descripción más larga. Si en Search Console bajan las "indexadas" en las semanas siguientes, es esto y es a propósito: no es un problema nuevo |
| 06/10/2026 | **84 fichas vuelven al índice**: se les escribió una descripción propia desde la ficha oficial (de 45 a 85 palabras) y dejaron de ser flacas. Primero las de juegos de octubre y noviembre, después las de junio a septiembre. De 134 flacas quedan 50, casi todas de 2027 o sin información en ninguna tienda. El sitemap pasa de 393 a 479 URLs. Si en octubre suben las "indexadas" o las impresiones de fichas chicas, es esto |
| 07/10/2026 | **15 fichas flacas más vuelven al índice** con descripción propia, sacada de Steam, la PS Store y Xbox. Quedan 35, casi todas de 2027 o juegos chicos de la eShop sin ficha en otra tienda. El sitemap pasa de 479 a 497 URLs, contando también `/game-pass-octubre-2026` y dos juegos nuevos del día. De paso se corrigieron tres estimados que Steam ya pasó a 2027: Mariachi Legends, Bestiario y Sublustrum |
| 08/10/2026 | **Canónica en la portada y arreglo del CLS de la portada.** Cloudflare marcaba 19% de visitas a `/` con CLS malo (el pie y el `main` saltaban cuando terminaba de bajar `juegos.js`). Ahora `#calendario` reserva el alto de la pantalla mientras está vacío. Si en Core Web Vitals el rojo del CLS baja en las semanas siguientes, es esto. Además, **16 descripciones copiadas de Steam reescritas** (Onimusha, Metaphor, Elden Ring en Switch 2 y otras), encontradas comparando contra el texto de la tienda. Y **18 fichas flacas más vuelven al índice** (Danganronpa 2x2, Metro 2039, Kingdom Hearts IV, Resident Evil Veronica y otras de 2027): quedan 17 y el sitemap pasa a 523 URLs |

Además, a lo largo de septiembre la rutina diaria sumó críticas y noticias a los estrenos del
día. Al 31/08 había 131 fichas con noticias y 103 con resumen de crítica; al 16/09 son 174 y
138. No tiene una fecha única, pero es la otra parte del contenido propio del mes.

## Septiembre de 2026 contra los objetivos (leído el 01/10/2026)

| Métrica | 01/09 | Objetivo "bien" | 01/10 | |
|---|---|---|---|---|
| Indexadas | 361 | 420 | **425** | bien (dato de Search Console del 20/09) |
| Impresiones (28 d) | 4.870 | 9.000 | **12.900** | bien, cerca de "muy bien" |
| Clics (28 d) | 32 | 100 | **108** | bien |
| CTR | 0,65% | ~1% | **0,8%** | subió, sin llegar |
| Posición media | — | — | **11,8** | en agosto era 27,7 |
| Visitas (30 d) | 240 | 500 | **500** | bien, justo |
| Páginas vistas | 590 | 1.300 | **1.090** | debajo de "bien"; 2,18 por visita contra 2,46 en agosto |

**Se cumplió todo lo que se midió, y con seis días perdidos.** Desde el 24/09 Google casi no
muestra el sitio (ver la caída en la tabla de cambios), y aun así el mes pasó los objetivos:
hasta el 23/09 venía a ~600 impresiones por día, un ritmo que daba unas 16.000 en 28 días,
es decir "muy bien". Lo mismo con los clics: 108 casi todos antes del 24.

**La posición pasó de 27,7 a 11,8.** Es el dato más importante del mes: es la diferencia
entre la tercera página de resultados y el borde de la primera. Es lo que explica que los
clics se hayan triplicado, más que las impresiones.

**Qué páginas trajeron los clics.** La portada concentra un tercio (35 de 108, 2.265
impresiones). Después vienen fichas sueltas, casi todas de juegos que salían ese mes y con
pocos competidores en español: NASCAR 26 (8), Solo Leveling: Arise Overdrive (6), Kernel
Hearts (6), Touhou Koumakyou (4), Train Sim World 7 (4). `/noviembre-2026` ya aparece con
2 clics y 287 impresiones: las páginas de mes empiezan a trabajar. Hay 302 páginas con al
menos una impresión.

**Las visitas crecieron al final del mes, con Google en cero.** Cloudflare marca 40 a 60
visitas por día del 24 al 30, contra 10 a 20 el resto del mes. No vienen del buscador: son
los posteos diarios y el tráfico directo. La mitad de las visitas es de Argentina (240 de
500), después Estados Unidos (110) y Japón (60).

**Las páginas por visita bajaron (2,46 → 2,18), pero el promedio esconde dos públicos.**
Argentina hace 820 páginas vistas en 240 visitas, unas 3,4 por visita: el que entra recorre.
Estados Unidos (120 en 110) y Japón (60 en 60) ven una sola página y se van, un patrón que
en buena parte son rastreadores y no gente. Ojo también con que las visitas del propio
usuario cuentan dentro de Argentina. El número a seguir en noviembre es el de Argentina
solo, no el total.

**Para el 15/10:** lo más probable es que la caída sea el spam update del 24/09 (ver la
tabla de cambios): la fecha coincide, aunque Google no dijo qué castiga ese update. La recuperación de esos golpes lleva meses, así que la lectura del
15/10 no busca que el gráfico vuelva, sino señales: que las fichas con contenido sigan
indexadas y que las impresiones dejen de estar en cero. **En noviembre las "indexadas"
pueden moverse en los dos sentidos**: bajar por el noindex del 05/10 y volver a subir por las
84 fichas recuperadas el 06/10. Las dos cosas son a propósito.

### Lectura semanal del 08/10/2026 (datos de Search Console con 31 horas de atraso)

| | 7 días anteriores | Últimos 7 días |
|---|---|---|
| Clics | 8 | **0** |
| Impresiones | 1.180 | **242** |
| Posición media | 12,8 | **59,4** |

Ojo con la comparación: los 7 días anteriores arrancan el 23/09, así que sus dos primeros
días son de antes de la caída y se llevan casi todo (los 8 clics y ~1.000 impresiones).

- **No es una desindexación, es una degradación.** El sitio sigue apareciendo, pero la
  posición media pasó de ~13 a ~59: de la primera página a la sexta. Encaja con un ajuste
  algorítmico de todo el sitio, no con páginas puntuales que se cayeron.
- **Hay una señal chica de movimiento.** En el gráfico de 3 meses las impresiones pasan de
  ~10 por día a fines de septiembre a ~40-50 en los primeros días de octubre. Es poco y puede
  ser ruido, pero va en la dirección correcta.
- **La portada concentra casi todo** (168 de 242 impresiones), con las búsquedas genéricas:
  "proximos lanzamientos videojuegos", "juegos lanzamientos", "ultimos juegos". `/switch`
  pasa de 3 a 15. Las fichas sueltas casi no aparecen.
- **3 meses:** 146 clics y 19.100 impresiones, CTR 0,8%, posición 15,9.
- **Cloudflare, 30 días:** 530 visitas y 990 páginas vistas, casi igual que septiembre (500 y
  1.090): el tráfico que no viene de Google se sostiene. Core Web Vitals: LCP e INP 100% bien,
  pero **CLS tiene una parte en rojo**: era toda de la portada y se arregló el mismo día (ver la tabla de cambios).

### Indexación al 12/10/2026: no son sólo las fichas flacas

Indexadas: **293** (eran 425 el 01/10). Sin indexar: 857. Por motivo, contra el 01/09:

| Motivo | 01/09 | 12/10 |
|---|---|---|
| Página con redirección | 282 | 316 |
| Excluida por `noindex` | 273 | 273 (el noindex del 05/10 todavía no se procesó) |
| **Rastreada: actualmente sin indexar** | 10 | **141** |
| **Descubierta: actualmente sin indexar** | 27 | **117** |
| 404 / error de redirección | 5 / 5 | 5 / 5 |

Cruzando los CSV exportados contra `datos/juegos.js`:

- **Rastreadas sin indexar (141): 101 son fichas con contenido**, nunca flacas — Denshattack
  (88), Kynseed, Teeto, Gothic Classic, Momento —, 25 son flacas ya recuperadas, 3 flacas de
  hoy, 9 la portada con `?plat=` y otras sueltas, 2 URLs `.html` y 1 página de mes. El último
  rastreo de casi todas es de agosto (76) o septiembre (53): **Google no las volvió a visitar,
  las sacó del índice al reevaluar el sitio.**
- **Descubiertas sin indexar (117): nunca rastreadas.** 84 fichas con contenido, 23
  recuperadas y páginas clave: `/octubre-2026`, `/septiembre-2026`, `/ps-plus-octubre-2026`,
  `/game-pass-octubre-2026`, `/recomendados`.

**Lectura:** es una degradación de todo el sitio, no sólo de las fichas flacas. Google bajó la
confianza y la prioridad de rastreo de todo el dominio, que es el patrón de un golpe de calidad
después de un spam update. El `noindex` y las descripciones ayudan, pero no alcanzan solos.
Opciones para decidir el 15/10: pedir indexación a mano de las páginas clave (unas 10 por día),
conseguir enlaces externos (el mensaje a @fran.pw sigue pendiente) y evaluar achicar el índice
a lo que tiene valor propio (crítica, noticias, gameplay, meses y suscripciones).

**Qué separa a las indexadas de las que no (12/10/2026):** la fecha de salida del juego, no el
contenido de la ficha. Fichas no flacas indexadas, por mes de salida: junio 42%, **julio 24%,
agosto 33%**, septiembre 75%, octubre 58%, noviembre en adelante y estimados entre 33% y 73%.
El 82% de las "rastreadas sin indexar" son de juegos salidos en julio o agosto; el 82% de las
indexadas son de juegos de septiembre en adelante. **Las descartadas tienen más crítica que
las indexadas (67% contra 39%)**; descripción, noticias, gameplay y duración están parejos. Las
"descubiertas" son otra cosa: casi todas se cargaron después del 24/09 o son de juegos futuros,
y todavía no se rastrearon.

Lectura: una ficha vale mientras contesta "cuándo sale". Pasados uno o dos meses del
lanzamiento, Google la ve como un resumen de lo que ya tienen Metacritic o IGN y la saca. Para
decidir el 15/10: poner `noindex` a las fichas de juegos salidos hace más de unos 60 días,
o no tocar nada y dejar que Google decida.

Nada de esto cambia el plan: la lectura de verdad es el 15/10, una semana después de que
termine el despliegue del update, y no se espera recuperación antes de semanas o meses.

### Lectura del 15/10/2026: el pedido a mano funciona, el sitio sigue sin volver

**Rendimiento (3 meses):** 146 clics, 19.200 impresiones, CTR 0,8%, posición 16,3. El gráfico
sigue plano desde el 24/09: ningún clic en los últimos 7 días y unas 20-50 impresiones por día,
con un repunte chico el último día que todavía no dice nada. La portada bajó de 179 a 85
impresiones contra la semana anterior; `/noticias` aparece por primera vez, con 39. Las
consultas siguen siendo las genéricas ("juegos lanzamientos", "proximos lanzamientos
videojuegos", "ultimos juegos"), todas en baja, más fichas sueltas con 3 impresiones
(Stupid Never Dies, Hellraiser Revival, Moadra).

**Indexación (CSV del 15/10; el gráfico llega hasta el 11/10):**

| Motivo | 12/10 | 15/10 |
|---|---|---|
| Rastreada: actualmente sin indexar | 141 | **162** (+21, el salto fue el 09/10) |
| Descubierta: actualmente sin indexar | 117 | 114 |

- **Las 10 del día 1 de pedidos a mano (12/10): 9 salieron de las dos listas.** `/octubre-2026`,
  `/ps-plus-octubre-2026`, `/game-pass-octubre-2026`, `/recomendados`, Deep Rock Galactic:
  Survivor, Isles of Sea and Sky, Well Dweller, The Witcher 3 Remastered y Trails in the Sky 2nd
  Chapter. Sólo Order of the Sinking Star sigue en "descubierta". Salir de la lista casi
  seguro quiere decir indexada; para confirmarlo, alcanza con inspeccionar dos o tres.
- **De los días 2 a 4 (pedidos del 13 al 15/10) salieron 3 de 30** (`/febrero-2027`, Kynseed,
  Dispatch), pero esos pedidos son posteriores a casi todos los datos del export: se leen la
  semana que viene.
- **Entraron 33 páginas nuevas a las listas**, 30 de ellas a "rastreada sin indexar". **El
  patrón del 12/10 ya no alcanza para explicarlas:** hay juegos de julio y agosto (The Alters,
  SOMA, Cloverpit), pero también de octubre (Dragon's Dogma 2: Dark Arisen, Ghost of Yōtei
  Complete Edition, Kingdom Hearts Collection) y futuros (He-Man, Whirlight, Marupoyo). 14 de
  las 33 tienen crítica. La degradación sigue alcanzando a todo el sitio, no sólo a los juegos
  ya salidos.

**Lectura:** el pedido a mano es lo único que mostró efecto medible: 9 de 10 en tres días.
Conviene seguir con tandas de 10 por día, priorizando lo que se busca ahora. El `noindex`
para fichas de juegos ya salidos **quedó descartado** (el usuario, 15/10: nunca le gustó), y
los datos de esta semana tampoco lo apoyaban: también se caen fichas de juegos de octubre y
futuros. Siguen pendientes los enlaces externos.

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
