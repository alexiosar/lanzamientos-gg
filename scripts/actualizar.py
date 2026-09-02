#!/usr/bin/env python3
"""Mantenimiento diario de lanzamientos.lat en un solo comando.

Hace la parte mecánica de la rutina:
  1. Busca en Metacritic los puntajes de juegos lanzados que siguen sin puntaje
     y los aplica a datos/juegos.js.
  2. Regenera las fichas estáticas y el sitemap.
  3. Imprime un reporte: puntajes nuevos, lanzamientos de hoy/mañana (candidatos
     a noticias), y qué falta (trailers, carátulas, duraciones).

Uso (desde la raíz del proyecto):
    python3 scripts/actualizar.py

Después del script: cargar noticias si hay, commit y deploy.
"""
import datetime
import re
import ssl
import subprocess
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO = RAIZ / "datos" / "juegos.js"
CTX = ssl._create_unverified_context()
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20, context=CTX).read().decode("utf-8", "replace")


# Cuántos días se sigue refrescando el puntaje de usuarios de un juego ya lanzado.
DIAS_REFRESCO = 90
# Debajo de esta cantidad de votos el puntaje de usuarios no se muestra en la ficha.
# Lo pone generar-fichas.py; acá está sólo para avisarlo en el reporte.
MIN_VOTOS = 20


def metascore(html):
    """El puntaje de crítica que muestra la página, para verificar que es el juego.

    Anclado al marcador propio del juego y no a la primera aparición del atributo. La página
    trae unas 24 apariciones de `title="Metascore N out of 100"`: la del juego y las de los
    carruseles de recomendados, ordenadas de mayor a menor. Cuando el juego TIENE puntaje la
    suya va primera y las dos lecturas coinciden, pero cuando dice "Metascore TBD" —todavía
    sin reseñas suficientes— la primera aparición es la del carrusel. Así, el 28/08/2026,
    Grounded 2 parecía tener 93 y Dungeon Antiqua 95, que eran los primeros de sus listas de
    recomendados. Ninguno de los dos tiene puntaje.

    Importa porque este valor no sólo verifica: también reescribe `metacritic` cuando cambió.
    Un juego nuestro que pase a TBD en Metacritic se habría llevado el puntaje de otro.
    """
    i = html.find('data-testid="global-score"')
    if i == -1:
        return None
    # La PRIMERA aparición después del ancla, aceptando "TBD" como valor: si sólo se
    # buscaran dígitos, un "Metascore TBD" no matchea y la búsqueda sigue de largo hasta
    # el primer número del carrusel, que es el error que se quería evitar.
    m = re.search(r'title="Metascore (TBD|\d+)', html[i:i + 600])
    if not m or m.group(1) == "TBD":
        return None
    return int(m.group(1))


def votos_usuarios(html):
    """Sobre cuántos votos se calculó el puntaje de usuarios.

    Metacritic muestra el puntaje sin decir de dónde sale, y con cinco votos un 5.9
    no significa nada: parece una controversia y es ruido. Sólo aparece en el bloque
    de usuarios —el de crítica dice "Critic Reviews"—, así que no se confunden.
    """
    m = re.search(r"Based on ([\d,]+) User Ratings", html)
    return int(m.group(1).replace(",", "")) if m else None


def puntaje_usuarios(html):
    """El puntaje de usuarios (0 a 10) de una página de Metacritic, o None si no hay.

    La página trae los dos puntajes con el mismo `data-testid`, primero el de crítica
    y después el de usuarios, así que hay que anclarse en el encabezado y tomar el
    valor que viene después. Cuando todavía no hay votos suficientes dice "tbd".
    """
    i = html.find('data-testid="global-score-header">User score')
    if i == -1:
        return None
    # Sólo la ventana del bloque: si el juego no tiene votos, ahí no hay ningún
    # valor y la búsqueda seguiría de largo hasta el Metascore de más abajo. Así
    # devolvía 79 en The Sinking City 2, que es su puntaje de crítica.
    ventana = html[i:i + 2000]
    if 'data-testid="global-score-tbd"' in ventana:
        return None   # "tbd": todavía no hay suficientes votos
    m = re.search(r'data-testid="global-score-value">([^<]*)<', ventana)
    if not m:
        return None
    try:
        nota = float(m.group(1).strip())
    except ValueError:
        return None
    return nota if 0 <= nota <= 10 else None   # red de seguridad: esto va de 0 a 10


