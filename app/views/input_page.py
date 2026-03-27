"""
views/input_page.py
Renders Page 1 — Patient Input, Clinical Context, and full Prediction Pipeline.
All ML logic is 100% unchanged. Variables names preserved exactly.
"""
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from datetime import datetime


def render(model, scaler, label_encoder, explainer):
    """Render the full input page and trigger prediction on button click."""

    # ── HERO ──
    components.html("""
    <!DOCTYPE html><html><head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;600&display=swap" rel="stylesheet">
    <style>*{margin:0;padding:0;box-sizing:border-box;}body{background:transparent;overflow:hidden;}</style>
    </head><body>
    <div style="text-align:center;padding:3rem 2rem 2rem;width:100%;display:flex;flex-direction:column;align-items:center;font-family:'DM Sans',sans-serif;">
      <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(255,228,233,0.9);color:#e11d48;font-size:0.72rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;padding:7px 20px;border-radius:100px;margin-bottom:1.5rem;border:1px solid #fecdd6;box-shadow:0 2px 8px rgba(140,60,90,0.08);">
        🌸 &nbsp; AI-Powered Clinical Decision Support
      </div>
      <h1 style="font-family:'Playfair Display',serif;font-size:clamp(2.4rem,5vw,3.8rem);font-weight:900;color:#18080f;line-height:1.12;margin:0 auto 1.1rem;max-width:760px;text-align:center;letter-spacing:-0.01em;">
        Maternal Health<br>
        <em style="font-style:italic;font-weight:700;background:linear-gradient(135deg,#f43f5e,#be123c);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Risk Prediction System</em>
      </h1>
      <p style="font-size:1.05rem;color:#5c4a52;font-weight:300;max-width:600px;margin:0 auto 1.8rem;line-height:1.75;text-align:center;">
        AI-powered system for predicting maternal health risk using key physiological parameters.
        It provides risk classification, confidence score, and clinical insights to support
        early detection and informed healthcare decisions.
      </p>
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:48px;height:2px;background:linear-gradient(90deg,transparent,#fb7185);border-radius:4px;"></div>
        <div style="width:8px;height:8px;background:#fb7185;border-radius:50%;"></div>
        <div style="width:48px;height:2px;background:linear-gradient(90deg,#fb7185,transparent);border-radius:4px;"></div>
      </div>
    </div>
    </body></html>
    """, height=360, scrolling=False)

    # Stats strip
    st.markdown("""
    <div style="display:flex;justify-content:center;max-width:680px;margin:-0.2rem auto 0.6rem;
                background:rgba(255,255,255,0.68);border:1px solid #ecdde3;
                border-radius:16px;box-shadow:0 2px 12px rgba(140,60,90,0.08);overflow:hidden;">
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;padding:1rem 0.4rem;border-right:1px solid #ecdde3;">
        <span style="font-size:1.45rem;font-weight:800;color:#e11d48;line-height:1;">9</span>
        <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:#9b8a92;margin-top:3px;">Input Features</span>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;padding:1rem 0.4rem;border-right:1px solid #ecdde3;">
        <span style="font-size:1.45rem;font-weight:800;color:#e11d48;line-height:1;">3</span>
        <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:#9b8a92;margin-top:3px;">Risk Levels</span>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;padding:1rem 0.4rem;border-right:1px solid #ecdde3;">
        <span style="font-size:1.45rem;font-weight:800;color:#e11d48;line-height:1;">AI</span>
        <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:#9b8a92;margin-top:3px;">SHAP Explained</span>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;padding:1rem 0.4rem;border-right:1px solid #ecdde3;">
        <span style="font-size:1.45rem;font-weight:800;color:#e11d48;line-height:1;">H+</span>
        <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:#9b8a92;margin-top:3px;">Hybrid Intelligence</span>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;padding:1rem 0.4rem;">
        <span style="font-size:1.45rem;font-weight:800;color:#e11d48;line-height:1;">PDF</span>
        <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:#9b8a92;margin-top:3px;">Clinical Report</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION 1 — Vitals ──
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-rose">👩</div>
            <span class="section-label-text">Patient Vitals &amp; Parameters</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        age      = st.number_input("Age (years)",                    min_value=0,   max_value=60,  value=0)
        systolic = st.number_input("Systolic Blood Pressure (mmHg)", min_value=0,   max_value=200, value=0)
    with col2:
        diastolic = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=0,   max_value=150, value=0)
        bs        = st.number_input("Blood Sugar (mmol/L)",             min_value=0.0, max_value=15.0, value=0.0, step=0.1, format="%.1f")
    with col3:
        temp = st.number_input("Body Temperature (°C)", min_value=0.0, max_value=42.0, value=0.0, step=0.1, format="%.1f")
        hr   = st.number_input("Heart Rate (bpm)",      min_value=0,   max_value=150, value=0)

    # ── SECTION 1b — Clinical Context ──
    st.markdown("""
    <div class="section-wrap" style="margin-top:1.6rem;">
        <div class="section-label">
            <div class="section-label-icon icon-purple">🏥</div>
            <span class="section-label-text">Clinical Context &amp; Patient History</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    ctx1, ctx2, ctx3, ctx4 = st.columns(4, gap="large")
    with ctx1:
        prev_complications = st.selectbox(
            "Previous Complications",
            ["None","Minor (e.g., mild anemia, previous C-section)","Major (e.g., preeclampsia, gestational diabetes)"],
            help="Select the most severe complication from previous pregnancies, if any."
        )
    with ctx2:
        diabetes_status = st.selectbox(
            "Diabetes Status", ["None","Controlled","Uncontrolled"],
            help="Controlled: managed with diet/medication. Uncontrolled: HbA1c persistently elevated."
        )
    with ctx3:
        hypertension_status = st.selectbox(
            "Hypertension Status", ["None","Mild","Severe"],
            help="Mild: BP 140–159/90–109 mmHg. Severe: BP ≥160/110 mmHg."
        )
    with ctx4:
        trimester = st.selectbox(
            "Current Trimester", ["First","Second","Third"],
            help="First: 0–12 wks. Second: 13–26 wks. Third: 27–40 wks."
        )

    # ── SECTION 2 — Reference Ranges ──
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-sage">📋</div>
            <span class="section-label-text">Clinical Reference Ranges</span>
        </div>
        <div class="section-rule"></div>
    </div>
    <div class="card" style="padding:1.6rem 2rem;">
        <div class="range-grid">
            <div class="range-pill"><span class="range-pill-label">Age</span><span class="range-pill-value">18 – 35 years</span></div>
            <div class="range-pill"><span class="range-pill-label">Systolic BP</span><span class="range-pill-value">90 – 120 mmHg</span></div>
            <div class="range-pill"><span class="range-pill-label">Diastolic BP</span><span class="range-pill-value">60 – 80 mmHg</span></div>
            <div class="range-pill"><span class="range-pill-label">Blood Sugar</span><span class="range-pill-value">4.0 – 7.0 mmol/L</span></div>
            <div class="range-pill"><span class="range-pill-label">Body Temperature</span><span class="range-pill-value">36.5 – 37.5 °C</span></div>
            <div class="range-pill"><span class="range-pill-label">Heart Rate</span><span class="range-pill-value">60 – 100 bpm</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION 3 — Predict ──
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-rose">🔬</div>
            <span class="section-label-text">Risk Assessment</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    pred_col, _ = st.columns([1, 2])
    with pred_col:
        predict_clicked = st.button("🔍  Analyse & Predict Risk Level")

    # ── PREDICTION PIPELINE  [BACKEND — 100% UNCHANGED] ──
    if predict_clicked:
        # Input validation
        errors = []
        if age <= 0:                       errors.append("Age must be greater than 0")
        if systolic <= 0 or diastolic <= 0: errors.append("Blood pressure values must be valid")
        if bs <= 0:                         errors.append("Blood sugar must be greater than 0")
        if temp <= 0:                       errors.append("Temperature must be valid")
        if hr <= 0:                         errors.append("Heart rate must be valid")

        if errors:
            for e in errors:
                st.error(f"⚠️ {e}")
            return

        # 1. Input
        input_data = pd.DataFrame([{
            "Age":           float(age),
            "SystolicBP":    float(systolic),
            "DiastolicBP":   float(diastolic),
            "BS":            float(bs),
            "BodyTemp":      float(temp),
            "HeartRate":     float(hr),
            "PulsePressure": float(systolic - diastolic),
            "MAP":           float((systolic + 2 * diastolic) / 3),
            "BP_Ratio":      float(systolic / diastolic)
        }])

        # 2. Preprocessing
        scaled = scaler.transform(input_data)

        # 3. Prediction  [BACKEND — UNCHANGED]
        pred       = model.predict(scaled)[0]
        prob       = model.predict_proba(scaled)[0]
        risk       = label_encoder.inverse_transform([pred])[0]
        confidence = float(np.max(prob) * 100)
        timestamp  = datetime.now().strftime("%d %B %Y, %H:%M:%S")

        # 4. SHAP  [BACKEND — UNCHANGED]
        shap_values   = explainer(scaled)
        feature_names = ["Age","SystolicBP","DiastolicBP","BS","BodyTemp",
                         "HeartRate","PulsePressure","MAP","BP_Ratio"]
        shap_vals = shap_values.values[0][:, pred]
        shap_df   = pd.DataFrame({"Feature": feature_names, "Impact": shap_vals})
        shap_df["AbsImpact"] = shap_df["Impact"].abs()
        shap_df = shap_df.sort_values(by="AbsImpact", ascending=False)

        # 5. Clinical Scoring Engine
        clinical_score  = 0
        score_breakdown = []
        if "Minor" in prev_complications:
            clinical_score += 1; score_breakdown.append(("Previous complications (Minor)", 1))
        elif "Major" in prev_complications:
            clinical_score += 3; score_breakdown.append(("Previous complications (Major)", 3))
        if diabetes_status == "Controlled":
            clinical_score += 1; score_breakdown.append(("Diabetes — Controlled", 1))
        elif diabetes_status == "Uncontrolled":
            clinical_score += 3; score_breakdown.append(("Diabetes — Uncontrolled", 3))
        if hypertension_status == "Mild":
            clinical_score += 1; score_breakdown.append(("Hypertension — Mild", 1))
        elif hypertension_status == "Severe":
            clinical_score += 3; score_breakdown.append(("Hypertension — Severe", 3))
        if trimester == "Third":
            clinical_score += 2; score_breakdown.append(("Third Trimester", 2))

        # 6. Hybrid Risk Adjustment
        ml_risk_original = risk
        adjustment_made  = "unchanged"
        if clinical_score >= 6:
            if "high" not in risk.lower():
                risk = "High Risk"; adjustment_made = "escalated"
        elif clinical_score >= 3 and "low" in risk.lower():
            risk = "Mid Risk"; adjustment_made = "upgraded"

        # 7. Confidence level
        if confidence >= 85:   confidence_level = "High Confidence"
        elif confidence >= 70: confidence_level = "Moderate Confidence"
        else:                  confidence_level = "Low Confidence"

        # 8. Dynamic Recommendations
        actions = []
        if systolic > 140:    actions.append("⚠️ Immediate BP monitoring required — systolic critically elevated")
        elif systolic > 120:  actions.append("📊 Systolic BP slightly elevated — monitor at every antenatal visit")
        if diastolic > 90:    actions.append("⚠️ Diastolic BP elevated — consider antihypertensive review")
        if bs > 9.0:          actions.append("🩸 Blood sugar critically high — urgent dietary review and insulin adjustment")
        elif bs > 7.0:        actions.append("🩸 Blood sugar elevated — dietary control and endocrinology consultation")
        if hr > 100:          actions.append("💓 Tachycardia detected — reduce exertion, investigate cause")
        elif hr < 60:         actions.append("💓 Bradycardia detected — cardiac evaluation recommended")
        if temp > 37.5:       actions.append("🌡️ Elevated temperature — screen for infection")
        elif 0 < temp < 36.0: actions.append("🌡️ Low temperature — assess for hypothermia or systemic illness")
        if age < 18:          actions.append("👶 Teenage pregnancy — enhanced psychosocial support required")
        elif age > 35:        actions.append("👩 Advanced maternal age — chromosomal screening advised")
        if diabetes_status == "Uncontrolled": actions.append("💉 Uncontrolled diabetes — urgent endocrinology referral")
        elif diabetes_status == "Controlled": actions.append("💉 Continue diabetes management — maintain glycaemic targets")
        if hypertension_status == "Severe":   actions.append("🩺 Severe hypertension — immediate obstetric review")
        elif hypertension_status == "Mild":   actions.append("🩺 Mild hypertension — increase monitoring frequency")
        if "Major" in prev_complications:     actions.append("📋 History of major complications — high-risk pathway required")
        elif "Minor" in prev_complications:   actions.append("📋 Minor previous complications — enhanced monitoring protocol")
        if trimester == "Third":   actions.append("🤰 Third trimester — prioritise delivery planning and fetal monitoring")
        elif trimester == "Second": actions.append("🤰 Second trimester — anomaly scan and GDM screening recommended")
        if not actions: actions.append("✅ All vitals and clinical indicators within normal range")
        recommendation = " &nbsp;|&nbsp; ".join(actions)

        # 9. Display props
        risk_lower = risk.strip().lower()
        if "low" in risk_lower:
            card_class="risk-low"; rec_class="rec-low"; risk_icon="💚"; badge_label="Low Risk"
            urgency = "Routine Care"
            risk_note = "Your current vitals indicate a low maternal risk level. Continue routine prenatal care and maintain healthy lifestyle habits."
        elif "high" in risk_lower:
            card_class="risk-high"; rec_class="rec-high"; risk_icon="🔴"; badge_label="High Risk"
            urgency = "High Priority — Immediate Attention"
            risk_note = "Elevated risk indicators detected. Immediate consultation with your obstetric care team is strongly recommended."
        else:
            card_class="risk-mid"; rec_class="rec-mid"; risk_icon="🟡"; badge_label="Moderate Risk"
            urgency = "Moderate Attention Required"
            risk_note = "Some risk indicators are outside the optimal range. Please schedule a follow-up with your healthcare provider."

        if confidence >= 85:   bar_class="conf-fill-high"; badge_cls="badge-high"
        elif confidence >= 70: bar_class="conf-fill-mid";  badge_cls="badge-mid"
        else:                  bar_class="conf-fill-low";  badge_cls="badge-low"

        r_key = "low" if "low" in risk_lower else ("high" if "high" in risk_lower else "mid")

        # 10. Clinical summary
        abnormal_flags = []
        if systolic > 120 or systolic < 90:   abnormal_flags.append("blood pressure (systolic)")
        if diastolic > 80  or diastolic < 60: abnormal_flags.append("blood pressure (diastolic)")
        if bs > 7.0        or bs < 4.0:       abnormal_flags.append("blood sugar levels")
        if temp > 37.5     or temp < 36.5:    abnormal_flags.append("body temperature")
        if hr > 100        or hr < 60:        abnormal_flags.append("heart rate")
        if age < 18        or age > 35:       abnormal_flags.append("age-related risk factors")
        if abnormal_flags:
            joined = (", ".join(abnormal_flags[:-1]) + " and " + abnormal_flags[-1]) if len(abnormal_flags) > 1 else abnormal_flags[0]
            cause_sentence = f"The assessment highlights deviations in <strong>{joined}</strong>."
        else:
            cause_sentence = "All measured parameters are within the expected clinical ranges."

        summary_map = {
            "low":  f"Based on the provided physiological parameters, the patient presents with <strong>stable and reassuring vital signs</strong>. {cause_sentence} Routine antenatal care and scheduled follow-up appointments are recommended.",
            "mid":  f"Based on the provided physiological parameters, the patient demonstrates <strong>borderline clinical indicators</strong> warranting closer attention. {cause_sentence} A structured care plan with increased monitoring frequency is advised.",
            "high": f"Based on the provided physiological parameters, the patient exhibits <strong>significant clinical risk indicators</strong> requiring prompt evaluation. {cause_sentence} Immediate referral to a maternal-fetal medicine specialist is strongly recommended.",
        }

        # 11. AI Risk Reasoning
        top_positive = shap_df[shap_df["Impact"] > 0].head(3)["Feature"].tolist()
        top_negative = shap_df[shap_df["Impact"] < 0].head(2)["Feature"].tolist()
        insight_text = ""
        if top_positive: insight_text += f"Key factors increasing risk: <strong>{', '.join(top_positive)}</strong>. "
        if top_negative: insight_text += f"Protective factors: <strong>{', '.join(top_negative)}</strong>."

        # 12. Build SHAP component HTML
        top_features = shap_df.head(6)
        max_impact   = top_features["AbsImpact"].max()
        shap_rows_html = ""
        for _, row in top_features.iterrows():
            feat=row["Feature"]; imp=row["Impact"]; abs_imp=row["AbsImpact"]
            bar_pct = (abs_imp / max_impact * 100) if max_impact > 0 else 0
            if imp > 0:
                bc="linear-gradient(90deg,#fb7185,#e11d48)"; dc="#be123c"; dl="&#8593; Increases Risk"
            else:
                bc="linear-gradient(90deg,#4ade80,#16a34a)"; dc="#15803d"; dl="&#8595; Reduces Risk"
            shap_rows_html += f"""<div style="display:flex;align-items:center;gap:16px;padding:14px 0;border-bottom:1px solid #ecdde3;font-family:'DM Sans',sans-serif;">
                <span style="width:155px;flex-shrink:0;font-size:15px;font-weight:600;color:#1c1018;">{feat}</span>
                <div style="flex:1;height:10px;background:#f3f4f6;border-radius:100px;overflow:hidden;">
                    <div style="height:100%;width:{bar_pct:.1f}%;background:{bc};border-radius:100px;"></div>
                </div>
                <span style="width:145px;flex-shrink:0;font-size:13px;font-weight:700;text-align:right;color:{dc};">{dl}</span>
            </div>"""

        shap_component_html = f"""<div style="background:rgba(255,255,255,0.9);border:1px solid #e8d8e0;border-radius:20px;padding:26px 30px;box-shadow:0 6px 24px rgba(140,60,90,0.11);font-family:'DM Sans',sans-serif;">
            <div style="display:flex;gap:28px;margin-bottom:16px;padding-bottom:12px;border-bottom:2px solid #fff1f2;">
                <span style="display:inline-flex;align-items:center;gap:7px;font-size:11px;font-weight:700;color:#be123c;letter-spacing:0.10em;text-transform:uppercase;">
                    <span style="width:12px;height:12px;border-radius:3px;flex-shrink:0;background:linear-gradient(90deg,#fb7185,#e11d48);display:inline-block;"></span>Increases Risk</span>
                <span style="display:inline-flex;align-items:center;gap:7px;font-size:11px;font-weight:700;color:#15803d;letter-spacing:0.10em;text-transform:uppercase;">
                    <span style="width:12px;height:12px;border-radius:3px;flex-shrink:0;background:linear-gradient(90deg,#4ade80,#16a34a);display:inline-block;"></span>Reduces Risk</span>
            </div>
            {shap_rows_html}
            <p style="font-size:13px;color:#5c4a52;margin:16px 0 0;line-height:1.7;font-style:italic;">
                Generated using SHAP (SHapley Additive exPlanations). Bar length reflects relative magnitude of influence.
            </p>
        </div>"""

        # 13. Risk Projection
        proj_input = input_data.copy()
        proj_input["SystolicBP"]    = proj_input["SystolicBP"] + 10
        proj_input["PulsePressure"] = proj_input["SystolicBP"] - proj_input["DiastolicBP"]
        proj_input["BP_Ratio"]      = proj_input["SystolicBP"] / proj_input["DiastolicBP"].replace(0, 1)
        proj_input["MAP"]           = (proj_input["SystolicBP"] + 2 * proj_input["DiastolicBP"]) / 3
        proj_scaled     = scaler.transform(proj_input)
        proj_pred_val   = model.predict(proj_scaled)[0]
        proj_prob       = model.predict_proba(proj_scaled)[0]
        proj_risk       = label_encoder.inverse_transform([proj_pred_val])[0]
        proj_confidence = float(np.max(proj_prob) * 100)
        proj_color_map  = {"low":"#14532d","mid":"#92400e","high":"#881337"}
        proj_key = "low" if "low" in proj_risk.lower() else ("high" if "high" in proj_risk.lower() else "mid")
        proj_changed = proj_risk.lower() != ml_risk_original.lower()
        change_note = (
            f"⚠️ A simulated 10 mmHg rise in Systolic BP changes the predicted risk from <strong>{ml_risk_original.title()}</strong> to <strong>{proj_risk.title()}</strong>. This highlights the sensitivity of cardiovascular parameters."
            if proj_changed else
            f"✅ A simulated 10 mmHg rise in Systolic BP does not change the predicted risk category (<strong>{proj_risk.title()}</strong>), though confidence shifts to {proj_confidence:.1f}%."
        )

        # ── Store everything in session_state ──
        st.session_state.history.append({
            "time": timestamp, "risk": risk,
            "confidence": confidence, "clinical_score": clinical_score
        })
        st.session_state.last_result = {
            # Core ML outputs
            "risk": risk, "confidence": confidence,
            "confidence_level": confidence_level,
            # Clinical scoring
            "clinical_score": clinical_score, "score_breakdown": score_breakdown,
            "adjustment_made": adjustment_made, "ml_risk_original": ml_risk_original,
            "clinical_score_str": "low" if clinical_score<=2 else ("high" if clinical_score>=6 else "mid"),
            # Display props
            "r_key": r_key, "urgency": urgency, "recommendation": recommendation,
            "card_class": card_class, "rec_class": rec_class,
            "risk_icon": risk_icon, "badge_label": badge_label, "risk_note": risk_note,
            "bar_class": bar_class, "badge_cls": badge_cls,
            "timestamp": timestamp,
            # Rich content
            "summary_text": summary_map[r_key],
            "insight_text": insight_text,
            "shap_component_html": shap_component_html,
            # Patient values
            "age": age, "systolic": systolic, "diastolic": diastolic,
            "bs": bs, "temp": temp, "hr": hr,
            "prev_complications": prev_complications,
            "diabetes_status": diabetes_status,
            "hypertension_status": hypertension_status,
            "trimester": trimester,
            # Parameter status list
            "params": [
                ("Age",         age,       18,   35,   f"{int(age)} yrs"),
                ("Systolic BP", systolic,  90,  120,   f"{int(systolic)} mmHg"),
                ("Diastolic BP",diastolic, 60,   80,   f"{int(diastolic)} mmHg"),
                ("Blood Sugar", bs,        4.0,  7.0,  f"{bs:.1f} mmol/L"),
                ("Body Temp",   temp,      36.5, 37.5, f"{temp:.1f} °C"),
                ("Heart Rate",  hr,        60,  100,   f"{int(hr)} bpm"),
            ],
            # Risk projection
            "proj_risk": proj_risk, "proj_confidence": proj_confidence,
            "proj_changed": proj_changed, "change_note": change_note,
            "proj_color_map": proj_color_map, "proj_key": proj_key,
        }

        # ── Navigate to results page ──
        st.session_state.page = "results"
        st.rerun()