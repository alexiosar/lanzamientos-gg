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

## Pasos (por el editor web, sin clonar nada)

GitHub hace el fork solo cuando editás un archivo de un repo ajeno, así que no hace falta
clonar ni usar la consola.

1. Abrir https://github.com/public-apis/public-apis/blob/master/README.md
2. Tocar el **lápiz** (*Edit this file*). GitHub avisa que va a crear un fork: aceptar.
3. Buscar con Ctrl+F (o Cmd+F) la palabra **`Jservice`**. Verificado el 29/07/2026: está en la
   línea 972, y la línea siguiente es `Lichess`. La línea nueva va **entre esas dos**:

   ```
   | [Jservice](http://jservice.io) | Jeopardy Question Database | No | No | Unknown |
   | [Lanzamientos](https://lanzamientos.lat/api) | Video game release calendar in Spanish for PS5, PS4, Xbox, Switch and Switch 2 | No | Yes | Yes |
   | [Lichess](https://lichess.org/api) | Access to all data of users, games, puzzles and etc on Lichess | `OAuth` | Yes | Unknown |
   ```

4. Abajo, en *Commit changes*, escribir un mensaje descriptivo (por ejemplo
   `Add Lanzamientos API to readme`) y tocar **Propose changes**.

   > No busques la opción "Create a new branch for this commit and start a pull request":
   > **ya no aparece**. Ese par de opciones sólo se muestra cuando tenés permiso de escritura
   > en el repo. Al editar un repo ajeno, GitHub crea el fork y la rama solo y te lleva
   > directo a la pantalla del pull request.

5. En la pantalla del pull request, título (este sí tiene que ser exacto, lo pide su guía):

   ```
   Add Lanzamientos API
   ```

6. Cuerpo del pull request:

   ```
   Adds Lanzamientos, a video game release calendar for Spanish-speaking players.

   - Endpoint: https://lanzamientos.lat/api/juegos.json
   - Docs: https://lanzamientos.lat/api
   - No authentication, no rate limits, HTTPS only, CORS enabled
   - Updated daily; currently 246 games for PS5, PS4, Xbox, Switch and Switch 2
   - Also available: https://lanzamientos.lat/api/proximos.json (next 30 days)
     and an RSS feed at https://lanzamientos.lat/rss.xml
   ```

7. Esperar a que pase la validación automática. Si pide cambios, corregir y **aplastar los
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
| public-apis | PR abierto, esperando revisión | 29/07/2026 | https://github.com/public-apis/public-apis/pull/6717 |
