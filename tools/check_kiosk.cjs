// Run with Playwright installed; optional KIOSK_BROWSER executable path.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const data=JSON.parse(fs.readFileSync(path.join(root,'materialien/arbeitsblaetter/loesungen_inhalte.json'),'utf8'));
 const browser=await chromium.launch({headless:true,...(process.env.KIOSK_BROWSER?{executablePath:process.env.KIOSK_BROWSER}:{})});
 const page=await browser.newPage({viewport:{width:1366,height:768}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.clock.install();
 await page.goto('file://'+path.join(root,'apps/kontroll-kiosk/index.html'));
 await page.context().setOffline(true);
 for(const mode of ['tip','solution'])for(let n=1;n<=24;n++){
  await page.locator('#homeHeader').click();await page.locator(`[data-mode="${mode}"]`).click();
  await page.keyboard.type(String(n));await page.keyboard.press('Enter');
  assert.equal(await page.locator('#resultText').textContent(),data[n][mode==='tip'?'tip':'solution']);
  assert.equal(await page.locator('#extra').isVisible(),mode==='solution'&&!!data[n].extra);
  assert.equal(await page.locator('#extra').evaluate(e=>e.open),false);
  assert.equal(await page.locator('#resultTitle').textContent(),`Blatt ${n} – ${data[n].title}`);
 }
 await page.locator('#another').click();await page.keyboard.type('99');await page.keyboard.press('Enter');assert(await page.locator('#error').textContent());
 await page.keyboard.press('Delete');assert.equal(await page.locator('#error').textContent(),'');await page.keyboard.type('10');await page.keyboard.press('Backspace');assert.equal(await page.locator('#display').textContent(),'1');
 await page.keyboard.press('Escape');assert(await page.locator('#startScreen').isVisible());
 await page.locator('[data-mode="tip"]').click();await page.getByRole('button',{name:'3',exact:true}).click();await page.locator('[data-action="show"]').click();
 await page.locator('#switchMode').click();await page.locator('#extra summary').click();assert(await page.locator('#extraText').isVisible());
 await page.clock.fastForward(180001);assert(await page.locator('#resultScreen').isVisible());
 await page.locator('#another').click();await page.clock.fastForward(180001);assert(await page.locator('#startScreen').isVisible());
 const out=process.env.KIOSK_SCREENSHOTS;if(out){fs.mkdirSync(out,{recursive:true});await page.screenshot({path:path.join(out,'start.png'),fullPage:true})}
 await page.locator('[data-mode="solution"]').click();await page.keyboard.type('10');await page.keyboard.press('Enter');
 if(out)await page.screenshot({path:path.join(out,'solution.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 if(out)await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
 assert.deepEqual(errors,[]);await browser.close();console.log('PASS: 48 entries, offline use, keypad, keyboard, errors, mode switch, optional extras, reading timer, input reset, responsive width, console.');
})().catch(e=>{console.error(e);process.exit(1)});
