/* Three browser-only animations using the UCI Wine measurements in wine-data.js. */
(function () {
  'use strict';
  const squaredDistance = (a, b) => (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2;
  function standardize(rows) {
    const mean = [0, 1].map(d => rows.reduce((s, p) => s + p[d], 0) / rows.length);
    const sd = [0, 1].map(d => Math.sqrt(rows.reduce((s, p) => s + (p[d] - mean[d]) ** 2, 0) / rows.length));
    return rows.map(p => [0, 1].map(d => (p[d] - mean[d]) / sd[d]));
  }
  function assign(rows, centers) {
    return rows.map(p => centers.reduce((best, c, j) => squaredDistance(p, c) < squaredDistance(p, centers[best]) ? j : best, 0));
  }
  function update(rows, labels, centers) {
    return centers.map((c, j) => {
      const members = rows.filter((_, i) => labels[i] === j);
      return members.length ? [0, 1].map(d => members.reduce((s, p) => s + p[d], 0) / members.length) : [...c];
    });
  }
  function initialize(rows, k) {
    const chosen = [0];
    while (chosen.length < k) {
      let best = -1, bestDistance = -1;
      rows.forEach((p, i) => {
        if (chosen.includes(i)) return;
        const distance = Math.min(...chosen.map(j => squaredDistance(p, rows[j])));
        if (distance > bestDistance) { best = i; bestDistance = distance; }
      });
      chosen.push(best);
    }
    return chosen.map(i => [...rows[i]]);
  }
  function objective(rows, labels, centers) {
    return rows.reduce((s, p, i) => s + squaredDistance(p, centers[labels[i]]), 0);
  }
  function classify(point, model) {
    const scores = model.coef.map((w, j) => w[0] * point[0] + w[1] * point[1] + model.intercept[j]);
    return scores.indexOf(Math.max(...scores));
  }
  const math = {standardize, squaredDistance, assign, update, initialize, objective, classify};
  if (typeof module !== 'undefined' && module.exports) module.exports = math;
  if (typeof document === 'undefined') return;

  const source = window.WINE_DATA;
  const rows = standardize(source.raw);
  const colors = ['#087e8b', '#b56000', '#7846a4'];
  const $ = id => document.getElementById(id);
  const X = x => 80 + (x + 4.8) * 420 / 9.6;
  const Y = y => 445 - (y + 4.8) * 420 / 9.6;
  let mode, centers, labels, phase, iteration, progress, timer, done, history;

  function stop() {
    if (timer !== null) clearInterval(timer);
    timer = null;
    $('play').disabled = done;
    $('pause').disabled = true;
  }
  function reset() {
    stop();
    mode = $('method').value;
    centers = initialize(rows, 3);
    labels = rows.map(() => -1);
    phase = 'assign'; iteration = 0; progress = 0; done = false; history = [];
    $('play').disabled = false;
    render();
  }
  function tick() {
    if (done) return;
    if (mode === 'kmeans') {
      if (phase === 'assign') {
        const next = assign(rows, centers);
        const stable = iteration > 0 && next.every((v, i) => v === labels[i]);
        labels = next;
        phase = 'update';
        history.push(`分配：J = ${objective(rows, labels, centers).toFixed(2)}`);
        if (stable) done = true;
      } else {
        centers = update(rows, labels, centers);
        iteration++;
        phase = 'assign';
        history.push(`第 ${iteration} 次更新：J = ${objective(rows, labels, centers).toFixed(2)}`);
        if (iteration >= 30) done = true;
      }
    } else {
      progress = Math.min(1, progress + 0.035);
      if (progress === 1) done = true;
    }
    render();
    if (done) stop();
  }
  function plotBase(xLabel, yLabel) {
    let svg = '<rect width="600" height="520" fill="white"/>';
    for (let v = -4; v <= 4; v += 2) {
      svg += `<path d="M${X(v)} 25V445 M80 ${Y(v)}H500" stroke="#e1e9ed"/>`;
      svg += `<text x="${X(v)}" y="466" text-anchor="middle" font-size="13">${v}</text>`;
      svg += `<text x="68" y="${Y(v) + 4}" text-anchor="end" font-size="13">${v}</text>`;
    }
    svg += `<text x="290" y="504" text-anchor="middle" font-size="15">${xLabel}</text>`;
    svg += `<text x="82" y="17" font-size="15">${yLabel}</text>`;
    return svg;
  }
  function pointsSvg(points, paint, opacity) {
    return points.map((p, i) => `<circle cx="${X(p[0])}" cy="${Y(p[1])}" r="4" fill="${paint(i)}" fill-opacity="${opacity}" stroke="white" stroke-width=".5"/>`).join('');
  }
  function render() {
    const descriptions = {
      kmeans: 'K-Means：178 个样品按酒精和苹果酸测量值分为 3 组。颜色表示算法当前给出的组别。',
      pca: 'PCA：从两个测量特征的散点图切换到 13 项化学指标的二维主成分投影。',
      svm: 'SVM：已知品种类别用于训练分类边界。淡色区域显示模型给出的类别。'
    };
    $('description').textContent = descriptions[mode];
    $('count').textContent = `${source.raw.length} 个真实样品`;
    $('step').textContent = mode === 'kmeans' ? `${iteration} 次中心更新` : `${Math.round(progress * 100)}%`;
    $('metric').textContent = mode === 'kmeans' && labels[0] >= 0 ? `J = ${objective(rows, labels, centers).toFixed(2)}` : '—';
    $('metricBox').hidden = mode !== 'kmeans';
    $('historyBox').hidden = mode !== 'kmeans';
    $('history').innerHTML = history.slice(-8).map(s => `<div>${s}</div>`).join('');
    $('play').disabled = done || timer !== null;
    $('pause').disabled = timer === null;
    let svg;
    if (mode === 'kmeans') {
      svg = plotBase('酒精测量值（标准化）', '苹果酸测量值（标准化）');
      svg += pointsSvg(rows, i => labels[i] < 0 ? '#667d8b' : colors[labels[i]], 0.85);
      svg += centers.map((p, j) => `<g stroke="${colors[j]}" stroke-width="4"><path d="M${X(p[0])-11} ${Y(p[1])}H${X(p[0])+11} M${X(p[0])} ${Y(p[1])-11}V${Y(p[1])+11}"/></g>`).join('');
      $('status').textContent = done ? '分组稳定，动画结束。' : labels[0] < 0 ? '点击播放，观察样品分组和中心移动。' : phase === 'update' ? '样品已按最近中心分组，下一步更新中心。' : '中心已移到组内平均位置，下一步重新分组。';
      $('detail').textContent = labels[0] < 0 ? '十字表示初始中心。' : colors.map((_, j) => `第 ${j+1} 组：${labels.filter(x => x === j).length} 个`).join('　');
    } else if (mode === 'pca') {
      const first = progress < 0.5;
      svg = plotBase(first ? '酒精测量值（标准化）' : '第一主成分', first ? '苹果酸测量值（标准化）' : '第二主成分');
      svg += pointsSvg(first ? rows : source.pca, () => '#087e8b', first ? 1 - progress * 1.8 : (progress - 0.5) * 2);
      $('status').textContent = done ? '二维主成分投影已显示。' : timer === null ? '点击播放，观察数据从两个原始特征视图切换到主成分视图。' : '正在切换二维视图。';
      $('detail').textContent = `前两个主成分分别解释 ${(source.pcaVariance[0]*100).toFixed(1)}% 和 ${(source.pcaVariance[1]*100).toFixed(1)}% 的标准化数据方差。`;
    } else {
      svg = plotBase('第一主成分', '第二主成分');
      for (let x = -4.8; x < 4.8; x += 0.4) for (let y = -4.8; y < 4.8; y += 0.4) {
        const group = classify([x + 0.2, y + 0.2], source.svm);
        svg += `<rect x="${X(x)}" y="${Y(y+0.4)}" width="17.5" height="17.5" fill="${colors[group]}" opacity="${(progress*0.20).toFixed(3)}"/>`;
      }
      svg += pointsSvg(source.pca, i => colors[source.labels[i]], 0.95);
      $('status').textContent = done ? '分类边界已显示。' : timer === null ? '点击播放，观察训练好的分类模型如何划分二维平面。' : '正在显示分类区域。';
      $('detail').textContent = '蓝、橙、紫分别表示品种类别 1、2、3；背景颜色表示 SVM 的分类结果。';
    }
    $('plot').innerHTML = svg;
  }
  $('method').addEventListener('change', reset);
  $('play').addEventListener('click', () => {
    if (done || timer !== null) return;
    timer = setInterval(tick, mode === 'kmeans' ? 650 : 35);
    $('play').disabled = true; $('pause').disabled = false;
  });
  $('pause').addEventListener('click', () => { stop(); render(); });
  $('reset').addEventListener('click', reset);
  timer = null;
  reset();
}());