def main():
    hoy = datetime.date.today().isoformat()
    maniana = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    src = ARCHIVO.read_text(encoding="utf-8")

    entradas = re.findall(
        r'id: "([^"]+)",\s*titulo: "([^"]+)",\s*(?:relanzamiento[^\n]*\n\s*)?(?:duracion[^\n]*\n\s*)?fecha: "([^"]+)",', src)
    # fallback robusto por bloque
    bloques = re.findall(r'\{\s*id: "([^"]+)",(.*?)\n  \}', src, re.S)
    juegos = []
    for gid, cuerpo in bloques:
        fecha = re.search(r'fecha: "([^"]+)"', cuerpo)
        mc = re.search(r'metacritic: (null|\d+)', cuerpo)
        mcu = re.search(r'metacriticUsuarios: (null|[\d.]+)', cuerpo)
        mcs = re.search(r'metacriticSlug: "([^"]+)"', cuerpo)
        mcv = re.search(r'metacriticVotos: (null|\d+)', cuerpo)
        juegos.append({
            "id": gid,
            "fecha": fecha.group(1) if fecha else "",
            "metacritic": mc.group(1) if mc else "null",
            "usuarios": mcu.group(1) if mcu else None,   # None = el campo todavía no existe
            "slug": mcs.group(1) if mcs else gid,
            "votos": mcv.group(1) if mcv else None,
            "sin_trailer": "trailer: null" in cuerpo,
            "sin_imagen": "imagen: null" in cuerpo,
            "sin_duracion": "duracion:" not in cuerpo,
            "sin_noticias": "noticias:" not in cuerpo,
            "sin_critica": "critica:" not in cuerpo,
            "relanzamiento": "relanzamiento:" in cuerpo,
            "alta": (re.search(r'alta: "([^"]+)"', cuerpo) or [None, ""])[1],
            "rel_texto": (re.search(r'relanzamiento: "([^"]*)"', cuerpo) or [None, ""])[1],
        })

    print(f"═══ MANTENIMIENTO {hoy} ═══  ({len(juegos)} juegos en el calendario)\n")

    # 1) Puntajes de Metacritic
    pendientes = [j["id"] for j in juegos if j["metacritic"] == "null" and j["fecha"] <= hoy]
    print(f"── Metacritic: {len(pendientes)} lanzados sin puntaje ──")
    aplicados = {}
    por_id = {j["id"]: j for j in juegos}
    sospechosos = []
    for gid in pendientes:
        try:
            html = get(f"https://www.metacritic.com/game/{gid}/")
            rv = re.search(r'"ratingValue":(\d+)', html)
            if not rv:
                continue
            # El slug puede coincidir con OTRO juego de la misma saga: el 04/08/2026
            # "final-fantasy-xiv-online" devolvió 49, que es el lanzamiento fallido de
            # 2010, no A Realm Reborn (86), que es lo que llega a Switch 2. Se compara
            # el año de Metacritic contra el que conocemos para detectarlo.
            fecha_mc = re.search(r'"datePublished":"(\d{4})', html)
            anio_mc = fecha_mc.group(1) if fecha_mc else "?"
            j = por_id[gid]
            # años válidos: el del lanzamiento + los que mencione el campo relanzamiento
            anios_esperados = {j["fecha"][:4]} | set(
                re.findall(r"\b((?:19|20)\d{2})\b", j["rel_texto"]))
            ok = anio_mc in anios_esperados or anio_mc == "?"
            aplicados[gid] = int(rv.group(1))
            marca = "" if ok else f"   ⚠ REVISAR: Metacritic dice {anio_mc}, esperábamos {sorted(anios_esperados)}"
            if not ok:
                sospechosos.append(gid)
            print(f"  ★ NUEVO PUNTAJE {gid}: {rv.group(1)}  (Metacritic {anio_mc}){marca}")
        except Exception:
            pass  # 404 = la página no existe con ese slug; queda para revisión manual
        time.sleep(0.4)
    if sospechosos:
        print(f"\n  ⚠ {len(sospechosos)} puntaje(s) con año que no cuadra: {', '.join(sospechosos)}")
        print("    Verificar a mano antes del commit — puede ser otro juego de la misma saga.")
    if not aplicados:
        print("  (sin puntajes nuevos)")

    # 1 ter) Puntaje de usuarios de Metacritic.
    #
    # Es el contraste que hace interesante a una ficha: Marvel Tōkon debutó con 87 de
    # crítica y a la vez con una avalancha de reseñas negativas. Es un número, igual que
    # el de crítica, así que se baja solo y no lo mantiene nadie.
    #
    # Se pide para los que ya tienen puntaje de crítica y todavía no tienen el de
    # usuarios, y además se refresca el de los lanzados hace menos de DIAS_REFRESCO:
    # el de crítica queda fijo a los pocos días, pero el de usuarios se sigue moviendo
    # durante semanas, que es justo cuando pasan las review bombs.
    limite = (datetime.date.today() - datetime.timedelta(days=DIAS_REFRESCO)).isoformat()
    pendientes_u = [j for j in juegos
                    if (j["metacritic"] != "null" or j["id"] in aplicados) and j["fecha"] <= hoy
                    and (j["usuarios"] in (None, "null") or j["votos"] is None
                         or j["fecha"] >= limite)]
    print(f"\n── Metacritic usuarios: {len(pendientes_u)} a consultar ──")
    usuarios = {}
    criticas = {}   # puntajes de crítica que se movieron desde la última corrida
    descartados = []
    for j in pendientes_u:
        gid = j["id"]
        try:
            html = get(f"https://www.metacritic.com/game/{j['slug']}/")
        except Exception:
            continue  # 404 o caída: se reintenta mañana, no se pisa lo que había
        finally:
            time.sleep(0.4)
        # Que el slug exista no quiere decir que sea el juego: "final-fantasy-xiv-online"
        # es el lanzamiento fallido de 2010 (49 de crítica, 3.9 de usuarios), no A Realm
        # Reborn, que es lo que llega a Switch 2. El puntaje de crítica ya lo tenemos
        # verificado, así que sirve de control: si el de la página no se le parece, la
        # página es de otro juego y el puntaje de usuarios sería de otro juego también.
        de_la_pagina = metascore(html)
        conocido = int(j["metacritic"]) if j["metacritic"] != "null" else aplicados.get(gid)
        # Una diferencia grande de puntaje puede ser otro juego —FFXIV Online daba 49 contra
        # nuestro 86— o un juego con tan pocas reseñas que el promedio salta solo: Pro Jank
        # Footy pasó de 59 a 85 con tres reseñas. Lo que los separa es el año: si la página
        # es del año que esperamos, es el juego nuestro y el puntaje se movió nomás.
        anio_pagina = re.search(r'"datePublished":"(\d{4})', html)
        anios_ok = {j["fecha"][:4]} | set(re.findall(r"\b((?:19|20)\d{2})\b", j["rel_texto"]))
        mismo_juego = anio_pagina is None or anio_pagina.group(1) in anios_ok
        if (de_la_pagina is not None and conocido is not None
                and abs(de_la_pagina - conocido) > 15 and not mismo_juego):
            descartados.append(f"{gid} (la página dice {de_la_pagina} y es de "
                               f"{anio_pagina.group(1)}, nosotros {conocido} de {j['fecha'][:4]})")
            continue
        # Ya tenemos la página en la mano: de paso se corrige el puntaje de crítica.
        # Hasta hoy se bajaba una sola vez y quedaba congelado para siempre, y un
        # puntaje viejo en un sitio que se vende por exacto es igual de malo que
        # una fecha vieja.
        if de_la_pagina is not None and conocido is not None and de_la_pagina != conocido:
            criticas[gid] = de_la_pagina
            print(f"  ~ {gid}: crítica {conocido} → {de_la_pagina}")
        nota, votos = puntaje_usuarios(html), votos_usuarios(html)
        if nota is None:
            # "tbd": todavía no hay suficientes votos. Se marca null para no volver
            # a pedirlo cada día una vez que el juego es viejo.
            if j["usuarios"] is None:
                # Tupla igual que en el caso normal: el escritor de más abajo desempaqueta
                # (nota, votos) y con un string suelto reventaba. Pasaba sólo cuando un
                # juego estrena puntaje de crítica el mismo día en que el de usuarios
                # todavía dice "tbd", que es justo lo que pasó el 21/08/2026.
                usuarios[gid] = ("null", None)
            continue
        if (j["usuarios"] not in (None, "null") and abs(float(j["usuarios"]) - nota) < 0.05
                and j["votos"] == str(votos)):
            continue  # no se movió
        usuarios[gid] = (f"{nota:.1f}", votos)
        antes = "—" if j["usuarios"] in (None, "null") else j["usuarios"]
        aviso = "  (pocos votos: no se muestra)" if (votos or 0) < MIN_VOTOS else ""
        print(f"  ★ {gid}: crítica {j['metacritic']} · usuarios {antes} → {nota:.1f}"
              f" ({votos} votos){aviso}")
    if descartados:
        print(f"\n  ⚠ {len(descartados)} descartado(s) porque la página no es del juego:")
        for d in descartados:
            print(f"    · {d}")
        print("    Se arregla con el campo metacriticSlug en datos/juegos.js.")
    if not usuarios:
        print("  (ningún puntaje de usuarios se movió)")

    for gid, score in criticas.items():
        patron = re.compile(r'(id: "' + re.escape(gid) + r'",.*?)metacritic: \d+,', re.S)
        src = patron.sub(lambda m: m.group(1) + f"metacritic: {score},", src, count=1)

    for gid, (nota, votos) in usuarios.items():
        bloque = re.compile(r'(id: "' + re.escape(gid) + r'",.*?metacritic: (?:null|\d+),)'
                            r'(\n\s*metacriticUsuarios: (?:null|[\d.]+),)?'
                            r'(\n\s*metacriticVotos: (?:null|\d+),)?', re.S)
        linea = f"\n    metacriticUsuarios: {nota},"
        if nota != "null":
            linea += f"\n    metacriticVotos: {votos if votos is not None else 'null'},"
        src = bloque.sub(lambda m: m.group(1) + linea, src, count=1)

    # 1 bis) Fecha de alta de los juegos cargados a mano desde la última corrida.
    # El badge ★ NUEVO sale de este campo, así que si nadie lo sella el juego
    # entra al calendario sin marcar. Se pone hoy, que es cuando se cargó.
    selladas = 0
    sin_alta = [j["id"] for j in juegos if not j["alta"]]
    if sin_alta:
        print(f"\n── Sellando fecha de alta: {len(sin_alta)} juego(s) nuevo(s) ──")
        for gid in sin_alta:
            patron = re.compile(r'(id: "' + re.escape(gid) + r'",.*?)(\n  \})', re.S)
            src, n = patron.subn(lambda m: m.group(1).rstrip() + f',\n    alta: "{hoy}"' + m.group(2), src, count=1)
            if n:
                print(f"  + {gid} → {hoy}")
                selladas += 1

    for gid, score in aplicados.items():
        patron = re.compile(r'(id: "' + re.escape(gid) + r'",.*?)metacritic: null,', re.S)
        src = patron.sub(lambda m: m.group(1) + f"metacritic: {score},", src, count=1)
    if aplicados or selladas or usuarios or criticas:
        ARCHIVO.write_text(src, encoding="utf-8")

    # 2) Regenerar
    print("\n── Regenerando fichas y sitemap ──")
    fallidos = []
    # cargar-meta-trailers.py va PRIMERO: generar-fichas.py lee su caché para
    # declarar el trailer en los datos estructurados. Si no falta ninguno no hace
    # una sola petición, así que en un día normal no cuesta nada.
    for script in ["cargar-meta-trailers.py", "generar-fichas.py", "generar-plataformas.py",
                   "generar-noticias.py", "generar-recomendados.py", "generar-meses.py",
                   "generar-feeds.py",
                   "generar-sitemap.py"]:
        r = subprocess.run(["python3", str(RAIZ / "scripts" / script)], capture_output=True, text=True)
        print(" ", r.stdout.strip() or r.stderr.strip())
        # Un generador que falla no se ve. El 31/08/2026 generar-plataformas.py estuvo un
        # commit entero con un error de sintaxis: el traceback salía acá, entre veinte
        # líneas de salida normal, y las cinco páginas de plataforma se quedaron viejas
        # sin que nada lo dijera. Se ven bien —son la última versión buena— y por eso
        # nadie lo nota. Ahora corta el paso y lo dice al final, donde se lee.
        if r.returncode != 0:
            fallidos.append(script)

    # 3) Reporte
    # Los duplicados van primero porque son el error más caro y el que no se ve mirando el
    # sitio: las dos fichas están bien hechas, el problema es que existan las dos. Corre
    # todos los días para que un duplicado no sobreviva más de una jornada.
    print()
    r = subprocess.run(["python3", str(RAIZ / "scripts" / "verificar-duplicados.py")],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())

    # Hermano del de duplicados y con el mismo modo de falla: un estimado vencido no se ve
    # roto. La fila sale prolija, en su bloque "SIN FECHA CONFIRMADA", diciendo que un juego
    # sale en un mes que ya pasó. El 02/09/2026 había tres de "AGOSTO 2026" y los encontró el
    # usuario mirando la página, no una rutina. Tampoco toca la red.
    print()
    r = subprocess.run(["python3", str(RAIZ / "scripts" / "verificar-estimados.py")],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())

    # La estrella de favoritos se llama desde js/main.js pero vive en js/favoritos.js. Si
    # esa función se renombra o el script deja de cargarse, renderCalendario() tira una
    # excepción en medio del render y la PORTADA QUEDA EN BLANCO. No se ve fea: no se ve.
    # El chequeo no toca la red, así que va todos los días.
    print()
    r = subprocess.run(["python3", str(RAIZ / "scripts" / "verificar-favoritos.py")],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    if r.returncode != 0:
        fallidos.append("verificar-favoritos.py")

    lanzan_hoy = [j["id"] for j in juegos if j["fecha"] == hoy]
    lanzan_maniana = [j["id"] for j in juegos if j["fecha"] == maniana]
    print("\n── Candidatos a noticias ──")
    print(f"  Lanzan HOY: {', '.join(lanzan_hoy) or '(nada)'}")
    print(f"  Lanzan MAÑANA: {', '.join(lanzan_maniana) or '(nada)'}")
    if aplicados:
        print(f"  Debuts en Metacritic para noticia: {', '.join(f'{g} ({s})' for g, s in aplicados.items())}")

    # Faltantes que se resuelven en la rutina SEMANAL (paso 6)
    print("\n── Backlog semanal: carátulas y trailers ──")
    print(f"  Sin trailer: {', '.join(j['id'] for j in juegos if j['sin_trailer']) or '(ninguno)'}")
    print(f"  Sin carátula: {', '.join(j['id'] for j in juegos if j['sin_imagen']) or '(ninguna)'}")

    # Faltantes que se resuelven en la rutina MENSUAL (pasos 10 y 11)
    print("\n── Backlog mensual: duraciones (cargar ~15 por mes) ──")
    ports_sin_duracion = [j["id"] for j in juegos if j["relanzamiento"] and j["sin_duracion"]]
    print(f"  Ports sin duración: {len(ports_sin_duracion)}")
    for gid in ports_sin_duracion[:15]:
        print(f"    · {gid}")
    if len(ports_sin_duracion) > 15:
        print(f"    … y {len(ports_sin_duracion) - 15} más")

    # El resumen de crítica lo escribe una persona leyendo las reseñas, así que no
    # se puede automatizar, pero sí avisar de cuáles faltan: si no aparece en el
    # reporte, no lo mantiene nadie.
    print("\n── Backlog: resumen de crítica (los mejor puntuados sin `critica`) ──")
    # El puntaje que se acaba de bajar en esta misma corrida no está en `juegos`, que se
    # leyó del archivo antes de escribirlo. Sin esto, el juego que debuta hoy con puntaje no
    # aparece en el backlog hasta mañana, que es justo el día en que menos sirve.
    for j in juegos:
        if j["metacritic"] == "null" and j["id"] in aplicados:
            j["metacritic"] = str(aplicados[j["id"]])

    sin_critica = sorted((j for j in juegos if j["sin_critica"] and j["metacritic"] != "null"),
                         key=lambda j: int(j["metacritic"]), reverse=True)
    con_puntaje = [j for j in juegos if j["metacritic"] != "null"]
    otros = sum(1 for j in juegos if not j["sin_critica"] and j["metacritic"] == "null")
    extra = f"  (+{otros} sin puntaje propio, otras ediciones del mismo juego)" if otros else ""
    print(f"  Con resumen: {sum(1 for j in con_puntaje if not j['sin_critica'])} de "
          f"{len(con_puntaje)} juegos con puntaje{extra}")
    for j in sin_critica[:8]:
        print(f"    · {j['metacritic']}  {j['id']}")

    print("\n── Backlog mensual: noticias (los mejor puntuados sin noticias) ──")
    sin_noticias = sorted(
        (j for j in juegos if j["sin_noticias"] and j["metacritic"] != "null"),
        key=lambda j: int(j["metacritic"]), reverse=True)
    print(f"  Juegos con noticias: {sum(1 for j in juegos if not j['sin_noticias'])} de {len(juegos)}")
    for j in sin_noticias[:10]:
        print(f"    · {j['metacritic']}  {j['id']}")
    if not sin_noticias:
        print("    (ninguno)")

    # Las noticias propias (retrasos, Directs, PS Plus/Game Pass) no las puede
    # detectar el script: no salen de datos/juegos.js. Se recuerdan acá para que
    # la rutina diaria no se limite a lo que ya está cargado.
    propias = RAIZ / "datos" / "noticias.js"
    cuantas = len(re.findall(r'\n    id: "', propias.read_text(encoding="utf-8"))) if propias.exists() else 0
    ultima = "—"
    if cuantas:
        fechas = re.findall(r'fecha: "(\d{4}-\d{2}-\d{2})"', propias.read_text(encoding="utf-8"))
        if fechas:
            ultima = max(fechas)
            dias = (datetime.date.fromisoformat(hoy) - datetime.date.fromisoformat(ultima)).days
            ultima = f"{ultima} (hace {dias} día{'s' if dias != 1 else ''})"
    print("\n── Noticias propias (datos/noticias.js) ──")
    print(f"  Cargadas: {cuantas}  |  última: {ultima}")
    print("  ¿Pasó algo que no cuelgue de un lanzamiento? Retrasos, un Direct o State of")
    print("  Play, PS Plus o Game Pass del mes. Si no pasó nada, no se fuerza.")
    print("  Fuentes:  blog.latam.playstation.com · news.xbox.com")
    print("            gematsu.com → usar el feed: curl -s https://www.gematsu.com/feed")
    print("            nintendo.com/us/nintendo-direct · vandal.elespanol.com · 3djuegos.com")
    print("  Vandal y 3DJuegos son radar: verificar en la tienda antes de tocar una fecha.")
    print("  De ahí no sale solo la noticia: también juegos que faltan y fechas a corregir.")

    if fallidos:
        print(f"\n  ⚠⚠ {len(fallidos)} PASO(S) FALLARON: {', '.join(fallidos)}")
        print("     Un generador que falla deja su página como estaba: se ve bien y está vieja.")
        print("     verificar-favoritos.py es peor: avisa que la portada puede quedar en blanco.")
        print("     NO subir hasta arreglarlo. El error está más arriba, en su línea.")

    print("\n═══ Siguiente paso: noticias (si hay), commit y deploy ═══")


if __name__ == "__main__":
    main()
