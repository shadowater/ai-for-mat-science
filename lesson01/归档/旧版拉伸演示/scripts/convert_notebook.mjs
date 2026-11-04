// Dependency-light fallback converter: .ipynb -> self-contained presentation HTML.
// Does not claim to be nbconvert or to provide a Jupyter kernel.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import MarkdownIt from '../slidev/node_modules/markdown-it/index.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const nb=JSON.parse(fs.readFileSync(path.join(root,'notebook/lesson01.ipynb'),'utf8'));
const md=new MarkdownIt({html:true});
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
let sections=[],current='',notes='';
const flush=()=>{if(current)sections.push(`<section>${current}<aside>${esc(notes)}</aside></section>`);current='';notes='';};
for(const c of nb.cells){
 const type=c.metadata?.slideshow?.slide_type||'slide',src=c.source.join('');
 if(type==='notes'){notes+=src;continue;}if(type==='skip')continue;
 if(type==='slide'||type==='subslide')flush();
 if(c.cell_type==='markdown'){
   let body=md.render(src);
   const match=src.match(/http:\/\/127\.0\.0\.1:8765\/slidev\/public\/lab\.html\?mode=(\w+)/);
   if(match){body=md.render(src.split('[打开交互演示]')[0])+`<iframe title="交互演示" src="../slidev/public/lab.html?mode=${match[1]}"></iframe>`;}
   current+=body;
 }else{
   current+=`<details ${src.length<900?'open':''}><summary>Python 代码（在 Notebook 中编辑执行）</summary><pre><code>${esc(src)}</code></pre></details>`;
   for(const out of c.outputs||[]){
    if(out.output_type==='stream')current+=`<pre class="output">${esc(out.text.join(''))}</pre>`;
    if(out.data?.['image/png'])current+=`<img alt="教学模拟应力曲线" src="data:image/png;base64,${out.data['image/png']}">`;
   }
 }
}
flush();
const html=`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第一课 · Notebook 转换版</title><style>
*{box-sizing:border-box}body{margin:0;background:#07121f;color:#e3edf6;font-family:system-ui,'Microsoft YaHei',sans-serif}section{display:none;max-width:1120px;margin:0 auto;padding:40px 64px 95px;height:100vh;overflow:auto}section.on{display:block}h1{color:#73e0c2;font-size:38px;line-height:1.3;margin:0 0 26px}p,li{font-size:24px;line-height:1.7}strong{color:#73e0c2}table{width:100%;font-size:21px;border-collapse:collapse}td,th{padding:12px;text-align:left;border-bottom:1px solid #395870}pre{font:18px/1.55 monospace;white-space:pre-wrap;background:#10283c;padding:18px;border-radius:10px}a{color:#8ddcf3}iframe{width:100%;height:450px;border:1px solid #395870;border-radius:12px}img{max-width:100%;max-height:48vh}aside{display:none;color:#ffc99b;background:#203244;padding:16px;margin-top:20px;font-size:18px}body.notes aside{display:block}nav{position:fixed;bottom:0;width:100%;padding:12px 24px;background:#07121ff5;display:flex;align-items:center;gap:12px;border-top:1px solid #395870}button{border:1px solid #395870;border-radius:7px;color:#e3edf6;background:#18364d;padding:8px 16px;cursor:pointer;font:16px system-ui}#status{margin-left:auto;font-size:15px;color:#a4b8cb}summary{cursor:pointer;color:#8ddcf3;font-size:17px}.output{font-size:17px}#count{min-width:70px;text-align:center}
@media print{section{display:block;height:auto;min-height:95vh;page-break-after:always}nav,aside{display:none!important}body{background:white;color:#111}}
</style>${sections.join('\n')}<nav><button id="prev">← 上一页</button><span id="count"></span><button id="next">下一页 →</button><button id="notes">讲者备注 N</button><span id="status">Notebook 转换版 · 静态输出 + 本机交互演示</span></nav><script>
const pages=[...document.querySelectorAll('section')];let i=Math.max(0,Math.min(pages.length-1,(parseInt(location.hash.slice(1))||1)-1));function show(){pages.forEach((p,j)=>p.classList.toggle('on',j===i));document.querySelector('#count').textContent=(i+1)+' / '+pages.length;history.replaceState(null,'','#'+(i+1));}document.querySelector('#prev').onclick=()=>{i=Math.max(0,i-1);show()};document.querySelector('#next').onclick=()=>{i=Math.min(pages.length-1,i+1);show()};document.querySelector('#notes').onclick=()=>document.body.classList.toggle('notes');addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();document.querySelector('#next').click()}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();document.querySelector('#prev').click()}if(e.key.toLowerCase()==='n')document.querySelector('#notes').click()});show();
</script></html>`;
fs.writeFileSync(path.join(root,'notebook/lesson01.slides.html'),html);
console.log(`Converted Notebook to ${sections.length} HTML pages.`);
