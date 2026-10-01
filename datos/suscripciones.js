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
//       imagen       carátula vertical, sólo si id es null (con ficha se usa la de la ficha).
//                    Mismo criterio que en juegos.js: primero library_600x900 de Steam.
//                    Sin imagen la tarjeta muestra el recuadro vacío.
//
// Un mes sin tandas no genera página: una página vacía es peor que ninguna.
// Comentarios dentro del objeto no: el lector de Python no los acepta.

const SUSCRIPCIONES = [
  {
    servicio: "psplus",
    mes: "2026-10",
    intro: "Los juegos mensuales de PS Plus de octubre son F1 25, Hunt: Showdown 1896 y Earth Defense Force: World Brothers 2. Se pueden reclamar desde el martes 6 de octubre hasta el lunes 2 de noviembre con cualquier plan, y una vez reclamados quedan en la biblioteca mientras dure la suscripción. Ninguno es un estreno: los tres ya estaban a la venta.",
    tandas: [
      {
        nombre: "JUEGOS MENSUALES",
        detalle: "Del martes 6 de octubre al lunes 2 de noviembre, con cualquier plan de PS Plus: Essential, Extra o Deluxe. Sony avisa que la lista puede cambiar según la región.",
        anunciado: "2026-09-30",
        fuente: "https://blog.latam.playstation.com/2026/09/30/juegos-mensuales-en-playstation-plus-de-octubre-f1-25-hunt-showdown-1896-earth-defense-force-world-brothers-2/",
        juegos: [
          {
            titulo: "F1 25",
            id: null,
            plataformas: ["PS5"],
            entra: null,
            texto: "El juego oficial de la temporada 2025 de Fórmula 1. Tiene modo carrera y My Team 2.0, donde se maneja una escudería como dueño, y en el online suma F1 World, con carreras en grupo contra pilotos de la máquina.",
            imagen: "https://image.api.playstation.com/vulcan/ap/rnd/202602/2009/ffb302a93b80b00487c680187bc959557d32fbaa39e51238.png"
          },
          {
            titulo: "Hunt: Showdown 1896",
            id: null,
            plataformas: ["PS5"],
            entra: null,
            texto: "Un shooter de extracción: se rastrea a un jefe monstruoso, se lo mata y hay que escapar con la recompensa mientras otros cazadores intentan quedársela. Se juega solo o en equipos de hasta tres.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/594650/library_600x900.jpg"
          },
          {
            titulo: "Earth Defense Force: World Brothers 2",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "La versión en bloques de Earth Defense Force: se arma un equipo de cuatro soldados de toda la saga y se pelea contra enemigos gigantes hechos de vóxeles. Tiene cooperativo online para cuatro y pantalla dividida para dos.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2370170/library_600x900.jpg"
          }
        ]
      }
    ]
  }
];

if (typeof module !== "undefined" && module.exports) module.exports = SUSCRIPCIONES;
