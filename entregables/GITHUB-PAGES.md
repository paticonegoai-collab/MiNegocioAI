# Abrir el portafolio sin descargar

GitHub Pages puede servir estos tres sitios como páginas web. La rama `gh-pages` contiene en su raíz `index.html`, los tres proyectos y `.nojekyll`; no necesita compilación ni dependencias.

En esta sesión el acceso Git permite subir ramas, pero las solicitudes a la API de GitHub para configurar Pages responden `Forbidden`. Por eso no se ha podido activar ni verificar una publicación. No se ha cambiado la visibilidad del repositorio.

Si quieres habilitarlo desde tu cuenta:

1. En el repositorio, abre **Settings → Pages**.
2. En **Build and deployment**, selecciona **Deploy from a branch**.
3. Elige **gh-pages**, carpeta **/ (root)** y pulsa **Save**.
4. Cuando termine la publicación, usa el enlace que GitHub muestre en ese panel.

Los repositorios privados requieren un plan de GitHub compatible con Pages; si la opción no está disponible, las descargas ZIP siguen funcionando. No hace falta volver público el repositorio para revisar los ZIP.

El contenido publicado sería una demostración de portafolio: restaurante, perfumería y hotel ficticios, con imágenes generadas con IA. Las compras y reservas son simulaciones.
