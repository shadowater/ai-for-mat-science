"""Course solubility experiment: grouped split, four descriptors, 4-8-1 MLP."""
from pathlib import Path
import csv, json, copy, hashlib, platform
import numpy as np
import sklearn, rdkit
from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, rdMolDescriptors
from rdkit.Chem.MolStandardize import rdMolStandardize
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

HERE = Path(__file__).resolve().parent
DATA = HERE / '../../内容/素材/04_AI与Agent的工作方式/ci034243x_si_001.txt'
FEATURES = ['MolLogP', 'MolWt', 'RotatableBonds_strict', 'AromaticHeavyAtomFraction']


def descriptors(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None or mol.GetNumHeavyAtoms() == 0:
        raise ValueError('Invalid SMILES: ' + smiles)
    values = [Crippen.MolLogP(mol), Descriptors.MolWt(mol),
              rdMolDescriptors.CalcNumRotatableBonds(mol, rdMolDescriptors.NumRotatableBondsOptions.Strict),
              sum(a.GetIsAromatic() for a in mol.GetAtoms() if a.GetAtomicNum() > 1) / mol.GetNumHeavyAtoms()]
    return values, Chem.MolToSmiles(mol, isomericSmiles=True)


def metrics(y, pred):
    return dict(MAE=float(mean_absolute_error(y, pred)), RMSE=float(np.sqrt(mean_squared_error(y, pred))), R2=float(r2_score(y, pred)))


def overlap_key(smiles):
    mol = rdMolStandardize.Cleanup(Chem.MolFromSmiles(smiles))
    mol = rdMolStandardize.FragmentParent(mol)
    mol = rdMolStandardize.Uncharger().uncharge(mol)
    Chem.RemoveStereochemistry(mol)
    mol = rdMolStandardize.TautomerEnumerator().Canonicalize(mol)
    return Chem.MolToSmiles(mol, isomericSmiles=False)


def main(external21=False):
    out = HERE / '外部21测试' if external21 else HERE
    out.mkdir(exist_ok=True)
    external = json.loads((HERE/'原论文验证数据/结构检索结果.json').read_text()) if external21 else []
    external_keys = {overlap_key(r['SMILES']) for r in external}
    external_names = {r['name_as_printed'].strip().casefold() for r in external}
    overlap_removed = []
    rows = list(csv.DictReader(DATA.open(encoding='utf-8-sig')))
    processed, excluded = [], []
    for i, row in enumerate(rows):
        try:
            values, key = descriptors(row['SMILES'])
            if external21:
                key = overlap_key(row['SMILES'])
                if key in external_keys or row['Compound ID'].strip().casefold() in external_names:
                    overlap_removed.append(dict(source_row=i, name=row['Compound ID'], key=key))
                    continue
            target = float(row['measured log(solubility:mol/L)'])
            if not np.isfinite(values + [target]).all(): raise ValueError('nonfinite')
            processed.append((i, row, values, key, target))
        except ValueError as exc:
            excluded.append(dict(row=i, error=str(exc)))
    X = np.array([r[2] for r in processed]); y = np.array([r[4] for r in processed])
    groups = np.array([r[3] for r in processed])
    development, test = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=42).split(X, y, groups))
    ti, vi = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=43).split(X[development], y[development], groups[development]))
    train, val = development[ti], development[vi]
    assert not (set(groups[train]) & set(groups[val]) or set(groups[train]) & set(groups[test]) or set(groups[val]) & set(groups[test]))
    scaler = StandardScaler().fit(X[train]); Z = scaler.transform(X)
    ym, ys = float(y[train].mean()), float(y[train].std())
    target = (y - ym) / ys
    linear = LinearRegression().fit(Z[train], target[train])
    network = MLPRegressor(hidden_layer_sizes=(8,), activation='tanh', solver='adam', alpha=.001,
                           batch_size=64, learning_rate_init=.003, random_state=42, max_iter=1)
    best_loss, best, stale, history = float('inf'), None, 0, []
    for epoch in range(1, 2001):
        network.partial_fit(Z[train], target[train])
        pred_train = network.predict(Z[train]) * ys + ym
        pred_val = network.predict(Z[val]) * ys + ym
        loss = float(mean_squared_error(y[val], pred_val))
        history.append(dict(epoch=epoch, train_MSE=float(mean_squared_error(y[train], pred_train)), validation_MSE=loss))
        if loss < best_loss - 1e-5:
            best_loss, best, stale, best_epoch = loss, copy.deepcopy(network), 0, epoch
        else: stale += 1
        if stale >= 150: break
    preds = {'linear': linear.predict(Z)*ys+ym, 'network': best.predict(Z)*ys+ym}
    splits = {'train': train, 'validation': val, 'test': test}
    result = dict(versions=dict(python=platform.python_version(), numpy=np.__version__, sklearn=sklearn.__version__, rdkit=rdkit.__version__),
        source_sha256=hashlib.sha256(DATA.read_bytes()).hexdigest(), total_rows=len(rows), usable_rows=len(processed), excluded=excluded,
        unique_structures=len(set(groups)), external21_mode=external21, overlap_removed=overlap_removed, split_counts={k:len(v) for k,v in splits.items()}, features=FEATURES,
        architecture=[4,8,1], parameters=49, best_epoch=best_epoch, stopped_epoch=epoch,
        metrics={model:{split:metrics(y[idx], pred[idx]) for split,idx in splits.items()} for model,pred in preds.items()})
    if external21:
        assert len(external) == 21
        assert not set(groups) & external_keys
        ex = np.array([descriptors(r['SMILES'])[0] for r in external])
        ey = np.array([float(r['measured_logS']) for r in external])
        ep = {'linear': linear.predict(scaler.transform(ex))*ys+ym,
              'network': best.predict(scaler.transform(ex))*ys+ym}
        result['external21_metrics'] = {k:metrics(ey,v) for k,v in ep.items()}
        result['paper_ESOL_reference'] = metrics(ey,np.array([float(r['ESOL_logS']) for r in external]))
        with (out/'外部21预测.csv').open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.writer(f,lineterminator='\n');w.writerow(['name','SMILES','measured_logS','paper_ESOL_logS','linear_logS','network_logS'])
            for i,r in enumerate(external):
                w.writerow([r['name_as_printed'],r['SMILES'],ey[i],r['ESOL_logS'],ep['linear'][i],ep['network'][i]])
    (out/'结果.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    model = dict(features=FEATURES, input_mean=scaler.mean_.tolist(), input_scale=scaler.scale_.tolist(),
        target_mean=ym, target_scale=ys, activation='tanh', weights=[v.tolist() for v in best.coefs_], biases=[v.tolist() for v in best.intercepts_])
    (out/'模型参数.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
    with (out/'训练过程.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(history[0]),lineterminator='\n');w.writeheader();w.writerows(history)
    split_by_index = {int(i): name for name,idx in splits.items() for i in idx}
    with (out/'样本与预测.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['source_row','name','canonical_smiles','split',*FEATURES,'measured_logS','linear_logS','network_logS'])
        for i,(rowid,row,values,key,actual) in enumerate(processed):
            w.writerow([rowid,row['Compound ID'],key,split_by_index[i],*values,actual,preds['linear'][i],preds['network'][i]])
    # Verify exported parameters reproduce the estimator predictions.
    h=np.tanh((X-np.array(model['input_mean']))/np.array(model['input_scale']) @ np.array(model['weights'][0]) + np.array(model['biases'][0]))
    exported=(h@np.array(model['weights'][1])+np.array(model['biases'][1])).ravel()*ys+ym
    np.testing.assert_allclose(exported,preds['network'],rtol=1e-10,atol=1e-10)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
    for name in ['train','validation']:
        axes[0].plot([h['epoch'] for h in history],[h[name+'_MSE'] for h in history],label=name)
    axes[0].axvline(best_epoch,color='gray',ls='--',label='selected epoch')
    axes[0].set(xlabel='Epoch',ylabel='MSE (logS units squared)',title='Training and validation');axes[0].legend()
    for name in preds: axes[1].scatter(y[test],preds[name][test],s=13,alpha=.55,label=name)
    lim=[min(y[test].min(),*(p[test].min() for p in preds.values()))-.3,max(y[test].max(),*(p[test].max() for p in preds.values()))+.3]
    axes[1].plot(lim,lim,'k--');axes[1].set(xlabel='Measured logS',ylabel='Predicted logS',title='Held-out test data',xlim=lim,ylim=lim);axes[1].legend()
    fig.savefig(out/'训练与测试.png',dpi=160);plt.close(fig)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--external21', action='store_true', help='排除表4结构后重训，并评价固定21条外部测试记录')
    main(parser.parse_args().external21)
