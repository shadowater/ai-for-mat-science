"""Fit the four cyclopropane data points from Stephen Lower's Chem1 textbook.
Source: https://chem1.com/acad/webtext/dynamics/dynamics-3.html
Standard library only. Fit unweighted squared errors in ln(k), with k in s^-1.
"""
import json
from math import exp, log

TEMPERATURE_C = [477, 523, 577, 623]
RATE_S_INV = [0.00018, 0.0027, 0.030, 0.26]
R = 8.314462618  # J mol^-1 K^-1


def fit():
    temperatures = [t + 273.15 for t in TEMPERATURE_C]
    x = [1 / t for t in temperatures]
    y = [log(k) for k in RATE_S_INV]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    m = sum((u - mx) * (v - my) for u, v in zip(x, y)) / sum((u - mx) ** 2 for u in x)
    b = my - m * mx
    return {
        'source': 'https://chem1.com/acad/webtext/dynamics/dynamics-3.html',
        'slope_K': m,
        'intercept': b,
        'Ea_kJ_mol': -m * R / 1000,
        'A_s_inv': exp(b),
        'sse_log_space': sum((v - (m * u + b)) ** 2 for u, v in zip(x, y)),
        'prediction_550_C_s_inv': exp(m / (550 + 273.15) + b),
        'rows': [dict(temperature_C=c, temperature_K=t, inverse_T_K_inv=u,
                      k_s_inv=k, log_k=v, fitted_k_s_inv=exp(m*u+b))
                 for c, t, u, k, v in zip(TEMPERATURE_C, temperatures, x, RATE_S_INV, y)],
    }


if __name__ == '__main__':
    print(json.dumps(fit(), ensure_ascii=False, indent=2))
