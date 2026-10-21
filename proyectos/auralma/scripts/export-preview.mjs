import { readFile, writeFile, mkdir } from 'node:fs/promises'
import { resolve, dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const dist = join(root, 'dist')
let html = await readFile(join(dist, 'index.html'), 'utf8')
const scriptTag = html.match(/<script[^>]*src="([^"]+)"[^>]*><\/script>/)
const cssTag = html.match(/<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*>/)
if (!scriptTag || !cssTag) throw new Error('Build assets were not found. Run npm run build first.')

const buildPath = path => join(dist, path.replace(/^\//, ''))
let script = await readFile(buildPath(scriptTag[1]), 'utf8')
let css = await readFile(buildPath(cssTag[1]), 'utf8')
for (const name of ['costa', 'suite', 'horizonte', 'terraza', 'spa', 'desayuno']) {
  const source = `/images/${name}.webp`
  if (!script.includes(source)) throw new Error(`Image ${name} is missing from the build.`)
  const buffer = await readFile(buildPath(source))
  script = script.replaceAll(source, `data:image/webp;base64,${buffer.toString('base64')}`)
}
const fontPaths = [...new Set([...css.matchAll(/url\(([^)]+)\)/g)].map(match => match[1].replace(/^["']|["']$/g, '')))]
for (const path of fontPaths) {
  if (path.startsWith('data:')) continue
  if (!path.startsWith('/assets/')) throw new Error(`Unexpected external CSS resource: ${path}`)
  const font = await readFile(buildPath(path))
  const mime = path.endsWith('.woff2') ? 'font/woff2' : 'font/woff'
  css = css.replaceAll(path, `data:${mime};base64,${font.toString('base64')}`)
}
const favicon = await readFile(join(dist, 'favicon.svg'), 'utf8')
html = html.replace('<html lang="es">', '<html lang="es" data-preview="standalone">')
html = html.replace(cssTag[0], () => `<style>${css}</style>`)
html = html.replace(scriptTag[0], () => `<script type="module">${script.replace(/<\/script/gi, '<\\/script')}</script>`)
html = html.replace('href="/favicon.svg"', `href="data:image/svg+xml,${encodeURIComponent(favicon)}"`)
const fontLicenses = await Promise.all(['baskervville', 'manrope'].map(async name => `${name}\n${await readFile(join(root, 'public', 'licenses', `${name}.txt`), 'utf8')}`))
html = html.replace('</body>', () => `<!-- Bundled font licenses\n${fontLicenses.join('\n\n').replaceAll('--', '—')}\n-->\n</body>`)
const destination = join(root, 'docs', 'vista-previa.html')
await mkdir(dirname(destination), { recursive: true })
await writeFile(destination, html)
console.log(`Standalone preview saved: docs/vista-previa.html (${(Buffer.byteLength(html) / 1024 / 1024).toFixed(1)} MiB)`)
