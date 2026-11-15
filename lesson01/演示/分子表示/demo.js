/* Neighborhood visualization, not a trained neural network. */
(function(){
'use strict';
const molecules={ethanol:{atoms:['C','C','O'],edges:[[0,1],[1,2]]},ether:{atoms:['C','O','C'],edges:[[0,1],[1,2]]}};
function neighborhood(molecule,root,hops){
 const visited=new Set([root]);let frontier=[root];
 for(let hop=0;hop<hops;hop++){
  const next=[];
  for(const node of frontier)for(const [a,b] of molecule.edges){
   const neighbor=a===node?b:b===node?a:null;
   if(neighbor!==null&&!visited.has(neighbor)){visited.add(neighbor);next.push(neighbor);}
  }
  frontier=next;
 }
 return [...visited];
}
if(typeof module!=='undefined'&&module.exports)module.exports={molecules,neighborhood};
if(typeof document==='undefined')return;
let hops=0,timer=null;const $=id=>document.getElementById(id);
function stop(){if(timer!==null)clearInterval(timer);timer=null;$('play').disabled=false;}
function render(){
 document.querySelectorAll('[data-hop]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.hop)===hops)));
 $('status').textContent=['只提供原子类型时，两边观察中心都是碳。','直接邻居不同：乙醇中连着碳，二甲醚中连着氧。','两步覆盖完整的重原子图：元素总数相同，连接顺序仍不同。'][hops];
 for(const [id,m] of Object.entries(molecules)){
  const selected=neighborhood(m,0,hops);let svg='';
  for(const [a,b]of m.edges)svg+=`<line x1="${65+a*140}" y1="100" x2="${65+b*140}" y2="100" stroke="#586e7a" stroke-width="5"/>`;
  m.atoms.forEach((element,i)=>{svg+=`<circle cx="${65+i*140}" cy="100" r="30" fill="${selected.includes(i)?'#075f70':'#e2eaf0'}" stroke="${i===0?'#b56c00':'#91aeba'}" stroke-width="${i===0?5:2}"/><text x="${65+i*140}" y="109" text-anchor="middle" fill="${selected.includes(i)?'white':'#182e3e'}" font-size="27">${element}</text><text x="${65+i*140}" y="160" text-anchor="middle" font-size="15">原子 ${i+1}</text>`;});
  $(id).innerHTML=svg;$(id+'Info').textContent=`当前覆盖：${selected.map(i=>`原子 ${i+1}（${m.atoms[i]}）`).join('、')}`;
 }
}
document.querySelectorAll('[data-hop]').forEach(b=>b.addEventListener('click',()=>{stop();hops=Number(b.dataset.hop);render();}));
$('play').addEventListener('click',()=>{stop();hops=0;render();$('play').disabled=true;timer=setInterval(()=>{hops++;render();if(hops===2)stop();},1400);});
$('pause').addEventListener('click',stop);render();
}());
