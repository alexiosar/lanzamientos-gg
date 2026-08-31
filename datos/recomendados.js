// RECOMENDADOS DEL MES
//
// La selección de lo que vale la pena de cada mes. La elige una persona, no un puntaje:
// el mes que arranca son lanzamientos futuros y ninguno tiene nota de Metacritic todavía,
// así que un ranking automático acá no puede existir. Ese es el punto de esta página —
// si se pudiera calcular, ya lo haría el ranking.
//
// Campos:
//   mes     "AAAA-MM". Lo que manda: la página muestra este mes y nada más.
//   juegos  lista ordenada por fecha de salida, con el id de datos/juegos.js y una línea
//           propia explicando por qué está. El texto es lo único que justifica la página:
//           sin él es una lista de doce carátulas que ya están en el calendario.
//
// Los meses viejos se dejan comentados abajo, así queda registro de lo que se recomendó
// y no hay que buscarlo en el historial de git.
//
// Al cambiar de mes: se arma la lista nueva y se actualiza `mes`. Va en la rutina mensual.
// Si `mes` no coincide con el mes en curso, la página lo dice en vez de mentir.

const RECOMENDADOS = {
  mes: "2026-09",
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
      texto: "Nintendo anunció un exclusivo de Switch 2 y dijo dos palabras: «We are one!». Nada más. Está acá justamente por eso — es lo único del mes de lo que no se sabe nada, y viene de la casa que no suele anunciar al pedo."
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
  ]
};

if (typeof module !== "undefined" && module.exports) module.exports = RECOMENDADOS;
