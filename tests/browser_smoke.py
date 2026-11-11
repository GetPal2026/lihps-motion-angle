"""Optional browser smoke test. Requires Python Playwright and Chromium."""
import asyncio
from pathlib import Path
import mimetypes
from playwright.async_api import async_playwright

URL='https://lihps-motion-angle.example/'
async def inject(page, alpha=0,beta=0,gamma=0,count=1,delay=.025):
    for i in range(count):
        await page.evaluate('''args => window.dispatchEvent(new DeviceOrientationEvent('deviceorientation', {alpha: args[0], beta: args[1], gamma:args[2],absolute:false}))''',[alpha,beta,gamma])
        await asyncio.sleep(delay)

async def main():
  async with async_playwright() as p:
    browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=await browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    # Browser environment blocks outbound and loopback network access. Build an
    # in-memory HTML test fixture with the same production source modules.
    import re
    root=Path('/mnt/data/LIHPS_Motion_Angle_PWA')
    html=(root/'index.html').read_text()
    styles=(root/'styles.css').read_text()
    math=(root/'math.js').read_text().replace('export ', '')
    app=(root/'app.js').read_text()
    app=re.sub(r"import\s*\{[^}]*\}\s*from\s*['\"]\./math\.js['\"];",'',app)
    app=app.replace('if(!window.isSecureContext){','if(false){') # test-fixture only
    html=html.replace('<link rel="stylesheet" href="./styles.css" />',f'<style>{styles}</style>')
    html=html.replace('<script defer type="module" src="./app.js"></script>',f'<script>Object.defineProperty(window,"localStorage",{{value:{{_store:{{}},getItem(k){{return this._store[k]??null}},setItem(k,v){{this._store[k]=String(v)}}}}}});window.DeviceOrientationEvent=class DeviceOrientationEvent extends Event {{constructor(type,opts){{super(type);Object.assign(this,opts)}}}};window.DeviceMotionEvent=class DeviceMotionEvent extends Event {{}}</script><script type="module">{math}\n{app}</script>')
    await page.set_content(html,wait_until='load')
    await page.wait_for_timeout(100)
    await page.screenshot(path='/mnt/data/LIHPS_Motion_Angle_PWA/tests/preview-ready.png',full_page=True)
    await page.get_by_role('button',name='Enable',exact=True).click()
    await inject(page,0,0,0,count=5)
    assert await page.locator('#sensor-status').inner_text()=='Motion sensors active'
    await page.locator('#trunk-tap').click()
    await inject(page,0,0,0,count=33)
    assert await page.locator('#trunk-phase').inner_text()=='MEASURING',await page.locator('#trunk-phase').inner_text()
    for a in range(1,46,3):await inject(page,a,count=1,delay=.03)
    for a in range(45,-1,-3):await inject(page,a,count=1,delay=.03)
    assert float(await page.locator('#trunk-peak').inner_text())>=42,await page.locator('#trunk-peak').inner_text()
    await page.locator('#trunk-tap').click()
    assert await page.locator('#trunk-phase').inner_text()=='TRIAL RECORDED'
    assert await page.locator('#stat-count').inner_text()=='1'
    await page.screenshot(path='/mnt/data/LIHPS_Motion_Angle_PWA/tests/preview-result.png',full_page=True)
    await page.locator('[data-screen="joint"]').click()
    await inject(page,0,40,0,count=26)
    assert '40' in await page.locator('#inclino-angle').inner_text()
    await page.locator('#capture-inclinometer').click()
    await page.locator('[data-tool="segments"]').click()
    await inject(page,0,10,0,count=27)
    await page.locator('#segments-capture').click()
    await inject(page,0,70,0,count=27)
    await page.locator('#segments-capture').click()
    assert '60' in await page.locator('#segments-angle').inner_text(),await page.locator('#segments-angle').inner_text()
    await page.locator('[data-tool="rom"]').click()
    await inject(page,0,0,0,count=5)
    await page.locator('#rom-tap').click()
    await inject(page,0,0,0,count=33)
    assert await page.locator('#rom-phase').inner_text()=='MEASURING'
    for b in range(0,31,3):await inject(page,0,b,0,count=1,delay=.035)
    assert float(await page.locator('#rom-magnitude').inner_text())>=27
    await page.locator('#rom-tap').click()
    await page.locator('[data-screen="records"]').click()
    assert '4 locally stored records' in await page.locator('#record-count').inner_text()
    async with page.expect_download() as downloadinfo:
        await page.locator('#export-csv').click()
    download=await downloadinfo.value
    assert download.suggested_filename.endswith('.csv')
    assert not errors,errors
    await page.screenshot(path='/mnt/data/LIHPS_Motion_Angle_PWA/tests/preview-records.png',full_page=True)
    await page.locator('[data-screen="trunk"]').click()
    await page.set_viewport_size({'width':320,'height':700})
    dims=await page.evaluate('({content:document.documentElement.scrollWidth,viewport:window.innerWidth})')
    assert dims['content']<=dims['viewport'],f'Horizontal overflow at 320px: {dims}'
    await page.screenshot(path='/mnt/data/LIHPS_Motion_Angle_PWA/tests/preview-320.png',full_page=True)
    print('UI smoke tests passed: sensor permission mock, zeroing, peak persistence, inclinometer, two-segment, ROM, local records, CSV.')
    await browser.close()

asyncio.run(main())
