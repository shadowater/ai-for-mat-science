/* Course-authored numerical least-squares demo. No network or external dependencies. */
(function () {
  'use strict';
  const training = [[1, 2], [2, 4], [3, 5]];
  const testing = [[4, 6.5], [5, 8.2]];
  function sse(data, a, b) {
    return data.reduce((sum, [x, y]) => sum + (y - a * x - b) ** 2, 0);
  }
  function gradientStep(data, a, b, rate = 0.05) {
    let da = 0, db = 0;
    for (const [x, y] of data) {
      const error = a * x + b - y;
      da += 2 * x * error / data.length;
      db += 2 * error / data.length;
    }
    return {a: a - rate * da, b: b - rate * db, norm: Math.hypot(da, db)};
  }
  function leastSquares(data) {
    const n = data.length;
    const mx = data.reduce((s, p) => s + p[0], 0) / n;
    const my = data.reduce((s, p) => s + p[1], 0) / n;
    const denominator = data.reduce((s, [x]) => s + (x - mx) ** 2, 0);
    if (!denominator) throw new Error('需要至少两个不同的 x 才能唯一确定斜率。');
    const a = data.reduce((s, [x, y]) => s + (x - mx) * (y - my), 0) / denominator;
    return {a, b: my - a * mx};
  }
  const math = {training, testing, sse, gradientStep, leastSquares};
  if (typeof module !== 'undefined' && module.exports) module.exports = math;
  if (typeof document === 'undefined') return;
  const $ = id => document.getElementById(id);
  let a = 1, b = 0, step = 0, history = [], timer = null;
  const number = value => Math.abs(value) < 0.0000005 ? '0.000' : value.toFixed(3);
  function pause() {
    if (timer !== null) clearInterval(timer);
    timer = null;
    $('pause').disabled = true;
    $('train').disabled = false;
  }
  function axes(width, height, xMax, yMin, yMax, xLabel, yLabel) {
    const left = 60, right = width - 20, top = 25, bottom = height - 48;
    const X = x => left + x / xMax * (right - left);
    const Y = y => bottom - (y - yMin) / (yMax - yMin) * (bottom - top);
    let svg = `<rect width="${width}" height="${height}" fill="white"/>`;
    for (let i = 0; i <= 5; i++) {
      const x = xMax * i / 5, y = yMin + (yMax - yMin) * i / 5;
      svg += `<path d="M${X(x)} ${top}V${bottom} M${left} ${Y(y)}H${right}" stroke="#e2eaf0"/>`;
      svg += `<text x="${X(x)}" y="${bottom + 22}" text-anchor="middle" font-size="13">${x.toFixed(xMax > 10 ? 0 : 1)}</text>`;
      svg += `<text x="${left - 9}" y="${Y(y) + 4}" text-anchor="end" font-size="13">${y.toFixed(1)}</text>`;
    }
    svg += `<path d="M${left} ${top}V${bottom}H${right}" fill="none" stroke="#536976"/>`;
    svg += `<text x="${right}" y="${height - 6}" text-anchor="end" font-size="14">${xLabel}</text><text x="8" y="15" font-size="14">${yLabel}</text>`;
    return {svg, X, Y};
  }
  function render() {
    $('equation').textContent = `ŷ = ${number(a)}x ${b < 0 ? '−' : '+'} ${number(Math.abs(b))}`;
    $('sse').textContent = sse(training, a, b).toFixed(6);
    $('aValue').textContent = a.toFixed(6); $('bValue').textContent = b.toFixed(6);
    $('slope').value = a; $('intercept').value = b;
    $('rows').innerHTML = training.map(([x, y]) => {
      const predicted = a * x + b, residual = y - predicted;
      return `<tr><td>${x}</td><td>${y}</td><td>${number(predicted)}</td><td>${number(residual)}</td><td>${(residual ** 2).toFixed(4)}</td></tr>`;
    }).join('');
    const p = axes(680, 430, 5.5, -2, 16, '输入 x（任意单位）', '测量 / 预测 y（任意单位）');
    let svg = p.svg;
    svg += `<defs><clipPath id="plotClip"><rect x="60" y="25" width="600" height="357"/></clipPath></defs><g clip-path="url(#plotClip)">`;
    svg += `<line x1="${p.X(0)}" y1="${p.Y(b)}" x2="${p.X(5.5)}" y2="${p.Y(a * 5.5 + b)}" stroke="#172d3b" stroke-width="3"/>`;
    for (const [x, y] of training) {
      svg += `<line x1="${p.X(x)}" y1="${p.Y(y)}" x2="${p.X(x)}" y2="${p.Y(a*x+b)}" stroke="#c44545" stroke-width="3" stroke-dasharray="6 4"/>`;
      svg += `<circle cx="${p.X(x)}" cy="${p.Y(y)}" r="7" fill="#087e8b"/><circle cx="${p.X(x)}" cy="${p.Y(a*x+b)}" r="4" fill="white" stroke="#172d3b"/>`;
    }
    if ($('showTest').checked) for (const [x, y] of testing) {
      const cx = p.X(x), cy = p.Y(y);
      svg += `<path d="M${cx} ${cy-8}l8 8 -8 8 -8 -8Z" fill="#b86700"/>`;
    }
    $('fitPlot').innerHTML = svg + '</g>';
    const maxLoss = history.length ? Math.max(0.2, ...history.map(p => p[1])) * 1.05 : 1;
    const l = axes(680, 225, Math.max(10, step), 0, maxLoss, '参数更新次数', '训练 SSE');
    $('lossPlot').innerHTML = l.svg + (history.length ? `<polyline points="${history.map(([i,v])=>`${l.X(i)},${l.Y(v)}`).join(' ')}" fill="none" stroke="#087e8b" stroke-width="3"/>` : '<text x="95" y="85" font-size="16" fill="#536976">点击“播放自动拟合”后显示真实误差曲线</text>');
    $('testMetric').hidden = !$('showTest').checked;
    $('testMetric').textContent = `新数据 MSE：${(sse(testing,a,b)/testing.length).toFixed(6)}。仅用于检查，未参与参数更新。`;
  }
  function clearRun() { pause(); step = 0; history = []; }
  for (const id of ['slope','intercept']) $(id).addEventListener('input', () => {
    clearRun(); a = Number($('slope').value); b = Number($('intercept').value);
    $('status').textContent = '手动调整参数：观察直线、残差和 SSE 的联动。'; render();
  });
  $('showTest').addEventListener('change',render);
  $('train').addEventListener('click', () => {
    if (step >= 800) { step = 0; history = []; }
    if (!history.length) history.push([0,sse(training,a,b)]);
    $('train').disabled = true; $('pause').disabled = false;
    timer = setInterval(() => {
      for (let i=0;i<4;i++) {
        const next = gradientStep(training,a,b); a=next.a; b=next.b; step++;
        history.push([step,sse(training,a,b)]);
        if (next.norm < 1e-6 || step >= 800) { pause(); break; }
      }
      $('status').textContent = timer === null ? `已停止，共更新 ${step} 次。可与直接最小二乘解比较。` : `正在根据训练误差更新参数：第 ${step} 次。`;
      render();
    },60);
  });
  $('pause').addEventListener('click',()=>{pause();$('status').textContent=`已暂停在第 ${step} 次，可继续播放。`;});
  $('exact').addEventListener('click',()=>{clearRun();({a,b}=leastSquares(training));$('status').textContent='直接求解：a = 1.5，b = 2/3，最小 SSE = 1/6。';render();});
  $('reset').addEventListener('click',()=>{clearRun();a=1;b=0;$('showTest').checked=false;$('status').textContent='已重置：a = 1，b = 0，SSE = 9。';render();});
  render();
}());
