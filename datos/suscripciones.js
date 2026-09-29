// PS PLUS Y GAME PASS DEL MES
//
// Una página por servicio y por mes: /ps-plus-octubre-2026, /game-pass-octubre-2026.
// Existen desde el 29/09/2026 porque "PS Plus octubre 2026" y "Game Pass octubre 2026" son
// búsquedas que se repiten todos los meses, con mucho volumen, y que ya seguimos para la
// rutina mensual. La página tiene que estar COMPLETA: quien la busca quiere la lista
// entera, no los dos juegos que nos interesan. Por eso acá van todos los juegos de cada
// tanda, estén o no en el calendario.
//
// Las noticias de datos/noticias.js siguen existiendo aparte: la noticia cuenta el anuncio
// el día que sale, la página junta el mes entero y se va completando tanda por tanda.
//
// Campos de cada mes:
//   servicio   "psplus" o "gamepass"
//   mes        "AAAA-MM"
//   intro      un párrafo que NOMBRA JUEGOS, igual que en recomendados.js
//   tandas     lista de anuncios del mes, en el orden en que salieron. Cada una:
//     nombre     "JUEGOS MENSUALES", "CATÁLOGO EXTRA Y PREMIUM", "PRIMERA TANDA"…
//     detalle    cuándo y hasta cuándo se juegan, qué plan hace falta
//     anunciado  "AAAA-MM-DD"
//     fuente     URL oficial del anuncio (blog de PlayStation LATAM, Xbox Wire)
//     juegos     lista con:
//       titulo       como lo escribe el servicio
//       id           el id de datos/juegos.js si el juego está en el calendario, si no null.
//                    Si está, la tarjeta enlaza a la ficha y usa su carátula.
//       plataformas  ["PS5", "PS4"]…
//       entra        "AAAA-MM-DD" o null si entra con la tanda
//       texto        una línea propia: qué es y por qué importa. Si entra el día que sale,
//                    decirlo, que es lo que más le sirve al que paga el servicio.
//
// Un mes sin tandas no genera página: una página vacía es peor que ninguna.
// Comentarios dentro del objeto no: el lector de Python no los acepta.

const SUSCRIPCIONES = [
];

if (typeof module !== "undefined" && module.exports) module.exports = SUSCRIPCIONES;
