"""Reproduce the frozen external-21 run and export actual epoch parameters."""
from pathlib import Path
import csv, json, sys
import numpy as np
from sklearn.neural_network import MLPRegressor
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE))
from train import descriptors


def main():
    model = json.loads((BASE/'外部21测试/模型参数.json').read_text())
    result = json.loads((BASE/'外部21测试/结果.json').read_text())
    rows = list(csv.DictReader((BASE/'外部21测试/样本与预测.csv').open(encoding='utf-8-sig')))
    train = [r for r in rows if r['split']=='train']
    features = model['features']
    mean, scale = np.array(model['input_mean']), np.array(model['input_scale'])
    ym, ys = model['target_mean'], model['target_scale']
    # GroupShuffleSplit indices in the original run are sorted within each split.
    X = (np.array([[float(r[f]) for f in features] for r in train])-mean)/scale
    y = (np.array([float(r['measured_logS']) for r in train])-ym)/ys
    network = MLPRegressor(hidden_layer_sizes=(8,), activation='tanh', solver='adam', alpha=.001,
                           batch_size=64, learning_rate_init=.003, random_state=42, max_iter=1)
    history = list(csv.DictReader((BASE/'外部21测试/训练过程.csv').open()))
    frames=[]
    for row in history:
        network.partial_fit(X,y)
        epoch=int(row['epoch'])
        frames.append(dict(epoch=epoch, weights=[a.tolist() for a in network.coefs_],
                           biases=[a.tolist() for a in network.intercepts_],
                           train_MSE=float(row['train_MSE']), validation_MSE=float(row['validation_MSE'])))
        mse=float(np.mean((network.predict(X)*ys+ym-(y*ys+ym))**2))
        np.testing.assert_allclose(mse,float(row['train_MSE']),rtol=1e-10,atol=1e-10)
        if epoch==result['best_epoch']:
            for a,b in zip(network.coefs_,model['weights']): np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10)
            for a,b in zip(network.intercepts_,model['biases']): np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10)
    samples=[dict(name=r['name'],split=r['split'],x=[float(r[f]) for f in features],y=float(r['measured_logS']),reference=float(r['network_logS'])) for r in rows]
    for r in csv.DictReader((BASE/'外部21测试/外部21预测.csv').open(encoding='utf-8-sig')):
        samples.append(dict(name=r['name'],split='external',x=descriptors(r['SMILES'])[0],y=float(r['measured_logS']),reference=float(r['network_logS'])))
    # Check the published model against every stored internal and external prediction.
    z=(np.array([s['x'] for s in samples])-mean)/scale
    h=np.tanh(z@np.array(model['weights'][0])+np.array(model['biases'][0]))
    pred=(h@np.array(model['weights'][1])+np.array(model['biases'][1])).ravel()*ys+ym
    np.testing.assert_allclose(pred,[s['reference'] for s in samples],rtol=1e-10,atol=1e-10)
    payload=dict(model=model,best_epoch=result['best_epoch'],frames=frames,samples=samples)
    (HERE/'data.js').write_text('window.SOLUBILITY_DEMO = '+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n')
    print(f'已核对 {len(frames)} 轮训练误差、第 {result["best_epoch"]} 轮参数和 {len(samples)} 条预测。')

if __name__=='__main__': main()
