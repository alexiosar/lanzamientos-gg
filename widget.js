/**
 * Widget embebible de LANZAMIENTOS.LAT
 * https://lanzamientos.lat/widget
 *
 * Se pega una sola línea en cualquier sitio y muestra los próximos lanzamientos
 * de videojuegos, con un enlace de vuelta al calendario.
 *
 *   <script src="https://lanzamientos.lat/widget.js" data-plataforma="PS5" data-cantidad="5"></script>
 *
 * Decisiones que importan para quien lo instala:
 * - Se dibuja donde está la etiqueta <script>, sin iframe: hereda el ancho del
 *   contenedor y no rompe el diseño de la página que lo aloja.
 * - Se dibuja dentro de un Shadow DOM: el CSS del sitio anfitrión no puede entrar
 *   ni el nuestro salir. Los estilos en línea NO alcanzan, porque una regla del
 *   anfitrión con !important los pisa (probado el 06/08/2026 contra una página con
 *   `a { color: crimson !important }`: los enlaces salían rojos y subrayados).
 * - No usa cookies, no guarda nada y no rastrea a nadie. Una sola petición GET
 *   a un JSON estático.
 * - Si la petición falla, el widget no muestra nada roto: deja un enlace al sitio.
 */
(function () {
  "use strict";

  var script = document.currentScript;
  if (!script) return;

  var API = "https://lanzamientos.lat/api/proximos.json";
  var SITIO = "https://lanzamientos.lat";

  var cantidad = parseInt(script.getAttribute("data-cantidad"), 10);
  if (!cantidad || cantidad < 1 || cantidad > 20) cantidad = 5;

  var plataforma = (script.getAttribute("data-plataforma") || "").toUpperCase();
  var VALIDAS = ["PS5", "PS4", "XBOX", "SWITCH2", "SWITCH"];
  if (VALIDAS.indexOf(plataforma) === -1) plataforma = "";

  var tema = script.getAttribute("data-tema") === "claro" ? "claro" : "oscuro";

  var c = tema === "claro"
    ? { fondo: "#ffffff", borde: "#d8d8d8", texto: "#111111", suave: "#666666", acento: "#3333cc" }
    : { fondo: "#000000", borde: "#333333", texto: "#ffffff", suave: "#999999", acento: "#a0a0ff" };

  var MESES = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN",
               "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"];

  var host = document.createElement("div");
  host.setAttribute("data-lanzamientos-lat", "");
  host.style.cssText = "all:initial;display:block;max-width:100%";
  script.parentNode.insertBefore(host, script.nextSibling);

  var raiz = host.attachShadow ? host.attachShadow({ mode: "open" }) : host;
  var contenedor = document.createElement("div");
  contenedor.className = "ll-caja";
  var hoja = document.createElement("style");
  hoja.textContent =
    ".ll-caja{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;" +
    "font-size:13px;line-height:1.5;font-style:normal;letter-spacing:normal;" +
    "border-radius:0;background:" + c.fondo + ";color:" + c.texto + ";" +
    "border:1px solid " + c.borde + ";padding:14px;box-sizing:border-box}" +
    ".ll-tit{font-size:11px;letter-spacing:2px;color:" + c.suave + ";margin-bottom:10px}" +
    ".ll-fila{display:flex;gap:10px;align-items:baseline;padding:5px 0;" +
    "color:" + c.texto + ";text-decoration:none;border-bottom:1px solid " + c.borde + "}" +
    ".ll-fila:hover .ll-nom{color:" + c.acento + "}" +
    ".ll-fecha{color:" + c.suave + ";font-size:11px;white-space:nowrap;min-width:48px}" +
    ".ll-nom{flex:1;min-width:0;overflow-wrap:anywhere}" +
    ".ll-plat{color:" + c.acento + ";font-size:11px;white-space:nowrap}" +
    ".ll-pie{margin-top:12px;padding-top:10px;border-top:1px solid " + c.borde + ";" +
    "font-size:11px;letter-spacing:1px}" +
    ".ll-pie a{color:" + c.acento + ";text-decoration:none}" +
    ".ll-vacio{color:" + c.suave + "}";
  raiz.appendChild(hoja);
  raiz.appendChild(contenedor);

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (m) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m];
    });
  }

  function fecha(f) {
    var p = f.split("-");
    return parseInt(p[2], 10) + " " + MESES[parseInt(p[1], 10) - 1];
  }

  function etiqueta(p) {
    return p === "SWITCH2" ? "SWITCH 2" : p;
  }

  function pie() {
    return '<div class="ll-pie"><a href="' + SITIO + '" target="_blank" rel="noopener">' +
      "LANZAMIENTOS.LAT ▸</a></div>";
  }

  function pintar(juegos) {
    var titulo = plataforma ? "PRÓXIMOS EN " + etiqueta(plataforma) : "PRÓXIMOS LANZAMIENTOS";
    var html = '<div class="ll-tit">' + titulo + "</div>";

    if (!juegos.length) {
      html += '<div class="ll-vacio">Sin lanzamientos próximos.</div>';
    } else {
      juegos.forEach(function (j) {
        html += '<a class="ll-fila" href="' + esc(j.url) + '" target="_blank" rel="noopener">' +
          '<span class="ll-fecha">' + fecha(j.fecha) + "</span>" +
          '<span class="ll-nom">' + esc(j.titulo) + "</span>" +
          '<span class="ll-plat">' + esc(j.plataformas.map(etiqueta).join(" ")) + "</span></a>";
      });
    }
    contenedor.innerHTML = html + pie();
  }

  fetch(API, { mode: "cors" })
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(function (d) {
      // El JSON se regenera una vez por día, pero el sitio puede quedar sin publicar
      // un par de días. Sin este filtro el widget mostraría juegos ya salidos en la
      // web de otra persona, que es la forma más rápida de que lo saquen.
      var hoy = new Date();
      var iso = hoy.getFullYear() + "-" +
        String(hoy.getMonth() + 1).padStart(2, "0") + "-" +
        String(hoy.getDate()).padStart(2, "0");
      var lista = d.juegos.filter(function (j) {
        return !j.estimado && j.fecha >= iso &&
          (!plataforma || j.plataformas.indexOf(plataforma) !== -1);
      });
      pintar(lista.slice(0, cantidad));
    })
    .catch(function () {
      // Nunca dejar un bloque roto en el sitio de otro: al menos el enlace
      contenedor.innerHTML = '<div class="ll-tit">PRÓXIMOS LANZAMIENTOS</div>' + pie();
    });
})();
