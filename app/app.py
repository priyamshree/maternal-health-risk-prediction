"""
app.py  ─  Main entry point for the Maternal Health Risk CDSS.

Folder structure (everything lives inside app/):
  app/
    app.py                    ← this file
    views/
      __init__.py
      input_page.py           ← Page 1: patient input + prediction pipeline
      results_page.py         ← Page 2: results dashboard
      model_insights.py       ← Page 3: model performance & visualisations
    utils/
      __init__.py
      styles.py               ← inject_styles()
      dashboard.py            ← KPI cards, charts, insights, transitions

Expected folder structure at project root:
  Pregnancy Risk/
    app/          ← run from here: streamlit run app.py
    models/       ← model.pkl, scaler.pkl, label_encoder.pkl
    outputs/      ← all 7 visualisation images

Run with:  streamlit run app.py
"""

import streamlit as st
import joblib
import shap

from utils.styles import inject_styles
from views import input_page, results_page, model_insights

# ═══════════════════════════════════════════════════════
#   PAGE CONFIG  (must be the very first Streamlit call)
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Maternal Health Risk Predictor",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════
#   SESSION STATE INIT
# ═══════════════════════════════════════════════════════
if "history"     not in st.session_state: st.session_state.history     = []
if "page"        not in st.session_state: st.session_state.page        = "input"
if "last_result" not in st.session_state: st.session_state.last_result = None

# ═══════════════════════════════════════════════════════
#   LOAD MODEL  [BACKEND — UNCHANGED]
# ═══════════════════════════════════════════════════════
@st.cache_resource
def load_models():
    import os
    # Resolve path relative to this file so it works regardless of
    # the working directory Streamlit is launched from.
    base       = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base, "..", "models")

    model         = joblib.load(os.path.join(models_dir, "model.pkl"))
    scaler        = joblib.load(os.path.join(models_dir, "scaler.pkl"))
    label_encoder = joblib.load(os.path.join(models_dir, "label_encoder.pkl"))
    explainer     = shap.Explainer(model.named_steps["model"])
    return model, scaler, label_encoder, explainer

model, scaler, label_encoder, explainer = load_models()

# ═══════════════════════════════════════════════════════
#   PREMIUM CSS
# ═══════════════════════════════════════════════════════
inject_styles()

# ═══════════════════════════════════════════════════════
#   NAVIGATION BAR
# ═══════════════════════════════════════════════════════
nav1, nav2, nav3, nav4 = st.columns([1.8, 1, 1, 1])

with nav1:
    st.markdown("""
    <div style="padding:0.6rem 0;font-family:'DM Sans',sans-serif;">
        <span style="font-family:'Playfair Display',serif;font-size:1.05rem;
                     font-weight:700;color:#be123c;">
            🌸 Maternal Health CDSS
        </span>
    </div>
    """, unsafe_allow_html=True)

with nav2:
    if st.button(
        "📋 Input",
        key="nav_input",
        use_container_width=True,
        type="primary" if st.session_state.page == "input" else "secondary"
    ):
        st.session_state.page = "input"
        st.rerun()

with nav3:
    has_results   = st.session_state.last_result is not None
    dash_label    = "📊 Dashboard ●" if has_results else "📊 Dashboard"
    if st.button(
        dash_label,
        key="nav_dashboard",
        use_container_width=True,
        type="primary" if st.session_state.page == "results" else "secondary"
    ):
        st.session_state.page = "results"
        st.rerun()

with nav4:
    if st.button(
        "🔬 Insights",
        key="nav_insights",
        use_container_width=True,
        type="primary" if st.session_state.page == "insights" else "secondary"
    ):
        st.session_state.page = "insights"
        st.rerun()

st.markdown(
    "<div style='height:1px;background:linear-gradient(90deg,#fecdd6,transparent);"
    "margin-bottom:0.5rem;'></div>",
    unsafe_allow_html=True
)

# ═══════════════════════════════════════════════════════
#   PAGE ROUTING
# ═══════════════════════════════════════════════════════
if st.session_state.page == "input":
    input_page.render(model, scaler, label_encoder, explainer)

elif st.session_state.page == "results":
    if st.session_state.last_result is None:
        # No prediction yet — redirect back to input
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;color:#9b8a92;">
            <div style="font-size:3rem;margin-bottom:1rem;">📋</div>
            <p style="font-size:1.1rem;font-weight:300;">
                No prediction has been run yet.<br>Please fill in the patient form first.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Go to Patient Input", key="goto_input"):
            st.session_state.page = "input"
            st.rerun()
    else:
        results_page.render()

elif st.session_state.page == "insights":
    model_insights.render()

# ═══════════════════════════════════════════════════════
#   FOOTER
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="app-footer">
    🌸 &nbsp; Maternal Health Risk Prediction System &nbsp;·&nbsp; AI-Powered Clinical Support<br>
    <em style="font-size:0.8rem;">Not a substitute for professional medical advice &nbsp;·&nbsp;
    Always consult a qualified healthcare provider</em>
</div>
""", unsafe_allow_html=True)
