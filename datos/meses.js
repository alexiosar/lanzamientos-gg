// INTRODUCCIÓN DE LAS PÁGINAS DE MES
//
// Un párrafo propio arriba de la lista de /noviembre-2026 y las demás (no en las de cada
// consola, porque nombra juegos de todas). Existe desde el 02/10/2026: esas páginas eran
// sólo una lista de enlaces, y la búsqueda que reciben —"juegos que salen en noviembre"—
// pide que alguien diga qué es lo importante del mes. Con GTA VI en noviembre, esa
// respuesta vale más que la lista.
//
// Campos:
//   mes    "AAAA-MM"
//   intro  un párrafo que NOMBRA JUEGOS y días, como el intro de los recomendados. Sólo
//          datos que estén en datos/juegos.js; nada sobre el sitio.
//
// Se escribe en la rutina mensual al estrenar un mes, y se repasa si un juego nombrado
// cambia de fecha: el generador avisa si el texto nombra un juego que ya no está en ese
// mes. Un mes sin intro se genera igual, sin el párrafo.
// Comentarios dentro del arreglo no: el lector de Python no los acepta.

const MESES_INTRO = [
  {
    mes: "2026-09",
    intro: "Septiembre fue el mes más cargado del año, con 112 lanzamientos. Entre los estrenos, lo mejor puntuado fue Trails in the Sky 2nd Chapter, con 90, seguido por Fire Emblem: Fortune's Weave y Well Dweller, con 89; Onimusha: Way of the Sword sacó 85, Control Resonant y The Blood of Dawnwalker 83, y Silent Hill: Townfall 81. Marvel's Wolverine se quedó en 75. Entre las versiones nuevas de juegos que ya existían, The Witcher 3 Remastered para Switch 2 y Maestro llegaron a 93."
  },
  {
    mes: "2026-10",
    intro: "Octubre trae más de cien juegos. Arrancó con Ace Combat 8: Wings of Theve, que debutó con 88 en la crítica, y el 6 siguen Gears of War: E-Day, Star Wars: Galactic Racer y la colección de Kingdom Hearts, que en Switch 2 llega el 8. El 15 sale Castlevania: Belmont's Curse, el 22 Final Fantasy Resonance y Nintendo Switch Sports Resort, el 23 Call of Duty: Modern Warfare 4, y el 29 cierran Phantom Blade Zero y la remasterización de The Wolf Among Us."
  },
  {
    mes: "2026-11",
    intro: "Noviembre gira alrededor de un solo día: el 19 sale Grand Theft Auto VI en PS5 y Xbox, después de dos retrasos. Antes, el 5 es el turno de Switch 2, con la nueva versión de The Legend of Zelda: Ocarina of Time, Stellar Blade y Guardians of the Galaxy el mismo día. El 10 sale Football Manager 27 y el 12 llegan a Switch 2 Metaphor: ReFantazio y Pikmin 4 con la Academia Dandori. El 3 abre el mes la remasterización de Godzilla: Destroy All Monsters Melee."
  },
  {
    mes: "2026-12",
    intro: "Diciembre arranca cargado: el 3 coinciden Rayman Legends Retold, Dragon Quest Monsters: El Reino Marchito, la edición de Switch 2 de Xenoblade Chronicles 3 y SOMBRAS: Negative Frames, y el 4 Monster Hunter Wilds llega a Switch 2. El 10 es el día más fuerte del mes, con El profesor Layton y el Nuevo Mundo a vapor, Attack on Titan 3 y Stage Tour, el regreso de los juegos de guitarra de plástico de la mano de los creadores de Guitar Hero. Además, más de veinte juegos anunciados para fin de año todavía no tienen día."
  },
  {
    mes: "2027-01",
    intro: "Enero de 2027 tiene su semana fuerte a mitad de mes: el 14 sale Danganronpa 2x2 y el 15 Stranger Than Heaven, lo nuevo del estudio de Like a Dragon. El cierre es el 28, con Until Dawn 2 en PS5, Metroid Ravenous en Switch 2, Tropico 7 y Fate/EXTRA Record."
  },
  {
    mes: "2027-02",
    intro: "Febrero de 2027 es de los meses más fuertes del año. El 16 sale God of War: Laufey en PS5, el mismo día que Romancing SaGa 3: Destinies United, y una semana después, el 23, llega Fable a Xbox y PS5. Antes, el 4 sale Metro 2039 y el 12 Tomb Raider: Legacy of Atlantis. El 18 es el turno de Persona 4 Revival, y el 25 cierran la edición de Switch 2 de Hyrule Warriors: La era del cataclismo y Atelier Karia."
  },
  {
    mes: "2027-03",
    intro: "Marzo de 2027 se concentra en su primera semana: el 4 salen Wo Long 2: Wings of Ember, Trine 6: Together in Time y Eternal Anima, y el 5 Gundam Rogue Orbit. El 9 llega Grave Seasons, un simulador de granja con un asesino serial sobrenatural suelto en el pueblo, y el 11 Road Kings."
  },
  {
    mes: "2027-04",
    intro: "Abril de 2027 tiene dos días marcados: el 7 sale EXODUS, el RPG de ciencia ficción de Archetype Entertainment, y el 8 Final Fantasy VII Revelation en PS5, Xbox y Switch 2. El 21 llega Melty Blood: Twi-Lumina."
  }
];

if (typeof module !== "undefined" && module.exports) module.exports = MESES_INTRO;
