from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "diabetesrisk.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "DiabetesRisk — Type-2 Diabetes Risk Predictor", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "A model that reads 8 health facts and predicts the risk of type-2 diabetes"])
add(1, "The Problem", ["Type-2 diabetes affects over 500 million people worldwide — and half of them do not know they have it", "It develops silently over years; early warning signs hide in routine health numbers", "Can a machine learn the risk pattern from a few simple health facts?", "DiabetesRisk answers that question with a simple, explainable model"])
add(2, "The Solution — DiabetesRisk", ["Enter 8 facts: pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, family history, age", "A trained model returns the diabetes risk as a percentage, with a low / moderate / high verdict", "Try a high-risk or low-risk profile with one click", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset generation and model training", "Logistic regression (C = 1.0) on 8 standardised features", "HTML, CSS and vanilla JavaScript for the interactive demo", "GitHub for source control, Vercel for free hosting"])
add(4, "Architecture", ["Dataset: 768 synthetic health records modelled on the classic Pima Indians Diabetes dataset", "Facts -> standardisation -> logistic regression -> sigmoid -> diabetes risk probability", "model.json ships with the site; JavaScript applies the same formula", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: enter your health facts and press Check My Risk", "6 pregnancies, glucose 180, BMI 38.5, age 55, pedigree 0.85 -> about 98.4% risk", "23-year-old, glucose 85, BMI 22.0, pedigree 0.17 -> about 1.1% risk", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["5-fold cross-validation accuracy: 76.3%, AUC: 0.81", "Baseline (always guessing the most common class): 67.2% — a clear lift", "Diabetes rate in the data: 32.8%, close to the real Pima dataset's 34.9%", "Browser demo matches Python probabilities exactly on all test samples"])
add(7, "Future Scope", ["Train on the real Pima Indians Diabetes dataset from Kaggle", "Add feature importance — show which health fact moved the risk most", "Add a risk-reduction advisor: how much would the risk fall if BMI or glucose dropped?", "Extend to other conditions such as heart disease and kidney disease"])
add(8, "Thank You", ["DiabetesRisk — Type-2 Diabetes Risk Predictor", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/diabetesrisk", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_DiabetesRisk_2026-11-12.pptx")
print("slides:", len(prs.slides._sldIdLst))
