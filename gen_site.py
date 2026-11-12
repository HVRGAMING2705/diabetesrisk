import json
m = json.load(open("model.json"))
features, mean, std = m["features"], m["mean"], m["std"]
coef, icpt = m["coef"], m["intercept"]
mt = m["metrics"]
acc, auc, base = mt["cv_accuracy"], mt["auc"], mt["baseline_accuracy"]
DOMAIN = "diabetesrisk.vercel.app"
JS_MODEL = f"""const MEAN = {json.dumps(mean)};
const STD = {json.dumps(std)};
const COEF = {json.dumps(coef)};
const INTERCEPT = {icpt};
function diabetesProb(vals){{
  let z = INTERCEPT;
  for (let i = 0; i < 8; i++) z += COEF[i] * (vals[i] - MEAN[i]) / STD[i];
  return 1 / (1 + Math.exp(-z)) * 100;
}}"""
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DiabetesRisk — Type-2 Diabetes Risk Predictor | AI/ML Project</title>
<meta name="description" content="DiabetesRisk predicts the risk of type-2 diabetes from 8 health facts — pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, family history and age — using a logistic regression model trained on 768 records. Try it live in your browser.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="DiabetesRisk — Type-2 Diabetes Risk Predictor">
<meta property="og:description" content="Enter 8 health facts and instantly see your type-2 diabetes risk, with a real trained ML model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="DiabetesRisk — Type-2 Diabetes Risk Predictor">
<meta name="twitter:description" content="Logistic regression diabetes risk predictor. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"DiabetesRisk","applicationCategory":"EducationalApplication","description":"Type-2 diabetes risk predictor using logistic regression.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:720px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
input,select{{width:100%;padding:10px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:16px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b{{font-size:1.6em}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}}
</style>
</head>
<body>
<h1>&#128138; DiabetesRisk — Diabetes Risk Predictor</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A logistic regression model trained on 768 synthetic health records modelled on the classic Pima Indians Diabetes dataset predicts the risk of type-2 diabetes from 8 health facts: pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, family history (diabetes pedigree function) and age. 5-fold CV: <b>accuracy = {acc:.1%}</b>, <b>AUC = {auc:.2f}</b> vs a majority-class baseline of {base:.1%}.</p>
<div class="grid">
<label>Pregnancies<input type="number" step="1" id="f0" value="1"></label>
<label>Glucose (mg/dL)<input type="number" step="any" id="f1" value="120"></label>
<label>Blood pressure (mm Hg)<input type="number" step="any" id="f2" value="70"></label>
<label>Skin thickness (mm)<input type="number" step="any" id="f3" value="20"></label>
<label>Insulin (mu U/ml)<input type="number" step="any" id="f4" value="80"></label>
<label>BMI (kg/m&sup2;)<input type="number" step="any" id="f5" value="28"></label>
<label>Diabetes pedigree function<input type="number" step="any" id="f6" value="0.45"></label>
<label>Age (years)<input type="number" step="1" id="f7" value="35"></label>
</div>
<button onclick="predict()">Check My Risk</button>
<button onclick="tryHigh()">Try high-risk profile</button>
<button onclick="tryLow()">Try low-risk profile</button>
<div id="result"></div>
<p class="note">How it works: each value is standardised (subtract the training mean, divide by the standard deviation), multiplied by the model&apos;s learned weight, and summed with a bias; a sigmoid turns the total into a probability of diabetes. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try it: 6 pregnancies, glucose 180, BMI 38.5, age 55, pedigree 0.85 &rarr; about 98.4% risk. A 23-year-old with glucose 85, BMI 22.0, pedigree 0.17 &rarr; about 1.1% risk. A borderline case — glucose 140, BMI 31, age 42 &rarr; about 55.8% risk.</p>
<p class="note">Honest note: this model was trained on synthetic data modelled on the classic Pima dataset patterns, so it is a classroom demo — it is not a medical diagnosis. Always consult a doctor for real health decisions.</p>
<p><a href="https://github.com/HVRGAMING2705/diabetesrisk">View source on GitHub</a></p>
<script>
{JS_MODEL}
function show(){{
  const vals = [];
  for (let i = 0; i < 8; i++) vals.push(parseFloat(document.getElementById("f" + i).value) || 0);
  const p = diabetesProb(vals);
  const el = document.getElementById("result");
  el.style.display = "block";
  const verdict = p >= 70 ? "&#128308; HIGH RISK — please see a doctor for a real test" : p >= 40 ? "&#128993; MODERATE RISK — worth a check-up and healthier habits" : "&#128994; LOW RISK — keep up the healthy habits";
  el.innerHTML = "<b>" + p.toFixed(1) + "% diabetes risk</b><br>" + verdict +
    "<br><span class=note>Probability of type-2 diabetes, from the 8 health facts above. This is a classroom demo on synthetic data, not a medical diagnosis.</span>";
}}
function predict(){{ show(); }}
function tryHigh(){{ const v = [6, 180, 80, 35, 220, 38.5, 0.85, 55]; for (let i = 0; i < 8; i++) document.getElementById("f" + i).value = v[i]; show(); }}
function tryLow(){{ const v = [1, 85, 66, 20, 70, 22, 0.17, 23]; for (let i = 0; i < 8; i++) document.getElementById("f" + i).value = v[i]; show(); }}
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — DiabetesRisk</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on DiabetesRisk.</p><p><a href="https://{DOMAIN}/">Back to DiabetesRisk</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>
""")
open("README.md", "w").write(f"""# DiabetesRisk — Type-2 Diabetes Risk Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Logistic regression (C=1.0) on standardized features — pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, diabetes pedigree function, age — trained on 768 synthetic health records modelled on the classic Pima Indians Diabetes dataset (seed 42).

- 5-fold CV accuracy: {acc:.1%}, AUC: {auc:.2f} (majority-class baseline: {base:.1%})
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.

Note: classroom demo on synthetic data — not a medical diagnosis.
""")
samples = json.load(open("parity_samples.json"))
parity = JS_MODEL + "\n" + "\n".join(
    f"console.log(JSON.stringify({{row: {json.dumps(s['row'])}, js: diabetesProb({json.dumps(s['row'])}), py: {s['prob']}}}));"
    for s in samples)
open("parity.js", "w").write(parity)
print("site files written, acc", acc)
