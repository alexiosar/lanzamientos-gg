// NOTICIAS PROPIAS DEL SITIO
//
// Acá van las noticias que NO cuelgan de un lanzamiento concreto: los juegos
// mensuales de PS Plus y Game Pass, retrasos, anuncios de un Direct o un State
// of Play, cierres de estudios.
//
// Las noticias de UN juego no van acá: van en su entrada de datos/juegos.js,
// en el campo `noticias`. La página /noticias mezcla las dos fuentes y las
// ordena por fecha, así que no hay que duplicar nada.
//
// Campos:
//   id         identificador único, en minúsculas y con guiones (va en la URL)
//   fecha      "AAAA-MM-DD" — la del anuncio, no la del día que se carga
//   categoria  SUSCRIPCIONES | RETRASOS | ANUNCIOS | EVENTOS
//   titulo     en mayúsculas, como el resto del sitio
//   texto      uno o dos párrafos, en español rioplatense
//   fuente     URL de donde salió el dato: siempre la oficial si existe
//   juegos     ids de datos/juegos.js que menciona (opcional); se enlazan solos
//
// Las de arriba son las más nuevas, pero el orden real lo pone la fecha.

const NOTICIAS = [
  {
    id: "direct-fire-emblem-agosto-2026",
    fecha: "2026-08-04",
    categoria: "EVENTOS",
    titulo: "UN DIRECT ENTERO PARA FIRE EMBLEM: FORTUNE'S WEAVE",
    texto: "Nintendo le dedicó veinte minutos a un solo juego. Se supo que la historia arranca con cuatro héroes compitiendo en los Juegos Heroicos de Dagsion, pero que el protagonista real es un héroe sin nombre que Sothis invoca cinco años en el futuro, con el mundo ya destruido, y que viaja al pasado para juntarlos. Se elige a uno de los cuatro y se puede cambiar de personaje sobre la marcha para ver las historias en paralelo. El combate es el de Three Houses, con una vuelta nueva: las Blaze Arts, ataques especiales que se pagan con vida propia en lugar de con durabilidad del arma. Sale el 17 de septiembre, solo en Switch 2.",
    fuente: "https://www.nintendo.com/us/nintendo-direct/8-4-2026/",
    juegos: ["fire-emblem-fortunes-weave"]
  },
  {
    id: "game-pass-agosto-2026",
    fecha: "2026-08-04",
    categoria: "SUSCRIPCIONES",
    titulo: "LO QUE ENTRA A GAME PASS EN AGOSTO",
    texto: "Diez juegos entre el 4 y el 18 de agosto. Tres ya están en el calendario y llegan al servicio el mismo día que salen: Beast of Reincarnation el 4, Monsters are Coming! el 6 y Grounded 2 el 11, este último en formato Game Preview. Aparte, la beta de Gears of War: E-Day está disponible desde el 6 para Ultimate y PC Game Pass. Del otro lado, el 15 se van cuatro: Atlas Fallen, Aliens: Fireteam Elite, Firewatch y Menace.",
    fuente: "https://news.xbox.com/es-mx/",
    juegos: ["beast-of-reincarnation", "monsters-are-coming", "grounded-2", "gears-of-war-e-day"]
  },
  {
    id: "ps-plus-agosto-2026",
    fecha: "2026-07-28",
    categoria: "SUSCRIPCIONES",
    titulo: "BIG WALK ENTRA A PS PLUS EL MISMO DÍA QUE SALE",
    texto: "Los tres juegos mensuales de PlayStation Plus de agosto son Dying Light 2 Stay Human: Reloaded Edition, Big Walk y Signalis. Big Walk es el único de los tres que se estrena este mes: sale el 4 de agosto y entra al servicio ese mismo día, así que quien tenga la suscripción no lo paga aparte. Los otros dos son juegos que ya existían y se suman al catálogo.",
    fuente: "https://blog.latam.playstation.com/",
    juegos: ["big-walk"]
  }
];

if (typeof module !== "undefined" && module.exports) module.exports = NOTICIAS;
