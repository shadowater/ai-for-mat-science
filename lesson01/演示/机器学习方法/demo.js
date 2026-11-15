/* Three browser-only animations using the UCI Wine measurements in wine-data.js. */
(function () {
  'use strict';
  const squaredDistance = (a, b) => a.reduce((sum, value, d) => sum + (value - b[d]) ** 2, 0);
  function standardize(rows) {
    const mean = rows[0].map((_, d) => rows.reduce((s, p) => s + p[d], 0) / rows.length);
    const sd = rows[0].map((_, d) => Math.sqrt(rows.reduce((s, p) => s + (p[d] - mean[d]) ** 2, 0) / rows.length));
    return rows.map(p => rows[0].map((_, d) => (p[d] - mean[d]) / (sd[d] || 1)));
  }
  function assign(rows, centers) {
    return rows.map(p => centers.reduce((best, c, j) => squaredDistance(p, c) < squaredDistance(p, centers[best]) ? j : best, 0));
  }
  function update(rows, labels, centers) {
    return centers.map((c, j) => {
      const members = rows.filter((_, i) => labels[i] === j);
      return members.length ? rows[0].map((_, d) => members.reduce((s, p) => s + p[d], 0) / members.length) : [...c];
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
    const scores = model.coef.map((w, j) => w.reduce((sum, value, d) => sum + value * point[d], 0) + model.intercept[j]);
    return scores.indexOf(Math.max(...scores));
  }
  function compareGroups(labels, truth) {
    const counts = Array.from({length: 3}, () => [0, 0, 0]);
    labels.forEach((group, i) => { if (group >= 0) counts[group][truth[i]]++; });
    const permutations = [[0,1,2], [0,2,1], [1,0,2], [1,2,0], [2,0,1], [2,1,0]];
    const matches = permutations.map(order => order.reduce((sum, category, group) => sum + counts[group][category], 0));
    const matched = Math.max(...matches);
    return {counts, matched, mapping: permutations[matches.indexOf(matched)]};
  }
  const math = {compareGroups, standardize, squaredDistance, assign, update, initialize, objective, classify};
  if (typeof module !== 'undefined' && module.exports) module.exports = math;
  if (typeof document === 'undefined') return;

  const source = window.WINE_DATA;
  const $ = id => document.getElementById(id);
  const clusterColors = ['#28788c', '#a86d1a', '#8754a2'];
  const varietyColors = ['#007f69', '#be4b38', '#5368bc'];
  const rawPair = standardize(source.raw.map(row => row.slice(0, 2)));
  const saved = new Map();
  let selected = [0, 1], dimensions = 2, rows = [], centers = [], labels = [];
  let mode = 'kmeans', phase = 'assign', iteration = 0, progress = 0;
  let timer = null, done = false, converged = false, history = [];
  const names = () => selected.map(i => source.featureNames[i]);
  const valid = () => mode !== 'kmeans' || selected.length >= 2;
  const animated = () => mode === 'kmeans' || dimensions === 2;
  function stop() { if (timer !== null) clearInterval(timer); timer = null; }
  function reset() {
    stop();
    mode = $('method').value;
    dimensions = Number($('components').value);
    rows = selected.length ? standardize(source.raw.map(row => selected.map(d => row[d]))) : [];
    centers = rows.length ? initialize(rows, 3) : [];
    labels = source.labels.map(() => -1);
    phase = 'assign'; iteration = 0; progress = 0; done = false; converged = false; history = [];
    $('saveHint').textContent = '';
    render();
  }
  function advance() {
    if (done || !valid()) return;
    if (mode === 'kmeans') {
      if (phase === 'assign') {
        const next = assign(rows, centers);
        converged = iteration > 0 && next.every((v, i) => v === labels[i]);
        labels = next;
        phase = 'update';
        history.push(`分配样品 · J = ${objective(rows, labels, centers).toFixed(2)}`);
        done = converged || iteration >= 100;
      } else {
        centers = update(rows, labels, centers);
        iteration++;
        phase = 'assign';
        history.push(`更新中心 ${iteration} · J = ${objective(rows, labels, centers).toFixed(2)}`);
      }
    } else { progress = Math.min(1, progress + 0.05); done = progress === 1; }
    if (done) stop();
  }
  function tick() { advance(); render(); }
  const legend = (colors, prefix) => colors.map((color, i) => `<span><i style="background:${color}"></i>${prefix} ${i + 1}</span>`).join('');
  function axes(points, xLabel, yLabel) {
    const extent = Math.max(2, Math.ceil(Math.max(...points.flat().map(Math.abs)) + 0.3));
    const X = x => 72 + (x + extent) * 456 / (2 * extent);
    const Y = y => 442 - (y + extent) * 396 / (2 * extent);
    const stride = Math.max(1, Math.ceil(extent / 3));
    let svg = '<rect width="600" height="520" fill="white"/>';
    for (let v = -Math.floor(extent / stride) * stride; v <= extent; v += stride) {
      svg += `<path d="M${X(v)} 46V442 M72 ${Y(v)}H528" stroke="#e2e9ee"/>`;
      svg += `<text x="${X(v)}" y="466" text-anchor="middle" font-size="14" fill="#567">${v}</text>`;
      svg += `<text x="60" y="${Y(v) + 5}" text-anchor="end" font-size="14" fill="#567">${v}</text>`;
    }
    svg += `<text x="72" y="25" font-size="16" fill="#345">${yLabel}</text><text x="300" y="502" text-anchor="middle" font-size="16" fill="#345">${xLabel}</text>`;
    return {svg, X, Y};
  }
  function pointsSvg(points, frame, paint, caption, error = () => false) {
    return points.map((point, i) => `<circle cx="${frame.X(point[0])}" cy="${frame.Y(point[1])}" r="4.5" fill="${paint(i)}" fill-opacity=".85" stroke="${error(i) ? '#172d39' : 'white'}" stroke-width="${error(i) ? 2 : 0.6}"><title>样品 ${i + 1} · ${caption(i)}</title></circle>`).join('');
  }
  function renderPlots() {
    const kmeans = mode === 'kmeans';
    const twoDimensions = kmeans ? selected.length === 2 : dimensions === 2;
    $('plots').hidden = !twoDimensions;
    $('plots').classList.toggle('single', !kmeans);
    $('truthView').hidden = !kmeans || !twoDimensions;
    $('highDimensional').hidden = twoDimensions;
    $('highDimensional').textContent = kmeans
      ? `当前在 ${selected.length} 维空间中分组。全部所选属性参与计算，结果见下方品种对照表。`
      : `当前保留 ${dimensions} 个主成分。${mode === 'svm' ? 'SVM 在相应维度中划分类别，' : ''}结果以数值和表格展示。`;
    if (!twoDimensions) { $('plot').innerHTML = ''; $('truthPlot').innerHTML = ''; return; }
    $('plotLegend').className = 'legend';
    let frame, svg;
    if (kmeans) {
      frame = axes(rows, names()[0] + '（标准化）', names()[1] + '（标准化）');
      svg = frame.svg + pointsSvg(rows, frame, i => labels[i] < 0 ? '#81929b' : clusterColors[labels[i]], i => `${labels[i] < 0 ? '待分组' : '第 ' + (labels[i] + 1) + ' 组'}；真实品种 ${source.labels[i] + 1}`);
      svg += centers.map((point, j) => `<path d="M${frame.X(point[0])-9} ${frame.Y(point[1])}h18 M${frame.X(point[0])} ${frame.Y(point[1])-9}v18" stroke="${clusterColors[j]}" stroke-width="3"><title>第 ${j + 1} 组中心</title></path>`).join('');
      $('truthPlot').innerHTML = frame.svg + pointsSvg(rows, frame, i => varietyColors[source.labels[i]], i => `真实品种 ${source.labels[i] + 1}`);
      $('plotTitle').textContent = '算法分组 · 十字表示组中心';
      $('plotLegend').className = 'legend cluster';
      $('plotLegend').innerHTML = legend(clusterColors, '组');
      $('truthLegend').innerHTML = legend(varietyColors, '品种');
    } else if (mode === 'pca') {
      const projected = source.pca.map(row => row.slice(0, 2));
      // Both views use the same scale; frames display a crossfade between coordinate systems.
      frame = axes([...rawPair, ...projected], progress < 0.5 ? '酒精（标准化）' : '第一主成分', progress < 0.5 ? '苹果酸（标准化）' : '第二主成分');
      const opacity = Math.abs(2 * progress - 1);
      svg = frame.svg + `<g opacity="${opacity}">` + pointsSvg(progress < 0.5 ? rawPair : projected, frame, () => '#28788c', i => `真实品种 ${source.labels[i] + 1}`) + '</g>';
      $('plotTitle').textContent = progress < 0.5 ? '原始视图 · 两项测量指标' : 'PCA 视图 · 前两个主成分';
      $('plotLegend').innerHTML = '<span>每个圆点代表一个样品</span>';
    } else {
      const points = source.pca.map(row => row.slice(0, 2)), model = source.models[dimensions];
      frame = axes(points, '第一主成分', '第二主成分');
      svg = frame.svg;
      // Draw within the plot bounds in screen space, avoiding overlapping grid rectangles.
      const extent = Math.max(2, Math.ceil(Math.max(...points.flat().map(Math.abs)) + 0.3));
      for (let ix = 0; ix < 40; ix++) for (let iy = 0; iy < 40; iy++) {
        const x = -extent + (ix + 0.5) * 2 * extent / 40;
        const y = extent - (iy + 0.5) * 2 * extent / 40;
        svg += `<rect x="${72 + ix * 456 / 40}" y="${46 + iy * 396 / 40}" width="${456 / 40}" height="${396 / 40}" fill="${varietyColors[classify([x, y], model)]}" opacity="${progress * 0.18}"/>`;
      }
      svg += pointsSvg(points, frame, i => varietyColors[source.labels[i]], i => `真实品种 ${source.labels[i] + 1}；预测品种 ${classify(points[i], model) + 1}`, i => classify(points[i], model) !== source.labels[i]);
      $('plotTitle').textContent = 'SVM 分类区域 · 点的颜色表示真实品种';
      $('plotLegend').innerHTML = legend(varietyColors, '品种') + '<span>深色外圈：预测与标签有差异</span>';
    }
    $('plot').setAttribute('aria-label', $('plotTitle').textContent);
    $('plot').innerHTML = svg;
  }
  function renderComparison() {
    const ready = labels.every(group => group >= 0);
    const {counts, matched, mapping} = compareGroups(labels, source.labels);
    $('compositionLegend').innerHTML = legend(varietyColors, '品种');
    $('comparisonBody').innerHTML = counts.map((row, group) => {
      const total = row.reduce((a, b) => a + b, 0);
      return `<tr><th scope="row" style="color:${clusterColors[group]}">第 ${group + 1} 组</th>`
        + row.map(count => `<td style="background:rgba(8,126,139,${total ? count / total * 0.25 : 0})">${ready ? count : '—'}</td>`).join('')
        + `<td>${ready ? total : '—'}</td><td><div class="composition" aria-hidden="true">`
        + row.map((count, category) => `<span style="width:${total ? count / total * 100 : 0}%;background:${varietyColors[category]}" title="品种 ${category + 1}：${count} 个"></span>`).join('') + '</div></td></tr>';
    }).join('');
    $('agreement').textContent = ready ? `${done ? '最终' : '当前'}对应比例：${matched} / 178 = ${(matched / 178 * 100).toFixed(1)}%` : '开始分组后显示对应比例';
    $('mapping').textContent = ready ? '最佳一一配对：' + mapping.map((category, group) => `组 ${group + 1} → 品种 ${category + 1}`).join('；') + '。' : '组编号与品种编号分别表示算法分组和真实类别。';
    $('comparisonConclusion').textContent = done ? `使用 ${selected.length} 项属性，最佳配对后有 ${178 - matched} 个样品与对应品种标签存在差异。保存本次结果后，可以更换属性组合继续比较。` : '品种数量表随每次样品分配更新。';
  }
  function renderModels() {
    const variance = source.pcaVariance.slice(0, dimensions).reduce((a, b) => a + b, 0);
    $('variance').textContent = `前 ${dimensions} 个主成分累计解释 ${(variance * 100).toFixed(1)}% 的方差`;
    $('varianceRows').innerHTML = source.pcaVariance.slice(0, dimensions).map((v, i) => `<tr><th scope="row">主成分 ${i + 1}</th><td>${(v * 100).toFixed(1)}%</td></tr>`).join('');
    const model = source.models[dimensions];
    $('accuracy').textContent = `训练集分类正确率：${(model.correct / 178 * 100).toFixed(1)}%（${model.correct} / 178）`;
    $('confusionRows').innerHTML = model.confusion.map((row, i) => `<tr><th scope="row">品种 ${i + 1}</th>${row.map((n, j) => `<td${i === j ? ' class="correct"' : ''}>${n}</td>`).join('')}</tr>`).join('');
  }
  function render() {
    const kmeans = mode === 'kmeans', running = timer !== null;
    $('featureControls').hidden = !kmeans;
    $('componentControls').hidden = kmeans;
    $('featureHint').textContent = selected.length >= 2 ? `已选 ${selected.length} 项 · 分别标准化后计算距离` : `已选 ${selected.length} 项，请选择至少两项属性。`;
    $('resultCard').hidden = !valid();
    $('animationControls').hidden = !animated();
    $('play').disabled = !valid() || done || running;
    $('play').textContent = iteration > 0 || progress > 0 || labels[0] >= 0 ? '继续播放' : '播放';
    if (done) $('play').textContent = '播放完成';
    $('pause').disabled = !running;
    $('singleStep').disabled = !valid() || done || running;
    $('finish').disabled = !valid() || done;
    $('reset').disabled = !valid();
    $('saveResult').disabled = kmeans && !done;
    $('description').textContent = kmeans ? `K-Means 按所选属性把样品分为 3 组，真实品种用于评价分组结果。` : mode === 'pca' ? `将全部 13 项测量指标组合为 ${dimensions} 个主成分，观察保留的数据变化。` : `使用前 ${dimensions} 个主成分及真实品种标签训练线性 SVM，观察品种预测结果。`;
    if (!valid()) { $('status').textContent = '补充属性后即可开始分组。'; return; }
    $('status').textContent = kmeans
      ? done ? (converged ? `分组已稳定，共更新中心 ${iteration} 次。` : '已达到 100 次中心更新，显示当前分组结果。')
        : running ? (phase === 'assign' ? '下一步：按最近的中心分配样品。' : '下一步：计算组内平均值，更新中心。')
          : labels[0] < 0 ? '点击播放逐轮观察，或直接查看结果。' : '已暂停，可以单步执行或继续播放。'
      : !animated() ? '所选维度的结果已显示。' : done ? '视图展示完成。数值结果见下方。' : running ? '正在展示视图变化。' : progress > 0 ? '展示已暂停。' : '点击播放观察视图变化，或直接查看最终视图。';
    $('resultTitle').textContent = kmeans ? '聚类与品种对照' : mode === 'pca' ? '主成分分析结果' : 'PCA + SVM 分类结果';
    $('dimensionBadge').textContent = kmeans ? `${selected.length} 项属性 · 3 组` : `${dimensions} 个主成分`;
    $('count').textContent = '178';
    $('stepLabel').textContent = kmeans ? '中心更新' : '保留的主成分';
    $('step').textContent = kmeans ? `${iteration} 次` : `${dimensions} / 13`;
    $('metricBox').hidden = !kmeans;
    $('metric').textContent = labels[0] >= 0 ? objective(rows, labels, centers).toFixed(2) : '—';
    $('comparison').hidden = !kmeans;
    $('modelResults').hidden = kmeans;
    $('svmResults').hidden = mode !== 'svm';
    $('historyBox').hidden = !kmeans;
    $('history').innerHTML = history.length ? history.slice(-12).map(s => `<div>${s}</div>`).join('') : '首次分配后记录每一步的组内距离平方和。';
    $('detail').textContent = kmeans ? (selected.length === 2 ? '两图使用相同坐标，分别显示算法组别和真实品种。悬停圆点可查看样品编号和类别。' : `参与计算：${names().join('、')}。`)
      : mode === 'pca' ? (dimensions === 2 ? '动画切换原始两属性视图与主成分视图；最终坐标由全部 13 项指标计算。' : '增加主成分会保留更多数据变化。各主成分的比例可在下方展开查看。')
        : '背景颜色表示预测类别，圆点颜色表示真实品种。高维结果通过下方数量表比较。';
    if (mode === 'svm' && dimensions > 2) $('detail').textContent = '数量表按真实品种分行、预测品种分列，显示当前维度的分类结果。';
    renderPlots();
    if (kmeans) renderComparison(); else renderModels();
  }
  function renderSaved() {
    $('savedResults').hidden = saved.size === 0;
    $('savedRows').innerHTML = Array.from(saved.values()).map(row => `<tr>${row.map(value => `<td>${value}</td>`).join('')}</tr>`).join('');
  }
  $('features').innerHTML = source.featureNames.map((name, i) => `<label><input type="checkbox" value="${i}" ${i < 2 ? 'checked' : ''}>${name}</label>`).join('');
  $('features').addEventListener('change', () => {
    selected = Array.from($('features').querySelectorAll('input:checked'), input => Number(input.value));
    reset();
  });
  function chooseFeatures(indices) {
    selected = indices;
    $('features').querySelectorAll('input').forEach(input => { input.checked = selected.includes(Number(input.value)); });
    reset();
  }
  $('allFeatures').addEventListener('click', () => chooseFeatures(source.featureNames.map((_, i) => i)));
  $('defaultFeatures').addEventListener('click', () => chooseFeatures([0, 1]));
  $('components').innerHTML = Array.from({length:12}, (_, i) => `<option value="${i + 2}">${i + 2} 个主成分</option>`).join('');
  $('components').value = '2';
  $('components').addEventListener('change', reset);
  $('method').addEventListener('change', reset);
  $('play').addEventListener('click', () => {
    if (!valid() || done || timer !== null || !animated()) return;
    timer = setInterval(tick, mode === 'kmeans' ? 650 : 60);
    render();
  });
  $('pause').addEventListener('click', () => { stop(); render(); });
  $('singleStep').addEventListener('click', () => { stop(); tick(); });
  $('finish').addEventListener('click', () => {
    stop();
    if (mode === 'kmeans') { while (!done && valid()) advance(); }
    else { progress = 1; done = true; }
    render();
  });
  $('reset').addEventListener('click', reset);
  $('saveResult').addEventListener('click', () => {
    if (!valid() || (mode === 'kmeans' && !done)) return;
    const key = mode + ':' + (mode === 'kmeans' ? selected.join(',') : dimensions);
    let row;
    if (mode === 'kmeans') {
      const {matched} = compareGroups(labels, source.labels);
      row = ['K-Means', names().join('、'), '最佳一一对应比例', `${(matched / 178 * 100).toFixed(1)}%（${matched}/178）`];
    } else if (mode === 'pca') {
      row = ['PCA', `${dimensions} 个主成分`, '累计解释方差比例', `${(source.pcaVariance.slice(0, dimensions).reduce((a,b)=>a+b,0) * 100).toFixed(1)}%`];
    } else {
      const correct = source.models[dimensions].correct;
      row = ['PCA + SVM', `${dimensions} 个主成分`, '训练集分类正确率', `${(correct / 178 * 100).toFixed(1)}%（${correct}/178）`];
    }
    const existed = saved.has(key);
    saved.set(key, row); renderSaved();
    $('saveHint').textContent = existed ? '此设置的记录已更新。' : '已保存，可在下方比较不同设置。';
  });
  $('clearSaved').addEventListener('click', () => { saved.clear(); renderSaved(); $('saveHint').textContent = '记录已清空。'; });
  reset();
}());
