#!/usr/bin/env python3
"""Busca fechas estimadas que ya vencieron o que no dicen lo que muestran.

**Un estimado vencido no se ve roto**, y ese es todo el problema. La fila sigue saliendo
prolija, en su bloque "SIN FECHA CONFIRMADA", afirmando que un juego sale en un mes que ya
pasó. Cuanto más viejo es el dato, más convincente parece: nadie mira agosto en septiembre.

Lo encontró el usuario a ojo el 02/09/2026, no una rutina. Había tres de "AGOSTO 2026" con
agosto terminado, y ninguno era un retraso:

  is-this-seat-taken  ya había salido, el 06/08/2026, y la PS Store lo vendía hacía un mes.
  mai-child-of-ages   la edición de PS5 había salido el 18/12/2025, ocho meses ANTES.
  nomad-drive         la PS Store decía "Fecha de lanzamiento por determinar": nunca hubo
                      agosto.

O sea que un estimado vencido no significa "se retrasó". Significa "acá hay un dato que
nadie volvió a mirar", y hay que ir a la tienda a ver qué pasó de verdad.

Es hermano de `verificar-lanzados.py`, que mira el otro lado —fechas confirmadas del pasado
de juegos que capaz no salieron— y que a los estimados los saltea a propósito. Este los cubre.

Qué mira:

  1. **Estimados vencidos**: `estimado: true` con la fecha ya pasada.
  2. **La etiqueta no coincide con la fecha**: `fechaEstimada` dice "OCTUBRE 2026" pero
     `fecha` cae en septiembre. La etiqueta es lo que se lee y la fecha es lo que ordena; si
     no coinciden, el juego aparece en el mes equivocado con el cartel del mes correcto.

No toca la red, así que va en la rutina diaria.

Uso (desde la raíz del proyecto):
    python3 scripts/verificar-estimados.py
"""
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comun import cargar_juegos

RAIZ = Path(__file__).resolve().parent.parent

MESES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
         "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
TRIMESTRES = {"PRIMER": (1, 3), "SEGUNDO": (4, 6), "TERCER": (7, 9), "CUARTO": (10, 12)}


def ventana(etiqueta):
    """De 'OCTUBRE 2026' o 'CUARTO TRIMESTRE 2026' saca (año, mes_desde, mes_hasta).

    Devuelve None si no la entiende. Eso NO es un error: la etiqueta es texto libre y puede
    decir cualquier cosa. Un formato que no se reconoce se saltea en vez de inventar una
    falla, porque un chequeo que grita por algo que está bien deja de mirarse.
    """
    if not etiqueta:
        return None
    e = etiqueta.upper()
    anio = re.search(r"\b(20\d{2})\b", e)
    if not anio:
        return None
    a = int(anio.group(1))
    for nombre, (desde, hasta) in TRIMESTRES.items():
        if f"{nombre} TRIMESTRE" in e:
            return a, desde, hasta
    for i, mes in enumerate(MESES, start=1):
        if mes in e:
            return a, i, i
    return None


def main():
    juegos = cargar_juegos()
    hoy = datetime.date.today().isoformat()
    estimados = [j for j in juegos if j.get("estimado")]
    print(f"═══ FECHAS ESTIMADAS ═══  ({len(estimados)} estimados de {len(juegos)} juegos)\n")

    vencidos = sorted((j for j in estimados if j["fecha"] < hoy), key=lambda j: j["fecha"])
    incoherentes = []
    for j in estimados:
        v = ventana(j.get("fechaEstimada"))
        if not v:
            continue
        a, desde, hasta = v
        anio, mes = int(j["fecha"][:4]), int(j["fecha"][5:7])
        if anio != a or not (desde <= mes <= hasta):
            incoherentes.append(j)

    if vencidos:
        print(f"── {len(vencidos)} estimado(s) VENCIDO(S) ──")
        for j in vencidos:
            print(f"  ⚠ {j['id']:42} decía «{j.get('fechaEstimada', '?')}» "
                  f"· ordena por {j['fecha']} · {'/'.join(j['plataformas'])}")
        print("\n  No asumir que se retrasaron: mirar la tienda. Puede que ya haya salido, que")
        print("  haya salido ANTES de lo que decimos, o que nunca haya tenido esa fecha.")
        print("  Si se queda sin fecha de ningún tipo, sale del calendario con un 301.\n")

    if incoherentes:
        print(f"── {len(incoherentes)} con la etiqueta y la fecha en desacuerdo ──")
        for j in incoherentes:
            print(f"  ⚠ {j['id']:42} dice «{j['fechaEstimada']}» pero ordena por {j['fecha']}")
        print("\n  El cartel lo lee la gente y la fecha decide en qué mes aparece: si no")
        print("  coinciden, el juego sale en el mes equivocado con el cartel del correcto.\n")

    if not vencidos and not incoherentes:
        print("  ✓ ninguno vencido, ninguno en desacuerdo con su etiqueta")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
