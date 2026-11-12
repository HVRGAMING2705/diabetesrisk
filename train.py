import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

rng = np.random.default_rng(42)
N = 768  # same record count as the classic Pima Indians Diabetes dataset

# Synthetic records modelled on the Pima Indians Diabetes dataset patterns
pregnancies = np.clip(rng.poisson(3.8, N), 0, 17)
glucose = np.clip(rng.normal(121, 32, N), 60, 200)
bp = np.clip(rng.normal(69, 19, N), 40, 122)
skin = np.clip(rng.normal(20, 16, N), 0, 60)
insulin = np.clip(rng.exponential(80, N), 0, 350)
bmi = np.clip(rng.normal(32, 8, N), 18, 60)
pedigree = np.clip(rng.normal(0.47, 0.33, N), 0.08, 2.4)
age = np.clip(rng.normal(33, 12, N), 21, 80)

X_raw = np.column_stack([pregnancies, glucose, bp, skin, insulin, bmi, pedigree, age])
FEATURES = ["pregnancies", "glucose", "blood_pressure", "skin_thickness",
            "insulin", "bmi", "pedigree", "age"]

# Generative logit from the known Pima risk factors: fasting glucose is the
# strongest signal, then BMI, age, family history (pedigree), pregnancies,
# insulin and blood pressure; skin thickness is weakest.
z = (-1.35
     + 0.10 * pregnancies
     + 0.035 * (glucose - 121)
     + 0.012 * (bp - 69)
     + 0.010 * (skin - 20)
     + 0.004 * (insulin - 80)
     + 0.085 * (bmi - 32)
     + 0.95 * (pedigree - 0.47)
     + 0.030 * (age - 33))
p = 1 / (1 + np.exp(-z))
y = (rng.random(N) < p).astype(int)

mean = X_raw.mean(axis=0)
std = X_raw.std(axis=0)
X = (X_raw - mean) / std

model = LogisticRegression(C=1.0, max_iter=2000).fit(X, y)
skf = StratifiedKFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(LogisticRegression(C=1.0, max_iter=2000), X, y, cv=skf)
proba_cv = cross_val_predict(LogisticRegression(C=1.0, max_iter=2000), X, y, cv=skf, method="predict_proba")[:, 1]
acc = float(accuracy_score(y, pred_cv))
auc = float(roc_auc_score(y, proba_cv))
base = float(max(np.bincount(y)) / len(y))
print(f"n={N} diabetes_rate={y.mean():.3f}")
print(f"CV accuracy={acc:.3f} AUC={auc:.3f} baseline={base:.3f}")
print(classification_report(y, pred_cv, target_names=["no diabetes", "diabetes"], digits=3))

mj = {"features": FEATURES, "mean": mean.tolist(), "std": std.tolist(),
      "coef": model.coef_[0].tolist(), "intercept": float(model.intercept_[0]),
      "metrics": {"cv_accuracy": acc, "auc": auc, "baseline_accuracy": base,
                  "diabetes_rate": float(y.mean()), "n": N}}
with open("model.json", "w") as f:
    json.dump(mj, f, indent=1)

def py_prob(row):
    xs = (np.array(row) - mean) / std
    return float(model.predict_proba([xs])[0][1] * 100)

samples = [
    [6, 180, 80, 35, 220, 38.5, 0.85, 55],   # high glucose + BMI + age: high risk
    [1, 85, 66, 20, 70, 22.0, 0.17, 23],     # young, healthy readings: low risk
    [3, 140, 72, 28, 150, 31.0, 0.55, 42],   # borderline middle case
    [0, 95, 60, 15, 60, 24.5, 0.20, 27],     # low risk
    [8, 195, 88, 40, 280, 42.0, 1.30, 62],   # very high risk
]
for s in samples:
    print(s, "->", round(py_prob(s), 2), "% diabetes risk")
with open("parity_samples.json", "w") as f:
    json.dump([{"row": s, "prob": py_prob(s)} for s in samples], f, indent=1)
