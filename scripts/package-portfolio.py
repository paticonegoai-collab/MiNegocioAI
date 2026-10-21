"""Package the three standalone previews without external files or services."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import base64
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'entregables'
GALLERY = ROOT / 'portafolio'
OUTPUT.mkdir(exist_ok=True)
GALLERY.mkdir(exist_ok=True)

def thumbnail(name):
    return 'data:image/jpeg;base64,' + base64.b64encode((GALLERY / f'{name}.jpg').read_bytes()).decode()

gallery = '''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Archivo de ideas — Portafolio de conceptos</title>
<style>
:root{font-family:Arial,sans-serif;color:#262825;background:#f5f2eb}*{box-sizing:border-box}body{margin:0}a{color:inherit;text-decoration:none}button{font:inherit;cursor:pointer}a:focus-visible,button:focus-visible{outline:2px solid #754b79;outline-offset:5px}.wrap{width:min(1180px,calc(100% - 72px));margin:auto}header{display:flex;justify-content:space-between;align-items:center;padding:30px 0;border-bottom:1px solid #cdc8bd}header>a{font-weight:700;letter-spacing:-1px;font-size:22px}header>span{font-size:9px;letter-spacing:2px;color:#5e625a}.intro{padding:80px 0 50px;display:flex;justify-content:space-between;gap:40px;align-items:end}.eyebrow{font-size:9px;letter-spacing:2px;color:#63586c}.intro h1{font:400 86px/1.02 Georgia,serif;letter-spacing:-3px;margin:22px 0 0}.intro h1 em{font-weight:400;color:#79627c}.intro>p{max-width:310px;font-size:13px;line-height:1.9;color:#62665d;margin:0 0 6px}.filters{display:flex;justify-content:space-between;align-items:center;padding:25px 0;border-block:1px solid #cdc8bd;gap:20px}.filter-list{display:flex;gap:10px;flex-wrap:wrap}.filter-list button{border:1px solid transparent;padding:12px 18px;background:none;font-size:11px;color:#565d50}.filter-list button[aria-pressed=true]{border-color:#52624c;background:#e7ebdf;color:#253323}#count{font-size:10px;color:#62665d}.projects{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;padding:38px 0 75px}.project{border-bottom:1px solid #cdc8bd;padding-bottom:25px}.project[hidden]{display:none}.cover{display:block;overflow:hidden;background:#ddd}.cover img{width:100%;aspect-ratio:1.5;object-fit:cover;object-position:top;display:block;transition:transform .4s}.cover:hover img{transform:scale(1.02)}.meta{display:flex;justify-content:space-between;gap:12px;font-size:8px;letter-spacing:1.5px;color:#62665d;margin-top:23px}.project h2{font:400 37px/1.15 Georgia,serif;letter-spacing:-.7px;margin:12px 0}.project p{font-size:12px;line-height:1.9;color:#62665d;max-width:440px;margin:0}.tags{display:flex;gap:8px;flex-wrap:wrap;margin-top:20px}.tags>span{font-size:8px;padding:7px 10px;border:1px solid #d3cabe}.open-project{display:flex;justify-content:space-between;align-items:center;margin-top:23px;padding:15px 17px;background:#263729;color:#f7f1e5;font-size:11px}.project:nth-child(2) .open-project{background:#95333c}.project:nth-child(3) .open-project{background:#173f91}@media(min-width:701px) and (max-width:1000px){.projects{grid-template-columns:1fr 1fr}}.open-project>span{font-size:17px}.note{border-top:1px solid #cdc8bd;padding:30px 0 55px;display:flex;justify-content:space-between;gap:40px}.note h2{font:400 30px Georgia,serif;margin:0}.note p{font-size:11px;line-height:1.9;color:#62665d;max-width:530px;margin:0}footer{background:#242c24;color:#e9e4d9;padding:25px 0}.footer-inner{display:flex;justify-content:space-between;gap:20px;font-size:9px;line-height:1.8}@media(max-width:700px){.wrap{width:calc(100% - 40px)}header{padding:24px 0}header>a{font-size:19px}header>span{font-size:6px;letter-spacing:1.2px;max-width:100px;text-align:right;line-height:1.8}.intro{display:block;padding:45px 0 35px}.eyebrow{font-size:7px;letter-spacing:1.5px}.intro h1{font-size:61px;letter-spacing:-2px}.intro>p{font-size:12px;margin-top:25px;max-width:350px}.filters{display:block;padding:18px 0}.filter-list{gap:7px}.filter-list button{padding:11px 12px;font-size:10px}#count{font-size:9px;margin-top:15px;display:block}.projects{grid-template-columns:1fr;gap:38px;padding:28px 0 45px}.cover img{aspect-ratio:1.3}.project h2{font-size:34px}.project p{font-size:12px}.meta{font-size:7px;letter-spacing:1px}.note{display:block;padding:25px 0 38px}.note h2{font-size:27px;margin-bottom:18px}.note p{font-size:11px}.footer-inner{font-size:8px;gap:20px;flex-wrap:wrap}}@media(prefers-reduced-motion:reduce){*{transition:none!important}.cover:hover img{transform:none}}
</style></head><body><div class="wrap"><header><a href="index.html">Archivo de ideas.</a><span>PORTAFOLIO DE CONCEPTOS DIGITALES</span></header><main><section class="intro"><div><span class="eyebrow">TRES PROYECTOS · TRES UNIVERSOS</span><h1>Ideas que<br />se vuelven <em>experiencia.</em></h1></div><p>Una colección de marcas imaginadas desde cero. Identidad, fotografía generada con IA e interfaces que puedes explorar de verdad.</p></section><div class="filters"><div class="filter-list" aria-label="Filtrar proyectos"><button data-filter="all" aria-pressed="true">Todos</button><button data-filter="gastronomia" aria-pressed="false">Gastronomía</button><button data-filter="perfumeria" aria-pressed="false">Perfumería</button><button data-filter="hoteleria" aria-pressed="false">Hotelería</button></div><span id="count" role="status">03 PROYECTOS</span></div><section class="projects" aria-label="Proyectos del portafolio">
<article class="project" data-category="gastronomia"><a class="cover" href="bruma-de-olivo.html" aria-label="Explorar Bruma de Olivo"><img src="BRUMA_IMAGE" alt="Vista de la web nocturna de Bruma de Olivo" width="1200" height="800"></a><div class="meta"><span>01 / GASTRONOMÍA</span><span>CONCEPTO FICTICIO</span></div><h2>Bruma de Olivo</h2><p>Una parrilla íntima donde las brasas, la luz de las velas y una buena sobremesa se convierten en una experiencia digital.</p><div class="tags"><span>IDENTIDAD NOCTURNA</span><span>CARTA INTERACTIVA</span><span>RESERVAS DE MUESTRA</span></div><a class="open-project" href="bruma-de-olivo.html">Abrir experiencia<span aria-hidden="true">↗</span></a></article>
<article class="project" data-category="perfumeria"><a class="cover" href="nebula-botanica.html" aria-label="Explorar Nébula Botánica"><img src="NEBULA_IMAGE" alt="Vista de la web de perfumería Nébula Botánica" width="1200" height="800"></a><div class="meta"><span>02 / PERFUMERÍA</span><span>CONCEPTO FICTICIO</span></div><h2>Nébula Botánica</h2><p>Una casa de perfumes imaginada con luz, color y memoria. Tres aromas, una bolsa interactiva y un descubrimiento personal.</p><div class="tags"><span>DIRECCIÓN EDITORIAL</span><span>TIENDA DE MUESTRA</span><span>CUESTIONARIO OLFATIVO</span></div><a class="open-project" href="nebula-botanica.html">Abrir experiencia<span aria-hidden="true">↗</span></a></article>
<article class="project" data-category="hoteleria"><a class="cover" href="auralma.html" aria-label="Explorar Auralma"><img src="AURALMA_IMAGE" alt="Vista de la web costera de Auralma" width="1440" height="900"></a><div class="meta"><span>03 / HOTELERÍA</span><span>CONCEPTO FICTICIO</span></div><h2>Auralma</h2><p>Un refugio costero donde el azul, la luz y los pequeños rituales invitan a bajar el ritmo. Diseña una escapada a tu manera.</p><div class="tags"><span>IDENTIDAD COSTERA</span><span>GALERÍAS DE SUITES</span><span>ESTANCIA DE MUESTRA</span></div><a class="open-project" href="auralma.html">Abrir experiencia<span aria-hidden="true">↗</span></a></article>
</section><section class="note"><h2>Creado para imaginar.<br />Listo para explorar.</h2><p>Las marcas, historias, productos y precios de estos proyectos son ficticios. Las imágenes fueron generadas con IA. Las reservas y compras son demostraciones: no se cobra, no se tramitan pedidos y no se envían datos personales. Mantén los cuatro archivos HTML juntos para navegar entre la portada y los proyectos.</p></section></main></div><footer><div class="wrap footer-inner"><span>ARCHIVO DE IDEAS · PORTAFOLIO DE CONCEPTOS</span><span>Diseño, identidad y experiencias interactivas.</span></div></footer><script>
const controls=[...document.querySelectorAll('[data-filter]')];const projects=[...document.querySelectorAll('[data-category]')];for(const control of controls)control.addEventListener('click',()=>{for(const button of controls)button.setAttribute('aria-pressed',String(button===control));let count=0;for(const project of projects){project.hidden=control.dataset.filter!=='all'&&control.dataset.filter!==project.dataset.category;if(!project.hidden)count++}document.getElementById('count').textContent=String(count).padStart(2,'0')+' '+(count===1?'PROYECTO':'PROYECTOS')});
</script></body></html>'''
gallery = gallery.replace('BRUMA_IMAGE', thumbnail('bruma')).replace('NEBULA_IMAGE', thumbnail('nebula')).replace('AURALMA_IMAGE', thumbnail('auralma'))
gallery = gallery.replace('</style>', '.cover img{height:auto}</style>')
gallery = gallery.replace('<span aria-hidden="true">↗</span>', '<svg width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 16 16 4M4 4h12v12" stroke="currentColor" stroke-width="1.4"/></svg>')
(GALLERY / 'index.html').write_text(gallery, encoding='utf-8')

nebula = ROOT / 'proyectos/nebula-botanica/docs/vista-previa.html'
bruma = ROOT / 'docs/propuesta-inicial/vista-previa.html'
individual = OUTPUT / 'nebula-botanica-v1.zip'
combined = OUTPUT / 'portafolio-v2.zip'
auralma = ROOT / 'proyectos/auralma/docs/vista-previa.html'
auralma_individual = OUTPUT / 'auralma-v1.zip'
nebula_readme = '''NEBULA BOTANICA — PROYECTO 02

1. Extrae el ZIP.
2. Abre nebula-botanica.html en un navegador moderno.
3. Explora la coleccion, los favoritos, las fichas, la bolsa y el cuestionario.

No necesitas instalar nada ni conectarte a Internet.
La marca y los productos son ficticios. Las cinco imagenes se generaron con IA.
No se realizan cobros, pedidos ni envios de informacion.
'''
portfolio_readme = '''ARCHIVO DE IDEAS — PORTAFOLIO DE CONCEPTOS

1. Extrae todos los archivos del ZIP a la misma carpeta.
2. Abre index.html en un navegador moderno.
3. Elige Bruma de Olivo, Nebula Botanica o Auralma.
4. Usa el enlace Volver al portafolio al pie de cada sitio para regresar a la portada.

Tambien puedes abrir cada proyecto directamente desde su archivo HTML.
Los tres sitios funcionan sin instalacion ni conexion a Internet.
Todo el contenido comercial es ficticio. Compras y reservas son demostraciones.
No se realizan cobros ni se envian datos personales.
'''
if not individual.exists():
    with ZipFile(individual, 'w', ZIP_DEFLATED, compresslevel=6) as archive:
        archive.write(nebula, 'nebula-botanica.html')
        archive.writestr('LEEME.txt', nebula_readme)
with ZipFile(auralma_individual, 'w', ZIP_DEFLATED, compresslevel=6) as archive:
    archive.write(auralma, 'auralma.html')
    archive.writestr('LEEME.txt', 'AURALMA — PROYECTO 03\n\nExtrae el ZIP y abre auralma.html en un navegador moderno.\nNo necesita instalacion ni conexion. Marca, hotel, tarifas y experiencias ficticias.\nSeis imagenes originales generadas con IA. Reserva demostrativa, sin cobros ni envio de datos.\n')

def portfolio_html(path):
    if path.exists():
        html = path.read_text(encoding='utf-8')
    else:
        # Earlier projects can be rebuilt into the gallery from their delivered ZIPs.
        previous = {bruma: ('bruma-de-olivo-v1.zip', 'bruma-de-olivo.html'), nebula: ('nebula-botanica-v1.zip', 'nebula-botanica.html')}
        archive_name, html_name = previous[path]
        with ZipFile(OUTPUT / archive_name) as archive:
            html = archive.read(html_name).decode('utf-8')
    back = '<div style="background:#f5f2eb;color:#263729;padding:24px;text-align:center;font:13px Arial,sans-serif"><a href="index.html" style="color:inherit;text-underline-offset:5px">Volver al portafolio</a></div>'
    return html.replace('</body>', back + '</body>')

web = ROOT / 'publicacion'
web.mkdir(exist_ok=True)
(web / 'index.html').write_text(gallery, encoding='utf-8')
(web / '.nojekyll').write_text('')
for source, name in [(bruma, 'bruma-de-olivo.html'), (nebula, 'nebula-botanica.html'), (auralma, 'auralma.html')]:
    (web / name).write_text(portfolio_html(source), encoding='utf-8')
with ZipFile(combined, 'w', ZIP_DEFLATED, compresslevel=6) as archive:
    for name in ['index.html', 'bruma-de-olivo.html', 'nebula-botanica.html', 'auralma.html']:
        archive.write(web / name, name)
    archive.writestr('LEEME.txt', portfolio_readme)

manifest = {}
for path in [OUTPUT / 'bruma-de-olivo-v1.zip', OUTPUT / 'portafolio-v1.zip', individual, auralma_individual, combined]:
    with ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise RuntimeError(f'Archive integrity failed: {path.name}')
        manifest[path.name] = {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'files': archive.namelist()}
(OUTPUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False, indent=2))
