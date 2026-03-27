"""
views/model_insights.py
Page 3 — Model Performance & Clinical Visualisations.

Displays the 7 pre-generated images from Pregnancy Risk/outputs/:
  age_vs_risk, bp_vs_risk, sugar_vs_risk   ← Clinical relationship charts
  class_distribution, feature_distribution  ← Data overview
  confusion_matrix                           ← Model performance
  heatmap                                    ← Feature correlation

Images are read from ../outputs/ relative to this file's location.
Path resolves correctly regardless of where `streamlit run` is called from.
"""

import os
import streamlit as st
from PIL import Image


# ── Resolve the outputs folder regardless of working directory ──
_HERE       = os.path.dirname(os.path.abspath(__file__))   # .../app/views/
_OUTPUTS    = os.path.join(_HERE, "..", "..", "outputs")   # .../Pregnancy Risk/outputs/

def _img(filename: str) -> str:
    """Return the absolute path to an image in the outputs folder."""
    return os.path.join(_OUTPUTS, filename)


def _load(filename: str):
    """Load image, return None gracefully if file is missing."""
    path = _img(filename)
    if os.path.exists(path):
        return Image.open(path)
    return None


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
        <h2 style="font-family:'Playfair Display',serif;font-size:clamp(1.8rem,3.5vw,2.6rem);
                   font-weight:900;color:#18080f;line-height:1.2;margin:0 auto 0.8rem;
                   text-align:center;">
            Model <em style="font-style:italic;background:linear-gradient(135deg,#7c3aed,#4c1d95);
                             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                             background-clip:text;">Performance &amp; Insights</em>
        </h2>
        <p style="font-size:1rem;color:#5c4a52;font-weight:300;max-width:600px;
                  margin:0 auto;line-height:1.75;text-align:center;">
            Visual evidence of model quality, training data characteristics, and
            clinical relationships — essential for understanding and trusting the
            AI predictions made by this system.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="height:1px;background:linear-gradient(90deg,#c4b5fd,transparent);
                margin-bottom:0.5rem;"></div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    #  GROUP 1 — MODEL PERFORMANCE
    # ════════════════════════════════════════════════════
    _section("icon-rose", "🎯", "Model Performance", mt="1.5rem")

    st.markdown("""
    <p style="color:#5c4a52;font-size:0.95rem;margin-bottom:1.2rem;">
        These charts evaluate the trained machine learning classifier against held-out test data.
        A strong confusion matrix and balanced class distribution are critical indicators of
        clinical reliability.
    </p>
    """, unsafe_allow_html=True)

    perf_col1, perf_col2 = st.columns(2, gap="large")

    with perf_col1:
        img = _load("confusion_matrix.png")
        if img:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.82);border:1px solid #e8d8e0;
                        border-radius:20px;padding:1.4rem 1.4rem 0.8rem;
                        box-shadow:0 6px 24px rgba(140,60,90,0.10);margin-bottom:0.6rem;">
            """, unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("""
            <p style="text-align:center;font-size:0.8rem;font-weight:700;
                      letter-spacing:0.09em;text-transform:uppercase;
                      color:#9b8a92;margin-top:0.5rem;">
                Confusion Matrix — Predicted vs Actual Risk Class
            </p>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ confusion_matrix.png not found in outputs/")

    with perf_col2:
        img = _load("class_distribution.png")
        if img:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.82);border:1px solid #e8d8e0;
                        border-radius:20px;padding:1.4rem 1.4rem 0.8rem;
                        box-shadow:0 6px 24px rgba(140,60,90,0.10);margin-bottom:0.6rem;">
            """, unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("""
            <p style="text-align:center;font-size:0.8rem;font-weight:700;
                      letter-spacing:0.09em;text-transform:uppercase;
                      color:#9b8a92;margin-top:0.5rem;">
                Class Distribution — Low / Mid / High Risk Counts
            </p>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ class_distribution.png not found in outputs/")

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

    feat_col1, feat_col2 = st.columns(2, gap="large")

    with feat_col1:
        img = _load("feature_distribution.png")
        if img:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.82);border:1px solid #e8d8e0;
                        border-radius:20px;padding:1.4rem 1.4rem 0.8rem;
                        box-shadow:0 6px 24px rgba(140,60,90,0.10);margin-bottom:0.6rem;">
            """, unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("""
            <p style="text-align:center;font-size:0.8rem;font-weight:700;
                      letter-spacing:0.09em;text-transform:uppercase;
                      color:#9b8a92;margin-top:0.5rem;">
                Feature Distribution — All Input Parameter Ranges
            </p>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ feature_distribution.png not found in outputs/")

    with feat_col2:
        img = _load("heatmap.png")
        if img:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.82);border:1px solid #e8d8e0;
                        border-radius:20px;padding:1.4rem 1.4rem 0.8rem;
                        box-shadow:0 6px 24px rgba(140,60,90,0.10);margin-bottom:0.6rem;">
            """, unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("""
            <p style="text-align:center;font-size:0.8rem;font-weight:700;
                      letter-spacing:0.09em;text-transform:uppercase;
                      color:#9b8a92;margin-top:0.5rem;">
                Correlation Heatmap — Feature Inter-dependencies
            </p>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ heatmap.png not found in outputs/")

    # ════════════════════════════════════════════════════
    #  GROUP 3 — CLINICAL RELATIONSHIPS
    # ════════════════════════════════════════════════════
    _section("icon-sage", "🩺", "Clinical Relationships")

    st.markdown("""
    <p style="color:#5c4a52;font-size:0.95rem;margin-bottom:1.2rem;">
        These charts directly visualise how key physiological parameters relate to maternal
        risk level in the training dataset — providing clinical context and validating that
        the model has learned medically meaningful patterns.
    </p>
    """, unsafe_allow_html=True)

    clin_col1, clin_col2, clin_col3 = st.columns(3, gap="large")

    clinical_images = [
        ("age_vs_risk.png",   clin_col1, "Age vs Risk Level"),
        ("bp_vs_risk.png",    clin_col2, "Blood Pressure vs Risk Level"),
        ("sugar_vs_risk.png", clin_col3, "Blood Sugar vs Risk Level"),
    ]

    for filename, col, caption in clinical_images:
        with col:
            img = _load(filename)
            if img:
                st.markdown("""
                <div style="background:rgba(255,255,255,0.82);border:1px solid #e8d8e0;
                            border-radius:20px;padding:1.2rem 1.2rem 0.6rem;
                            box-shadow:0 6px 24px rgba(140,60,90,0.10);margin-bottom:0.6rem;">
                """, unsafe_allow_html=True)
                st.image(img, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <p style="text-align:center;font-size:0.78rem;font-weight:700;
                          letter-spacing:0.08em;text-transform:uppercase;
                          color:#9b8a92;margin-top:0.5rem;">
                    {caption}
                </p>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ {filename} not found in outputs/")

    # ════════════════════════════════════════════════════
    #  DISCLAIMER
    # ════════════════════════════════════════════════════
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(245,243,255,0.88),rgba(237,233,254,0.88));
                border:1px solid #c4b5fd;border-radius:20px;
                padding:1.6rem 2rem;margin-top:2rem;margin-bottom:1rem;">
        <p style="font-size:0.85rem;color:#6d28d9;font-weight:600;
                  letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.5rem;">
            📋 &nbsp; About These Visualisations
        </p>
        <p style="font-size:0.92rem;color:#4c1d95;line-height:1.7;margin:0;font-weight:300;">
            All charts were generated during model training and evaluation on the maternal health
            dataset. They represent the characteristics of the <strong>training and test data</strong>,
            not live patient data. These visualisations are intended to demonstrate model
            transparency and clinical plausibility to clinicians and evaluators.
        </p>
    </div>
    """, unsafe_allow_html=True)