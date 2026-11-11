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
    intro: "Los juegos mensuales de PS Plus de noviembre son Dead Island 2, Tomb Raider IV – VI Remastered y Monster Train 2, para reclamar del martes 3 al lunes 30 de noviembre con cualquier plan. El catálogo de Extra y Deluxe suma desde el martes 17 Death Stranding 2: On the Beach, Atomfall y Dragon Quest III HD-2D Remake, el 24 Like a Dragon: Pirate Yakuza in Hawaii y MotoGP 26, y Hell Let Loose ya el 11. Deluxe agrega Soul Reaver 2 y Freedom Wars Remastered.",
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
      },
      {
        nombre: "CATÁLOGO EXTRA Y DELUXE",
        detalle: "Desde el martes 17 de noviembre, con PS Plus Extra o Deluxe, salvo los que tienen otra fecha; los dos últimos son sólo para Deluxe. Las fechas del 24 son las que Sony da para Estados Unidos, y avisa que la lista puede cambiar según la región.",
        anunciado: "2026-11-10",
        fuente: "https://blog.latam.playstation.com/2026/11/10/catalogo-de-juegos-de-playstation-plus-para-noviembre-death-stranding-2-on-the-beach-like-a-dragon-pirate-yakuza-in-hawaii-atomfall-dr/",
        juegos: [
          {
            titulo: "Death Stranding 2: On the Beach",
            id: null,
            plataformas: ["PS5"],
            entra: null,
            texto: "El segundo viaje de Sam Porter Bridges, ahora para conectar Australia a la red quiral. Se arma infraestructura y se cargan paquetes entre terremotos, tormentas de arena, incendios y la lluvia que envejece todo lo que toca.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3280350/9b523fd411eeaefe80f238489745325a1cd2317f/library_capsule_2x.jpg"
          },
          {
            titulo: "Like a Dragon: Pirate Yakuza in Hawaii",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: "2026-11-24",
            texto: "Entra el 24. Goro Majima despierta sin memoria en una isla y se hace capitán pirata: peleas en tierra y batallas navales en alta mar, en busca de sus recuerdos y de un tesoro.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3061810/library_600x900_2x.jpg"
          },
          {
            titulo: "Atomfall",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "Acción y supervivencia de Rebellion, los de Sniper Elite, en la zona de cuarentena del norte de Inglaterra, cinco años después del desastre nuclear de Windscale. Se explora libremente entre sectas, búnkeres y agencias del gobierno.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/801800/2b7ed6a84485e94108c4cedd2388040858302242/library_600x900_2x.jpg"
          },
          {
            titulo: "Dragon Quest III HD-2D Remake",
            id: null,
            plataformas: ["PS5"],
            entra: null,
            texto: "El remake del RPG que abre la trilogía de Erdrick, con el estilo de pixel art y escenarios 3D de Octopath Traveler. El hijo del héroe Ortega cumple 16 y sale a terminar la misión de su padre contra Baramos.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2701660/library_600x900_2x.jpg"
          },
          {
            titulo: "Trepang2",
            id: null,
            plataformas: ["PS5"],
            entra: "2026-11-24",
            texto: "Entra el 24. Un shooter en primera persona frenético, con cámara lenta, invisibilidad y patadas: un soldado sin memoria escapa de un laboratorio y se venga de quienes lo encerraron.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1164940/library_600x900_2x.jpg"
          },
          {
            titulo: "MotoGP 26",
            id: null,
            plataformas: ["PS5"],
            entra: "2026-11-24",
            texto: "Entra el 24. El juego oficial del campeonato 2026, con pilotos, equipos y circuitos reales. Por primera vez los resultados de las carreras reales cambian el rendimiento de cada piloto en el juego durante la temporada.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3875050/d1fa1483cd16f54f14060da35ecfe9ce166c3e4e/library_capsule_2x.jpg"
          },
          {
            titulo: "Hell Let Loose",
            id: null,
            plataformas: ["PS5"],
            entra: "2026-11-11",
            texto: "Entra antes que el resto, el 11. Un shooter de la Segunda Guerra Mundial con batallas de 50 contra 50 en mapas enormes, tanques, artillería y catorce roles distintos, que premia jugar en equipo.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/686810/4f69ae652d90d488bc09fcb0f12893a0e2bc2be1/library_capsule_2x.jpg"
          },
          {
            titulo: "Cricket 26 – The Official Game of the Ashes",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: "2026-11-24",
            texto: "Entra el 24. El juego oficial de The Ashes, la serie entre Inglaterra y Australia, con una carrera de gestión nueva y más equipos profesionales.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3468650/a0a0e8bd57ff492637f49973f310838306c59315/library_capsule_2x.jpg"
          },
          {
            titulo: "Soul Reaver 2",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "Sólo Deluxe. El clásico de 2001 de la saga Legacy of Kain: Raziel viaja por distintas épocas de Nosgoth persiguiendo a Kain y desentraña quién corrompió los Pilares.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/224940/library_600x900_2x.jpg"
          },
          {
            titulo: "Freedom Wars Remastered",
            id: null,
            plataformas: ["PS5", "PS4"],
            entra: null,
            texto: "Sólo Deluxe. El juego de acción de PS Vita, remasterizado: en un futuro sin recursos cada persona nace condenada a un millón de años de cárcel y los reduce cumpliendo misiones contra máquinas gigantes, solo o en cooperativo.",
            imagen: "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3004100/5afef40644eee5d48ff6f577005b953737324c21/library_600x900_2x.jpg"
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
    mes: "2026-11",
    intro: "Lo más fuerte de Game Pass en noviembre son los estrenos del primer día: Football Manager 27 el 3 en PC y el 10 en consolas, Escape Academy 2: Back 2 School el 5, Warhammer Survivors y Tanuki: Pon's Summer el 10, y Hope in the City el 11. Void/Breaker deja el Game Preview el 4, Thronefall llega a Xbox el 11 y Aphelion, de Don't Nod, suma Premium el 17. El 15 entran a Essential ocho clásicos, de Banjo-Kazooie y Perfect Dark a Viva Piñata, y se van 1000xResist, GoldenEye 007, Dragon Ball Xenoverse 2 y Wreckfest, entre otros.",
    tandas: [
      {
        nombre: "PRIMERA TANDA DE NOVIEMBRE",
        detalle: "Anunciada el 3 de noviembre. Salvo que se aclare otra cosa, cada juego entra a Ultimate y PC Game Pass. El 15 se van 1000xResist, Barbie Horse Trails, Dragon Ball Xenoverse 2, Firefighting Simulator – The Squad, GoldenEye 007, Great God Grove, Moonlighter, Pigeon Simulator, Police Simulator: Patrol Officers, Relic Hunters Legend, Total Chaos, Winter Burrow y Wreckfest.",
        anunciado: "2026-11-03",
        fuente: "https://news.xbox.com/en-us/2026/11/03/xbox-game-pass-november-2026-wave-1/",
        juegos: [
          {
            titulo: "Football Manager 27",
            id: null,
            plataformas: ["PC"],
            entra: "2026-11-03",
            texto: "Sólo PC: entra el día que sale. La entrega anual del simulador de gestión de fútbol de Sports Interactive; la versión de consolas llega el 10.",
            imagen: "https://store-images.s-microsoft.com/image/apps.47586.13984136076613493.b5146129-a992-4e04-8b43-ffa40460c569.40797f8e-48ea-47e2-aab8-9ea6e13f5a79?w=600&h=900&format=jpg"
          },
          {
            titulo: "Pit of Goblin",
            id: "pit-of-goblin",
            plataformas: ["XBOX"],
            entra: "2026-11-03",
            texto: "Entra el día que llega a Xbox, también en Premium. Un cooperativo de terror para cuatro goblins que bajan a mazmorras a buscar comida para su Rey Reina."
          },
          {
            titulo: "Vampire Crawlers: The Turbo Wildcard from Vampire Survivors",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-11-04",
            texto: "Ya estaba en Ultimate y PC Game Pass, y desde el 4 también se juega con Premium. De los creadores de Vampire Survivors: un dungeon crawler por turnos con cartas, en los escenarios de la saga.",
            imagen: "https://store-images.s-microsoft.com/image/apps.58093.13753975954973331.f68a6dfe-1345-43d2-9cf7-a4facb1f9857.c7421d49-f1f3-4904-b01e-7a14e4c92e1a?w=600&h=900&format=jpg"
          },
          {
            titulo: "Void/Breaker",
            id: "void-breaker",
            plataformas: ["XBOX"],
            entra: "2026-11-04",
            texto: "Entra el día que deja el Game Preview, también en Premium. Un shooter roguelite en primera persona contra máquinas, con armas que se modifican casi sin límite."
          },
          {
            titulo: "Escape Academy 2: Back 2 School",
            id: "escape-academy-2-back-2-school",
            plataformas: ["XBOX"],
            entra: "2026-11-05",
            texto: "Entra el día que sale. Salas de escape en un mundo abierto: la academia de escapismo se recorre libremente, con cooperativo para dos online o en la misma pantalla."
          },
          {
            titulo: "Firefighting Simulator: Ignite",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-11-05",
            texto: "También en Premium. Un simulador de bomberos de Estados Unidos: se apagan incendios y se rescata gente con hasta tres amigos o con una dotación manejada por la máquina.",
            imagen: "https://store-images.s-microsoft.com/image/apps.32408.14039390486448903.600abc2c-9f2a-489a-8d46-0eefc0946576.cabef57c-c072-408a-a400-ef040fd8bca9?w=600&h=900&format=jpg"
          },
          {
            titulo: "MySims: Cozy Bundle",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-11-05",
            texto: "Ya estaba en PC Game Pass y ahora se suma en consola y en la nube. Reúne MySims y MySims Kingdom, los dos juegos de construir y decorar de la serie de EA, en versión renovada.",
            imagen: "https://store-images.s-microsoft.com/image/apps.7236.13655706602498995.149ae955-10f2-4011-a323-545ac134caef.0f4c4264-87e9-426e-8792-f4956f69b0a5?w=600&h=900&format=jpg"
          },
          {
            titulo: "Football Manager 27 Console",
            id: "football-manager-27",
            plataformas: ["XBOX"],
            entra: "2026-11-10",
            texto: "Entra el día que sale. La entrega anual del simulador de gestión de fútbol, esta vez con una interfaz rediseñada para hacer menos clics."
          },
          {
            titulo: "Warhammer Survivors",
            id: "warhammer-survivors",
            plataformas: ["XBOX"],
            entra: "2026-11-10",
            texto: "Entra el día que sale. Un survivors-like en los universos de Warhammer, hecho junto con los creadores de Vampire Survivors."
          },
          {
            titulo: "Tanuki: Pon's Summer",
            id: "tanuki-pons-summer",
            plataformas: ["XBOX"],
            entra: "2026-11-10",
            texto: "Entra el día que sale. Un simulador de vida tranquilo: Pon tiene un mes para arreglar el santuario antes del Festival Tanuki, y lo hace repartiendo paquetes en BMX."
          },
          {
            titulo: "Hope in the City",
            id: "hope-in-the-city",
            plataformas: ["XBOX"],
            entra: "2026-11-11",
            texto: "Entra el día que sale. Un misterio en la ciudad china de Shenyang: una chica de 17 años busca a sus padres desaparecidos y convierte sus dibujos en pistas."
          },
          {
            titulo: "Thronefall",
            id: "thronefall",
            plataformas: ["XBOX"],
            entra: "2026-11-11",
            texto: "Entra el día que llega a Xbox, también en Premium. Estrategia minimalista: de día se construye un reino chico y de noche se lo defiende de oleadas de enemigos."
          },
          {
            titulo: "John Carpenter's Toxic Commando",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-11-12",
            texto: "También en Premium. Un cooperativo para cuatro contra hordas de zombis en escenarios semiabiertos, con el sello de John Carpenter. Salió en marzo.",
            imagen: "https://store-images.s-microsoft.com/image/apps.29766.13813225504277272.60187aa7-cee5-4670-9406-da8555a77e6d.c837b95c-ea53-45ca-8a1d-e10bea8f2ff1?w=600&h=900&format=jpg"
          },
          {
            titulo: "Aphelion",
            id: null,
            plataformas: ["XBOX"],
            entra: "2026-11-17",
            texto: "Ya estaba en Ultimate y PC Game Pass, y desde el 17 también se juega con Premium. La aventura de ciencia ficción de Don't Nod: dos astronautas varados en un planeta helado, hecha junto con la Agencia Espacial Europea.",
            imagen: "https://store-images.s-microsoft.com/image/apps.46058.13661171777966781.f2079bb0-25c3-4356-bff7-576d8707eb18.770e543b-11c7-448c-81b8-71a9af644846?w=600&h=900&format=jpg"
          },
          {
            titulo: "Paw Patrol: Dino World",
            id: "paw-patrol-dino-world",
            plataformas: ["XBOX"],
            entra: "2026-11-17",
            texto: "También en Premium. Una aventura para chicos en la Isla de los Dinosaurios con los cachorros de la serie, solo o en cooperativo para dos."
          },
          {
            titulo: "Gravhounds",
            id: null,
            plataformas: ["XBOX"],
            entra: null,
            texto: "Ya disponible, en Game Preview: un cooperativo para cuatro perros espaciales que juntan todo lo que pueden en un planeta hostil mientras el enjambre se pone cada vez más bravo.",
            imagen: "https://store-images.s-microsoft.com/image/apps.62712.14119486704236036.abde8f1d-835f-498a-a443-5a7c4d6c7932.5340b529-7333-4472-82f3-634458f9a584?w=600&h=900&format=jpg"
          }
        ]
      },
      {
        nombre: "SE SUMAN A ESSENTIAL",
        detalle: "Desde el 15 de noviembre entran también al catálogo de Game Pass Essential, el plan más barato. Se juegan en consola y en la nube.",
        anunciado: "2026-11-03",
        fuente: "https://news.xbox.com/en-us/2026/11/03/xbox-game-pass-november-2026-wave-1/",
        juegos: [
          {
            titulo: "Banjo-Kazooie",
            id: null,
            plataformas: ["XBOX"],
            entra: null,
            texto: "El plataformas de Rare de 1998, en la versión de Xbox 360: un oso y un pájaro contra la bruja Gruntilda.",
            imagen: "https://store-images.s-microsoft.com/image/apps.33130.70306648669442933.0ad02883-9547-43ed-a595-2a807684ce15.661619f7-c356-407c-87b7-276750817874?w=600&h=900&format=jpg"
          },
          {
            titulo: "Banjo-Tooie",
            id: null,
            plataformas: ["XBOX"],
            entra: null,
            texto: "La secuela de 2000, también de Rare, con mundos más grandes y conectados entre sí.",
            imagen: "https://store-images.s-microsoft.com/image/apps.51096.63435052096425467.cd1eef72-5707-4f2b-807d-ab3c5baf858c.feb06dbe-5615-42c2-8e26-fa15d1745896?w=600&h=900&format=jpg"
          },
          {
            titulo: "Banjo-Kazooie: Nuts & Bolts",
            id: null,
            plataformas: ["XBOX"],
            entra: null,
            texto: "La entrega de 2008 que cambió los saltos por armar vehículos con piezas.",
            imagen: "https://store-images.s-microsoft.com/image/apps.65096.71100151761088573.88824642-fc7e-4e99-9b5b-32e26f7c27b9.4b7be015-afcd-42ca-9db2-364cd29734df?w=600&h=900&format=jpg"
          },
          {
            titulo: "Gears of War: Judgment",
            id: null,
            plataformas: ["XBOX"],
            entra: null,
            texto: "La precuela de 2013 con el escuadrón Kilo de Baird y Cole, contada como un juicio militar.",
            imagen: "https://store-images.s-microsoft.com/image/apps.38790.70323071690757883.aa344172-c923-4b38-a055-9ce9a093bc86.fa2e3328-f1d7-4b43-b5e3-cfd7c69ee9d2?w=600&h=900&format=jpg"
          },
          {
            titulo: "Halo: Spartan Assault",
            id: null,
            plataformas: ["XBOX"],
            entra: null,
            texto: "Un Halo de disparos con vista desde arriba, de 2013, ambientado entre Halo 3 y Halo 4. Es el único de la lista que también se juega en PC.",
            imagen: "https://store-images.s-microsoft.com/image/apps.20431.70634858521726340.aed5ca97-d1dc-4d71-ae1f-b3f94bf8b727.1e47fef5-905e-40b4-8765-f294f6bbff1f?w=600&h=900&format=jpg"
          },
          {
            titulo: "Perfect Dark",
            id: null,
            plataformas: ["XBOX"],
            entra: null,
            texto: "La remasterización para Xbox 360 del shooter de Rare de Nintendo 64, con la agente Joanna Dark.",
            imagen: "https://store-images.s-microsoft.com/image/apps.24811.65049759038650156.9c9f4a81-e21a-4dcb-b819-b75ab00b696e.7461a932-7d28-4f09-b6c8-695ccfc367bb?w=600&h=900&format=jpg"
          },
          {
            titulo: "Viva Piñata",
            id: null,
            plataformas: ["XBOX"],
            entra: null,
            texto: "El juego de Rare de 2006 en el que se arma un jardín para atraer piñatas vivas.",
            imagen: "https://store-images.s-microsoft.com/image/apps.29775.71972951279590291.af9c2fdb-151a-4c1d-8ae7-d7bfb2a756ee.62ce58fd-eccf-4da7-8c33-bc66f5175dbd?w=600&h=900&format=jpg"
          },
          {
            titulo: "Viva Piñata: Trouble in Paradise",
            id: null,
            plataformas: ["XBOX"],
            entra: null,
            texto: "La secuela de 2008, con más especies y excursiones fuera del jardín para atraparlas.",
            imagen: "https://store-images.s-microsoft.com/image/apps.13926.69467662407886849.eb318d40-1e77-4848-b633-b9ee445d2f63.c32b9b59-01cd-43fd-b374-d60e0217acb2?w=600&h=900&format=jpg"
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
