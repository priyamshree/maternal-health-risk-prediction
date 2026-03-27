"""
views/results_page.py
Renders Page 2 — Full Results Dashboard.
Reads all data from st.session_state.last_result (set by input_page.py).
"""
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

from utils.dashboard import (
    render_kpi_cards,
    render_charts,
    render_smart_insights,
    render_risk_transitions,
)


def _param_status(value, low, high):
    if value < low:  return "below", "Below Normal"
    if value > high: return "above", "Above Normal"
    return "normal", "Normal"


def _section(icon_class, icon, title, mt="2.4rem"):
    st.markdown(f"""
    <div class="section-wrap" style="margin-top:{mt};">
        <div class="section-label">
            <div class="section-label-icon {icon_class}">{icon}</div>
            <span class="section-label-text">{title}</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)


def render():
    """Render the full results and analytics dashboard."""

    r = st.session_state.last_result

    # ── BACK BUTTON ──
    if st.button("⬅  Back to Patient Input", key="back_btn"):
        st.session_state.page = "input"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  1. CLINICAL ALERTS
    # ══════════════════════════════════════════════════
    alerts = []
    if r["hypertension_status"] == "Severe" or r["systolic"] > 160:
        alerts.append(("critical", "🚨", "Severe hypertension detected — immediate obstetric review required"))
    elif r["systolic"] > 140 or r["hypertension_status"] == "Mild":
        alerts.append(("warning", "⚠️", "Elevated blood pressure — increased monitoring frequency advised"))
    if r["diabetes_status"] == "Uncontrolled" or r["bs"] > 9.0:
        alerts.append(("critical", "🚨", "Uncontrolled / critical blood sugar — urgent endocrinology referral"))
    elif r["bs"] > 7.0:
        alerts.append(("warning", "⚠️", "Elevated blood sugar levels — dietary review and clinical follow-up"))
    if "high" in r["risk"].lower():
        alerts.append(("critical", "🚨", "High-risk pregnancy classification — specialist consultation required"))
    if "Major" in r["prev_complications"]:
        alerts.append(("warning", "⚠️", "History of major complications — high-risk obstetric pathway activated"))
    if r["trimester"] == "Third":
        alerts.append(("info", "ℹ️", "Third trimester — delivery planning and fetal growth monitoring priority"))

    if alerts:
        _section("icon-rose", "🚨", "Clinical Alerts", mt="1rem")
        for level, icon, msg in alerts:
            st.markdown(f"""
            <div class="alert-banner alert-{level}">
                <span class="alert-icon">{icon}</span>
                <span class="alert-text"><strong>{msg}</strong></span>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  2. CASE SUMMARY CARD
    # ══════════════════════════════════════════════════
    rc_map = {"low":"#14532d","mid":"#78350f","high":"#881337"}
    risk_color = rc_map.get(r["r_key"], "#881337")
    _section("icon-amber", "📋", "Case Summary")
    st.markdown(f"""
    <div class="case-summary">
        <span style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:#18080f;">Patient Assessment</span>
        <span class="case-chip">🎂 {int(r['age'])} yrs</span>
        <span class="case-chip">💉 {r['trimester']} Trimester</span>
        <span class="case-chip">BP {int(r['systolic'])}/{int(r['diastolic'])} mmHg</span>
        <span class="case-chip">BS {r['bs']:.1f} mmol/L</span>
        <span class="case-chip" style="color:{risk_color};border-color:{risk_color};">
            {r['risk_icon']} {r['risk'].title()}
        </span>
        <span class="case-chip">⚖️ Score {r['clinical_score']}/11</span>
        <span class="case-chip">🕒 {r['timestamp']}</span>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  3. SESSION KPI + CHARTS + INSIGHTS + TRANSITIONS
    # ══════════════════════════════════════════════════
    history_df = pd.DataFrame(st.session_state.history)
    render_kpi_cards(history_df, r)
    st.markdown("<br>", unsafe_allow_html=True)
    render_charts(history_df)
    render_smart_insights(history_df, r)
    render_risk_transitions(history_df)

    # ══════════════════════════════════════════════════
    #  4. PREDICTION RESULT (Risk + Confidence)
    # ══════════════════════════════════════════════════
    _section("icon-rose", "📊", "Latest Prediction Result")
    res_col, conf_col = st.columns([3, 2], gap="large")
    with res_col:
        st.markdown(f"""
        <div class="risk-card {r['card_class']}">
            <div class="risk-icon">{r['risk_icon']}</div>
            <div style="flex:1;min-width:0;">
                <span class="risk-badge">{r['badge_label']}</span>
                <div class="risk-level-text">{r['risk'].title()}</div>
                <p class="risk-note">{r['risk_note']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with conf_col:
        st.markdown(f"""
        <div class="conf-wrap">
            <div class="conf-top">
                <div class="conf-label-row">
                    <span class="conf-title">Model Confidence</span>
                    <span class="conf-pct">{r['confidence']:.1f}%</span>
                </div>
                <div class="conf-bar-bg">
                    <div class="conf-bar-fill {r['bar_class']}" style="width:{r['confidence']:.1f}%"></div>
                </div>
                <span class="conf-level-badge {r['badge_cls']}">{r['confidence_level']}</span>
            </div>
            <p class="conf-note">The model analysed 9 clinical parameters including derived cardiovascular indicators using a trained ML classifier.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="timestamp-row">🕒 &nbsp; Assessment generated on &nbsp;<strong>{r['timestamp']}</strong></div>
    <br>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  5. CLINICAL CONTEXT SCORE
    # ══════════════════════════════════════════════════
    _section("icon-amber", "⚖️", "Clinical Context Score")

    score_cls = "score-" + r["clinical_score_str"]
    adj_map = {
        "escalated": ('<span class="adjustment-badge adj-escalated">⬆ Risk Escalated to High by Clinical Context</span>',
                      "Clinical history overrides ML prediction due to critical risk factors."),
        "upgraded":  ('<span class="adjustment-badge adj-upgraded">⬆ Risk Upgraded from Low to Moderate</span>',
                      "Clinical history suggests higher risk than vitals alone indicate."),
        "unchanged": ('<span class="adjustment-badge adj-unchanged">✔ ML Prediction Confirmed by Clinical Context</span>',
                      "Clinical history is consistent with the machine learning prediction."),
    }
    adj_badge, adj_note = adj_map[r["adjustment_made"]]
    bdwn_html = ""
    if r["score_breakdown"]:
        for item, pts in r["score_breakdown"]:
            bdwn_html += f'<div class="score-item"><span class="score-dot active"></span><span>{item} <strong style="color:#e11d48;">+{pts}</strong></span></div>'
    else:
        bdwn_html = '<div class="score-item"><span class="score-dot inactive"></span><span style="color:#9b8a92;">No clinical risk factors recorded</span></div>'

    st.markdown(f"""
    <div class="clinical-score-wrap">
        <div class="score-row">
            <div style="text-align:center;padding-right:1.6rem;border-right:1px solid #e8d8e0;min-width:100px;">
                <div style="font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#9b8a92;margin-bottom:6px;">Clinical Score</div>
                <div class="score-number {score_cls}">{r['clinical_score']}</div>
                <div style="font-size:0.72rem;color:#9b8a92;margin-top:4px;">out of 11</div>
            </div>
            <div class="score-breakdown">
                {bdwn_html}
                <div style="margin-top:10px;">{adj_badge}</div>
                <p style="font-size:0.84rem;color:#5c4a52;margin-top:6px;line-height:1.55;">{adj_note}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Score interpretation
    cs = r["clinical_score"]
    if cs <= 2:
        st.info("🧠 Clinical Interpretation: Low clinical concern — history does not significantly elevate risk.")
    elif cs <= 5:
        st.warning("🧠 Clinical Interpretation: Moderate concern — clinical history contributes to risk.")
    else:
        st.error("🧠 Clinical Interpretation: High concern — strong clinical risk factors present.")

    # ══════════════════════════════════════════════════
    #  6. PARAMETER STATUS
    # ══════════════════════════════════════════════════
    _section("icon-sage", "📈", "Parameter Status")
    for row_params in [r["params"][:3], r["params"][3:]]:
        pcols = st.columns(3, gap="medium")
        for col, (name, val, lo, hi, display) in zip(pcols, row_params):
            css_class, label = _param_status(val, lo, hi)
            with col:
                st.markdown(f"""
                <div class="param-card {css_class}">
                    <span class="param-name">{name}</span>
                    <span class="param-value">{display}</span>
                    <span class="param-status">{label}</span>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  7. CLINICAL SUMMARY
    # ══════════════════════════════════════════════════
    _section("icon-purple", "🩺", "Clinical Summary")
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-label">🩺 &nbsp; AI Clinical Interpretation</div>
        <p class="summary-text">{r['summary_text']}</p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  8. CLINICAL RECOMMENDATION
    # ══════════════════════════════════════════════════
    _section("icon-rose", "🩺", "Clinical Recommendation")
    st.markdown(f"""
    <div class="rec-card {r['rec_class']}">
        <div class="rec-urgency">{r['urgency']}</div>
        <p class="rec-text">{r['recommendation']}</p>
        <span class="rec-conf">Model Confidence: &nbsp;<strong>{r['confidence']:.1f}% &nbsp;({r['confidence_level']})</strong></span>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  9. AI RISK REASONING
    # ══════════════════════════════════════════════════
    _section("icon-purple", "🧠", "AI Risk Reasoning")
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-label">🧠 &nbsp; Model Interpretation</div>
        <p class="summary-text">{r['insight_text']}</p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  10. SHAP EXPLANATION
    # ══════════════════════════════════════════════════
    _section("icon-purple", "🧠", "AI Clinical Explanation (SHAP)")
    components.html(r["shap_component_html"], height=430, scrolling=False)
    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  11. RISK PROJECTION
    # ══════════════════════════════════════════════════
    _section("icon-rose", "📈", "Risk Projection — What-If Simulation")
    st.markdown(f"""
    <div class="projection-card">
        <div class="proj-label">📈 &nbsp; What-If Simulation — If Systolic BP increases by +10 mmHg</div>
        <div class="proj-row">
            <div class="proj-item"><span class="proj-item-label">Current BP</span><span class="proj-item-value">{int(r['systolic'])} mmHg</span></div>
            <div class="proj-arrow">→</div>
            <div class="proj-item"><span class="proj-item-label">Simulated BP</span><span class="proj-item-value">{int(r['systolic'])+10} mmHg</span></div>
            <div class="proj-arrow">→</div>
            <div class="proj-item"><span class="proj-item-label">Current Risk</span><span class="proj-item-value" style="color:{r['proj_color_map'].get(r['r_key'],'#1e40af')};">{r['ml_risk_original'].title()}</span></div>
            <div class="proj-arrow">→</div>
            <div class="proj-item"><span class="proj-item-label">Projected Risk</span><span class="proj-item-value" style="color:{r['proj_color_map'].get(r['proj_key'],'#1e40af')};">{r['proj_risk'].title()}</span></div>
            <div class="proj-item" style="margin-left:auto;"><span class="proj-item-label">Projected Confidence</span><span class="proj-item-value">{r['proj_confidence']:.1f}%</span></div>
        </div>
        <p class="proj-note">{r['change_note']}</p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  12. SYSTEM TRANSPARENCY
    # ══════════════════════════════════════════════════
    _section("icon-purple", "🔍", "System Transparency")
    st.markdown(f"""
    <div class="transparency-card">
        <div class="trans-label">🔍 &nbsp; How This Prediction Was Made</div>
        <div class="trans-flow">
            <div class="trans-node">📊 Physiological Vitals<br><small style="font-weight:400;color:#6d28d9;">6 Parameters</small></div>
            <div class="trans-arrow">+</div>
            <div class="trans-node">🏥 Clinical Context<br><small style="font-weight:400;color:#6d28d9;">History &amp; Comorbidities</small></div>
            <div class="trans-arrow">→</div>
            <div class="trans-node">🤖 ML Model<br><small style="font-weight:400;color:#6d28d9;">Trained Classifier</small></div>
            <div class="trans-arrow">+</div>
            <div class="trans-node">⚖️ Clinical Rules<br><small style="font-weight:400;color:#6d28d9;">Score = {r['clinical_score']}/11</small></div>
            <div class="trans-arrow">→</div>
            <div class="trans-node">🎯 Hybrid Decision<br><small style="font-weight:400;color:#6d28d9;">{r['risk'].title()}</small></div>
        </div>
        <p class="trans-text">This system combines <strong>machine learning prediction</strong> with a <strong>clinical rule-based scoring engine</strong> incorporating patient history, comorbidities, and trimester context. SHAP values ensure full interpretability.</p>
        <p class="trans-text" style="margin-top:0.8rem;font-size:0.88rem;color:#9b8a92;">⚠️ This is a <strong>clinical decision-support tool</strong>. All outputs must be validated by a licensed clinician.</p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    #  13. PDF REPORT
    # ══════════════════════════════════════════════════
    _section("icon-amber", "📄", "Clinical Report")

    # Re-extract local vars from session state for PDF generation
    age=r["age"]; systolic=r["systolic"]; diastolic=r["diastolic"]
    bs=r["bs"];   temp=r["temp"];         hr=r["hr"]
    risk=r["risk"]; confidence=r["confidence"]
    confidence_level=r["confidence_level"]; timestamp=r["timestamp"]
    r_key=r["r_key"]; clinical_score=r["clinical_score"]

    def generate_pdf():
        file_name = "Maternal_Risk_Report.pdf"
        doc = SimpleDocTemplate(file_name, pagesize=letter,
            rightMargin=0.9*inch, leftMargin=0.9*inch,
            topMargin=0.9*inch,   bottomMargin=0.9*inch)

        hts = ParagraphStyle("HT", fontName="Helvetica-Bold", fontSize=16,
            textColor=colors.HexColor("#881337"), alignment=TA_CENTER,
            spaceAfter=8, leading=22)
        hs = ParagraphStyle("HS", fontName="Helvetica", fontSize=9.5,
            textColor=colors.HexColor("#9d6b7e"), alignment=TA_CENTER,
            spaceAfter=12, leading=14)
        sh = ParagraphStyle("SH", fontName="Helvetica-Bold", fontSize=10,
            textColor=colors.HexColor("#be123c"), spaceBefore=14, spaceAfter=6)
        bs_ = ParagraphStyle("BS", fontName="Helvetica", fontSize=9.5,
            textColor=colors.HexColor("#1c1018"), spaceAfter=5, leading=14)
        cap = ParagraphStyle("CAP", fontName="Helvetica-Oblique", fontSize=8.5,
            textColor=colors.HexColor("#5c4a52"), spaceAfter=4, leading=12)
        ts_ = ParagraphStyle("TS", fontName="Helvetica", fontSize=8,
            textColor=colors.HexColor("#9d6b7e"), alignment=TA_RIGHT, spaceAfter=0)
        footer_s = ParagraphStyle("FT", fontName="Helvetica", fontSize=7.5,
            textColor=colors.HexColor("#9d6b7e"), alignment=TA_CENTER)

        def _st(val, lo, hi):
            if val < lo: return "Below Normal"
            if val > hi: return "Above Normal"
            return "Normal"

        story = [Spacer(1,4)]
        story.append(Paragraph("Maternal Health Risk Prediction System", hts))
        story.append(Paragraph("AI-Powered Clinical Risk Assessment Report", hs))
        story.append(HRFlowable(width="100%",thickness=2,color=colors.HexColor("#f43f5e"),spaceAfter=3))
        story.append(HRFlowable(width="100%",thickness=0.5,color=colors.HexColor("#fecdd3"),spaceAfter=10))
        story.append(Paragraph(f"Report Generated: {timestamp}", ts_))
        story.append(Spacer(1,12))

        story.append(Paragraph("PATIENT VITALS &amp; PARAMETERS", sh))
        story.append(HRFlowable(width="100%",thickness=0.5,color=colors.HexColor("#ecdde3"),spaceAfter=8))
        pdata = [
            ["Parameter","Recorded Value","Normal Range","Status"],
            ["Age",f"{age} years","18 – 35 yrs",_st(age,18,35)],
            ["Systolic BP",f"{systolic} mmHg","90 – 120 mmHg",_st(systolic,90,120)],
            ["Diastolic BP",f"{diastolic} mmHg","60 – 80 mmHg",_st(diastolic,60,80)],
            ["Blood Sugar",f"{bs:.1f} mmol/L","4.0 – 7.0 mmol/L",_st(bs,4.0,7.0)],
            ["Body Temperature",f"{temp:.1f} °C","36.5 – 37.5 °C",_st(temp,36.5,37.5)],
            ["Heart Rate",f"{hr} bpm","60 – 100 bpm",_st(hr,60,100)],
        ]
        pt = Table(pdata, colWidths=[2.3*inch,1.6*inch,1.65*inch,1.25*inch])
        pt.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#fff1f2")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#be123c")),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,0),8.5),
            ("TOPPADDING",(0,0),(-1,0),7),("BOTTOMPADDING",(0,0),(-1,0),7),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,1),(-1,-1),8.5),
            ("TEXTCOLOR",(0,1),(-1,-1),colors.HexColor("#1c1018")),
            ("TOPPADDING",(0,1),(-1,-1),5),("BOTTOMPADDING",(0,1),(-1,-1),5),
            ("BACKGROUND",(0,2),(-1,2),colors.HexColor("#fdf2f5")),
            ("BACKGROUND",(0,4),(-1,4),colors.HexColor("#fdf2f5")),
            ("BACKGROUND",(0,6),(-1,6),colors.HexColor("#fdf2f5")),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#ecdde3")),
            ("ALIGN",(1,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ]))
        story.append(pt); story.append(Spacer(1,14))

        story.append(Paragraph("RISK PREDICTION RESULT", sh))
        story.append(HRFlowable(width="100%",thickness=0.5,color=colors.HexColor("#ecdde3"),spaceAfter=8))
        rc_col = {"low":"#14532d","mid":"#78350f","high":"#881337"}.get(r_key,"#881337")
        rc_bg  = {"low":"#f0fdf4","mid":"#fffbeb","high":"#fff1f2"}.get(r_key,"#fff1f2")
        rt = Table(
            [["Predicted Risk Level","Model Confidence","Confidence Label","Clinical Score"],
             [risk.title(),f"{confidence:.1f}%",confidence_level,f"{clinical_score}/11"]],
            colWidths=[1.8*inch,1.8*inch,1.8*inch,1.45*inch])
        rt.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#fff1f2")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#9f1239")),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,0),9),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
            ("BACKGROUND",(0,1),(-1,1),colors.HexColor(rc_bg)),
            ("TEXTCOLOR",(0,1),(-1,1),colors.HexColor(rc_col)),
            ("FONTNAME",(0,1),(-1,1),"Helvetica-Bold"),("FONTSIZE",(0,1),(-1,1),13),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#ecdde3")),
            ("TOPPADDING",(0,1),(-1,1),12),("BOTTOMPADDING",(0,1),(-1,1),12),
        ]))
        story.append(rt); story.append(Spacer(1,14))

        story.append(Paragraph("CLINICAL INTERPRETATION", sh))
        story.append(HRFlowable(width="100%",thickness=0.5,color=colors.HexColor("#ecdde3"),spaceAfter=8))
        interp = {
            "low":  "The patient's vitals are within or close to normal ranges. The AI model classifies this case as <b>Low Risk</b>. Routine prenatal care and regular monitoring are recommended.",
            "mid":  "One or more parameters fall outside the ideal reference range. The AI model classifies this as <b>Moderate Risk</b>. A prompt follow-up with the obstetric team is advised.",
            "high": "The patient's vitals indicate significant deviations. The AI model classifies this as <b>High Risk</b>. Immediate consultation with an obstetrician is strongly recommended.",
        }
        story.append(Paragraph(interp.get(r_key,""), bs_)); story.append(Spacer(1,10))
        story.append(HRFlowable(width="100%",thickness=0.5,color=colors.HexColor("#ecdde3"),spaceAfter=6))
        story.append(Paragraph(
            "⚠  Disclaimer: This report is generated by an AI-based predictive model and is intended solely as a clinical decision-support tool. It does not constitute a medical diagnosis.",
            cap))
        story.append(Spacer(1,10))
        story.append(HRFlowable(width="100%",thickness=1,color=colors.HexColor("#fecdd3"),spaceAfter=5))
        story.append(Paragraph("Maternal Health Risk Prediction System  ·  AI Clinical Assessment  ·  Confidential", footer_s))
        doc.build(story)
        return file_name

    pdf_file = generate_pdf()
    st.markdown("""
    <div class="report-card">
        <p style="font-size:1rem;color:#5c4a52;margin:0 0 1.1rem;line-height:1.7;">
            A structured clinical PDF report has been generated. Download it for your records or to share with a healthcare provider.
        </p>
    </div>
    """, unsafe_allow_html=True)
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📥  Download Clinical Report (PDF)",
            data=f, file_name="Maternal_Risk_Report.pdf", mime="application/pdf"
        )

    # Bottom back button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  Run New Prediction", key="back_btn_bottom"):
        st.session_state.page = "input"
        st.rerun()