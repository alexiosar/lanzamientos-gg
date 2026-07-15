// ── ESTADO ──
let filtroActivo = "TODAS";
let filtroGenero = "TODOS";
let filtroTexto = "";
let vistaActiva = "calendario";

// ── HELPERS ──
const MESES_ES = [
  "ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
  "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"
];
const DIAS_ES = ["DOM","LUN","MAR","MIE","JUE","VIE","SAB"];

function parseFecha(str) {
  const [y, m, d] = str.split("-").map(Number);
  return new Date(y, m - 1, d);
}

function plataformaClass(p) {
  if (p === "PS5")     return "plat-PS5";
  if (p === "PS4")     return "plat-PS4";
  if (p === "XBOX")    return "plat-XBOX";
  if (p === "SWITCH2") return "plat-SWITCH2";
  if (p === "SWITCH")  return "plat-SWITCH";
  return "plat-MULTI";
}

function plataformaLabel(p) {
  if (p === "SWITCH2") return "SWITCH 2";
  return p;
}

function claseMetacritic(n) {
  if (n >= 75) return "meta-alto";
  if (n >= 50) return "meta-medio";
  return "meta-bajo";
}

// días entre hoy y una fecha (positivo = futuro)
function diasHasta(fechaStr) {
  const hoy = parseFecha(getDiaKeyHoy());
  return Math.round((parseFecha(fechaStr) - hoy) / 86400000);
}

