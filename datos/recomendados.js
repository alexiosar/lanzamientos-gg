// RECOMENDADOS DEL MES
//
// La selección de lo que vale la pena de cada mes. La elige una persona, no un puntaje:
// el mes que arranca son lanzamientos futuros y ninguno tiene nota de Metacritic todavía,
// así que un ranking automático acá no puede existir. Ese es el punto de esta página —
// si se pudiera calcular, ya lo haría el ranking.
//
// Campos:
//   mes         "AAAA-MM". Lo que manda: /recomendados muestra este mes y nada más.
//   intro       el párrafo de arriba de la lista. Opcional pero conviene escribirlo, y va
//               NOMBRANDO JUEGOS. La primera versión explicaba en qué se diferencia esta
//               página del ranking del sitio, y eso es hablarle al lector de nosotros
//               cuando vino a leer de juegos: si hay que justificar la lista, la lista no
//               se sostiene sola. Sin este campo sale una línea genérica de respaldo.
//   juegos      lista ordenada por fecha de salida, con el id de datos/juegos.js y una línea
//               propia explicando por qué está. El texto es lo único que justifica la página:
//               sin él es una lista de doce carátulas que ya están en el calendario.
//   anteriores  los meses que ya pasaron, cada uno con la misma forma { mes, juegos }.
//               Cada uno se convierte en su propia página, /mejores-juegos-agosto-2026 y
//               así, y todas se enlazan entre sí con los botones de arriba.
//
// Antes los meses viejos se dejaban comentados acá, "así queda registro". Registro sin
// página es lo mismo que nada: la selección de agosto era trabajo hecho que no leía nadie,
// y en septiembre los puntajes ya están, o sea que la lista vieja dice MÁS que cuando se
// escribió. Desde el 08/09/2026 cada mes pasado tiene su URL.
//
// Al cambiar de mes: el mes que termina se mueve a `anteriores` y se arma la lista nueva.
// Va en la rutina mensual. Si `mes` no coincide con el mes en curso, /recomendados lo dice
// en vez de mentir.
//
// Ojo con no duplicar: un mes NO va en `mes` y en `anteriores` al mismo tiempo. Serían dos
// URLs con el mismo contenido, que es justo lo que le hace mal a la indexación.

