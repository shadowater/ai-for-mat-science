'use strict';
const D=window.SOLUBILITY_DEMO;
if(!D) throw new Error('缺少 data.js，请保留演示目录中的全部文件。');
const $=id=>document.getElementById(id), clone=x=>JSON.parse(JSON.stringify(x));
let index=D.best_epoch-1, state, dirty=false, timer=null, selected={kind:'c'};
const names=['logP','分子量','可旋转键数','芳香重原子比例'];
function forward(x,m){
 const z=x.map((v,i)=>(v-D.model.input_mean[i])/D.model.input_scale[i]);
 const a=Array.from({length:8},(_,j)=>z.reduce((s,v,i)=>s+v*m.weights[0][i][j],m.biases[0][j]));
 const h=a.map(Math.tanh), t=h.reduce((s,v,j)=>s+v*m.weights[1][j][0],m.biases[1][0]);
 return {z,a,h,t,y:t*D.model.target_scale+D.model.target_mean};
}
function get(p,m=state){return p.kind==='w'?m.weights[0][p.i][p.j]:p.kind==='b'?m.biases[0][p.j]:p.kind==='v'?m.weights[1][p.j][0]:m.biases[1][0];}
function put(p,v){if(p.kind==='w')state.weights[0][p.i][p.j]=v;else if(p.kind==='b')state.biases[0][p.j]=v;else if(p.kind==='v')state.weights[1][p.j][0]=v;else state.biases[1][0]=v;}
function label(p){return p.kind==='w'?`w${p.j+1},${p.i+1}`:p.kind==='b'?`b${p.j+1}`:p.kind==='v'?`v${p.j+1}`:'输出偏置 c';}
function pause(){clearInterval(timer);timer=null;$('play').textContent='播放训练';}
function load(i){$('error').textContent='';index=i;state=clone(D.frames[index]);dirty=false;$('epoch').value=index+1;render();}
function metrics(rows,m){let abs=0,sq=0;for(const r of rows){const e=forward(r.x,m).y-r.y;abs+=Math.abs(e);sq+=e*e;}return {mae:abs/rows.length,rmse:Math.sqrt(sq/rows.length)};}
function canvas(id){const el=$(id), dpr=window.devicePixelRatio||1,w=el.clientWidth,h=el.clientHeight;el.width=w*dpr;el.height=h*dpr;const c=el.getContext('2d');c.scale(dpr,dpr);return {c,w,h};}
function chart(id,xmin,xmax,ymin,ymax,xlabel,ylabel){
 const {c,w,h}=canvas(id),l=58,r=w-18,t=25,b=h-45;
 const x=v=>l+(v-xmin)/(xmax-xmin)*(r-l),y=v=>b-(v-ymin)/(ymax-ymin)*(b-t);
 c.font='11px system-ui';c.fillStyle='#586b80';
 for(let i=0;i<=4;i++){let xx=xmin+(xmax-xmin)*i/4,yy=ymin+(ymax-ymin)*i/4;c.strokeStyle='#e6ebf2';c.beginPath();c.moveTo(l,y(yy));c.lineTo(r,y(yy));c.stroke();c.textAlign='right';c.fillText(yy.toFixed(2),l-7,y(yy)+4);c.textAlign='center';c.fillText(xx.toFixed(id==='loss'?0:1),x(xx),b+18);}
 c.textAlign='center';c.fillText(xlabel,(l+r)/2,h-5);c.textAlign='left';c.fillText(ylabel,5,13);return {c,x,y,l,r,t,b};
}
function loss(){
 const ymax=Math.max(...D.frames.flatMap(f=>[f.train_MSE,f.validation_MSE]))*1.05;
 const {c,x,y,t,b}=chart('loss',1,D.frames.length,0,ymax,'训练轮数','MSE（logS²）');
 for(const [key,color] of [['train_MSE','#195cd5'],['validation_MSE','#d47720']]){c.strokeStyle=color;c.lineWidth=2;c.beginPath();D.frames.forEach((f,i)=>i?c.lineTo(x(f.epoch),y(f[key])):c.moveTo(x(f.epoch),y(f[key])));c.stroke();}
 for(const [ep,dash,col] of [[D.best_epoch,[5,4],'#79869a'],[index+1,[],'#203047']]){c.setLineDash(dash);c.strokeStyle=col;c.beginPath();c.moveTo(x(ep),t);c.lineTo(x(ep),b);c.stroke();}c.setLineDash([]);
}
function scatter(rows){
 const pts=rows.map(r=>[r.y,forward(r.x,state).y]);const vs=pts.flat();let lo=Math.min(...vs)-.5,hi=Math.max(...vs)+.5;
 const {c,x,y}=chart('scatter',lo,hi,lo,hi,'实测 logS','预测 logS');c.strokeStyle='#98a4b5';c.beginPath();c.moveTo(x(lo),y(lo));c.lineTo(x(hi),y(hi));c.stroke();c.fillStyle='#195cd599';
 for(const [a,b]of pts){c.beginPath();c.arc(x(a),y(b),3,0,Math.PI*2);c.fill();}
}
function paramUI(){
 const p=selected,base=get(p,D.frames[index]);$('paramLabel').textContent=label(p);$('paramSlider').min=Math.min(base-3,get(p));$('paramSlider').max=Math.max(base+3,get(p));$('paramSlider').value=get(p);$('paramNumber').value=Number(get(p).toPrecision(10));
 $('effect').textContent=`本轮原值：${base.toFixed(6)}；当前值：${get(p).toFixed(6)}。修改 c 增加 0.1，会使所有预测 logS 增加 ${(D.model.target_scale*.1).toFixed(4)}。`;
}
function parameterTable(){
 const table=$('params');table.replaceChildren();
 const head=document.createElement('tr');for(const text of ['参数 / 隐藏单元',...Array.from({length:8},(_,j)=>`h${j+1}`)]){const th=document.createElement('th');th.textContent=text;head.append(th);}table.append(head);
 const rows=[...names.map((n,i)=>({name:`${n} 的权重`,params:Array.from({length:8},(_,j)=>({kind:'w',i,j}))})),{name:'隐藏偏置 b',params:Array.from({length:8},(_,j)=>({kind:'b',j}))},{name:'输出权重 v',params:Array.from({length:8},(_,j)=>({kind:'v',j}))},{name:'输出偏置 c',params:[{kind:'c'}]}];
 for(const row of rows){const tr=document.createElement('tr'),th=document.createElement('th');th.textContent=row.name;tr.append(th);for(const p of row.params){const td=document.createElement('td'),btn=document.createElement('button'),v=get(p);btn.className='param'+(JSON.stringify(p)===JSON.stringify(selected)?' selected':'');btn.textContent=v.toFixed(4);btn.title=label(p);btn.setAttribute('aria-label',`${label(p)}，${v.toFixed(6)}`);btn.style.background=`rgba(${v>=0?'25,92,213':'212,119,32'},${.06+Math.min(Math.abs(v)/3,1)*.32})`;btn.onclick=()=>{selected=p;parameterTable();paramUI();};td.append(btn);tr.append(td);}table.append(tr);}
}
function sampleUI(){
 const r=D.samples[Number($('sample').value)],f=forward(r.x,state);
 $('inputs').innerHTML='<tr><th>输入</th><th>原值</th><th>标准化后</th></tr>'+names.map((n,i)=>`<tr><td>${n}</td><td>${r.x[i].toFixed(4)}</td><td>${f.z[i].toFixed(4)}</td></tr>`).join('');
 $('hidden').innerHTML='<tr><th>单元</th><th>加权和 aⱼ</th><th>tanh(aⱼ)</th><th>vⱼhⱼ</th></tr>'+f.h.map((h,j)=>`<tr><td>h${j+1}</td><td>${f.a[j].toFixed(4)}</td><td>${h.toFixed(4)}</td><td>${(h*state.weights[1][j][0]).toFixed(4)}</td></tr>`).join('');
 $('output').textContent=`8 项贡献求和再加 c = ${f.t.toFixed(6)}；还原尺度：${D.model.target_mean.toFixed(6)} + ${D.model.target_scale.toFixed(6)} × (${f.t.toFixed(6)}) = ${f.y.toFixed(6)}。实测 logS = ${r.y.toFixed(4)}；预测误差 = ${(f.y-r.y).toFixed(4)}。`;
}
function render(){
 $('mode').textContent=dirty?'手动修改':'训练记录';$('epochLabel').textContent=`${index+1} / ${D.frames.length}`;
 const rows=D.samples.filter(r=>r.split===$('split').value),m=metrics(rows,state),base=metrics(rows,D.frames[index]);$('mae').textContent=m.mae.toFixed(3);$('rmse').textContent=m.rmse.toFixed(3);$('baseRmse').textContent=base.rmse.toFixed(3);
 loss();scatter(rows);parameterTable();paramUI();sampleUI();
}
function edit(v){if(!Number.isFinite(v)||Math.abs(v)>1000){$('error').textContent='请输入 −1000 到 1000 之间的有限数值。';return;}$('error').textContent='';pause();put(selected,v);dirty=true;render();}
function play(){pause();if(index===D.frames.length-1)load(0);else if(dirty)load(index);$('play').textContent='暂停';timer=setInterval(()=>{if(index>=D.frames.length-1){pause();return;}load(index+1);},Number($('speed').value));}
$('play').onclick=()=>timer?pause():play();$('speed').onchange=()=>{if(timer)play();};$('epoch').oninput=e=>{pause();load(Number(e.target.value)-1);};$('best').onclick=()=>{pause();load(D.best_epoch-1);};$('reset').onclick=()=>{pause();load(index);};$('split').onchange=()=>{fillSamples();render();};$('sample').onchange=sampleUI;
$('paramSlider').oninput=e=>edit(Number(e.target.value));$('paramNumber').onchange=e=>{if(e.target.value.trim()===''){$('error').textContent='请输入数值。';return;}edit(Number(e.target.value));};$('plus').onclick=()=>{selected={kind:'c'};edit(get(selected)+.1);};
$('export').onclick=()=>{const model={...D.model,weights:state.weights,biases:state.biases,demo_origin:{epoch:index+1,manually_modified:dirty}},url=URL.createObjectURL(new Blob([JSON.stringify(model,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`溶解度参数-第${index+1}轮${dirty?'-手动修改':''}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
function fillSamples(){const el=$('sample');el.replaceChildren();D.samples.forEach((r,i)=>{if(r.split!==$('split').value)return;const o=document.createElement('option');o.value=i;o.textContent=r.name;el.append(o);});}
$('epoch').max=D.frames.length;fillSamples();load(index);window.addEventListener('resize',()=>render());
// Expose the same forward calculation for numerical verification.
window.solubilityForward=forward;
