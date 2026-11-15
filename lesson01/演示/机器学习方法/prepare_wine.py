"""Regenerate the browser demo data from scikit-learn's copy of UCI Wine."""

import json
from pathlib import Path

from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


def rounded_rows(values):
    return [[round(float(v), 6) for v in row] for row in values]


wine = load_wine()
assert wine.data.shape == (178, 13)
assert wine.feature_names[:2] == ["alcohol", "malic_acid"]

raw = wine.data[:, :2]
standardized = StandardScaler().fit_transform(wine.data)
pca = PCA(n_components=2).fit(standardized)
projected = pca.transform(standardized)
svm = LinearSVC(random_state=0, dual="auto", max_iter=10000).fit(projected, wine.target)

payload = {
    "raw": rounded_rows(raw),
    "pca": rounded_rows(projected),
    "labels": [int(v) for v in wine.target],
    "pcaVariance": [round(float(v), 6) for v in pca.explained_variance_ratio_],
    "svm": {
        "coef": rounded_rows(svm.coef_),
        "intercept": [round(float(v), 6) for v in svm.intercept_],
    },
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
