# Auralma · proyecto 03

Hotel boutique ficticio de estética costera: azul profundo, blanco sal, arena y fotografía editorial original generada con IA. React, Vite, React Router y CSS propio. Fuentes Baskervville y Manrope alojadas localmente, con sus licencias en `public/licenses`.

## Desarrollo

Desde esta carpeta:

```bash
npm ci --cache /tmp/auralma-npm-cache
npm run dev
```

```bash
npm run export:preview
npm run test:e2e
```

El exportador crea `docs/vista-previa.html`, un único HTML que incluye seis fotografías WebP, fuentes, CSS y JavaScript. Usa rutas con `#` al abrirse como exportación, por lo que también funciona en alojamiento estático dentro de una subcarpeta. El desarrollo usa rutas normales.

## Recorridos

- Inicio: fotografía costera, acceso a estancia con fechas y huéspedes, suites y rituales.
- Habitaciones: tres suites, filtro de capacidad y galería con botones, flechas del teclado y Escape.
- Experiencias: filtros de calma, sabores y aire libre; detalle y selección de un complemento.
- Tu estancia: fechas, huéspedes, suite, rituales, desglose del importe, revisión editable y resumen demostrativo. No solicita datos personales.

Las fechas admiten llegada desde hoy hasta los próximos 365 días y estancias de 1 a 14 noches. La capacidad de las suites se valida antes de revisar. Cada ritual se suma una vez por estancia para todo el grupo. No se verifica disponibilidad real.

## Validación

Diez pruebas de navegador cubren las cuatro páginas a 375, 768 y 1440 píxeles, imágenes, desbordamientos, errores de JavaScript, filtros, galerías, navegación móvil, formularios inválidos, totales, edición, accesibilidad de teclado, movimiento reducido, página 404 y exportación sin solicitudes externas. Se usa Chromium del sistema si existe o `CHROMIUM_PATH`.

Capturas en `docs/capturas`. Procedencia de las imágenes en `docs/imagenes-ia.json`. Los originales permanecen en el entorno; WebP es una conversión técnica para reducir el peso.

Todos los nombres, espacios, servicios y tarifas son ficticios. No hay pagos, reservas reales, envío de datos, base de datos ni almacenamiento local persistente.
