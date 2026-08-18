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
//   categoria  SUSCRIPCIONES | RETRASOS | ANUNCIOS | EVENTOS | RUMORES
//   titulo     en mayúsculas, como el resto del sitio
//   texto      uno o dos párrafos, en español rioplatense
//   fuente     URL de donde salió el dato: siempre la oficial si existe
//   juegos     ids de datos/juegos.js que menciona (opcional); se enlazan solos
//   imagen     URL de una imagen para la tarjeta (opcional). Sólo hace falta cuando la
//              noticia NO cita ningún juego del calendario: si cita alguno, se usa su
//              carátula sola. Qué poner, en este orden:
//                1. La carátula del juego del que trata, aunque no esté en el calendario.
//                   Se saca de Steam igual que las demás, así que es estable y encaja con
//                   el resto del sitio. Para "Netflix cierra el estudio de Oxenfree" va la
//                   de Oxenfree; para el catálogo de PS Plus, la de su juego más fuerte.
//                2. Si es un evento con video (un Direct, un State of Play), la miniatura
//                   de YouTube: https://i.ytimg.com/vi/<id>/hqdefault.jpg
//                3. Si no hay nada de lo anterior, se deja sin imagen. Mejor una tarjeta
//                   sin foto que una foto que no dice nada.
//
// Las de arriba son las más nuevas, pero el orden real lo pone la fecha.
//
// REGLA DE LOS RUMORES (decidida el 18/08/2026)
//
// Un rumor puede ser noticia, pero NUNCA un dato. Jamás modifica `fecha`,
// `plataformas` ni ningún campo de datos/juegos.js: vive solo dentro de la noticia.
//
// El sitio se sostiene en ser exacto — por eso se sacó Creepshow (salía solo en PC),
// se sacó Man of Honor (era DLC) y The Relic se partió en tres entradas. Si un rumor
// se filtrara a una fecha del calendario y saliera mal, pasaríamos a ser el sitio que
// tiene las fechas mal, que es lo único que un calendario no puede permitirse.
//
// Cómo se escribe uno: categoría RUMORES, nombrando siempre quién lo reportó, en
// condicional ("según X, el juego llegaría…") y nunca en presente afirmativo. En la
// página se distingue solo: la etiqueta va con borde punteado.

const NOTICIAS = [
  {
    id: "kingdom-hearts-iv-2027",
    fecha: "2026-08-17",
    categoria: "ANUNCIOS",
    titulo: "KINGDOM HEARTS IV SALE A FINES DE 2027",
    texto: "Square Enix puso fecha a Kingdom Hearts IV: finales de 2027, o sea fuera del alcance de este calendario por ahora. En el mismo anuncio se confirmó una serie de anime original de la saga. La colección de los juegos anteriores, esa sí, sigue en pie para el 8 de octubre.",
    fuente: "https://www.gematsu.com/",
    juegos: ["kingdom-hearts-collection"]
  },
  {
    id: "netflix-cierra-night-school-2026",
    fecha: "2026-08-14",
    categoria: "ANUNCIOS",
    titulo: "NETFLIX CIERRA NIGHT SCHOOL, EL ESTUDIO DE OXENFREE",
    texto: "Netflix cierra Night School Studio, el estudio de Oxenfree, y Moonloot Games. Es otro capítulo del repliegue de la compañía en videojuegos: había comprado Night School en 2021, cuando arrancaba su apuesta por el sector.",
    fuente: "https://www.gematsu.com/",
    imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/388880/library_600x900.jpg",
    juegos: []
  },
  {
    id: "ps-plus-catalogo-agosto-2026",
    fecha: "2026-08-12",
    categoria: "SUSCRIPCIONES",
    titulo: "EL CATÁLOGO DE PS PLUS DE AGOSTO SUMA HELLDIVERS 2",
    texto: "Entran al catálogo de PlayStation Plus Helldivers 2, Kingdom Come: Deliverance 2, Vampire Survivors y Hell is Us, entre otros. Ojo con la diferencia: estos no son los juegos mensuales, que se reclaman y quedan para siempre, sino el catálogo de los planes Extra y Deluxe, que se puede jugar mientras dure la suscripción y mientras el juego siga ahí. Ninguno es un estreno, así que no llevan el distintivo de PS Plus en el calendario.",
    fuente: "https://blog.latam.playstation.com/",
    imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/553850/library_600x900.jpg",
    juegos: []
  },
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
    texto: "Diez juegos entre el 4 y el 18 de agosto. Dos están en el calendario y llegan al servicio el mismo día que salen: Beast of Reincarnation el 4 y Monsters are Coming! el 6. Grounded 2 entra el 11 en formato Game Preview, pero en Xbox y PC: la fecha que figura en el calendario es la de su debut en PS5, que no tiene nada que ver con el servicio. Aparte, la beta de Gears of War: E-Day está disponible desde el 6 para Ultimate y PC Game Pass. Del otro lado, el 15 se van cuatro: Atlas Fallen, Aliens: Fireteam Elite, Firewatch y Menace.",
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
