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
//                   OJO: el recuadro de la tarjeta es 2:3 vertical desde el 28/08/2026, y
//                   una miniatura de YouTube es 16:9. Se recorta a la franja del medio y
//                   suele quedar ilegible. Antes de usarla, mirar cómo queda; si no se
//                   entiende, es mejor dejar la noticia sin imagen.
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
    id: "nintendo-direct-9-septiembre-2026",
    fecha: "2026-09-09",
    categoria: "EVENTOS",
    titulo: "EL DIRECT LLENÓ OCTUBRE, NOVIEMBRE Y DICIEMBRE DE SWITCH 2",
    texto: "Nintendo dedicó el Direct a lo que queda del año y a 2027, y lo del año se puede resumir en una frase: la Switch 2 se lleva casi todo lo grande que faltaba. El 16 de octubre llegan los tres rehechos de Resident Evil —el 2, el 3 y el 4—, el 5 de noviembre Marvel's Guardians of the Galaxy en su Encore Edition, el 12 Pikmin 4 con un modo nuevo y con órdenes por voz para Oatchi, y el 4 de diciembre Monster Hunter Wilds. El profesor Layton y el Nuevo Mundo a vapor, que venía sin día, quedó para el 10 de diciembre.\n\nLo de 2027 fue más largo todavía: Metroid Ravenous el 28 de enero, Danganronpa 2×2 el 14, Tomb Raider: Legacy of Atlantis el 12 de febrero, Persona 4 Revival el 20 de mayo y Kirby and the World Beyond en primavera boreal, además de una versión de Persona 6 para la consola. Esas fechas todavía no entran al calendario, que hoy llega hasta marzo de 2027.",
    fuente: "https://www.nintendo.com/us/nintendo-direct/",
    juegos: ["resident-evil-4-switch-2", "monster-hunter-wilds-switch-2", "pikmin-4-switch-2", "professor-layton-nuevo-mundo-a-vapor"]
  },
  {
    id: "zelda-40-aniversario-direct-2026",
    fecha: "2026-09-08",
    categoria: "EVENTOS",
    titulo: "OCARINA OF TIME VUELVE EL 5 DE NOVIEMBRE",
    texto: "El Direct por los 40 años de The Legend of Zelda dejó tres anuncios. El grande es el remake de Ocarina of Time para Switch 2, que ya tiene fecha: 5 de noviembre. Eiji Aonuma lo mostró jugado durante un cuarto de hora y se ve que es un remake y no un port — gráficos y banda sonora rehechos, cinemáticas dobladas al español, diálogos que no estaban en el original, una habilidad para correr y una cronología para repasar por dónde va la aventura.\n\nEse mismo día sale una Nintendo Switch 2 con diseño de la edición 40.º aniversario de la saga. Y la película en imagen real, que llega en 2027, se va a llamar simplemente The Legend of Zelda. Mañana hay un segundo Direct, el general, de unos 45 minutos.",
    fuente: "https://www.nintendo.com/es-es/Juegos/Juegos-de-Nintendo-Switch-2/The-Legend-of-Zelda-Ocarina-of-Time-3115664.html",
    juegos: ["the-legend-of-zelda-ocarina-of-time-switch-2"]
  },
  {
    id: "nintendo-directs-8-y-9-septiembre-2026",
    fecha: "2026-09-04",
    categoria: "EVENTOS",
    titulo: "NINTENDO HACE DOS DIRECTS SEGUIDOS: EL 8 Y EL 9",
    texto: "El martes 8 va un Direct dedicado a los 40 años de The Legend of Zelda, de unos 30 minutos, y el miércoles 9 un Direct general de unos 45. Los dos a las 11 de la mañana de Argentina. Después del segundo hay un Nintendo Treehouse con jugabilidad de lo que hayan mostrado. De estas transmisiones suelen salir las fechas de los juegos de Switch y Switch 2 que todavía se anuncian por trimestre y no por día.",
    fuente: "https://www.nintendo.com/us/nintendo-direct/"
  },

  {
    id: "state-of-play-resumen-3-septiembre-2026",
    fecha: "2026-09-03",
    categoria: "EVENTOS",
    titulo: "LOS DOS STATE OF PLAY DEJARON MÁS DE 30 JUEGOS, Y CASI TODOS PARA 2027",
    texto: "Fueron dos transmisiones seguidas y el saldo es raro: de los treinta y pico de juegos que mostraron, casi ninguno sale este año. Final Fantasy VII Revelation, que cierra la trilogía, va al 8 de abril de 2027; Until Dawn 2 y Fate/EXTRA Record al 28 de enero de 2027; Gundam Rogue Orbit al 5 de marzo; Dragon Ball Xenoverse 3 y una expansión de Digimon Story: Time Stranger quedaron en «2027» sin día. Lo que sí toca lo que viene: Dragon Quest Monsters: The Withered World confirmó el 3 de diciembre, Final Fantasy Resonance ratificó el 22 de octubre y soltó el primer capítulo como demo —con Sephiroth anunciado en el elenco—, y la Edición Completa de Ghost of Yōtei llega el 1 de octubre con los dos modos nuevos adentro, Los más buscados y Ecos de Sekigahara. Las tres fechas que ya estaban anunciadas se ratificaron sin cambios.",
    fuente: "https://blog.latam.playstation.com/2026/09/03/state-of-play-y-state-of-play-japan-todos-los-anuncios-y-trailers/",
    juegos: ["dragon-quest-monsters-the-withered-world", "final-fantasy-resonance", "ghost-of-yotei-complete-edition", "digimon-story-time-stranger"]
  },

  {
    id: "no-rest-for-the-wicked-retraso-marzo-2027",
    fecha: "2026-09-02",
    categoria: "RETRASOS",
    titulo: "NO REST FOR THE WICKED SE VA A MARZO DE 2027",
    texto: "Moon Studios movió la versión 1.0 de octubre de 2026 a marzo de 2027, y el anuncio lo hicieron ellos mismos en Steam. El motivo que dan es que son un equipo chico y que el juego todavía no está donde lo quieren: los meses extra van a rendimiento, al sistema de clases y a pulir el conjunto. De paso prometen más betas cerradas y abiertas en el camino.",
    fuente: "https://store.steampowered.com/news/app/1371980",
    juegos: ["no-rest-for-the-wicked"]
  },

  {
    id: "game-pass-primera-quincena-septiembre-2026",
    fecha: "2026-09-01",
    categoria: "SUSCRIPCIONES",
    titulo: "GAME PASS ARRANCA SEPTIEMBRE CON SPEEDRUNNERS 2 EL DÍA UNO",
    texto: "Microsoft anunció la primera tanda de septiembre y varios entran el mismo día que salen: SpeedRunners 2: King of Speed el 3 y The Royal Writ el 10. Shelldiver ya está desde el 1, que es también el día que llegó a Xbox. El 15 se suma RuneScape: Dragonwilds y, el mismo día, TCG Card Shop Simulator abandona el acceso anticipado y estrena su 1.0 adentro del servicio. Completan la tanda Call of Duty: Black Ops Cold War, Virtua Fighter 5 R.E.V.O. World Stage —que no es un estreno: está en Xbox desde octubre de 2025 y ahora entra al catálogo— y Dice a Million, que en Xbox es solo para PC. Ojo con Aniimo el 16: no entra al servicio: lo que da es un paquete de recompensas para quien esté suscrito.",
    fuente: "https://news.xbox.com/en-us/2026/09/01/xbox-game-pass-update-september-wave-1/",
    juegos: ["speedrunners-2-king-of-speed", "the-royal-writ", "shelldiver", "runescape-dragonwilds", "tcg-card-shop-simulator", "aniimo"]
  },

  {
    id: "konami-press-start-3-septiembre-2026",
    fecha: "2026-09-01",
    categoria: "EVENTOS",
    titulo: "KONAMI TAMBIÉN TRANSMITE EL 3, CON CASTLEVANIA Y SILENT HILL",
    texto: "El mismo día que los dos State of Play, Konami hace su propio Press Start. Muestra tres juegos: Castlevania: Belmont's Curse, que sale el 15 de octubre; Silent Hill: Townfall, que sale el 24 de septiembre; y Rev. NOiR. La hora todavía no está clara porque el anuncio no aclara la zona horaria, y el enlace de abajo tiene el detalle. Jueves cargado: si va a moverse alguna fecha del último trimestre, es probable que se mueva ese día.",
    fuente: "https://www.gematsu.com/2026/08/konami-press-start-live-stream-set-for-september-3-featuring-castlevania-belmonts-curse-silent-hill-townfall-and-rev-noir",
    juegos: ["castlevania-belmonts-curse", "silent-hill-townfall"]
  },

  {
    id: "state-of-play-3-septiembre-2026",
    fecha: "2026-08-31",
    categoria: "EVENTOS",
    titulo: "DOS STATE OF PLAY SEGUIDOS EL 3 DE SEPTIEMBRE",
    texto: "Sony anunció dos transmisiones al hilo para el jueves 3, desde las 10 de la mañana de Argentina, por YouTube y Twitch. Primero el State of Play con novedades de PlayStation Studios y estudios asociados, que cierra con un vistazo largo a Final Fantasy VII Revelation, lo nuevo de Square Enix. Después el State of Play Japón, otra vez con Yuki Kaji de presentador, dedicado a juegos de estudios de Japón y Asia. Conviene tenerlo en el radar: de estas transmisiones suelen salir las fechas de lo que viene. Final Fantasy VII Revelation, por ahora, apunta a 2027.",
    fuente: "https://blog.latam.playstation.com/2026/08/31/state-of-play-y-state-of-play-japon-regresan-el-3-de-septiembre/",
    imagen: "https://images.igdb.com/igdb/image/upload/t_cover_big_2x/cocbgb.jpg",
    juegos: []
  },

  {
    id: "ps-plus-mensuales-septiembre-2026",
    fecha: "2026-08-26",
    categoria: "SUSCRIPCIONES",
    titulo: "LOS MENSUALES DE PS PLUS DE SEPTIEMBRE: SNIPER ELITE RESISTANCE Y TRES MÁS",
    texto: "Sony anunció los cuatro juegos mensuales de septiembre: Sniper Elite: Resistance en PS5 y PS4, MLB The Show 26 en PS5, Wobbly Life y Chained Echoes. Se pueden reclamar desde el martes 1 de septiembre hasta el lunes 5 de octubre, y una vez reclamados quedan mientras dure la suscripción. Ojo con la diferencia respecto del catálogo Extra y Deluxe, que es otra cosa: estos son los mensuales. Ninguno de los cuatro es un estreno: los cuatro ya estaban a la venta. Ojo con Wobbly Life, que se presta a confusión: la versión que entra a PS Plus es la de PlayStation, no la de Switch 2 que salió el 20 de agosto.",
    fuente: "https://blog.latam.playstation.com/2026/08/26/juegos-mensuales-en-playstation-plus-de-septiembre-sniper-elite-resistence-mlb-the-show-26-wobbly-life-chained-echoes/",
    juegos: ["wobbly-life"]
  },

  {
    id: "terranigma-vuelve-2027",
    fecha: "2026-08-25",
    categoria: "ANUNCIOS",
    titulo: "TERRANIGMA VUELVE EN 2027, TREINTA AÑOS DESPUÉS",
    texto: "Clear River Games, junto con Square Enix, anunció el regreso del RPG de acción de 1995. Sale en 2027 para PS5, PS4, Xbox, Switch 2, Switch y PC. Es uno de los clásicos de Super Nintendo que nunca llegó a América, y volver a ponerlo en circulación es noticia por sí solo.",
    fuente: "https://www.gematsu.com/",
    juegos: []
  },
  {
    id: "duskbloods-sin-fecha-2026",
    fecha: "2026-08-21",
    categoria: "ANUNCIOS",
    titulo: "NINTENDO DESMIENTE LA FECHA QUE CIRCULABA DE THE DUSKBLOODS",
    texto: "Un medio que probó The Duskbloods publicó una fecha de lanzamiento y Nintendo salió a decir que es inexacta: lo nuevo de FromSoftware para Switch 2 todavía no tiene día confirmado, y hasta que Nintendo lo anuncie no hay fecha que valga. La beta, esa sí, ya está en marcha para los seleccionados.",
    fuente: "https://vandal.elespanol.com/",
    juegos: []
  },
  {
    id: "game-pass-segunda-quincena-agosto-2026",
    fecha: "2026-08-18",
    categoria: "SUSCRIPCIONES",
    titulo: "GAME PASS CIERRA AGOSTO CON TRES ESTRENOS EL DÍA UNO",
    texto: "Microsoft anunció la segunda tanda del mes. Tres entran al servicio el mismo día que salen: Vapor World: Over the Mind, hoy, aunque en formato Game Preview y no como versión terminada; Blood Dungeon el 25, lo nuevo de los creadores de Nidhogg; y Resonance: A Plague Tale Legacy el 27. Starsand Island también se suma, el 20, pero salió el 18, así que no es estreno en el servicio. El resto de la tanda son juegos que ya existían.",
    fuente: "https://news.xbox.com/en-us/2026/08/18/xbox-game-pass-august-2026-wave-2/",
    juegos: ["vapor-world-over-the-mind", "blood-dungeon", "resonance-a-plague-tale-legacy", "starsand-island"]
  },
  {
    id: "xbox-anuncio-gamescom-2026",
    fecha: "2026-08-15",
    categoria: "RUMORES",
    titulo: "SEGÚN NATETHEHATE, XBOX GUARDA UN ANUNCIO PARA LA GAMESCOM",
    texto: "El filtrador NateTheHate dijo que Xbox tendría listo «un anuncio genial» para la Gamescom, que va del 26 al 30 de agosto. No dio nombres: sólo que sería un juego nuevo de una licencia que ya es de Microsoft, que no es The Elder Scrolls VI ni un remaster de Fallout, que no es un shooter, y que lo estaría haciendo un estudio que hoy no le pertenece. Él mismo aclaró que todavía está tratando de confirmar si el anuncio llega a la feria. Lo confirmado por Xbox es otra cosa: 25 juegos en el evento, entre ellos Gears of War: E-Day, y dos emisiones propias.",
    fuente: "https://vandal.elespanol.com/noticia/1350792356/xbox-tendria-preparado-un-anuncio-genial-de-una-de-sus-licencias-para-la-gamescom-segun-una-filtracion/",
    juegos: []
  },
  {
    id: "marvel-tokon-rocket-datamining",
    fecha: "2026-08-18",
    categoria: "RUMORES",
    titulo: "UN DATAMINING APUNTA A ROCKET RACCOON COMO DLC DE MARVEL TŌKON",
    texto: "El usuario Neoxon publicó en ResetEra capturas del código de la versión de PC de Marvel Tōkon: Fighting Souls. Según ese hallazgo, una línea de diálogo de Kamala Khan trataría a Rocket como «futuro DLC», y aparecerían además trajes «Legacy» y «Classic» para Hulk, Spider-Man, Green Goblin y Doctor Doom, más código de un pase de batalla que el juego hoy no tiene. Arc System Works no confirmó nada de esto, y que algo esté en los archivos no quiere decir que llegue: puede ser contenido descartado o provisional. Lo que sí es oficial es que el juego suma cuatro personajes descargables hasta septiembre de 2027, con Phoenix y Cíclope ya anunciados.",
    fuente: "https://vandal.elespanol.com/noticia/1350792352/marvel-tokon-podria-sumar-a-rocket-raccoon-un-datamining-revela-pase-de-batalla-y-nuevos-trajes/",
    juegos: ["marvel-tokon-fighting-souls"]
  },
  {
    id: "kingdom-hearts-iv-2027",
    fecha: "2026-08-17",
    categoria: "ANUNCIOS",
    titulo: "KINGDOM HEARTS IV SALE A FINES DE 2027",
    texto: "Square Enix puso fecha a Kingdom Hearts IV: finales de 2027. En el mismo anuncio se confirmó una serie de anime original de la saga. La colección de los juegos anteriores, esa sí, sigue en pie para el 8 de octubre.",
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
    texto: "Entran al catálogo de PlayStation Plus Helldivers 2, Kingdom Come: Deliverance 2, Vampire Survivors y Hell is Us, entre otros. Ojo con la diferencia: estos no son los juegos mensuales, que se reclaman y quedan para siempre, sino el catálogo de los planes Extra y Deluxe, que se puede jugar mientras dure la suscripción y mientras el juego siga ahí. Ninguno es un estreno: los cuatro ya estaban a la venta desde antes.",
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
    texto: "Diez juegos entre el 4 y el 18 de agosto. Dos llegan al servicio el mismo día que salen: Beast of Reincarnation el 4 y Monsters are Coming! el 6. Grounded 2 entra el 11 en formato Game Preview, pero sólo en Xbox y PC: su debut en PS5 es otra fecha y no tiene nada que ver con el servicio. Aparte, la beta de Gears of War: E-Day está disponible desde el 6 para Ultimate y PC Game Pass. Del otro lado, el 15 se van cuatro: Atlas Fallen, Aliens: Fireteam Elite, Firewatch y Menace.",
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
