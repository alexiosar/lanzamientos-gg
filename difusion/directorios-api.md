# Postulaciones a directorios de APIs

Con la especificación OpenAPI publicada en `/api/openapi.yaml` se destraban dos directorios
que estaban anotados como pendientes. Los dos dan **enlaces reales**, no `nofollow`, que es
lo que le falta al dominio.

La especificación está validada: pasa `openapi-spec-validator` como OpenAPI 3.1 y coincide
campo por campo con lo que devuelve la API de verdad (verificado el 05/08/2026 contra los
292 juegos: ningún campo sin declarar, ninguno declarado que no exista, el enum de
plataformas coincide).

---

## 1. APIs.guru

Directorio de APIs con especificación OpenAPI. Lo mantiene la comunidad en GitHub.

**Repositorio:** https://github.com/APIs-guru/openapi-directory

**Cómo se postula:** con un pull request que agrega el archivo en la ruta que ellos usan,
`APIs/lanzamientos.lat/1.0.0/openapi.yaml`. El repositorio tiene su propio `CONTRIBUTING.md`
con los requisitos exactos; leerlo antes, igual que hicimos con public-apis.

**Lo que van a pedir y ya está cumplido:**

- Especificación válida de OpenAPI 3.x → sí, 3.1 validada
- `info.title`, `info.description`, `info.version`, `info.contact` y `info.license` → los cinco
- Servidor con URL absoluta y HTTPS → `https://lanzamientos.lat`
- API accesible públicamente sin clave → sí

**Ojo con una cosa:** APIs.guru es más exigente que public-apis y prioriza APIs con cierto
recorrido. Puede que no la acepten por ser nueva. No es un problema: la especificación sirve
igual para el resto.

---

## 2. Catálogo público de Postman

Postman permite publicar una colección en su red pública, que es indexable y tiene buscador
propio.

**Cómo se hace:**

1. Crear cuenta en postman.com (con contacto@lanzamientos.lat).
2. *Import* → pegar `https://lanzamientos.lat/api/openapi.yaml`. Postman genera la colección
   sola a partir de la especificación.
3. Crear un *Public Workspace* y mover la colección adentro.
4. En la colección, *Share* → *Publish*, con la descripción y el enlace a lanzamientos.lat.

No hace falta escribir nada a mano: la especificación ya trae los ejemplos y las descripciones
de cada campo, así que la colección sale documentada.

---

## 3. Otros lugares donde la especificación sirve

Aunque los dos directorios de arriba no salgan, el archivo ya rinde:

- Cualquiera puede importar la API de un clic en Postman, Insomnia o Bruno.
- Se puede generar un cliente automático en casi cualquier lenguaje con `openapi-generator`.
- Es lo que suelen pedir los agregadores de datos abiertos.

---

## Registro

| Directorio | Estado | Fecha | Enlace |
|---|---|---|---|
| public-apis | PR abierto, esperando revisión | 29/07/2026 | https://github.com/public-apis/public-apis/pull/6717 |
| APIs.guru | pendiente | — | — |
| Postman (catálogo público) | pendiente | — | — |

---

## Mantenimiento

Si algún día se agrega, se saca o se renombra un campo en `datos/juegos.js`, hay que
actualizar `api/openapi.yaml`. Para comprobar que sigue coincidiendo con los datos reales:

```bash
python3 -c "
import json,yaml
spec=yaml.safe_load(open('api/openapi.yaml'))
props=set(spec['components']['schemas']['Juego']['properties'])
d=json.load(open('api/juegos.json'))
faltan=set().union(*(set(j)-props for j in d['juegos']))
print('campos sin declarar:', faltan or 'ninguno')
"
```
