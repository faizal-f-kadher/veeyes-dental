import asyncio, json, sys, io, os, re, glob
from PIL import Image
from playwright.async_api import async_playwright
META = json.load(open('meta.json'))
CACHE = {}
def placeholder(url):
    base = url.split('?')[0]
    m = META.get(url) or META.get(base) or next((v for k, v in META.items() if k.split('?')[0] == base), None)
    if not m: return None
    if url in CACHE: return CACHE[url]
    w, h = m['w'], m['h']; s = min(1, 900 / max(w, h)); W, H = max(1, int(w*s)), max(1, int(h*s))
    if m['grid']:
        g = Image.new('RGB', (6, 4)); g.putdata([tuple(int(c[i:i+2], 16) for i in (0, 2, 4)) for c in m['grid']])
        im = g.resize((W, H), Image.BICUBIC)
    else:
        im = Image.new('RGB', (W, H), m['avg'])
    b = io.BytesIO(); im.save(b, 'JPEG', quality=70); CACHE[url] = b.getvalue(); return CACHE[url]

async def route(r):
    u = r.request.url
    if u.startswith('http://localhost'): return await r.continue_()
    if r.request.resource_type == 'image':
        body = placeholder(u)
        if body: return await r.fulfill(status=200, content_type='image/jpeg', body=body)
    await r.abort()

CHECK = r"""() => {
  const out = {overflow: document.documentElement.scrollWidth - innerWidth, clipped: [], overlaps: [], noalt: [], emptyLinks: []};
  const vis = e => { const s = getComputedStyle(e); return s.display !== 'none' && s.visibility !== 'hidden' && e.offsetParent !== null; };
  document.querySelectorAll('h1,h2,h3,p,a,b,span,li,dt,dd,label,button').forEach(e => {
    if (!vis(e) || e.closest('.sr-only,.ba,[hidden]')) return;
    if (e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflowX !== 'visible' && e.clientWidth > 0) out.clipped.push(e.tagName + '.' + e.className + ': ' + e.textContent.trim().slice(0, 40));
    const r = e.getBoundingClientRect(); if (r.right > innerWidth + 1 && !e.closest('.filters')) out.clipped.push('OUT ' + e.tagName + '.' + e.className + ': ' + e.textContent.trim().slice(0, 40) + ' ' + Math.round(r.right));
  });
  document.querySelectorAll('img').forEach(i => { if (!i.hasAttribute('alt')) out.noalt.push(i.src.slice(-50)); });
  document.querySelectorAll('a').forEach(a => { if (!a.textContent.trim() && !a.getAttribute('aria-label') && !a.querySelector('img[alt]:not([alt=""])')) out.emptyLinks.push(a.getAttribute('href')); });
  out.clipped = [...new Set(out.clipped)].slice(0, 12);
  return out;
}"""

async def main(pages, sizes, shots=True):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for (w, h, tag) in sizes:
            ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: m.type == 'error' and not 'ERR_FAILED' in m.text and not 'net::' in m.text and errs.append(m.text))
            await pg.route('**/*', route)
            for name in pages:
                errs.clear()
                await pg.goto(f'http://localhost:8765/{name}.html', wait_until='load')
                await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
                await pg.wait_for_timeout(1500)
                res = await pg.evaluate(CHECK)
                flag = res['overflow'] or res['clipped'] or res['noalt'] or res['emptyLinks'] or errs
                print(f"{tag} {name}: overflow={res['overflow']} clipped={res['clipped']} noalt={res['noalt']} empty={res['emptyLinks']} errs={errs}" if flag else f"{tag} {name}: ok")
                if shots:
                    os.makedirs('shots', exist_ok=True)
                    await pg.screenshot(path=f"shots/{name.replace('/','_')}_{tag}.png", full_page=True)
            await ctx.close()
        await b.close()

if __name__ == '__main__':
    pages = sys.argv[1].split(',') if len(sys.argv) > 1 and sys.argv[1] != 'all' else \
        [os.path.relpath(f, 'site')[:-5] for f in sorted(glob.glob('site/*.html') + glob.glob('site/post/*.html')) if '<meta http-equiv="refresh"' not in open(f).read()]
    sizes = {'d': (1440, 900, 'd'), 't': (1024, 1366, 't'), 'm': (390, 844, 'm')}
    sel = [sizes[k] for k in (sys.argv[2] if len(sys.argv) > 2 else 'dtm')]
    asyncio.run(main(pages, sel, shots=(len(sys.argv) <= 3)))
