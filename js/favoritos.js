// ── FAVORITOS ──
//
// Una lista de juegos guardada en el navegador de quien visita. Sin cuentas y sin
// servidor, y ese es el punto: el sitio son archivos estáticos que Cloudflare sirve,
// y si algo se rompe se regenera todo desde datos/juegos.js. Meter cuentas rompería
// eso de raíz — base de datos, mails de recuperación, ser responsable de datos
// personales de terceros — y encima dejaría la función atrás de un registro que la
// mayoría no completa. Acá funciona desde el primer clic, para todos, y no agrega
// ni una línea de mantenimiento.
//
// Lo que se pierde es la sincronización entre dispositivos. Para eso está el link
// compartible de /mis-juegos (?lista=id,id,id): se copia de un aparato al otro a mano.
//
// localStorage tira excepción en Safari privado y con el almacenamiento bloqueado,
// así que TODOS los accesos van con try/catch: si falla, la función se apaga sola y
// el resto del sitio sigue andando igual.

const FAV_CLAVE = "favoritos";

function favLeer() {
  try {
    const crudo = JSON.parse(localStorage.getItem(FAV_CLAVE) || "[]");
    return Array.isArray(crudo) ? crudo.filter(x => typeof x === "string") : [];
  } catch (e) {
    return [];
  }
}

function favGuardar(lista) {
  try {
    localStorage.setItem(FAV_CLAVE, JSON.stringify(lista));
    return true;
  } catch (e) {
    return false;
  }
}

function favTiene(id) {
  return favLeer().indexOf(id) !== -1;
}

// Los ids guardados que todavía existen en el calendario. Un juego que se saca de
// datos/juegos.js —o que cambia de id, como pasó con gta-vi— deja un id huérfano que
// no se puede mostrar, y sin este filtro el menú contaría 9 mientras /mis-juegos
// lista 8.
//
// El huérfano NO se borra del almacenamiento a propósito: si juegos.js no cargó
// (conexión cortada, bloqueador), JUEGOS no existe y podar acá le vaciaría la lista
// a alguien por un problema de red. Se filtra al mostrar, que no rompe nada.
function favIds() {
  const guardados = favLeer();
  if (typeof JUEGOS === "undefined" || !Array.isArray(JUEGOS)) return guardados;
  return guardados.filter(id => JUEGOS.some(j => j.id === id));
}

function favEnMisJuegos() {
  return location.pathname.replace(/\.html$/, "").replace(/\/$/, "") === "/mis-juegos";
}

// ── BOTÓN ──
// Dos formas del mismo botón: sola la estrella para las filas del calendario, donde
// el espacio es de una línea, y con texto donde va al lado de AGENDAR y COMPARTIR y
// tiene que pesar lo mismo que ellos.
// Los ids son slugs (a-z, 0-9 y guiones), así que entran sin escapar en el onclick.
function favBotonHtml(id, conTexto) {
  const guardado = favTiene(id);
  const contenido = conTexto
    ? (guardado ? "★ GUARDADO EN MIS JUEGOS" : "☆ GUARDAR EN MIS JUEGOS")
    : (guardado ? "★" : "☆");
  return `<button class="btn-fav${guardado ? " activo" : ""}" data-fav="${id}"` +
         (conTexto ? ' data-fav-texto=""' : "") +
         ` onclick="favAlternar('${id}', event)" aria-pressed="${guardado}"` +
         ` title="${guardado ? "Quitar de MIS JUEGOS" : "Guardar en MIS JUEGOS"}"` +
         ` aria-label="${guardado ? "Quitar de mis juegos" : "Guardar en mis juegos"}">` +
         `${contenido}</button>`;
}

// Repinta todos los botones de la página. Se llama al tocar uno (para que la ficha
// desplegable y la fila del calendario no queden diciendo cosas distintas del mismo
// juego) y cuando otra pestaña cambia la lista.
function favPintar() {
  const lista = favLeer();
  document.querySelectorAll("[data-fav]").forEach(b => {
    const guardado = lista.indexOf(b.dataset.fav) !== -1;
    b.classList.toggle("activo", guardado);
    // El botón de la ficha de juego lleva texto además de la estrella.
    b.textContent = "favTexto" in b.dataset
      ? (guardado ? "★ GUARDADO EN MIS JUEGOS" : "☆ GUARDAR EN MIS JUEGOS")
      : (guardado ? "★" : "☆");
    b.setAttribute("aria-pressed", guardado);
    b.title = guardado ? "Quitar de MIS JUEGOS" : "Guardar en MIS JUEGOS";
    b.setAttribute("aria-label", guardado ? "Quitar de mis juegos" : "Guardar en mis juegos");
  });
}