const RECOMENDADOS = {
  mes: "2026-09",
  intro: "Marvel's Wolverine el 15, la primera Fire Emblem pensada para Switch 2 el 17, y Control y Silent Hill el mismo día a fin de mes. Septiembre trae 112 lanzamientos al calendario, y estos doce son los que valen el tiempo.",
  juegos: [
    {
      id: "moonlighter-2-the-endless-vault",
      texto: "El primero se ganó su público con una idea que nadie más estaba haciendo: de día atendés tu tienda y ponés los precios, de noche bajás a la mazmorra a buscar qué vender. La secuela mantiene el doble turno y agranda todo lo demás."
    },
    {
      id: "the-blood-of-dawnwalker",
      texto: "El debut de Rebel Wolves, el estudio que armaron varios de los que hicieron The Witcher 3. Sos Coen, humano de día y vampiro de noche, en la Europa del siglo XIV: el reloj no es decorativo, cambia lo que podés hacer."
    },
    {
      id: "orbitals",
      texto: "Entró a esta lista cuando Nintendo lo había anunciado con dos palabras —«We are one!»— y nada más. Salió el 3 de septiembre con 82 y ahora se entiende la frase: es un cooperativo para DOS, sin modo individual, con un diseño de niveles que las reseñas comparan con It Takes Two. Si tenés con quién jugarlo, era la apuesta buena del mes; si no, no es para vos."
    },
    {
      id: "marsupilami-2-salsa-palombia",
      texto: "Plataformas clásico y sin vueltas, de los que ya casi no se hacen para consola. El primero sorprendió por lo prolijo, y este mes es de los pocos que se puede jugar con chicos al lado."
    },
    {
      id: "onimusha-way-of-the-sword",
      texto: "Capcom vuelve a Onimusha veinte años después. Un samurái con el guantelete Oni en el Kioto de los Genma, con la misma receta de combate cuerpo a cuerpo pesado que hizo grande a la saga en PS2."
    },
    {
      id: "marvels-wolverine",
      texto: "Lo nuevo de Insomniac después de los dos Spider-Man, y el tono es el opuesto: crudo, adulto y con las garras a la vista. Es el exclusivo grande de PS5 del año y llega sin haber mostrado casi nada."
    },
    {
      id: "fire-emblem-fortunes-weave",
      texto: "La primera Fire Emblem pensada para Switch 2. Estrategia por turnos en cuadrícula, unidades que si mueren no vuelven, y los vínculos entre personajes pesando tanto como las estadísticas."
    },
    {
      id: "graveyard-keeper-2",
      texto: "La secuela del simulador de cementerios más incómodo que existe. El primero se reía de Stardew Valley haciéndote administrar un negocio con los muertos del pueblo; este suma automatización y zombis a las órdenes."
    },
    {
      id: "control-resonant",
      texto: "Remedy vuelve a la Casa Inmemorial, esta vez con Dylan Faden y un Manhattan deformado. Del mismo estudio que Alan Wake 2, que es probablemente lo mejor que hicieron."
    },
    {
      id: "silent-hill-townfall",
      texto: "El otro Silent Hill, el que no es remake. Lo hace Screen Burn, no Bloober, y se aleja del molde: menos pueblo con niebla y más una isla, un tipo que vuelve a arreglar algo y un descenso que se pone incómodo rápido."
    },
    {
      id: "garfield-escape-from-monday",
      texto: "Un plataformas 3D de Garfield en el que hay que despertarlo de una pesadilla de verduras. Está en la lista sin ironía: el mes tiene doce juegos de vampiros, samuráis y demonios, y este es el único que se ríe."
    },
    {
      id: "the-witcher-3-wild-hunt-remastered",
      texto: "Uno de los mejores RPG de mundo abierto que se hicieron, remasterizado y entero —con Hearts of Stone y Blood and Wine— y por primera vez portátil de verdad en Switch 2. Si nunca lo jugaste, es la mejor forma de empezar."
    }
  ],

  anteriores: [
    {
      mes: "2026-08",
      intro: "Metal Gear Solid 4 salió de la PS3 después de dieciocho años, Arc System Works hizo un 4 contra 4 de Marvel y Game Freak se animó a un RPG de acción sin Pokémon adentro. Ocho juegos de agosto, con el puntaje de la crítica y un gameplay en español de cada uno.",
      juegos: [
        {
          id: "beast-of-reincarnation",
          texto: "El primer RPG de acción grande de Game Freak fuera de Pokémon, y el más discutido del mes: cerró en 71 con reseñas que van de un extremo al otro. En lo que coinciden todas es en dos cosas, el combate y la relación entre Emma y su perro Kuu. Lo que le reprochan es el mundo alrededor, que varias describen como vacío. Está en la lista por lo que intenta, no por lo que le salió parejo."
        },
        {
          id: "marvel-tokon-fighting-souls",
          texto: "Arc System Works, los de Guilty Gear, haciendo un 4 contra 4 de Marvel, y resolvieron lo difícil: se entiende sin haber jugado un juego de peleas en la vida y abajo sigue teniendo la profundidad de siempre. El modo entrenamiento enseña de verdad, que en el género es raro. Lo flojo está afuera del ring, en los modos para un jugador."
        },
        {
          id: "the-sinking-city-2",
          texto: "Frogwares cambió de género a mitad de camino: la primera era un detective suelto en la ciudad y esta es survival horror del molde de los Resident Evil modernos, con mejor combate y mejores puzzles. Se pierde la investigación a mano, que era lo que la hacía distinta. Está hecha en Ucrania durante la guerra, y varias reseñas le perdonan la falta de pulido por eso."
        },
        {
          id: "mortal-shell-2",
          texto: "La secuela del soulslike de Cold Symmetry, el estudio chico que en 2020 se metió a competirle a From Software y salió bien parado. Vuelve la idea que lo hacía distinto: no tenés un personaje, poseés cuerpos ajenos y cada uno pelea diferente. Es el único de esta lista sin nota de Metacritic, así que acá no hay consenso de prensa que valga: está por lo que era el primero."
        },
        {
          id: "resonance-a-plague-tale-legacy",
          texto: "La precuela de A Plague Tale, con Sophia como protagonista, y el otro juego discutido del mes: hay reseñas de 95 y de 60 hablando de lo mismo. El desacuerdo es por el cambio de género —menos sigilo y menos ratas, más acción tipo Uncharted—, no por la factura. En lo visual y en la música nadie discute, y Sophia gusta por unanimidad."
        },
        {
          id: "star-wars-zero-company",
          texto: "Tácticas por turnos al estilo XCOM en el final de las Guerras Clon, y aguanta la comparación: es un juego del género hecho en serio, no una licencia pegada encima. La sorpresa fue la historia, que varias reseñas ponen a la altura de Andor y Rogue One, con un escuadrón donde nadie usa la Fuerza. Lo que le marcan es que arranca lento y que tiene algún problema técnico."
        },
        {
          id: "metal-gear-solid-master-collection-vol-2",
          texto: "Metal Gear Solid 4 sale de la PS3 después de dieciocho años, y eso solo ya justifica el paquete. Vienen también Peace Walker y Ghost Babel, y las conversiones se elogiaron sin peros. Las quejas no son de los juegos sino de la caja: trae menos que el Vol. 1 y hay que saltar entre aplicaciones sueltas porque no tiene un menú común."
        },
        {
          id: "captain-tsubasa-2-world-fighters",
          texto: "El acuerdo de las reseñas es que no hay que medirlo como un juego de fútbol: es uno de peleas con once por lado, y con esa vara funciona. El modo historia cubre entero el Mundial Juvenil y hay 110 personajes. Si creciste con Supercampeones, el espectáculo de la serie está bien capturado; si no, el ritmo cortado te va a molestar."
        }
      ]
    }
  ]
};

if (typeof module !== "undefined" && module.exports) module.exports = RECOMENDADOS;
