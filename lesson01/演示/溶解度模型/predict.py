"""Predict logS using the exported 4-8-1 network. No sklearn required."""
import argparse, json, math
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, rdMolDescriptors

parser=argparse.ArgumentParser(description='用教学模型从 SMILES 预测水溶解度')
parser.add_argument('smiles')
parser.add_argument('--model', type=Path, default=Path(__file__).parent/'模型参数.json')
a=parser.parse_args()
mol=Chem.MolFromSmiles(a.smiles)
if mol is None or not mol.GetNumHeavyAtoms(): parser.error('无法解析 SMILES')
x=[Crippen.MolLogP(mol),Descriptors.MolWt(mol),rdMolDescriptors.CalcNumRotatableBonds(mol,rdMolDescriptors.NumRotatableBondsOptions.Strict),sum(atom.GetIsAromatic() for atom in mol.GetAtoms() if atom.GetAtomicNum()>1)/mol.GetNumHeavyAtoms()]
m=json.loads(a.model.read_text())
z=[(v-mu)/scale for v,mu,scale in zip(x,m['input_mean'],m['input_scale'])]
h=[math.tanh(sum(z[i]*m['weights'][0][i][j] for i in range(4))+m['biases'][0][j]) for j in range(8)]
y=(sum(h[j]*m['weights'][1][j][0] for j in range(8))+m['biases'][1][0])*m['target_scale']+m['target_mean']
print(json.dumps(dict(SMILES=a.smiles,descriptors=dict(zip(m['features'],x)),predicted_logS=y,predicted_S_mol_L=10**y),ensure_ascii=False,indent=2))
