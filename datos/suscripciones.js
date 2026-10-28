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
    mes: "2026-11",
    intro: "Los juegos mensuales de PS Plus de noviembre son Dead Island 2, Tomb Raider IV – VI Remastered y Monster Train 2, para reclamar del martes 3 al lunes 30 de noviembre con cualquier plan.",
    tandas: [
      {
        nombre: "JUEGOS MENSUALES",
        detalle: "Del martes 3 al lunes 30 de noviembre, con cualquier plan de PS Plus: Essential, Extra o Deluxe. Los de octubre se pueden reclamar hasta el lunes 2.",
        anunciado: "2026-10-28",
        fuente: "https://blog.latam.playstation.com/2026/10/28/juegos-mensuales-en-playstation-plus-de-noviembre-dead-island-2-tomb-raider-iv-vi-remastered-monster-train-2/",
        juegos: [
          {
            titulo: "Dead Island 2",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "Un RPG de acción con zombis en Los Ángeles, convertida en HELL-A. Se recorren lugares famosos de la ciudad, se hacen misiones para sobrevivientes excéntricos y se pelea cuerpo a cuerpo con armas improvisadas. Se juega solo o en cooperativo online para tres.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/934700/library_600x900_2x.jpg"
          },
          {
            titulo: "Tomb Raider IV – VI Remastered",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "La trilogía oscura de Lara Croft remasterizada: The Last Revelation, Chronicles y The Angel of Darkness. Se puede pasar en cualquier momento de los gráficos nuevos a los modelos poligonales originales.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2525380/library_600x900_2x.jpg"
          },
          {
            titulo: "Monster Train 2",
            id: null,
            plataformas: ["PS5"],
            entra: null,
            texto: "Un roguelite de armar mazos para un jugador: clanes de ángeles y demonios aliados viajan en tren por el Infierno, el Cielo y el Abismo para derrotar a los Titanes. Hay cinco clanes nuevos y tres niveles verticales para defender.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2742830/31030af53f318f6a06566ba3bcb8723b006fd45f/library_600x900_2x.jpg"
          }
        ]
      }
    ]
  },
  {
    servicio: "psplus",
    mes: "2026-10",
    intro: "Los juegos mensuales de PS Plus de octubre son F1 25, Hunt: Showdown 1896 y Earth Defense Force: World Brothers 2, para reclamar del martes 6 de octubre al lunes 2 de noviembre con cualquier plan. El catálogo de Extra y Deluxe suma desde el martes 20 Mafia: The Old Country, Horizon Forbidden West, Tales of Arise con Beyond the Dawn y Mycopunk, que entra el mismo día que sale en PS5. Deluxe agrega Dino Crisis 2 y RollerCoaster Tycoon 3.",
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
      },
      {
        nombre: "CATÁLOGO EXTRA Y DELUXE",
        detalle: "Desde el martes 20 de octubre, con PS Plus Extra o Deluxe; los dos últimos son sólo para Deluxe. Ese día Deluxe suma además pruebas por tiempo limitado de Resonance: A Plague Tale Legacy y Mortal Shell II. Sony avisa que la lista puede cambiar según la región.",
        anunciado: "2026-10-14",
        fuente: "https://blog.latam.playstation.com/2026/10/14/catalogo-de-juegos-de-playstation-plus-para-octubre-mafia-el-viejo-continente-horizon-forbidden-west-mycopunk-y-mucho-mas/",
        juegos: [
          {
            titulo: "Mafia: el viejo continente",
            id: null,
            plataformas: ["PS5"],
            entra: null,
            texto: "La precuela de la saga Mafia (Mafia: The Old Country), en la Sicilia de 1900: Enzo Fava pelea por hacerse un lugar en una familia mafiosa, en una aventura de acción en tercera persona muy apoyada en la historia.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1941540/library_600x900.jpg"
          },
          {
            titulo: "Horizon Forbidden West",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "La segunda aventura de Aloy, en el Oeste Prohibido: un mundo abierto posapocalíptico con máquinas más grandes, tribus nuevas y un enemigo que parece invencible.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2420110/library_600x900.jpg"
          },
          {
            titulo: "Mycopunk",
            id: "mycopunk",
            plataformas: ["PS5"],
            entra: null,
            texto: "Entra el día que sale: el 20 deja el acceso anticipado en PC y debuta en PS5. Un shooter cooperativo para cuatro contra una plaga de hongos alienígenas, con cientos de mejoras para las armas."
          },
          {
            titulo: "Poppy Playtime: Capítulo 2",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "La segunda parte del terror en la fábrica de juguetes Playtime Co.: más abajo, con puzles, una mano extensible para engancharse y colgarse, y juguetes que persiguen.",
            imagen: "https://image.api.playstation.com/vulcan/ap/rnd/202408/2820/a308e999cc0872aac44aa6e95715a5ecc2b0974fc9b7e001.png"
          },
          {
            titulo: "The Midnight Walk",
            id: null,
            plataformas: ["PS5"],
            entra: null,
            texto: "Una aventura de fantasía oscura hecha con arcilla real y animación cuadro a cuadro, de los creadores de Lost in Random. Se acompaña a Potboy, una criatura con forma de farol, a lo largo de cinco historias. También se juega con PS VR2.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2863640/library_600x900.jpg"
          },
          {
            titulo: "Tales of Arise – Beyond the Dawn Edition",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "El JRPG de la saga Tales con la expansión Beyond the Dawn incluida. Dos personas de mundos enfrentados se unen contra Rena, que gobierna Dahna desde hace 300 años.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/740130/library_600x900.jpg"
          },
          {
            titulo: "Monster Energy Supercross 25 – The Official Video Game",
            id: null,
            plataformas: ["PS5"],
            entra: null,
            texto: "El juego oficial del supercross, con pistas que reproducen las del campeonato, los pilotos de la temporada y un modo carrera con rivalidades.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2581370/library_600x900.jpg"
          },
          {
            titulo: "Dino Crisis 2",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "Sólo Deluxe. Después de un accidente temporal que hace desaparecer un centro de investigación, Regina y Dylan pelean contra más de diez especies de dinosaurios entre junglas, cavernas y lagos del Cretácico.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/4249140/54e18b7c8196fc17aac75dfce6a7d0caca8c1303/library_capsule_2x.jpg"
          },
          {
            titulo: "RollerCoaster Tycoon 3 Complete Edition",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "Sólo Deluxe. Se diseña y administra un parque de diversiones: montañas rusas, tiendas, personal y finanzas en decenas de escenarios, o un modo libre sin preocuparse por la plata.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1368820/library_600x900.jpg"
          }
        ]
      }
    ]
  },
  {
    servicio: "gamepass",
    mes: "2026-10",
    intro: "Lo más fuerte de Game Pass en octubre son los estrenos del primer día: Gears of War: E-Day el 6, Echo Weaver, Forever Ago y Neon Abyss 2 el 8, Valor Mortis y Deep Dish Dungeon el 13, Bluey's Happy Snaps y Chained Beasts el 15, The Séance of Blake Manor el 27, Mouthwashing y Terrible Lizards el 29, y Pit of Goblin el 3 de noviembre. Además entran Battlefield 6 el 13 y Final Fantasy VII Remake Intergrade el 29. El 15 se fueron Clair Obscur: Expedition 33 y A Plague Tale: Requiem, entre otros, y el 31 se van Grim Fandango Remastered, Deep Rock Galactic y Lego Star Wars: The Skywalker Saga.",
    tandas: [
      {
        nombre: "ANUNCIADOS EN SEPTIEMBRE",
        detalle: "De la tanda que Xbox anunció el 15 de septiembre, estos dos entran en octubre.",
        anunciado: "2026-09-15",
        fuente: "https://news.xbox.com/en-us/2026/09/15/xbox-game-pass-september-2026-wave-2/",
        juegos: [
          {
            titulo: "Keeper",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-10-02",
            texto: "Ya estaba en Ultimate y PC Game Pass, y desde el 2 de octubre también se juega con Premium. La aventura de Double Fine en la que un faro olvidado despierta y recorre una isla junto a un ave marina, una historia contada sin palabras.",
            imagen: "https://store-images.s-microsoft.com/image/apps.44400.13566978592979529.a309a78d-6446-4646-b4cf-5f86cff39735.4294039d-21f3-4d7d-9443-6cda909325bb?w=600&h=900&format=jpg"
          },
          {
            titulo: "Gears of War: E-Day",
            id: "gears-of-war-e-day",
            plataformas: ["XBOX"],
            entra: "2026-10-06",
            texto: "Entra el día de su estreno, en Ultimate y PC Game Pass. La precuela de la saga: Marcus Fenix y Dom Santiago en el Día de la Emergencia, catorce años antes del primer Gears."
          }
        ]
      },
      {
        nombre: "PRIMERA TANDA DE OCTUBRE",
        detalle: "Anunciada el 7 de octubre. Salvo que se aclare otra cosa, cada juego entra a Ultimate y PC Game Pass. El 16 llega también Beyond These Stars, sólo para PC Game Pass. El 15 se van A Plague Tale: Requiem, Clair Obscur: Expedition 33, Crime Scene Cleaner, Donut County, Evil West, Pacific Drive, Superball y The Casting of Frank Stone.",
        anunciado: "2026-10-07",
        fuente: "https://news.xbox.com/en-us/2026/10/07/xbox-game-pass-october-2026-wave-1/",
        juegos: [
          {
            titulo: "Echo Weaver",
            id: "echo-weaver",
            plataformas: ["XBOX"],
            entra: "2026-10-08",
            texto: "Entra el día que sale. Un metroidvania de bucle temporal donde lo que se junta no son mejoras sino información para romper el ciclo."
          },
          {
            titulo: "Forever Ago",
            id: "forever-ago",
            plataformas: ["XBOX"],
            entra: "2026-10-08",
            texto: "Entra el día que sale. Un viaje en ruta para un jugador: Alfred va hacia el norte buscando redención y guarda recuerdos con su cámara instantánea."
          },
          {
            titulo: "Neon Abyss 2",
            id: "neon-abyss-2",
            plataformas: ["XBOX"],
            entra: "2026-10-08",
            texto: "Entra el día que deja el acceso anticipado y llega a consolas, también en Premium. Roguelike de acción en 2D con objetos que se combinan entre sí y cooperativo para cuatro."
          },
          {
            titulo: "Battlefield 6",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-10-13",
            texto: "El Battlefield de 2025: guerra a gran escala, combate cerrado y destrucción del escenario. Ultimate trae EA Play incluido, con recompensas propias dentro del juego.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2807960/library_600x900.jpg"
          },
          {
            titulo: "Deep Dish Dungeon",
            id: "deep-dish-dungeon",
            plataformas: ["XBOX"],
            entra: "2026-10-13",
            texto: "Entra el día que sale. Exploración de una mazmorra llena de puzles, solo o en cooperativo online, donde lo que se cocina es clave para seguir bajando."
          },
          {
            titulo: "Valor Mortis",
            id: "valor-mortis",
            plataformas: ["XBOX"],
            entra: "2026-10-13",
            texto: "Entra el día que sale. Acción en primera persona a la manera de los Souls, de los creadores de Ghostrunner, con un soldado de Napoleón que vuelve de la muerte."
          },
          {
            titulo: "Bluey's Happy Snaps",
            id: "blueys-happy-snaps",
            plataformas: ["XBOX"],
            entra: "2026-10-15",
            texto: "Entra el día que sale. Un juego de sacar fotos con Bluey y Bingo por lugares de la serie, pensado para chicos y para jugar de a dos."
          },
          {
            titulo: "Chained Beasts",
            id: "chained-beasts",
            plataformas: ["XBOX"],
            entra: "2026-10-15",
            texto: "Entra el día que sale. Un roguelite de gladiadores para hasta cuatro jugadores que pelean encadenados entre sí."
          }
        ]
      },
      {
        nombre: "SEGUNDA TANDA DE OCTUBRE",
        detalle: "Anunciada el 20 de octubre. Salvo que se aclare otra cosa, cada juego entra a Ultimate, Premium y PC Game Pass. El 31 se van Day of the Tentacle Remastered, Full Throttle Remastered, Grim Fandango Remastered, Deep Rock Galactic, Lego Star Wars: The Skywalker Saga, Wartales y otros; el 10 de noviembre, Football Manager 26.",
        anunciado: "2026-10-20",
        fuente: "https://news.xbox.com/en-us/2026/10/20/xbox-game-pass-october-2026-wave-2/",
        juegos: [
          {
            titulo: "Sandustry",
            id: null,
            plataformas: ["PC"],
            entra: "2026-10-21",
            texto: "Sólo PC, en acceso anticipado: ya estaba en Ultimate y PC Game Pass y ahora suma Premium. Un juego de fábricas en mundos de arena totalmente destructibles.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2764460/8836172e9ba1cac149cad8aaa8c43d1e7cecb078/library_capsule_2x.jpg"
          },
          {
            titulo: "Dodo Duckie",
            id: "dodo-duckie",
            plataformas: ["XBOX"],
            entra: "2026-10-22",
            texto: "Un plataformas de puzles en el que un pato cambia entre 2D y 3D para rescatar a sus amigas gallinas. Salió en julio y entra a Ultimate, Premium y PC Game Pass."
          },
          {
            titulo: "Scramble Knights Online",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-10-26",
            texto: "Entra el día que sale, en acceso anticipado: un RPG de acción online para jugar con amigos en el reino de Terracott.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2379350/5ae55ff27f6174a7beb3130e42a66fc247eb3754/library_capsule_2x.jpg"
          },
          {
            titulo: "The Séance of Blake Manor",
            id: "the-seance-of-blake-manor",
            plataformas: ["XBOX"],
            entra: "2026-10-27",
            texto: "Entra el día que sale. Un misterio sobrenatural en la Irlanda de 1897: una huésped desaparecida en una mansión donde se prepara una sesión de espiritismo."
          },
          {
            titulo: "Final Fantasy VII Remake Intergrade",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-10-29",
            texto: "La primera parte del remake de Final Fantasy VII, hasta la huida de Midgar, con combate que mezcla acción en tiempo real y comandos. Está en Xbox desde enero.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1462040/library_600x900_2x.jpg"
          },
          {
            titulo: "Mouthwashing",
            id: "mouthwashing",
            plataformas: ["XBOX"],
            entra: "2026-10-29",
            texto: "Entra el día que llega a consolas. Terror psicológico en un carguero espacial varado, con una tripulación de cinco condenada por su capitán."
          },
          {
            titulo: "Plants vs. Zombies: Replanted",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-10-29",
            texto: "Sólo Ultimate y PC Game Pass, a través de EA Play. La versión en alta definición del clásico de plantas contra zombis, con niveles nuevos.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3654560/4239904dc76eae613171cd3dec950b9e0abfbd5f/library_600x900_2x.jpg"
          },
          {
            titulo: "Terrible Lizards",
            id: "terrible-lizards",
            plataformas: ["XBOX"],
            entra: "2026-10-29",
            texto: "Entra el día que sale, sólo en Ultimate y PC Game Pass. Terror con parkour en un parque de dinosaurios abandonado de la Ruta 66."
          },
          {
            titulo: "Pit of Goblin",
            id: "pit-of-goblin",
            plataformas: ["XBOX"],
            entra: "2026-11-03",
            texto: "Entra el día que llega a Xbox. Un cooperativo de terror para cuatro goblins que bajan a mazmorras a buscar comida para su Rey Reina."
          }
        ]
      }
    ]
  }
];

if (typeof module !== "undefined" && module.exports) module.exports = SUSCRIPCIONES;
