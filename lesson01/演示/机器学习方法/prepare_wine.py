"""Regenerate the browser demo data from scikit-learn's copy of UCI Wine."""

import json
from pathlib import Path

from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix


def rounded_rows(values):
    return [[round(float(v), 6) for v in row] for row in values]


wine = load_wine()
assert wine.data.shape == (178, 13)
assert wine.feature_names[:2] == ["alcohol", "malic_acid"]

raw = wine.data
standardized = StandardScaler().fit_transform(wine.data)
pca = PCA(n_components=13).fit(standardized)
projected = pca.transform(standardized)
models = {}
for dimensions in range(2, 14):
    inputs = projected[:, :dimensions]
    svm = LinearSVC(random_state=0, dual="auto", max_iter=10000).fit(inputs, wine.target)
    predictions = svm.predict(inputs)
    models[str(dimensions)] = {
        "coef": rounded_rows(svm.coef_),
        "intercept": [round(float(v), 6) for v in svm.intercept_],
        "confusion": confusion_matrix(wine.target, predictions).tolist(),
        "correct": int((predictions == wine.target).sum()),
    }

payload = {
    "raw": rounded_rows(raw),
    "featureNames": ["酒精", "苹果酸", "灰分", "灰分碱度", "镁", "总酚", "黄酮类", "非黄酮类酚", "原花青素", "颜色强度", "色调", "280/315 纳米吸光度比", "脯氨酸"],
    "pca": rounded_rows(projected),
    "labels": [int(v) for v in wine.target],
    "pcaVariance": [round(float(v), 6) for v in pca.explained_variance_ratio_],
    "models": models,
}
path = Path(__file__).with_name("wine-data.js")
path.write_text(
    "/* UCI Wine: Aeberhard & Forina (1992), CC BY 4.0. "
    "https://archive.ics.uci.edu/dataset/109/wine */\n"
    "(function (root) {\n"
    f"  const data = {json.dumps(payload, ensure_ascii=False, separators=(',', ':'))};\n"
    "  if (typeof module !== 'undefined' && module.exports) module.exports = data;\n"
    "  if (root) root.WINE_DATA = data;\n"
    "}(typeof window !== 'undefined' ? window : null));\n",
    encoding="utf-8",
)
