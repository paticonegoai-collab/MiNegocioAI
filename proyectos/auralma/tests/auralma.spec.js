import { test, expect } from '@playwright/test'
import { readFile } from 'node:fs/promises'

const date = n => {const d=new Date();d.setDate(d.getDate()+n);return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`}
async function fillDates(page){await page.getByLabel('Llegada',{exact:true}).fill(date(20));await page.getByLabel('Salida',{exact:true}).fill(date(23))}

for (const width of [375, 768, 1440]) test(`Las cuatro páginas cargan sin errores ni desbordamientos a ${width}px`,async({page})=>{
  await page.setViewportSize({width,height:900});const errors=[];page.on('pageerror',e=>errors.push(e.message))
  for(const route of ['/','/habitaciones','/experiencias','/tu-estancia']){
    await page.goto(route);await expect(page.locator('h1')).toBeVisible();await page.evaluate(()=>document.fonts.ready)
    await page.locator('footer').scrollIntoViewIfNeeded();await page.evaluate(()=>Promise.all([...document.images].map(i=>{i.loading='eager';return i.decode().catch(()=>{})})))
    expect(await page.evaluate(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0))).toBeTruthy()
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy()
    await expect(page.locator('h1')).toHaveCount(1)
  }
  expect(errors).toEqual([])
})

test('Las habitaciones filtran capacidad y su galería funciona con teclado',async({page})=>{
  await page.goto('/habitaciones');await page.getByLabel('Filtrar por huéspedes').selectOption('4');await expect(page.locator('.room-card')).toHaveCount(1)
  await expect(page.getByRole('heading',{name:'Suite Terraza',exact:true})).toBeVisible()
  const trigger=page.getByRole('button',{name:'Ver detalles de Suite Terraza'});await trigger.click();const dialog=page.getByRole('dialog')
  await expect(dialog).toBeVisible();await expect(dialog.getByRole('status')).toContainText('01 / 03')
  await dialog.getByRole('button',{name:'Imagen siguiente'}).click();await expect(dialog.getByRole('status')).toContainText('El entorno')
  await page.keyboard.press('ArrowRight');await expect(dialog.getByRole('status')).toContainText('Los pequeños rituales')
  await page.keyboard.press('ArrowLeft');await expect(dialog.getByRole('status')).toContainText('02 / 03')
  await page.keyboard.press('Escape');await expect(dialog).not.toBeVisible();await expect(trigger).toBeFocused()
  await trigger.click();await dialog.getByRole('link',{name:'Elegir esta suite'}).click();await expect(page.getByRole('radio',{name:/Suite Terraza/})).toBeChecked()
})

test('Los filtros de rituales y sus enlaces conservan la elección',async({page})=>{
  await page.goto('/experiencias');await page.getByRole('button',{name:'Sabores',exact:true}).click();await expect(page.locator('.ritual-card')).toHaveCount(1)
  await page.getByRole('button',{name:'Conoce el ritual',exact:true}).click();const dialog=page.getByRole('dialog');await expect(dialog).toContainText('35')
  await dialog.getByRole('link',{name:'Añadir a mi escapada'}).click();await expect(page.getByRole('checkbox',{name:/Mañanas sin prisa/})).toBeChecked()
  await page.goBack();await page.getByRole('button',{name:'Todos los rituales'}).click();await expect(page.locator('.ritual-card')).toHaveCount(3)
})

test('Las fechas y huéspedes de inicio llegan al formulario sin recargar',async({page})=>{
  await page.goto('/');await page.getByLabel('Fecha de llegada').fill(date(20));await page.getByLabel('Fecha de salida').fill(date(23));await page.getByLabel('Número de huéspedes').selectOption('3')
  await page.getByRole('button',{name:'Diseña tu escapada'}).click();await expect(page).toHaveURL(/tu-estancia/)
  await expect(page.getByLabel('Llegada',{exact:true})).toHaveValue(date(20));await expect(page.getByLabel('Salida',{exact:true})).toHaveValue(date(23));await expect(page.getByLabel('Huéspedes',{exact:true})).toHaveValue('3')
})

test('Valida fechas, duración y capacidad, preservando campos y enfocando errores',async({page})=>{
  await page.goto('/tu-estancia');await page.getByRole('button',{name:'Revisar mi escapada'}).click();await expect(page.getByRole('alert')).toBeFocused();await expect(page.locator('#arrival')).toHaveAttribute('aria-invalid','true')
  await fillDates(page);await page.getByLabel('Huéspedes',{exact:true}).selectOption('4');await page.getByRole('button',{name:'Revisar mi escapada'}).click();await expect(page.getByRole('alert')).toContainText('Esta suite admite hasta 2 personas')
  await page.getByRole('radio',{name:/Suite Terraza/}).check();await page.getByLabel('Salida',{exact:true}).fill(date(20));await page.getByRole('button',{name:'Revisar mi escapada'}).click();await expect(page.getByRole('alert')).toContainText('salida posterior')
  await page.getByLabel('Salida',{exact:true}).fill(date(40));await page.getByRole('button',{name:'Revisar mi escapada'}).click();await expect(page.getByRole('alert')).toContainText('máximo de 14 noches')
  await page.getByLabel('Llegada',{exact:true}).fill(date(-1));await page.getByRole('button',{name:'Revisar mi escapada'}).click();await expect(page.getByRole('alert')).toContainText('próximos 365 días')
  await fillDates(page);await page.getByRole('button',{name:'Revisar mi escapada'}).click();await expect(page.getByRole('heading',{name:'Todo, a tu ritmo.'})).toBeFocused()
})

test('Calcula estancia y extras, permite editar y crea solo un resumen local',async({page})=>{
  const posts=[];page.on('request',r=>{if(r.method()==='POST')posts.push(r.url())})
  await page.goto('/tu-estancia?suite=terraza');await fillDates(page);await page.getByLabel('Huéspedes',{exact:true}).selectOption('4');await page.getByRole('checkbox',{name:/El ritual del agua/}).check();await page.getByRole('checkbox',{name:/Mañanas sin prisa/}).check()
  await expect(page.locator('.summary-total')).toContainText('1460');await page.getByRole('button',{name:'Revisar mi escapada'}).click();await expect(page.locator('.review-details')).toContainText('3 noches · 4 personas')
  await page.getByRole('button',{name:'Editar estancia'}).click();await expect(page.getByLabel('Llegada',{exact:true})).toHaveValue(date(20));await expect(page.getByRole('checkbox',{name:/El ritual del agua/})).toBeChecked()
  await page.getByRole('checkbox',{name:/Mañanas sin prisa/}).uncheck();await expect(page.locator('.summary-total')).toContainText('1425');await page.getByRole('button',{name:'Revisar mi escapada'}).click()
  await page.getByRole('button',{name:'Crear resumen de muestra'}).click();await expect(page.locator('.demo-accept input')).not.toBeChecked();await expect(page.getByText('Resumen de muestra creado')).not.toBeVisible()
  await page.getByRole('checkbox',{name:/Entiendo que es una demostración/}).check();await page.getByRole('button',{name:'Crear resumen de muestra'}).click();await expect(page.getByText('Resumen de muestra creado')).toBeVisible()
  await expect(page.getByText('No se han enviado ni almacenado datos.',{exact:false})).toBeVisible();expect(posts).toEqual([]);expect(await page.evaluate(()=>localStorage.length)).toBe(0)
  await page.getByRole('button',{name:'Imaginar otra estancia'}).click();await expect(page.getByLabel('Llegada',{exact:true})).toHaveValue(date(20))
})

test('Menú móvil, FAQ, 404 y movimiento reducido',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/')
  const toggle=page.getByRole('button',{name:'Abrir menú'});await toggle.focus();await page.keyboard.press('Enter');await expect(page.getByRole('dialog')).toBeVisible();await page.keyboard.press('Escape');await expect(toggle).toBeFocused()
  await toggle.click();await page.getByRole('navigation',{name:'Navegación móvil'}).getByRole('link',{name:/Habitaciones/}).click();await expect(page.getByRole('dialog')).not.toBeVisible()
  await page.getByText('¿Esto es un hotel real?',{exact:true}).click();await expect(page.getByText('Auralma es una marca ficticia creada para este portafolio.',{exact:false})).toBeVisible()
  await page.goto('/no-existe');await expect(page.getByText('404 — UN PEQUEÑO DESVÍO')).toBeVisible();await page.getByRole('link',{name:'Volver al inicio'}).click();await expect(page).toHaveURL('/')
  expect(await page.locator('.hero').evaluate(el=>getComputedStyle(el).animationName)).toBe('none')
})

test('El HTML autónomo funciona sin recursos externos, con navegación y reservas',async({page})=>{
  const html=await readFile(new URL('../docs/vista-previa.html',import.meta.url),'utf8');const unexpected=[],errors=[]
  page.on('pageerror',e=>errors.push(e.message));await page.route('**/*',route=>{const u=route.request().url();if(u==='http://auralma.test/')return route.fulfill({contentType:'text/html',body:html});unexpected.push(u);return route.abort()})
  await page.goto('http://auralma.test/');await expect(page.locator('h1')).toContainText('El arte de');await page.getByRole('navigation',{name:'Navegación principal'}).getByRole('link',{name:'Habitaciones'}).click();await expect(page).toHaveURL(/#\/habitaciones/)
  await page.locator('.room-card').first().getByRole('link',{name:'Elegir esta suite'}).click();await fillDates(page);await page.getByRole('button',{name:'Revisar mi escapada'}).click();await expect(page.getByRole('heading',{name:'Todo, a tu ritmo.'})).toBeVisible()
  expect(unexpected).toEqual([]);expect(errors).toEqual([]);await expect(page.locator('script[type="module"]')).toHaveCount(1)
})
