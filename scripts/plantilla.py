#!/usr/bin/env python3
"""La cabecera, el menú, el pie y el script de tema que comparten todas las páginas.

**Por qué existe.** Hasta el 02/09/2026 cada generador tenía su propia copia de los cuatro
bloques, y las páginas escritas a mano otra cada una: catorce fuentes de verdad para el mismo
HTML. Eso ya se cobró lo suyo, siempre de la misma forma —se toca el menú en trece lugares y
el catorceavo queda distinto—:

  · el 31/08/2026 /noticias salió sin el enlace a RECOMENDADOS. El reemplazo buscaba el
    enlace tal cual estaba en los otros archivos, y ahí llevaba `class="activo"`, así que no
    coincidió y esa página se quedó sin el enlace nuevo;
  · el mismo día /recomendados salió con el "volver" sin estilo, porque se armó copiando el
    molde de /noticias y la regla CSS vivía suelta en cada página;
  · el 01/09/2026 el enlace de Cafecito hubo que ponerlo en catorce lugares, y el primer
    intento lo metió adentro de un párrafo de /acerca.

Es el mismo problema que ya se resolvió del lado del CSS, cuando `.volver` se consolidó desde
once lugares y `.fila-plat` desde dos. Esto es la otra mitad.

**Qué NO cubre.** Las nueve páginas sueltas (index, archivo, acerca, api, widget, privacidad,
terminos, 404, mis-juegos) siguen con su copia a mano, porque el sitio no tiene proceso de
build y no hay dónde meterles esto sin convertirlas en generadas. Cubre los cinco
generadores, que son los que producen 386 de las 401 páginas. **Al cambiar el menú hay que
tocar acá y esas nueve.**

**La regla al tocar el menú:** se agrega en NAV y listo. No hace falta buscar el `<a>` en cada
archivo, que es exactamente lo que fallaba.
"""
import datetime

# El menú, en orden. La página que se está generando pasa su href como `activo` y ese enlace
# sale con class="activo"; el resto, sin nada.
NAV = [
    ("/", "INICIO"),
    ("/recomendados", "RECOMENDADOS"),
    ("/noticias", "NOTICIAS"),
    ("/ps5", "PS5"),
    ("/xbox", "XBOX"),
    ("/switch-2", "SWITCH 2"),
    ("/switch", "SWITCH"),
    ("/ps4", "PS4"),
]

TAGLINE = "▸ CALENDARIO DE VIDEOJUEGOS EN ESPAÑOL ◂"


def nav(activo=None):
    """Los <a> del menú, ya indentados para ir adentro de <nav class="nav">."""
    filas = []
    for href, etiqueta in NAV:
        act = ' class="activo"' if href == activo else ""
        filas.append(f'<a href="{href}"{act}>{etiqueta}</a>')
    return "\n        ".join(filas)


def cabecera(activo=None):
    """El <header> entero, listo para insertar en la plantilla (arranca con su sangría)."""
    return f'''  <header class="site-header">
    <div class="contenedor">
      <button class="btn-tema" onclick="toggleTema()" id="btn-tema" title="Cambiar tema" aria-label="Cambiar tema">☾</button>
      <a href="/" class="site-logo">LANZAMIENTOS.LAT</a>
      <span class="site-tagline">{TAGLINE}</span>
      <nav class="nav">
        {nav(activo)}
      </nav>
    </div>
  </header>'''


def pie(rss="/rss.xml"):
    """El <footer> entero.

    `rss` es lo único que cambia entre páginas: las fichas viven en /juegos/ y lo piden
    relativo. El año se calcula siempre — generar-fichas.py lo tenía escrito a mano como
    "2026", así que el 1 de enero las 371 fichas iban a decir el año pasado hasta que
    alguien lo notara.
    """
    anio = datetime.date.today().year
    return f'''  <footer class="site-footer">
    <div class="contenedor" style="display:flex; justify-content:space-between; width:100%; flex-wrap:wrap; gap:0.5rem;">
      <span>LANZAMIENTOS.LAT &copy; {anio}</span>
      <span class="footer-links"><a href="/acerca">ACERCA DE</a> · <a href="/api">API</a> · <a href="/widget">WIDGET</a> · <a href="/privacidad">PRIVACIDAD</a> · <a href="/terminos">TÉRMINOS</a> · <a href="{rss}">RSS</a> · <a href="https://cafecito.app/lanzamientos" target="_blank" rel="noopener">CAFECITO</a></span>
      <span>DATOS: STEAM · NINTENDO · METACRITIC · HLTB <span class="cursor"></span></span>
    </div>
  </footer>'''


def script_tema():
    """El bloque de tema claro/oscuro y el registro del service worker.

    Va SIN la etiqueta <script>: generar-fichas.py agrega más código propio adentro del mismo
    bloque (el enlace de volver, compartir, agendar), así que el envoltorio lo pone cada uno.

    Ojo con las llaves: acá van simples. Estas cadenas se insertan como VALOR en el f-string
    de cada generador, así que no vuelven a interpretarse y no hay que duplicarlas.
    """
    return '''    function toggleTema() {
      const claro = document.documentElement.classList.toggle("tema-claro");
      document.getElementById("btn-tema").textContent = claro ? "☀" : "☾";
      localStorage.setItem("tema", claro ? "claro" : "oscuro");
    }
    function aplicarTema(claro) {
      document.documentElement.classList.toggle("tema-claro", claro);
      document.getElementById("btn-tema").textContent = claro ? "☀" : "☾";
    }
    const temaGuardado = localStorage.getItem("tema");
    const sistemaClaro = window.matchMedia("(prefers-color-scheme: light)");
    aplicarTema(temaGuardado ? temaGuardado === "claro" : sistemaClaro.matches);
    sistemaClaro.addEventListener("change", ev => {
      if (!localStorage.getItem("tema")) aplicarTema(ev.matches);
    });
    if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");'''
