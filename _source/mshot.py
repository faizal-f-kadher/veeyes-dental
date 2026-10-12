import asyncio, sys, json
from playwright.async_api import async_playwright
sys.path.insert(0, '.')
from qa import placeholder
pages = sys.argv[1].split(',')
W = int(sys.argv[2]) if len(sys.argv) > 2 else 390

async def route(r):
    u = r.request.url
    if u.startswith('http://localhost'): return await r.continue_()
    if r.request.resource_type == 'image':
        b = placeholder(u)
        if b: return await r.fulfill(status=200, content_type='image/jpeg', body=b)
    await r.abort()

AUDIT = r"""()=>{const out={small:[],tapsmall:[]};
document.querySelectorAll('p,li,a,span,dd,dt,label,button,b,figcaption,h3').forEach(e=>{const s=getComputedStyle(e);if(e.offsetParent===null||e.closest('.sr-only,[hidden]'))return;const fs=parseFloat(s.fontSize);if([...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())&&fs<15)out.small.push(e.tagName+'.'+(e.className||'')+' '+fs+' '+e.textContent.trim().slice(0,24))});
document.querySelectorAll('a,button,summary,input,select,textarea').forEach(e=>{if(e.offsetParent===null||e.closest('.sr-only,[hidden],.ba'))return;const r=e.getBoundingClientRect();if(r.width&&r.height<44&&!e.closest('p'))out.tapsmall.push(e.tagName+'.'+(e.className||'')+' '+Math.round(r.width)+'x'+Math.round(r.height)+' '+(e.textContent||'').trim().slice(0,22))});
out.small=[...new Set(out.small)].slice(0,30);out.tapsmall=[...new Set(out.tapsmall)].slice(0,40);out.h=document.body.scrollHeight;out.ov=document.documentElement.scrollWidth-innerWidth;return out}"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': W, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); await pg.route('**/*', route)
        for n in pages:
            await pg.goto(f'http://localhost:8765/{n}.html', wait_until='domcontentloaded', timeout=20000)
            await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
            await pg.wait_for_timeout(700)
            a = await pg.evaluate(AUDIT)
            print('==', n, 'height', a['h'], 'overflow', a['ov'])
            print(' small text:', a['small'])
            print(' small taps:', a['tapsmall'])
            await pg.evaluate("document.querySelector('.actionbar') && (document.querySelector('.actionbar').style.position='static')")
            await pg.screenshot(path=f'shots/m_{n.replace("/", "_")}.png', full_page=True, timeout=30000)
        await b.close()
asyncio.run(main())
