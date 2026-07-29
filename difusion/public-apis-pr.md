# PR al directorio public-apis

Objetivo: sumar la API de lanzamientos.lat a
[public-apis/public-apis](https://github.com/public-apis/public-apis), el directorio de APIs
públicas de GitHub. Es el enlace de más peso real que podemos conseguir sin audiencia previa:
lo rastrean los buscadores todo el tiempo y lo copian decenas de sitios espejo.

Verificado el 29/07/2026: la API cumple los requisitos (HTTPS, CORS `*`, sin autenticación,
JSON válido, documentación propia en `/api`).

## La línea exacta que hay que agregar

En `README.md`, sección **Games & Comics**, respetando el orden alfabético: va **entre
`Jservice` y `Lichess`**.

```
| [Lanzamientos](https://lanzamientos.lat/api) | Video game release calendar in Spanish for PS5, PS4, Xbox, Switch and Switch 2 | No | Yes | Yes |
```

Las cinco columnas son: nombre con enlace, descripción, autenticación, HTTPS, CORS.

## Reglas que ya están contempladas

- El nombre no lleva la palabra "API" ni el dominio: por eso es `Lanzamientos`, no
  `Lanzamientos.lat API`.
- La descripción tiene 78 caracteres (el máximo es 100) y va en inglés, como todo el archivo.
- El enlace apunta a la documentación (`/api`), no al JSON crudo, que es lo que piden.
- `Auth` va como `No` sin comillas invertidas; los otros valores (`OAuth`, `apiKey`) sí las llevan.
- Un solo API por pull request.

## Pasos

1. Fork de `public-apis/public-apis`.
2. Editar `README.md` y pegar la línea en su lugar alfabético dentro de Games & Comics.
3. Commit: `Add Lanzamientos API`
4. Pull request contra la rama `master`, con el título:

   ```
   Add Lanzamientos API
   ```

5. Cuerpo del pull request:

   ```
   Adds Lanzamientos, a video game release calendar for Spanish-speaking players.

   - Endpoint: https://lanzamientos.lat/api/juegos.json
   - Docs: https://lanzamientos.lat/api
   - No authentication, no rate limits, HTTPS only, CORS enabled
   - Updated daily; currently 246 games for PS5, PS4, Xbox, Switch and Switch 2
   - Also available: https://lanzamientos.lat/api/proximos.json (next 30 days)
     and an RSS feed at https://lanzamientos.lat/rss.xml
   ```

6. Esperar a que pase la validación automática. Si pide cambios, corregir y **aplastar los
   commits en uno solo** (lo piden explícitamente).

## Si lo rechazan

El motivo más habitual es que el proyecto se considere demasiado nuevo o de nicho. En ese caso
quedan otros directorios donde la API también encaja:

- [APIs.guru](https://apis.guru/) — requiere una especificación OpenAPI.
- El catálogo público de Postman.
- Directorios de datos abiertos en español.

## Después

Cuando el PR esté aceptado, anotarlo acá con la fecha y el enlace, para no repetir el trabajo
ni perder el rastro de dónde está enlazado el sitio.

| Directorio | Estado | Fecha | Enlace |
|---|---|---|---|
| public-apis | pendiente | — | — |
