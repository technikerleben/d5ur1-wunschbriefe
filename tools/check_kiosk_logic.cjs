// Browser-independent regression checks for the kiosk's event and timer logic.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'apps/kontroll-kiosk/index.html'),'utf8');
const source=JSON.parse(fs.readFileSync(path.join(root,'materialien/arbeitsblaetter/loesungen_inhalte.json'),'utf8'));
class El {constructor(id='',classes=''){this.id=id;this.textContent='';this.dataset={};this.open=false;this.events={};const c=new Set(classes.split(' '));this.classList={add:x=>c.add(x),remove:x=>c.delete(x),contains:x=>c.has(x),toggle:(x,b)=>b?c.add(x):c.delete(x)}}addEventListener(t,f){this.events[t]=f}focus(){} }
const els={};for(const m of html.matchAll(/<\w+[^>]*\bid="([^"]+)"[^>]*>/g)){const cls=m[0].match(/class="([^"]*)"/);els[m[1]]=new El(m[1],cls?.[1]||'')}
const modes=['tip','solution'].map(mode=>Object.assign(new El(),{dataset:{mode}}));
const keys=['1','2','3','4','5','6','7','8','9','0','clear','backspace','show'].map(k=>Object.assign(new El(),{textContent:k,dataset:/^\d$/.test(k)?{}:{action:k}}));
const events={},timers=new Map();let tid=0;
const doc={getElementById:id=>els[id],querySelectorAll:s=>s==='[data-mode]'?modes:keys,querySelector:s=>s.includes('data-mode')?modes[0]:keys.at(-1),addEventListener:(t,f)=>events[t]=f,documentElement:{}};
const ctx={document:doc,window:{scrollTo(){}},location:{search:''},URLSearchParams,setTimeout:(f,ms)=>{timers.set(++tid,{f,ms});return tid},clearTimeout:id=>timers.delete(id)};vm.createContext(ctx);vm.runInContext(html.match(/<script>([\s\S]*)<\/script>/)[1],ctx);
const key=k=>events.keydown({key:k,preventDefault(){}});
for(const mode of ['tip','solution'])for(let n=1;n<=24;n++){ctx.chooseMode(mode);for(const c of String(n))key(c);key('Enter');assert.equal(els.resultText.textContent,source[n][mode==='tip'?'tip':'solution']);assert.equal(els.extra.classList.contains('hidden'),mode==='tip'||!source[n].extra);assert.equal(timers.size,0,'No reading timer');assert(!els.resultScreen.classList.contains('hidden'))}
ctx.chooseMode('solution');key('9');key('9');key('Enter');assert(els.error.textContent);key('Delete');assert.equal(els.error.textContent,'');key('1');key('0');key('Backspace');assert.equal(els.display.textContent,'1');key('Escape');assert.equal(els.display.textContent,'–');
ctx.chooseMode('tip');keys.find(k=>k.textContent==='3').events.click();keys.at(-1).events.click();assert.equal(els.resultText.textContent,source[3].tip);els.switchMode.onclick();assert.equal(els.resultText.textContent,source[3].solution);assert(!els.extra.classList.contains('hidden'));els.another.onclick();assert.equal(els.display.textContent,'–');assert.equal([...timers.values()][0].ms,180000);[...timers.values()][0].f();assert(!els.startScreen.classList.contains('hidden'));
assert(!/<(?:script|link|img)[^>]+(?:src|href)="https?:/.test(html),'No remote assets');
console.log('PASS: 48 content views, keys, keypad, validation, mode switch, extras, input reset, unlimited reading; no remote assets. DOM simulation; visual browser check separate.');
