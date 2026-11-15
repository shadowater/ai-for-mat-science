/* Course-authored K-Means / Lloyd iteration demo. No external dependencies. */
(function () {
  'use strict';
  const datasets = {
    six: [[1,1],[1,2],[2,1],[7,7],[7,8],[8,7]],
    rectangle: [[1,1],[1,2],[2,1],[2,2],[7,1],[7,2],[8,1],[8,2]]
  };
  const squaredDistance = (a,b) => (a[0]-b[0])**2+(a[1]-b[1])**2;
  function assign(data,centers) {
    return data.map(point=>{
      let best=0;
      for(let j=1;j<centers.length;j++) {
        if(squaredDistance(point,centers[j])<squaredDistance(point,centers[best])) best=j;
      }
      return best;
    });
  }
  function update(data,labels,centers) {
    return centers.map((center,j)=>{
      const members=data.filter((_,i)=>labels[i]===j);
      return members.length ? [0,1].map(dim=>members.reduce((s,p)=>s+p[dim],0)/members.length) : [...center];
    });
  }
  function objective(data,labels,centers) {
    return data.reduce((s,p,i)=>s+squaredDistance(p,centers[labels[i]]),0);
  }
  function initialize(data,k,mode) {
    const indexes=mode==='near' ? [0,1,data.length-1] : [0,Math.floor(data.length/2),data.length-1];
    return indexes.slice(0,k).map(i=>[...data[i]]);
  }
  const math={datasets,squaredDistance,assign,update,objective,initialize};
  if(typeof module!=='undefined'&&module.exports) module.exports=math;
  if(typeof document==='undefined') return;
  const $=id=>document.getElementById(id);
  const colors=['#087e8b','#b56000','#7846a4'];
  let data,centers,labels,phase,iteration,done,timer=null,log=[];
  function pause(){if(timer!==null)clearInterval(timer);timer=null;$('pause').disabled=true;$('play').disabled=done;}
  function render(){
    $('iteration').textContent=`${iteration} 次`;
    $('objective').textContent=labels[0]<0?'—':objective(data,labels,centers).toFixed(4);
    $('next').disabled=done;$('next').textContent=done?'已停止':phase==='assign'?'下一步：分配样本':'下一步：更新中心';
    $('rows').innerHTML=data.map((p,i)=>`<tr><td>${String.fromCharCode(65+i)}</td><td>${p[0]}</td><td>${p[1]}</td><td style="color:${labels[i]<0?'#536976':colors[labels[i]]}">${labels[i]<0?'未分配':`第 ${labels[i]+1} 组`}</td></tr>`).join('');
    $('centers').innerHTML=centers.map((p,j)=>`<p style="color:${colors[j]}">中心 ${j+1}：(${p[0].toFixed(3)}, ${p[1].toFixed(3)})</p>`).join('');
    $('history').innerHTML=log.map(p=>`<p>${p}</p>`).join('');
    // Equal pixel scale on both axes: range 0..9 spans 420px each.
    const X=x=>90+x*420/9,Y=y=>455-y*420/9;
    let svg='<rect width="660" height="510" fill="white"/>';
    for(let i=0;i<=9;i++) {
      svg+=`<path d="M${X(i)} 35V455 M90 ${Y(i)}H510" stroke="#e2eaf0"/>`;
      svg+=`<text x="${X(i)}" y="476" text-anchor="middle" font-size="13">${i}</text><text x="78" y="${Y(i)+4}" text-anchor="end" font-size="13">${i}</text>`;
    }
    svg+='<text x="512" y="502" text-anchor="end" font-size="15">描述符 1（教学坐标）</text><text x="90" y="20" font-size="15">描述符 2（教学坐标）</text>';
    data.forEach((p,i)=>{if(labels[i]>=0){const c=centers[labels[i]];svg+=`<line x1="${X(p[0])}" y1="${Y(p[1])}" x2="${X(c[0])}" y2="${Y(c[1])}" stroke="${colors[labels[i]]}" opacity=".45" stroke-width="2"/>`;}});
    data.forEach((p,i)=>{svg+=`<circle cx="${X(p[0])}" cy="${Y(p[1])}" r="8" fill="${labels[i]<0?'#71818d':colors[labels[i]]}"/><text x="${X(p[0])+11}" y="${Y(p[1])-9}" font-size="15">${String.fromCharCode(65+i)}${labels[i]<0?'':` · ${labels[i]+1}`}</text>`;});
    centers.forEach((p,j)=>{const x=X(p[0]),y=Y(p[1]);svg+=`<g stroke="${colors[j]}" stroke-width="4"><path d="M${x-11} ${y}H${x+11} M${x} ${y-11}V${y+11}"/></g><text x="${x+13}" y="${y+20}" font-size="15" fill="${colors[j]}">中心 ${j+1}</text>`;});
    $('plot').innerHTML=svg;
  }
  function reset(){
    done=false;pause();data=datasets[$('dataset').value];centers=initialize(data,Number($('k').value),$('init').value);
    labels=data.map(()=>-1);phase='assign';iteration=0;log=[];
    $('status').textContent='尚未分组。先预测每个样本离哪个中心更近，再点击下一步。';render();
  }
  function next(){
    if(done)return;
    if(phase==='assign'){
      const nextLabels=assign(data,centers);
      const stable=iteration>0&&nextLabels.every((j,i)=>j===labels[i]);
      labels=nextLabels;phase='update';
      log.push(`分配样本：J = ${objective(data,labels,centers).toFixed(4)}`);
      if(stable){done=true;pause();$('status').textContent='分组不再改变，中心已是组内平均，停止。得到的是当前初始化下的一个解。';}
      else $('status').textContent='样本已分给最近中心。接下来计算各组平均位置；此时中心还未移动。';
    }else{
      centers=update(data,labels,centers);iteration++;phase='assign';
      log.push(`第 ${iteration} 次更新中心：J = ${objective(data,labels,centers).toFixed(4)}`);
      $('status').textContent='中心已移到各组平均位置；样本位置不变。下一步重新按最近中心分组。';
      if(iteration>=30){done=true;pause();$('status').textContent='已达到 30 次更新上限，未进一步确认收敛。';}
    }
    render();
  }
  $('next').addEventListener('click',next);
  $('play').addEventListener('click',()=>{if(done||timer!==null)return;timer=setInterval(next,900);$('play').disabled=true;$('pause').disabled=false;});
  $('pause').addEventListener('click',()=>{pause();$('status').textContent+=' 已暂停，可继续逐步操作或播放。';});
  $('reset').addEventListener('click',reset);
  for(const id of ['dataset','k','init'])$(id).addEventListener('change',reset);
  reset();
}());
