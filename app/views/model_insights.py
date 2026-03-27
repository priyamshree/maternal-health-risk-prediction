"""
views/model_insights.py
Page 3 — Model Performance & Clinical Visualisations.

Images are loaded from: Pregnancy Risk/outputs/
Path resolves correctly regardless of where `streamlit run` is called from.
"""

import os
import streamlit as st
from PIL import Image


_HERE    = os.path.dirname(os.path.abspath(__file__))       # .../app/views/
_OUTPUTS = os.path.join(_HERE, "..", "..", "outputs")        # .../Pregnancy Risk/outputs/


def _load(filename: str):
    """Load image; return None gracefully if file is missing."""
    path = os.path.join(_OUTPUTS, filename)
    if os.path.exists(path):
        return Image.open(path)
    return None


def _image_card(filename: str, caption: str):
    """
    Render a single image inside a styled card.
    Uses a SINGLE st.markdown block + st.image — no split open/close divs
    that would cause Streamlit to render an empty white box.
    """
    img = _load(filename)

    # Card wrapper — fully self-contained, no split tags
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.88);
        border: 1px solid #e8d8e0;
        border-radius: 20px;
        padding: 1rem 1rem 0.3rem;
        box-shadow: 0 6px 24px rgba(140,60,90,0.10);
        margin-bottom: 0.4rem;
    ">
    </div>
    """, unsafe_allow_html=True)  # intentionally empty — CSS only; actual image below

    # NOTE: we do NOT wrap st.image() in st.markdown divs.
    # Instead we use a CSS-class container approach via st.container().
    if img:
        # Apply styling by targeting the native Streamlit image element
        st.markdown("""
        <style>
        [data-testid="stImage"] img {
            border-radius: 14px;
        }
        </style>
        """, unsafe_allow_html=True)
        st.image(img, use_container_width=True)
    else:
        st.warning(f"⚠️  {filename} not found in outputs/")

    st.markdown(f"""
    <p style="
        text-align: center;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: #9b8a92;
        margin: 0.3rem 0 1rem;
    ">{caption}</p>
    """, unsafe_allow_html=True)


def _image_card_v2(filename: str, caption: str):
    """
    Cleaner version: render card using only native Streamlit primitives.
    st.image has a `caption` param — use that to avoid any HTML wrapping entirely.
    The card look is applied via CSS on the stImage container injected once at page load.
    """
    img = _load(filename)
    if img:
        st.image(img, caption=caption, use_container_width=True)
    else:
        st.warning(f"⚠️  {filename} not found in outputs/")


def _section(icon_class: str, icon: str, title: str, mt: str = "2.4rem"):
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
    """Render the Model Insights page."""

    # ── Inject image card styling ONCE at top of page ──
    st.markdown("""
    <style>
    /* Style the native Streamlit image + caption container */
    [data-testid="stImage"] {
        background: rgba(255,255,255,0.88) !important;
        border: 1px solid #e8d8e0 !important;
        border-radius: 20px !important;
        padding: 1rem !important;
        box-shadow: 0 6px 24px rgba(140,60,90,0.10) !important;
        transition: box-shadow 0.25s ease, transform 0.2s ease !important;
        margin-bottom: 0.4rem !important;
    }
    [data-testid="stImage"]:hover {
        box-shadow: 0 16px 48px rgba(140,60,90,0.15) !important;
        transform: translateY(-2px) !important;
    }
    [data-testid="stImage"] img {
        border-radius: 12px !important;
        width: 100% !important;
    }
    /* Caption styling */
    [data-testid="stImage"] > div:last-child p {
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.09em !important;
        text-transform: uppercase !important;
        color: #9b8a92 !important;
        text-align: center !important;
        margin-top: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Page header ──
    st.markdown("""
    <div style="text-align:center;padding:2.8rem 1rem 1.5rem;">
        <div style="display:inline-flex;align-items:center;gap:8px;
                    background:rgba(237,233,254,0.9);color:#6d28d9;
                    font-size:0.74rem;font-weight:700;letter-spacing:0.13em;
                    text-transform:uppercase;padding:7px 20px;border-radius:100px;
                    margin-bottom:1.3rem;border:1px solid #c4b5fd;">
            🔬 &nbsp; Model Evaluation &amp; Data Visualisation
        </div>
        <h2 style="font-family:'Playfair Display',serif;
                   font-size:clamp(1.8rem,3.5vw,2.6rem);font-weight:900;
                   color:#18080f;line-height:1.2;margin:0 auto 0.8rem;text-align:center;">
            Model
            <em style="font-style:italic;
                       background:linear-gradient(135deg,#7c3aed,#4c1d95);
                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                       background-clip:text;">Performance &amp; Insights</em>
        </h2>
        <p style="font-size:1rem;color:#5c4a52;font-weight:300;max-width:600px;
                  margin:0 auto;line-height:1.75;text-align:center;">
            Visual evidence of model quality, training data characteristics, and clinical
            relationships — essential for understanding and trusting the AI predictions
            made by this system.
        </p>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,#c4b5fd,transparent);
                margin-bottom:0.5rem;"></div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    #  GROUP 1 — MODEL PERFORMANCE
    # ════════════════════════════════════════════════════
    _section("icon-rose", "🎯", "Model Performance", mt="1.5rem")
    st.markdown("""
    <p style="color:#5c4a52;font-size:0.95rem;margin-bottom:1.2rem;">
        These charts evaluate the trained machine learning classifier against held-out
        test data. A strong confusion matrix and balanced class distribution are critical
        indicators of clinical reliability.
    </p>
    """, unsafe_allow_html=True)

    p1, p2 = st.columns(2, gap="large")
    with p1:
        _image_card_v2("confusion_matrix.png",
                       "Confusion Matrix — Predicted vs Actual Risk Class")
    with p2:
        _image_card_v2("class_distribution.png",
                       "Class Distribution — Low / Mid / High Risk Counts")

    # ════════════════════════════════════════════════════
    #  GROUP 2 — FEATURE ANALYSIS
    # ════════════════════════════════════════════════════
    _section("icon-purple", "📐", "Feature Analysis")
    st.markdown("""
    <p style="color:#5c4a52;font-size:0.95rem;margin-bottom:1.2rem;">
        Understanding input feature distributions and inter-feature correlations is essential
        for detecting bias, ensuring data quality, and explaining why certain parameters
        influence the model's predictions.
    </p>
    """, unsafe_allow_html=True)

    f1, f2 = st.columns(2, gap="large")
    with f1:
        _image_card_v2("feature_distribution.png",
                       "Feature Distribution — All Input Parameter Ranges")
    with f2:
        _image_card_v2("heatmap.png",
                       "Correlation Heatmap — Feature Inter-dependencies")

    # ════════════════════════════════════════════════════
    #  GROUP 3 — CLINICAL RELATIONSHIPS
    # ════════════════════════════════════════════════════
    _section("icon-sage", "🩺", "Clinical Relationships")
    st.markdown("""
    <p style="color:#5c4a52;font-size:0.95rem;margin-bottom:1.2rem;">
        These charts directly visualise how key physiological parameters relate to maternal
        risk level in the training dataset — validating that the model has learned
        medically meaningful patterns.
    </p>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        _image_card_v2("age_vs_risk.png",   "Age vs Risk Level")
    with c2:
        _image_card_v2("bp_vs_risk.png",    "Blood Pressure vs Risk Level")
    with c3:
        _image_card_v2("sugar_vs_risk.png", "Blood Sugar vs Risk Level")

    # ════════════════════════════════════════════════════
    #  FOOTER NOTE
    # ════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(245,243,255,0.88),rgba(237,233,254,0.88));
                border:1px solid #c4b5fd;border-radius:20px;
                padding:1.6rem 2rem;margin-top:2rem;margin-bottom:1rem;">
        <p style="font-size:0.82rem;color:#6d28d9;font-weight:700;
                  letter-spacing:0.09em;text-transform:uppercase;margin-bottom:0.5rem;">
            📋 &nbsp; About These Visualisations
        </p>
        <p style="font-size:0.92rem;color:#4c1d95;line-height:1.7;margin:0;font-weight:300;">
            All charts were generated during model training and evaluation on the maternal
            health dataset. They represent characteristics of the
            <strong>training and test data</strong>, not live patient data.
            These visualisations are intended to demonstrate model transparency and clinical
            plausibility to clinicians and evaluators.
        </p>
    </div>
    """, unsafe_allow_html=True)