// ── AGENDAR (.ics) ──
// genera un evento de calendario de día completo y lo descarga
function agendarJuego(id, e) {
  if (e) e.stopPropagation();
  const j = JUEGOS.find(x => x.id === id);
  if (!j) return;

  const inicio = j.fecha.replace(/-/g, "");
  const fin = parseFecha(j.fecha);
  fin.setDate(fin.getDate() + 1);
  const finStr = `${fin.getFullYear()}${String(fin.getMonth() + 1).padStart(2, "0")}${String(fin.getDate()).padStart(2, "0")}`;
  const ahora = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
  const esc = t => t.replace(/\\/g, "\\\\").replace(/[,;]/g, m => "\\" + m);

  const ics = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//lanzamientos.lat//Calendario de Videojuegos//ES",
    "BEGIN:VEVENT",
    `UID:${j.id}@lanzamientos.lat`,
    `DTSTAMP:${ahora}`,
    `DTSTART;VALUE=DATE:${inicio}`,
    `DTEND;VALUE=DATE:${finStr}`,
    `SUMMARY:${esc("🎮 Sale " + j.titulo)}`,
    `DESCRIPTION:${esc(`Lanzamiento en ${j.plataformas.map(plataformaLabel).join(" / ")}. Ficha: https://lanzamientos.lat/juegos/${j.id}.html`)}`,
    `URL:https://lanzamientos.lat/juegos/${j.id}.html`,
    "END:VEVENT",
    "END:VCALENDAR"
  ].join("\r\n");

  const blob = new Blob([ics], { type: "text/calendar;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `${j.id}.ics`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(a.href);
}

function cuentaRegresivaHtml(fechaStr) {
  const dias = diasHasta(fechaStr);
  if (dias === 0) return `<span class="cuenta-regresiva regresiva-hoy">▸ ¡SALE HOY!</span>`;
  if (dias === 1) return `<span class="cuenta-regresiva">▸ FALTA 1 DÍA</span>`;
  if (dias > 1)   return `<span class="cuenta-regresiva">▸ FALTAN ${dias} DÍAS</span>`;
  return "";
}

// ── HOY ──
function getMesKeyHoy() {
  const hoy = new Date();
  return `${hoy.getFullYear()}-${String(hoy.getMonth() + 1).padStart(2, "0")}`;
}

function getDiaKeyHoy() {
  const hoy = new Date();
  return `${hoy.getFullYear()}-${String(hoy.getMonth() + 1).padStart(2, "0")}-${String(hoy.getDate()).padStart(2, "0")}`;
}

function esHoy(diaKey) {
  return diaKey === getDiaKeyHoy();
}

// encuentra el día más próximo a hoy dentro de un mes
function diaProximo(diasOrdenados) {
  const hoy = getDiaKeyHoy();
  // primero busca exacto
  if (diasOrdenados.includes(hoy)) return hoy;
  // si no, el más cercano hacia adelante
  const futuro = diasOrdenados.filter(d => d >= hoy);
  if (futuro.length) return futuro[0];
  // si no hay futuro, el último del mes
  return diasOrdenados[diasOrdenados.length - 1];
}

// ── URL COMPARTIBLE ──
// refleja los filtros activos en la URL (sin recargar) para poder compartir el link
function actualizarURL() {
  const params = new URLSearchParams();
  if (filtroActivo !== "TODAS")     params.set("plat", filtroActivo);
  if (filtroGenero !== "TODOS")     params.set("gen", filtroGenero);
  if (filtroTexto !== "")           params.set("q", filtroTexto);
  if (vistaActiva !== "calendario") params.set("vista", vistaActiva);
  const qs = params.toString();
  history.replaceState(null, "", qs ? `?${qs}` : window.location.pathname);
}

// ── FILTROS PLATAFORMA ──
function activarFiltro(plataforma) {
  filtroActivo = plataforma;
  document.querySelectorAll(".filtro-btn-plat").forEach(b => {
    b.classList.toggle("activo", b.dataset.plat === plataforma);
  });
  actualizarURL();
  renderCalendario();
}

// ── FILTRO GÉNERO ──
function generarFiltrosGenero() {
  const generos = new Set();
  JUEGOS.forEach(j => j.genero.forEach(g => generos.add(g)));
 
  const contenedor = document.getElementById("filtros-genero");
  contenedor.innerHTML = ["TODOS", ...Array.from(generos).sort()].map(g => `
    <button class="filtro-btn ${g === filtroGenero ? 'activo' : ''}"
            data-gen="${g}"
            onclick="activarFiltroGenero('${g}')">${g}</button>
  `).join("");
}

 function activarFiltroGenero(genero) {
  filtroGenero = genero;
  document.querySelectorAll("#filtros-genero .filtro-btn").forEach(b => {
    b.classList.toggle("activo", b.dataset.gen === genero);
  });
  actualizarURL();
  renderCalendario();
}

// ── BUSCADOR ──
function buscarJuego(texto) {
  filtroTexto = texto.trim().toLowerCase();
  actualizarURL();
  renderCalendario();
}

// ── VISTA (calendario / ranking) ──
function cambiarVista(vista) {
  vistaActiva = vista;
  document.querySelectorAll(".vista-btn").forEach(b => {
    b.classList.toggle("activo", b.dataset.vista === vista);
  });
  actualizarURL();
  renderCalendario();
}

// ── RANKING POR METACRITIC ──
function renderRanking(juegos) {
  const conPuntaje = juegos
    .filter(j => j.metacritic)
    .sort((a, b) => b.metacritic - a.metacritic);

  if (conPuntaje.length === 0) {
    return `<div class="sin-resultados">// NINGÚN JUEGO CON PUNTAJE PARA ESTE FILTRO</div>`;
  }

  const filas = conPuntaje.map((j, i) => {
    const fecha = parseFecha(j.fecha);
    const fechaStr = `${String(fecha.getDate()).padStart(2, "0")} ${MESES_ES[fecha.getMonth()].slice(0, 3)}`;
    const platsHtml = j.plataformas.map(p =>
      `<span class="plat ${plataformaClass(p)}">${plataformaLabel(p)}</span>`
    ).join("");
    return `
      <a class="ranking-fila" href="juegos/${j.id}.html">
        <span class="ranking-pos">#${String(i + 1).padStart(2, "0")}</span>
        <span class="badge-metacritic ${claseMetacritic(j.metacritic)}">${j.metacritic}</span>
        <span class="juego-nombre">${j.titulo}</span>
        <span class="ranking-fecha">${fechaStr}</span>
        <div class="plataformas">${platsHtml}</div>
      </a>`;
  }).join("");

  return `
    <div class="ranking">
      <div class="ranking-header">★ MEJOR PUNTUADOS <span class="mes-contador">[ PUNTAJE METACRITIC ]</span></div>
      ${filas}
    </div>`;
}

// ── JUEGOS FILTRADOS ──
function juegosFiltrados() {
  return JUEGOS.filter(j => {
    const porPlat  = filtroActivo === "TODAS" || j.plataformas.includes(filtroActivo);
    const porGen   = filtroGenero === "TODOS"  || j.genero.includes(filtroGenero);
    const porTexto = filtroTexto === "" || j.titulo.toLowerCase().includes(filtroTexto);
    return porPlat && porGen && porTexto;
  });
}

// ── RENDER ──
function agruparPorMesYDia(juegos) {
  const mapa = {};
  juegos.forEach(j => {
    const fecha = parseFecha(j.fecha);
    const mesKey = `${fecha.getFullYear()}-${String(fecha.getMonth() + 1).padStart(2, "0")}`;
    const diaKey = j.fecha;
    if (!mapa[mesKey]) mapa[mesKey] = {};
    if (!mapa[mesKey][diaKey]) mapa[mesKey][diaKey] = [];
    mapa[mesKey][diaKey].push(j);
  });
  return mapa;
}

function renderCalendario() {
  const contenedor = document.getElementById("calendario");
  const juegos = juegosFiltrados();

  if (juegos.length === 0) {
    contenedor.innerHTML = `<div class="sin-resultados">// NO HAY JUEGOS PARA ESTE FILTRO</div>`;
    return;
  }

  if (vistaActiva === "ranking") {
    contenedor.innerHTML = renderRanking(juegos);
    return;
  }

  const agrupado = agruparPorMesYDia(juegos);
  const mesesOrdenados = Object.keys(agrupado).sort();
  const mesKeyHoy = getMesKeyHoy();

  // el día PRÓXIMO es el primer día con lanzamientos posterior a hoy (en cualquier mes)
  const hoyKey = getDiaKeyHoy();
  const todosLosDias = mesesOrdenados.flatMap(m => Object.keys(agrupado[m])).sort();
  const proximoKey = todosLosDias.find(d => d > hoyKey) || null;

  // bloque PRÓXIMOS 7 DÍAS (lanzamientos entre mañana y dentro de una semana)
  const en7 = parseFecha(hoyKey);
  en7.setDate(en7.getDate() + 7);
  const limite7 = `${en7.getFullYear()}-${String(en7.getMonth() + 1).padStart(2, "0")}-${String(en7.getDate()).padStart(2, "0")}`;
  const proximos7 = juegos
    .filter(j => j.fecha > hoyKey && j.fecha <= limite7)
    .sort((a, b) => a.fecha.localeCompare(b.fecha));

  const proximosHtml = proximos7.length ? `
    <div class="proximos">
      <div class="proximos-header">▸ PRÓXIMOS 7 DÍAS</div>
      ${proximos7.map(j => {
        const f = parseFecha(j.fecha);
        const dia = `${DIAS_ES[f.getDay()]} ${String(f.getDate()).padStart(2, "0")}`;
        const plats = j.plataformas.map(p =>
          `<span class="plat ${plataformaClass(p)}">${plataformaLabel(p)}</span>`
        ).join("");
        return `
        <a class="proximos-fila" href="juegos/${j.id}.html">
          <span class="proximos-dia">${dia}</span>
          <span class="juego-nombre">${j.titulo}</span>
          <div class="plataformas">${plats}</div>
        </a>`;
      }).join("")}
    </div>` : "";

  contenedor.innerHTML = proximosHtml + mesesOrdenados.map((mesKey, idx) => {
    const [year, month] = mesKey.split("-").map(Number);
    const nombreMes = `${MESES_ES[month - 1]} ${year}`;
    const diasOrdenados = Object.keys(agrupado[mesKey]).sort();
    const totalJuegos = diasOrdenados.reduce((acc, d) => acc + agrupado[mesKey][d].length, 0);
    
    // abrir solo el mes actual, cerrar el resto (si hay búsqueda, abrir todos)
    const abierto = mesKey === mesKeyHoy || filtroTexto !== "";

    // abrir al que hacer scroll dentro del mes actual
    const diaFoco = abierto ? diaProximo(diasOrdenados) : null;

    const diasHtml = diasOrdenados.map(diaKey => {
      const fecha = parseFecha(diaKey);
      const diaNombre = DIAS_ES[fecha.getDay()];
      const diaNum = String(fecha.getDate()).padStart(2, "0");
      const mesNom = MESES_ES[fecha.getMonth()].slice(0, 3);
      const esDiaHoy = esHoy(diaKey);
      const esDiaFoco = diaKey === diaFoco;

      // indicador HOY, PROXIMO o YA DISPONIBLE
      let indicador = "";
      if (esDiaHoy) {
        indicador = `<span class="dia-hoy">[ HOY ]</span>`;
      } else if (diaKey === proximoKey) {
        indicador = `<span class="dia-proximo">[ PRÓXIMO ]</span>`;
      } else if (diaKey < hoyKey) {
        indicador = `<span class="dia-disponible">[ YA DISPONIBLE ]</span>`;
      }

      const juegosHtml = agrupado[mesKey][diaKey].map(j => {
        const platsHtml = j.plataformas.map(p =>
          `<span class="plat ${plataformaClass(p)}">${plataformaLabel(p)}</span>`
        ).join("");

        // ★ NUEVO solo para lanzamientos de hoy en adelante (no para los ya disponibles)
        const nuevoHtml = (j.nuevo && diaKey >= hoyKey) ? `<span class="juego-nuevo">★ NUEVO</span>` : "";

        const tagsHtml = [
          ...j.genero.map(g => `<span class="tag">${g}</span>`),
          ...j.plataformas.map(p => `<span class="plat ${plataformaClass(p)}" style="font-size:10px;padding:2px 7px;">${plataformaLabel(p)}</span>`),
          j.gamepass ? `<span class="tag tag-gamepass">GAME PASS</span>` : "",
          j.psplus   ? `<span class="tag tag-psplus">PS PLUS</span>` : ""
        ].filter(Boolean).join("");

        const platsMetaHtml = j.plataformas.map(p => plataformaLabel(p)).join(" / ");

        const portadaHtml = j.imagen
          ? `<img class="ficha-portada" src="${j.imagen}" alt="Portada de ${j.titulo}" loading="lazy" onerror="this.remove()" onload="if(this.naturalWidth>this.naturalHeight)this.classList.add('apaisada')">`
          : "";

        return `
          <div class="juego-fila" id="fila-${j.id}" tabindex="0" role="button" aria-label="Ver ficha de ${j.titulo}" onclick="toggleFicha('${j.id}')" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();toggleFicha('${j.id}');}">
            <span class="juego-nombre">${j.titulo}</span>
            <div class="plataformas">${platsHtml}</div>
            ${nuevoHtml}
          </div>
          <div class="juego-ficha" id="ficha-${j.id}">
            <div class="ficha-header">
              <span class="ficha-titulo">${j.titulo}</span>
              <span class="ficha-cerrar" onclick="cerrarFicha('${j.id}')">[ CERRAR ]</span>
            </div>
            <div class="ficha-cuerpo">
              ${portadaHtml}
              <div class="ficha-info">
                <div class="ficha-meta">
                  <div>
                    <span class="ficha-campo-label">FECHA</span>
                    <span class="ficha-campo-valor">${diaNum} ${MESES_ES[fecha.getMonth()]} ${year}</span>
                    ${cuentaRegresivaHtml(j.fecha)}
                    ${j.relanzamiento ? `<span class="relanzamiento">↺ ${j.relanzamiento}</span>` : ""}
                  </div>
                  <div>
                    <span class="ficha-campo-label">PLATAFORMAS</span>
                    <span class="ficha-campo-valor">${platsMetaHtml}</span>
                  </div>
                  <div>
                    <span class="ficha-campo-label">GÉNERO</span>
                    <span class="ficha-campo-valor">${j.genero.join(" / ")}</span>
                  </div>
                  ${j.duracion ? `
                  <div>
                    <span class="ficha-campo-label">DURACIÓN</span>
                    <span class="ficha-campo-valor">${j.duracion}</span>
                  </div>` : ""}
                  <div>
                    <span class="ficha-campo-label">DESARROLLADOR</span>
                    <span class="ficha-campo-valor">${j.desarrollador}</span>
                  </div>
                  ${j.metacritic ? `
                  <div>
                    <span class="ficha-campo-label">METACRITIC</span>
                    <span class="badge-metacritic ${claseMetacritic(j.metacritic)}">${j.metacritic}</span>
                  </div>` : ""}
                </div>
                <p class="ficha-descripcion">${j.descripcion}</p>
              </div>
            </div>
            <div class="ficha-tags">${tagsHtml}</div>
            <div class="ficha-acciones">
              ${j.trailer ? `<button class="btn-trailer" onclick="abrirTrailer('${j.id}', event)">▶ VER TRAILER</button>` : ""}
              ${diasHasta(j.fecha) > 0 ? `<button class="btn-trailer" onclick="agendarJuego('${j.id}', event)">◷ AGENDAR</button>` : ""}
              <a href="juegos/${j.id}.html" class="btn-trailer">+ INFO</a>
            </div>
          </div>
        `;
      }).join("");

      return `
        <div class="dia ${esDiaFoco ? 'dia-foco' : ''}" id="dia-${diaKey}">
          <div class="dia-label ${esDiaHoy ? 'dia-label-hoy' : ''}">
            ${diaNombre} <span>${diaNum} ${mesNom}</span> ${indicador}
          </div>
          ${juegosHtml}
        </div>
      `;
    }).join("");

    return `
      <div class="mes" id="mes-${mesKey}">
        <div class="mes-header" tabindex="0" role="button" aria-expanded="${abierto}" onclick="toggleMes('${mesKey}')" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();toggleMes('${mesKey}');}">
          <span class="mes-arrow ${abierto ? 'abierto' : ''}" id="arrow-${mesKey}">▶</span>
          ${nombreMes}
          <span class="mes-contador">[ ${totalJuegos} JUEGO${totalJuegos !== 1 ? "S" : ""} ]</span>
        </div>
        <div class="mes-contenido ${abierto ? 'visible' : ''}" id="contenido-${mesKey}">
          ${diasHtml}
        </div>
      </div>
    `;
  }).join("");

  // scroll al día foco del mes actual
  if (agrupado[mesKeyHoy]) {
    const diasDelMes = Object.keys(agrupado[mesKeyHoy]).sort();
    const diaFoco = diaProximo(diasDelMes);
    setTimeout(() => {
      const el = document.getElementById(`dia-${diaFoco}`);
      if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 100);
  }
}

// ── TOGGLE MES ──
function toggleMes(mesKey) {
  const contenido = document.getElementById(`contenido-${mesKey}`);
  const arrow = document.getElementById(`arrow-${mesKey}`);
  const abierto = contenido.classList.toggle("visible");
  arrow.classList.toggle("abierto", abierto);
  const header = document.querySelector(`#mes-${CSS.escape(mesKey)} .mes-header`);
  if (header) header.setAttribute("aria-expanded", abierto);
}

// ── TOGGLE FICHA ──
function toggleFicha(id) {
  const ficha = document.getElementById(`ficha-${id}`);
  const fila = document.getElementById(`fila-${id}`);
  const estaAbierta = ficha.classList.contains("visible");

  // cerrar todas
  document.querySelectorAll(".juego-ficha").forEach(f => f.classList.remove("visible"));
  document.querySelectorAll(".juego-fila").forEach(f => f.classList.remove("abierto"));

  if (!estaAbierta) {
    ficha.classList.add("visible");
    fila.classList.add("abierto");
    setTimeout(() => ficha.scrollIntoView({ behavior: "smooth", block: "nearest" }), 50);
  }
}

function cerrarFicha(id) {
  document.getElementById(`ficha-${id}`).classList.remove("visible");
  document.getElementById(`fila-${id}`).classList.remove("abierto");
}

// ── MODAL TRAILER ──
function abrirTrailer(id, e) {
  e.stopPropagation();
  const juego = JUEGOS.find(j => j.id === id);
  if (!juego) return;
  document.getElementById("modal-titulo").textContent = juego.titulo;
  // autoplay solo aplica a embeds de YouTube; los videos de Steam (mp4) se cargan directo
  const esYoutube = juego.trailer.includes("youtube");
  document.getElementById("modal-iframe").src = esYoutube ? juego.trailer + "?autoplay=1" : juego.trailer;
  document.getElementById("modal-overlay").classList.add("visible");
}

function cerrarTrailer() {
  document.getElementById("modal-overlay").classList.remove("visible");
  document.getElementById("modal-iframe").src = "";
}

// cerrar modal con ESC o click fuera
document.addEventListener("keydown", e => {
  if (e.key === "Escape") cerrarTrailer();
});

// ── INIT ──
document.addEventListener("DOMContentLoaded", () => {
  // leer filtros combinables de la URL: ?plat=PS5&gen=RPG&q=texto&vista=ranking
  const params = new URLSearchParams(window.location.search);

  const platURL = params.get("plat");
  if (platURL && ["PS5","PS4","XBOX","SWITCH2","SWITCH"].includes(platURL)) {
    filtroActivo = platURL;
    document.querySelectorAll(".filtro-btn-plat").forEach(b => {
      b.classList.toggle("activo", b.dataset.plat === platURL);
    });
  }

  const genURL = (params.get("gen") || "").toUpperCase();
  if (genURL && JUEGOS.some(j => j.genero.includes(genURL))) {
    filtroGenero = genURL;
  }

  const qURL = params.get("q");
  if (qURL) {
    filtroTexto = qURL.trim().toLowerCase();
    const buscador = document.getElementById("buscador");
    if (buscador) buscador.value = qURL;
  }

  if (params.get("vista") === "ranking") {
    vistaActiva = "ranking";
    document.querySelectorAll(".vista-btn").forEach(b => {
      b.classList.toggle("activo", b.dataset.vista === "ranking");
    });
  }

  generarFiltrosGenero();
  renderCalendario();

  document.getElementById("modal-overlay").addEventListener("click", function(e) {
    if (e.target === this) cerrarTrailer();
  });

  // cerrar el modal del trailer con Escape
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") cerrarTrailer();
  });
});
