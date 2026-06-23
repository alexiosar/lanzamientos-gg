// ── ESTADO ──
let filtroActivo = "TODAS";

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
  if (p === "PS5")    return "plat-PS5";
  if (p === "XBOX")   return "plat-XBOX";
  if (p === "SWITCH2") return "plat-SWITCH2";
  return "plat-MULTI";
}

function plataformaLabel(p) {
  if (p === "SWITCH2") return "SWITCH 2";
  return p;
}

// ── FILTROS ──
function activarFiltro(plataforma) {
  filtroActivo = plataforma;
  document.querySelectorAll(".filtro-btn").forEach(b => {
    b.classList.toggle("activo", b.dataset.plat === plataforma);
  });
  renderCalendario();
}

// ── RENDER ──
function juegosFiltrados() {
  if (filtroActivo === "TODAS") return JUEGOS;
  return JUEGOS.filter(j => j.plataformas.includes(filtroActivo));
}

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
    contenedor.innerHTML = `<div class="sin-resultados">// NO HAY JUEGOS PARA ESTA PLATAFORMA AUN</div>`;
    return;
  }

  const agrupado = agruparPorMesYDia(juegos);
  const mesesOrdenados = Object.keys(agrupado).sort();

  contenedor.innerHTML = mesesOrdenados.map((mesKey, idx) => {
    const [year, month] = mesKey.split("-").map(Number);
    const nombreMes = `${MESES_ES[month - 1]} ${year}`;
    const diasOrdenados = Object.keys(agrupado[mesKey]).sort();
    const totalJuegos = diasOrdenados.reduce((acc, d) => acc + agrupado[mesKey][d].length, 0);
    const abierto = idx === 0;

    const diasHtml = diasOrdenados.map(diaKey => {
      const fecha = parseFecha(diaKey);
      const diaNombre = DIAS_ES[fecha.getDay()];
      const diaNum = String(fecha.getDate()).padStart(2, "0");
      const mesNom = MESES_ES[fecha.getMonth()].slice(0, 3);

      const juegosHtml = agrupado[mesKey][diaKey].map(j => {
        const platsHtml = j.plataformas.map(p =>
          `<span class="plat ${plataformaClass(p)}">${plataformaLabel(p)}</span>`
        ).join("");

        const nuevoHtml = j.nuevo ? `<span class="juego-nuevo">★ NUEVO</span>` : "";

        const tagsHtml = [
          ...j.genero.map(g => `<span class="tag">${g}</span>`),
          ...j.plataformas.map(p => `<span class="plat ${plataformaClass(p)}" style="font-size:10px;padding:2px 7px;">${plataformaLabel(p)}</span>`),
          j.gamepass ? `<span class="tag tag-gamepass">GAME PASS</span>` : "",
          j.psplus   ? `<span class="tag tag-psplus">PS PLUS</span>` : ""
        ].filter(Boolean).join("");

        const platsMetaHtml = j.plataformas.map(p => plataformaLabel(p)).join(" / ");

        return `
          <div class="juego-fila" id="fila-${j.id}" onclick="toggleFicha('${j.id}')">
            <span class="juego-nombre">${j.titulo}</span>
            <div class="plataformas">${platsHtml}</div>
            ${nuevoHtml}
          </div>
          <div class="juego-ficha" id="ficha-${j.id}">
            <div class="ficha-header">
              <span class="ficha-titulo">${j.titulo}</span>
              <span class="ficha-cerrar" onclick="cerrarFicha('${j.id}')">[ CERRAR ]</span>
            </div>
            <div class="ficha-meta">
              <div>
                <span class="ficha-campo-label">FECHA</span>
                <span class="ficha-campo-valor">${diaNum} ${MESES_ES[fecha.getMonth()]} ${year}</span>
              </div>
              <div>
                <span class="ficha-campo-label">PLATAFORMAS</span>
                <span class="ficha-campo-valor">${platsMetaHtml}</span>
              </div>
              <div>
                <span class="ficha-campo-label">GÉNERO</span>
                <span class="ficha-campo-valor">${j.genero.join(" / ")}</span>
              </div>
              <div>
                <span class="ficha-campo-label">DESARROLLADOR</span>
                <span class="ficha-campo-valor">${j.desarrollador}</span>
              </div>
            </div>
            <p class="ficha-descripcion">${j.descripcion}</p>
            <div class="ficha-tags">${tagsHtml}</div>
            <div class="ficha-acciones">
              <button class="btn-trailer" onclick="abrirTrailer('${j.id}', event)">▶ VER TRAILER</button>
              <a href="juegos/juego.html?id=${j.id}" class="btn-trailer">+ INFO</a>
            </div>
          </div>
        `;
      }).join("");

      return `
        <div class="dia">
          <div class="dia-label">${diaNombre} <span>${diaNum} ${mesNom}</span></div>
          ${juegosHtml}
        </div>
      `;
    }).join("");

    return `
      <div class="mes" id="mes-${mesKey}">
        <div class="mes-header" onclick="toggleMes('${mesKey}')">
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
}

// ── TOGGLE MES ──
function toggleMes(mesKey) {
  const contenido = document.getElementById(`contenido-${mesKey}`);
  const arrow = document.getElementById(`arrow-${mesKey}`);
  const abierto = contenido.classList.toggle("visible");
  arrow.classList.toggle("abierto", abierto);
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
  document.getElementById("modal-iframe").src = juego.trailer + "?autoplay=1";
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
  renderCalendario();

  document.getElementById("modal-overlay").addEventListener("click", function(e) {
    if (e.target === this) cerrarTrailer();
  });
});