function favAlternar(id, ev) {
  if (ev) { ev.stopPropagation(); ev.preventDefault(); }
  const lista = favLeer();
  const i = lista.indexOf(id);
  const agregado = i === -1;
  if (agregado) lista.push(id); else lista.splice(i, 1);

  if (!favGuardar(lista)) {
    favAviso("NO SE PUDO GUARDAR — REVISÁ SI EL NAVEGADOR BLOQUEA EL ALMACENAMIENTO", false);
    return;
  }

  favPintar();
  favNav();
  favAviso(agregado ? "GUARDADO EN MIS JUEGOS" : "QUITADO DE MIS JUEGOS", agregado);
  // /mis-juegos se vuelve a dibujar sola cuando sacás algo desde ahí
  if (typeof favAlCambiar === "function") favAlCambiar();
}

// ── ENLACE EN EL MENÚ ──
// Aparece recién cuando hay algo guardado: quien no usa la función no ve un menú más
// largo, y quien guarda su primer juego ve dónde fue a parar sin que se lo expliquen.
function favNav() {
  const nav = document.querySelector(".nav");
  if (!nav) return;
  const n = favIds().length;
  let link = document.getElementById("nav-mis-juegos");

  if (!n && !favEnMisJuegos()) {
    if (link) link.remove();
    return;
  }
  if (!link) {
    link = document.createElement("a");
    link.id = "nav-mis-juegos";
    link.href = "/mis-juegos";
    if (favEnMisJuegos()) link.className = "activo";
    const noticias = nav.querySelector('a[href="/noticias"]');
    if (noticias) noticias.after(link); else nav.appendChild(link);
  }
  link.textContent = n ? `★ MIS JUEGOS (${n})` : "★ MIS JUEGOS";
}

// ── AVISO ──
let favAvisoTimer = null;
function favAviso(texto, conLink) {
  let caja = document.getElementById("fav-aviso");
  if (!caja) {
    caja = document.createElement("div");
    caja.id = "fav-aviso";
    caja.className = "fav-aviso";
    caja.setAttribute("role", "status");
    document.body.appendChild(caja);
  }
  caja.textContent = texto;
  if (conLink && !favEnMisJuegos()) {
    caja.insertAdjacentHTML("beforeend", ' · <a href="/mis-juegos">VER LISTA ▸</a>');
  }
  caja.classList.add("visible");
  clearTimeout(favAvisoTimer);
  favAvisoTimer = setTimeout(() => caja.classList.remove("visible"), 2800);
}

// ── AGENDAR TODOS (.ics) ──
// Un solo archivo con un evento de día completo por juego. Es lo que reemplaza a la
// notificación por mail que traerían las cuentas: el recordatorio lo da el calendario
// que la persona ya usa, y no hay que mantener un sistema de envíos.
function favEscIcs(t) {
  return String(t).replace(/\\/g, "\\\\").replace(/[,;]/g, m => "\\" + m).replace(/\n/g, "\\n");
}

function favIcs(juegos) {
  const ahora = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
  const etiqueta = p => p === "SWITCH2" ? "SWITCH 2" : p;
  const lineas = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//lanzamientos.lat//Calendario de Videojuegos//ES",
    "X-WR-CALNAME:Mis juegos — LANZAMIENTOS.LAT"
  ];
  juegos.forEach(j => {
    const [y, m, d] = j.fecha.split("-").map(Number);
    const fin = new Date(y, m - 1, d + 1);
    const finStr = `${fin.getFullYear()}${String(fin.getMonth() + 1).padStart(2, "0")}${String(fin.getDate()).padStart(2, "0")}`;
    lineas.push(
      "BEGIN:VEVENT",
      `UID:${j.id}@lanzamientos.lat`,
      `DTSTAMP:${ahora}`,
      `DTSTART;VALUE=DATE:${j.fecha.replace(/-/g, "")}`,
      `DTEND;VALUE=DATE:${finStr}`,
      `SUMMARY:${favEscIcs("🎮 Sale " + j.titulo)}`,
      `DESCRIPTION:${favEscIcs("Lanzamiento en " + j.plataformas.map(etiqueta).join(" / ") + ". Ficha: " + location.origin + "/juegos/" + j.id)}`,
      `URL:${location.origin}/juegos/${j.id}`,
      "END:VEVENT"
    );
  });
  lineas.push("END:VCALENDAR");
  return lineas.join("\r\n");
}

function favDescargar(texto, nombre, tipo) {
  const blob = new Blob([texto], { type: tipo });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = nombre;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(a.href);
}

// ── ARRANQUE ──
// Otra pestaña abierta en el mismo sitio: si ahí guardan un juego, acá se refleja.
window.addEventListener("storage", e => {
  if (e.key !== FAV_CLAVE) return;
  favPintar();
  favNav();
  if (typeof favAlCambiar === "function") favAlCambiar();
});

document.addEventListener("DOMContentLoaded", () => {
  favPintar();
  favNav();
});
