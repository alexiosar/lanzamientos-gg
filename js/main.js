// ── ESTADO ──
let filtroActivo = "TODAS";
let filtroGenero = "TODOS";
let filtroTexto = "";
let vistaActiva = "calendario";
let rankingPeriodo = "todo"; // todo | mes | 30dias

// archivo.html declara data-archivo en el body: muestra solo meses pasados
const MODO_ARCHIVO = !!(document.body && document.body.dataset.archivo);

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
    `DESCRIPTION:${esc("Lanzamiento en " + j.plataformas.map(plataformaLabel).join(" / ") + ". Ficha: " + location.origin + "/juegos/" + j.id)}`,
    `URL:${location.origin}/juegos/${j.id}`,
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

// miniatura de carátula para filas de listas (cuadrada, carga diferida)
// Los pseudo-elementos no se aplican sobre un <img>, así que cuando una carátula
// falla se cambia el elemento por un <span> y el marcador se ve igual que cuando
// el juego directamente no tiene imagen cargada.
function sinCaratula(el, clases) {
  const s = document.createElement("span");
  s.className = clases;
  el.replaceWith(s);
}

function miniaturaHtml(j) {
  return j.imagen
    ? `<img class="mini-portada" src="${j.imagen}" alt="" loading="lazy" decoding="async" onerror="sinCaratula(this,'mini-portada mini-vacia')">`
    : `<span class="mini-portada mini-vacia"></span>`;
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
  const contenedor = document.getElementById("filtros-genero");
  if (!contenedor) return; // archivo.html no tiene filtros
  // solo géneros de juegos visibles en la portada (mes actual en adelante),
  // para no ofrecer filtros que quedarían vacíos por el archivo
  const mesActual = getMesKeyHoy();
  const generos = new Set();
  JUEGOS.filter(j => j.fecha.slice(0, 7) >= mesActual)
        .forEach(j => j.genero.forEach(g => generos.add(g)));
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
function cambiarPeriodoRanking(periodo) {
  rankingPeriodo = periodo;
  renderCalendario();
}

function renderRanking(juegos) {
  const hoy = getDiaKeyHoy();
  const hace30 = parseFecha(hoy);
  hace30.setDate(hace30.getDate() - 30);
  const limite30 = `${hace30.getFullYear()}-${String(hace30.getMonth() + 1).padStart(2, "0")}-${String(hace30.getDate()).padStart(2, "0")}`;

  const enPeriodo = j =>
    rankingPeriodo === "mes"    ? j.fecha.slice(0, 7) === getMesKeyHoy() :
    rankingPeriodo === "30dias" ? j.fecha >= limite30 && j.fecha <= hoy :
    true;

  // Solo juegos ya lanzados: algunos ports traen el puntaje del original y sin este
  // filtro encabezarían el ranking sin haber salido todavía (el puntaje sí se muestra
  // en la ficha del juego, que es donde tiene sentido).
  const conPuntaje = juegos
    .filter(j => j.metacritic && j.fecha <= hoy && enPeriodo(j))
    .sort((a, b) => b.metacritic - a.metacritic);

  const selectorHtml = `
    <div class="ranking-periodos">
      ${[["todo", "TODO EL CALENDARIO"], ["mes", "ESTE MES"], ["30dias", "ÚLTIMOS 30 DÍAS"]].map(([clave, label]) =>
        `<button class="filtro-btn ${rankingPeriodo === clave ? "activo" : ""}" onclick="cambiarPeriodoRanking('${clave}')">${label}</button>`
      ).join("")}
    </div>`;

  if (conPuntaje.length === 0) {
    return selectorHtml + `<div class="sin-resultados">// NINGÚN JUEGO CON PUNTAJE PARA ESTE FILTRO</div>`;
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
        ${miniaturaHtml(j)}
        <span class="badge-metacritic ${claseMetacritic(j.metacritic)}">${j.metacritic}</span>
        <span class="juego-nombre">${j.titulo}</span>
        <span class="ranking-fecha">${fechaStr}</span>
        <div class="plataformas">${platsHtml}</div>
      </a>`;
  }).join("");

  return selectorHtml + `
    <div class="ranking">
      <div class="ranking-header">★ MEJOR PUNTUADOS <span class="mes-contador">[ ${conPuntaje.length} JUEGO${conPuntaje.length !== 1 ? "S" : ""} · METACRITIC ]</span></div>
      ${filas}
    </div>`;
}

// ── FICHA DESPLEGABLE ──
// se usa tanto en los días del calendario como en el bloque de fechas estimadas
function fichaHtml(j) {
  const f = parseFecha(j.fecha);
  const tagsHtml = [
    ...j.genero.map(g => `<span class="tag">${g}</span>`),
    ...j.plataformas.map(p => `<span class="plat ${plataformaClass(p)}" style="font-size:0.6875rem;padding:2px 7px;">${plataformaLabel(p)}</span>`),
    j.gamepass ? `<span class="tag tag-gamepass">GAME PASS</span>` : "",
    j.psplus   ? `<span class="tag tag-psplus">PS PLUS</span>` : ""
  ].filter(Boolean).join("");

  const portadaHtml = j.imagen
    ? `<img class="ficha-portada" src="${j.imagen}" alt="Portada de ${j.titulo}" loading="lazy" onerror="this.remove()" onload="if(this.naturalWidth>this.naturalHeight)this.classList.add('apaisada')">`
    : "";

  // los estimados muestran el mes anunciado, sin cuenta regresiva ni botón de agendar
  const fechaHtml = j.estimado
    ? `<span class="ficha-campo-valor">${j.fechaEstimada || MESES_ES[f.getMonth()] + " " + f.getFullYear()}</span>
       <span class="relanzamiento">◔ FECHA EXACTA SIN CONFIRMAR</span>`
    : `<span class="ficha-campo-valor">${String(f.getDate()).padStart(2, "0")} ${MESES_ES[f.getMonth()]} ${f.getFullYear()}</span>
       ${cuentaRegresivaHtml(j.fecha)}`;

  return `
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
                    ${fechaHtml}
                    ${j.relanzamiento ? `<span class="relanzamiento">↺ ${j.relanzamiento}</span>` : ""}
                  </div>
                  <div>
                    <span class="ficha-campo-label">PLATAFORMAS</span>
                    <span class="ficha-campo-valor">${j.plataformas.map(plataformaLabel).join(" / ")}</span>
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
              ${!j.estimado && diasHasta(j.fecha) > 0 ? `<button class="btn-trailer" onclick="agendarJuego('${j.id}', event)">◷ AGENDAR</button>` : ""}
              <button class="btn-trailer" onclick="compartirJuego('${j.id}', event)">⇗ COMPARTIR</button>
              <a href="juegos/${j.id}.html" class="btn-trailer">+ INFO</a>
            </div>
          </div>`;
}

// ── VISTA GRILLA ──
// mosaico de carátulas ordenado por fecha
function renderGrilla(juegos) {
  const hoyKey = getDiaKeyHoy();
  const orden = [...juegos].sort((a, b) => a.fecha.localeCompare(b.fecha));

  const tarjetas = orden.map(j => {
    const f = parseFecha(j.fecha);
    const fechaCorta = j.estimado
      ? (j.fechaEstimada || `${MESES_ES[f.getMonth()]} ${f.getFullYear()}`)
      : `${DIAS_ES[f.getDay()]} ${String(f.getDate()).padStart(2, "0")} ${MESES_ES[f.getMonth()].slice(0, 3)}`;

    const portada = j.imagen
      ? `<img class="grilla-portada" src="${j.imagen}" alt="Portada de ${j.titulo}" loading="lazy" decoding="async" onerror="sinCaratula(this,'grilla-portada grilla-vacia')">`
      : `<span class="grilla-portada grilla-vacia"></span>`;

    const badge = j.metacritic
      ? `<span class="grilla-nota badge-metacritic ${claseMetacritic(j.metacritic)}">${j.metacritic}</span>`
      : "";

    const hoyTag = j.fecha === hoyKey ? `<span class="grilla-hoy">HOY</span>` : "";

    return `
      <a class="grilla-item" href="juegos/${j.id}.html">
        <div class="grilla-marco">
          ${portada}
          ${badge}
          ${hoyTag}
        </div>
        <span class="grilla-fecha">${fechaCorta}</span>
        <span class="grilla-titulo">${j.titulo}</span>
        <div class="plataformas">${j.plataformas.map(p =>
          `<span class="plat ${plataformaClass(p)}">${plataformaLabel(p)}</span>`).join("")}</div>
      </a>`;
  }).join("");

  return `<div class="grilla">${tarjetas}</div>`;
}

// ── JUEGOS FILTRADOS ──
function juegosFiltrados() {
  return JUEGOS.filter(j => {
    const porPlat  = filtroActivo === "TODAS" || j.plataformas.includes(filtroActivo);
    const porGen   = filtroGenero === "TODOS"  || j.genero.includes(filtroGenero);
    // busca en título, desarrollador y géneros
    const pajar = `${j.titulo} ${j.desarrollador} ${j.genero.join(" ")}`.toLowerCase();
    const porTexto = filtroTexto === "" || pajar.includes(filtroTexto);
    return porPlat && porGen && porTexto;
  });
}

// ── COMPARTIR ──
// en el celular abre el menú nativo; en desktop copia el link al portapapeles
function compartirJuego(id, e) {
  if (e) e.stopPropagation();
  const j = JUEGOS.find(x => x.id === id);
  if (!j) return;
  const url = location.origin + "/juegos/" + j.id;
  if (navigator.share) {
    navigator.share({ title: `${j.titulo} — LANZAMIENTOS.LAT`, url }).catch(() => {});
  } else {
    navigator.clipboard.writeText(url).then(() => {
      const btn = e && e.target;
      if (btn) {
        const original = btn.textContent;
        btn.textContent = "✓ LINK COPIADO";
        setTimeout(() => { btn.textContent = original; }, 1600);
      }
    });
  }
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
  let juegos = juegosFiltrados();

  // el ranking siempre considera todos los meses (incluido el archivo)
  if (vistaActiva === "ranking") {
    contenedor.innerHTML = juegos.length
      ? renderRanking(juegos)
      : `<div class="sin-resultados">// NO HAY JUEGOS PARA ESTE FILTRO</div>`;
    return;
  }

  // portada: mes actual en adelante; archivo: solo meses anteriores
  const mesActual = getMesKeyHoy();
  juegos = juegos.filter(j => MODO_ARCHIVO ? j.fecha.slice(0, 7) < mesActual : j.fecha.slice(0, 7) >= mesActual);

  if (juegos.length === 0) {
    const hayEnArchivo = !MODO_ARCHIVO && juegosFiltrados().some(j => j.fecha.slice(0, 7) < mesActual);
    contenedor.innerHTML = `<div class="sin-resultados">// NO HAY JUEGOS PRÓXIMOS PARA ESTE FILTRO${
      hayEnArchivo ? ` — <a href="archivo.html${window.location.search}">BUSCAR EN EL ARCHIVO →</a>` : ""}</div>`;
    return;
  }

  if (vistaActiva === "grilla") {
    contenedor.innerHTML = renderGrilla(juegos);
    return;
  }

  // los juegos sin fecha confirmada van a un bloque aparte al final de su mes
  const estimadosPorMes = {};
  juegos.filter(j => j.estimado).forEach(j => {
    const mk = j.fecha.slice(0, 7);
    (estimadosPorMes[mk] = estimadosPorMes[mk] || []).push(j);
  });

  const agrupado = agruparPorMesYDia(juegos.filter(j => !j.estimado));
  // meses que solo tienen juegos estimados también deben aparecer
  Object.keys(estimadosPorMes).forEach(mk => { agrupado[mk] = agrupado[mk] || {}; });
  const mesesOrdenados = Object.keys(agrupado).sort();
  const mesKeyHoy = getMesKeyHoy();

  // el día PRÓXIMO es el primer día con lanzamientos posterior a hoy (en cualquier mes)
  const hoyKey = getDiaKeyHoy();
  const todosLosDias = mesesOrdenados.flatMap(m => Object.keys(agrupado[m])).sort();
  const proximoKey = todosLosDias.find(d => d > hoyKey) || null;

  // juego DESTACADO: el próximo lanzamiento notable (con noticias); si no hay, el próximo con carátula.
  // solo en la portada y sin filtros activos
  let destacadoHtml = "";
  const sinFiltros = filtroActivo === "TODAS" && filtroGenero === "TODOS" && filtroTexto === "";
  if (!MODO_ARCHIVO && sinFiltros) {
    const futuros = JUEGOS.filter(j => !j.estimado && j.fecha > hoyKey).sort((a, b) => a.fecha.localeCompare(b.fecha));
    const dest = futuros.find(j => j.noticias && j.imagen) || futuros.find(j => j.imagen);
    if (dest) {
      const f = parseFecha(dest.fecha);
      destacadoHtml = `
      <a class="destacado" href="juegos/${dest.id}.html">
        <img class="destacado-portada" src="${dest.imagen}" alt="Portada de ${dest.titulo}" onerror="this.remove()">
        <div class="destacado-info">
          <span class="destacado-tag">▸ PRÓXIMO DESTACADO</span>
          <span class="destacado-titulo">${dest.titulo}</span>
          <span class="destacado-meta">${DIAS_ES[f.getDay()]} ${String(f.getDate()).padStart(2, "0")} ${MESES_ES[f.getMonth()].slice(0, 3)} · ${dest.plataformas.map(plataformaLabel).join(" / ")}</span>
          ${cuentaRegresivaHtml(dest.fecha)}
        </div>
      </a>`;
    }
  }

  // bloque PRÓXIMOS 7 DÍAS (lanzamientos entre mañana y dentro de una semana)
  const en7 = parseFecha(hoyKey);
  en7.setDate(en7.getDate() + 7);
  const limite7 = `${en7.getFullYear()}-${String(en7.getMonth() + 1).padStart(2, "0")}-${String(en7.getDate()).padStart(2, "0")}`;
  const proximos7 = juegos
    .filter(j => !j.estimado && j.fecha > hoyKey && j.fecha <= limite7)
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
          ${miniaturaHtml(j)}
          <span class="proximos-dia">${dia}</span>
          <span class="juego-nombre">${j.titulo}</span>
          <div class="plataformas">${plats}</div>
        </a>`;
      }).join("")}
    </div>` : "";

  // link al archivo (solo en la portada, si hay meses pasados)
  const hayArchivo = !MODO_ARCHIVO && JUEGOS.some(j => j.fecha.slice(0, 7) < mesActual);
  const archivoHtml = hayArchivo
    ? `<a class="link-archivo" href="archivo.html">≡ LANZAMIENTOS DE MESES ANTERIORES → VER ARCHIVO</a>`
    : "";

  contenedor.innerHTML = destacadoHtml + proximosHtml + archivoHtml + mesesOrdenados.map((mesKey, idx) => {
    const [year, month] = mesKey.split("-").map(Number);
    const nombreMes = `${MESES_ES[month - 1]} ${year}`;
    const diasOrdenados = Object.keys(agrupado[mesKey]).sort();
    const totalJuegos = diasOrdenados.reduce((acc, d) => acc + agrupado[mesKey][d].length, 0);
    
    // abrir solo el mes actual, cerrar el resto (si hay búsqueda, abrir todos);
    // en el archivo se abre el mes más reciente
    const abierto = MODO_ARCHIVO
      ? mesKey === mesesOrdenados[mesesOrdenados.length - 1] || filtroTexto !== ""
      : mesKey === mesKeyHoy || filtroTexto !== "";

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

        return `
          <div class="juego-fila" id="fila-${j.id}" tabindex="0" role="button" aria-label="Ver ficha de ${j.titulo}" onclick="toggleFicha('${j.id}')" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();toggleFicha('${j.id}');}">
            ${miniaturaHtml(j)}
            <span class="juego-nombre">${j.titulo}</span>
            <div class="plataformas">${platsHtml}</div>
            ${nuevoHtml}
          </div>
          ${fichaHtml(j)}
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

    // bloque de juegos anunciados para el mes pero sin día confirmado
    const estimados = estimadosPorMes[mesKey] || [];
    const estimadosHtml = estimados.length ? `
          <div class="dia dia-estimado">
            <div class="dia-label">SIN FECHA CONFIRMADA <span class="dia-estimado-tag">[ ${estimados[0].fechaEstimada || nombreMes} ]</span></div>
            ${estimados.map(j => {
              const plats = j.plataformas.map(p =>
                `<span class="plat ${plataformaClass(p)}">${plataformaLabel(p)}</span>`
              ).join("");
              return `
            <div class="juego-fila" id="fila-${j.id}" tabindex="0" role="button" aria-label="Ver ficha de ${j.titulo}" onclick="toggleFicha('${j.id}')" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();toggleFicha('${j.id}');}">
              ${miniaturaHtml(j)}
              <span class="juego-nombre">${j.titulo}</span>
              ${j.nuevo ? `<span class="juego-nuevo">★ NUEVO</span>` : ""}
              <div class="plataformas">${plats}</div>
            </div>
            ${fichaHtml(j)}`;
            }).join("")}
          </div>` : "";

    return `
      <div class="mes" id="mes-${mesKey}">
        <div class="mes-header" tabindex="0" role="button" aria-expanded="${abierto}" onclick="toggleMes('${mesKey}')" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();toggleMes('${mesKey}');}">
          <span class="mes-arrow ${abierto ? 'abierto' : ''}" id="arrow-${mesKey}">▶</span>
          ${nombreMes}
          <span class="mes-contador">[ ${totalJuegos + estimados.length} JUEGO${(totalJuegos + estimados.length) !== 1 ? "S" : ""} ]</span>
        </div>
        <div class="mes-contenido ${abierto ? 'visible' : ''}" id="contenido-${mesKey}">
          ${diasHtml}${estimadosHtml}
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

  const vistaURL = params.get("vista");
  if (vistaURL === "ranking" || vistaURL === "grilla") {
    vistaActiva = vistaURL;
    document.querySelectorAll(".vista-btn").forEach(b => {
      b.classList.toggle("activo", b.dataset.vista === vistaURL);
    });
  }

  generarFiltrosGenero();
  renderCalendario();

  const overlay = document.getElementById("modal-overlay");
  if (overlay) overlay.addEventListener("click", function(e) {
    if (e.target === this) cerrarTrailer();
  });

  // cerrar el modal del trailer con Escape
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") cerrarTrailer();
  });
});
