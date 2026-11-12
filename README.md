# DiabetesRisk — Type-2 Diabetes Risk Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Logistic regression (C=1.0) on standardized features — pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, diabetes pedigree function, age — trained on 768 synthetic health records modelled on the classic Pima Indians Diabetes dataset (seed 42).

- 5-fold CV accuracy: 76.3%, AUC: 0.81 (majority-class baseline: 67.2%)
- Live demo: https://diabetesrisk.vercel.app (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.

Note: classroom demo on synthetic data — not a medical diagnosis.
