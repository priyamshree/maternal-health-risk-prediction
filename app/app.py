import streamlit as st
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import base64

# ── Load Model  [BACKEND — UNCHANGED] ──
model         = joblib.load("models/model.pkl")
scaler        = joblib.load("models/scaler.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

import shap
explainer = shap.Explainer(model.named_steps["model"])   # [BACKEND — UNCHANGED]

# ── Page Config ──
st.set_page_config(
    page_title="Maternal Health Risk Predictor",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════
#   PREMIUM CSS
# ═══════════════════════════════════════════════════════
def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

    /* ─── Tokens ─── */
    :root {
        --rose-50:   #fff1f3;
        --rose-100:  #ffe4e9;
        --rose-200:  #fecdd6;
        --rose-300:  #fda4b5;
        --rose-400:  #fb7185;
        --rose-500:  #f43f5e;
        --rose-600:  #e11d48;
        --rose-700:  #be123c;
        --mauve:     #9d6b7e;
        --mauve-lt:  #e8d5dc;
        --sage-lt:   #d9ede0;
        --amber-lt:  #fef3c7;
        --purple-lt: #ede9fe;
        --ink:       #18080f;
        --ink-soft:  #5c4a52;
        --ink-muted: #9b8a92;
        --surface:   #fdfafc;
        --border:    #e8d8e0;
        --white:     #ffffff;
        --sh-sm: 0 2px 8px rgba(140,60,90,0.07);
        --sh-md: 0 6px 24px rgba(140,60,90,0.11), 0 2px 8px rgba(140,60,90,0.06);
        --sh-lg: 0 16px 48px rgba(140,60,90,0.15), 0 4px 16px rgba(140,60,90,0.09);
        --r:     20px;
        --r-sm:  12px;
    }

    /* ─── Fonts & reset ─── */
    html, body { font-size: 17px !important; }
    .stApp, .stApp * { font-family: 'DM Sans', sans-serif !important; }
    .stMarkdown p,
    div[data-testid="stMarkdownContainer"] p { font-size: 1.05rem !important; line-height: 1.78 !important; }
    .stNumberInput input  { font-size: 1.05rem !important; }
    label[data-testid="stWidgetLabel"] p,
    .stNumberInput label  {
        font-size: 0.82rem !important; font-weight: 700 !important;
        color: var(--ink-soft) !important; letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    .stButton > button, .stDownloadButton > button { font-size: 1rem !important; }
    p { font-size: 1.05rem; line-height: 1.78; }

    /* ─── Hide Streamlit chrome ─── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ─── Remove white iframe backgrounds (components.html containers) ─── */
    .stCustomComponentV1,
    .stCustomComponentV1 > div,
    .stCustomComponentV1 iframe {
        background: transparent !important;
        background-color: transparent !important;
    }
    /* Catch-all for any iframe Streamlit renders */
    iframe { background-color: transparent !important; }

    /* ─── Animated gradient background ─── */
    @keyframes gradientBreath {
        0%   { background-position: 0% 50%; }
        33%  { background-position: 100% 50%; }
        66%  { background-position: 50% 100%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg,
            #fdf0f4, #fff0f6, #fce8f5,
            #f5eeff, #ede8fe, #fce4f0, #fff1f3);
        background-size: 600% 600%;
        animation: gradientBreath 24s ease infinite;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }

    /* ─── Decorative blurred orbs filling the sides ─── */
    .stApp::before {
        content: '';
        position: fixed;
        top: -120px; left: -160px;
        width: 520px; height: 520px;
        background: radial-gradient(circle, rgba(244,63,94,0.12) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        filter: blur(40px);
    }
    .stApp::after {
        content: '';
        position: fixed;
        bottom: -100px; right: -140px;
        width: 560px; height: 560px;
        background: radial-gradient(circle, rgba(139,92,246,0.10) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        filter: blur(50px);
    }

    /* ─── Main container ─── */
    .block-container {
        padding: 0 3rem 6rem 3rem !important;
        max-width: 1160px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        position: relative;
        z-index: 1;
    }

    /* ─── Animations ─── */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(22px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    /* ═══════════════════════════════
       HERO
    ═══════════════════════════════ */
    .hero-wrap {
        text-align: center;
        padding: 5rem 2rem 3.5rem;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        animation: fadeIn 0.8s ease both;
        position: relative;
    }

    /* Decorative side flourishes */
    .hero-wrap::before,
    .hero-wrap::after {
        content: '✦';
        position: absolute;
        top: 50%;
        font-size: 1.4rem;
        color: var(--rose-300);
        opacity: 0.5;
        transform: translateY(-50%);
    }
    .hero-wrap::before { left: 0; }
    .hero-wrap::after  { right: 0; }

    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(8px);
        color: var(--rose-600);
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 7px 20px;
        border-radius: 100px;
        margin-bottom: 1.6rem;
        border: 1px solid var(--rose-200);
        box-shadow: var(--sh-sm);
    }

    /* ── THE FIX: big bold centered title ── */
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: clamp(2.6rem, 5.5vw, 4rem) !important;
        font-weight: 900 !important;
        color: var(--ink) !important;
        line-height: 1.12 !important;
        margin: 0 auto 1.1rem !important;
        max-width: 780px !important;
        text-align: center !important;
        letter-spacing: -0.01em !important;
    }
    .hero-title em {
        font-style: italic !important;
        font-weight: 700 !important;
        color: var(--rose-600) !important;
        background: linear-gradient(135deg, var(--rose-500), var(--rose-700));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        font-size: 1.1rem !important;
        color: var(--ink-soft);
        font-weight: 300;
        max-width: 620px;
        margin: 0 auto 1.8rem;
        line-height: 1.75;
        text-align: center;
    }

    /* Decorative divider */
    .hero-divider-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0 auto;
    }
    .hero-divider-line {
        width: 48px; height: 2px;
        background: linear-gradient(90deg, transparent, var(--rose-300));
        border-radius: 4px;
    }
    .hero-divider-line.right {
        background: linear-gradient(90deg, var(--rose-300), transparent);
    }
    .hero-divider-dot {
        width: 8px; height: 8px;
        background: var(--rose-400);
        border-radius: 50%;
    }

    /* Stats strip below hero */
    .stats-strip {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 2.5rem auto 0;
        padding: 1.4rem 3rem;
        background: rgba(255,255,255,0.65);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.9);
        border-radius: var(--r);
        box-shadow: var(--sh-sm);
        max-width: 640px;
    }
    .stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
    }
    .stat-value {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--rose-600);
    }
    .stat-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--ink-muted);
    }

    /* ═══════════════════════════════
       SECTION DIVIDERS & LABELS
    ═══════════════════════════════ */
    .section-wrap {
        position: relative;
        margin-top: 2.4rem;
        margin-bottom: 1rem;
    }
    .section-label {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .section-label-icon {
        width: 38px; height: 38px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem; flex-shrink: 0;
        box-shadow: var(--sh-sm);
    }
    .icon-rose   { background: linear-gradient(135deg,#fff0f2,#ffd6de); border:1px solid var(--rose-200); }
    .icon-sage   { background: linear-gradient(135deg,#f0fdf4,#d9ede0); border:1px solid #bbf7d0; }
    .icon-amber  { background: linear-gradient(135deg,#fffbeb,#fef3c7); border:1px solid #fde68a; }
    .icon-purple { background: linear-gradient(135deg,#faf5ff,#ede9fe); border:1px solid #ddd6fe; }
    .section-label-text {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.4rem !important;
        color: var(--ink);
        font-weight: 700;
    }
    .section-rule {
        height: 1px;
        background: linear-gradient(90deg, var(--border), transparent);
        margin-top: 0.7rem;
        margin-bottom: 1rem;
    }

    /* ═══════════════════════════════
       GLASS CARDS
    ═══════════════════════════════ */
    .card {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.95);
        border-radius: var(--r);
        padding: 2rem 2.4rem;
        box-shadow: var(--sh-md);
        margin-bottom: 1.4rem;
        transition: box-shadow 0.3s ease, transform 0.25s ease;
        width: 100%; max-width: 100%;
        box-sizing: border-box;
    }
    .card:hover { box-shadow: var(--sh-lg); transform: translateY(-2px); }

    /* Hide "Press Enter to apply" message */
    .stNumberInput div[data-testid="InputInstructions"],
    .stNumberInput > div > div > div > small,
    div[data-testid="stNumberInput"] small,
    div[data-testid="stNumberInputContainer"] ~ small,
    .stNumberInput small {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* ─── Input columns card ─── */
    [data-testid="stHorizontalBlock"] {
        background: rgba(255,255,255,0.82) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.95) !important;
        border-radius: var(--r) !important;
        padding: 2rem 2rem 1rem !important;
        box-shadow: var(--sh-md) !important;
        margin-bottom: 1.4rem !important;
        transition: box-shadow 0.3s ease !important;
    }
    [data-testid="stHorizontalBlock"]:hover { box-shadow: var(--sh-lg) !important; }
    [data-testid="column"] { gap: 0 !important; }

    /* ─── Make result row columns equal height ─── */
    [data-testid="stHorizontalBlock"]:has(.risk-card) {
        align-items: stretch !important;
    }

    /* ═══════════════════════════════
       INPUT FIELDS
    ═══════════════════════════════ */
    .stNumberInput > div > div > input {
        border: 1.5px solid var(--border) !important;
        border-radius: var(--r-sm) !important;
        background: rgba(253,250,252,0.9) !important;
        color: var(--ink) !important;
        font-size: 1.05rem !important;
        padding: 0.65rem 1rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stNumberInput > div > div > input:focus {
        border-color: var(--rose-400) !important;
        box-shadow: 0 0 0 3px rgba(244,63,94,0.10) !important;
        outline: none !important;
        background: #fff !important;
    }

    /* ═══════════════════════════════
       REFERENCE RANGE PILLS
    ═══════════════════════════════ */
    .range-grid {
        display: grid;
        grid-template-columns: repeat(3,1fr);
        gap: 0.9rem;
    }
    .range-pill {
        background: rgba(253,250,252,0.9);
        border: 1px solid var(--border);
        border-radius: var(--r-sm);
        padding: 1rem 1.2rem;
        display: flex; flex-direction: column; gap: 4px;
        transition: border-color 0.2s, transform 0.2s;
    }
    .range-pill:hover { border-color: var(--rose-300); transform: translateY(-1px); }
    .range-pill-label {
        font-size: 0.72rem; font-weight: 700;
        color: var(--mauve); letter-spacing: 0.09em; text-transform: uppercase;
    }
    .range-pill-value { font-size: 1rem; color: var(--ink); font-weight: 400; }

    /* ═══════════════════════════════
       PARAMETER STATUS CARDS
    ═══════════════════════════════ */
    .param-card {
        border-radius: var(--r-sm);
        padding: 1.1rem 1.3rem;
        display: flex; flex-direction: column; gap: 6px;
        animation: slideUp 0.35s ease both;
        margin-bottom: 0.8rem;
        transition: transform 0.2s;
    }
    .param-card:hover { transform: translateY(-2px); }
    .param-card.normal { background:linear-gradient(135deg,#f0fdf4,#dcfce7); border:1.5px solid #a7f3d0; }
    .param-card.above  { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:1.5px solid #fcd34d; }
    .param-card.high   { background:linear-gradient(135deg,#fff1f2,#ffe4e6); border:1.5px solid #fca5a5; }
    .param-card.below  { background:linear-gradient(135deg,#eff6ff,#dbeafe); border:1.5px solid #93c5fd; }
    .param-name {
        font-size: 0.73rem; font-weight: 700;
        letter-spacing: 0.09em; text-transform: uppercase; color: var(--ink-soft);
    }
    .param-value {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.3rem; font-weight: 700;
    }
    .param-card.normal .param-value { color:#14532d; }
    .param-card.above  .param-value { color:#92400e; }
    .param-card.high   .param-value { color:#881337; }
    .param-card.below  .param-value { color:#1e40af; }
    .param-status {
        font-size: 0.77rem; font-weight: 700;
        border-radius: 100px; padding: 3px 11px;
        display: inline-block; width: fit-content;
    }
    .param-card.normal .param-status { background:#dcfce7; color:#15803d; }
    .param-card.above  .param-status { background:#fef3c7; color:#92400e; }
    .param-card.high   .param-status { background:#ffe4e6; color:#9f1239; }
    .param-card.below  .param-status { background:#dbeafe; color:#1d4ed8; }

    /* ═══════════════════════════════
       PREDICT BUTTON
    ═══════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg,#f43f5e 0%,#be123c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 100px !important;
        padding: 0.85rem 3rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 6px 24px rgba(225,29,72,0.35) !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
        height: 3.5rem !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 32px rgba(225,29,72,0.42) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ═══════════════════════════════
       RISK RESULT CARD
    ═══════════════════════════════ */
    .risk-card {
        border-radius: var(--r);
        padding: 2.2rem 2.4rem;
        display: flex; align-items: flex-start;
        gap: 1.6rem; flex-wrap: wrap;
        box-shadow: var(--sh-md);
        animation: slideUp 0.4s ease both;
        width: 100%; box-sizing: border-box;
        height: 100%;
    }
    .risk-icon { font-size: 3rem; line-height:1; flex-shrink:0; margin-top:3px; }
    .risk-badge {
        font-size: 0.68rem; font-weight: 700;
        letter-spacing: 0.14em; text-transform: uppercase;
        border-radius: 100px; padding: 4px 13px;
        display: inline-block; margin-bottom: 7px;
    }
    .risk-level-text {
        font-family: 'Playfair Display', serif !important;
        font-size: 2rem !important; font-weight: 800 !important;
        line-height: 1.1; margin: 3px 0 10px;
    }
    .risk-note { font-size: 0.96rem; line-height: 1.65; font-weight: 300; margin:0; }

    .risk-low  { background:linear-gradient(135deg,#f0fdf4,#dcfce7); border:1.5px solid #a7f3d0; }
    .risk-low  .risk-badge      { background:#dcfce7; color:#15803d; }
    .risk-low  .risk-level-text { color:#14532d; }
    .risk-low  .risk-note       { color:#166534; }
    .risk-mid  { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:1.5px solid #fcd34d; }
    .risk-mid  .risk-badge      { background:#fef3c7; color:#92400e; }
    .risk-mid  .risk-level-text { color:#78350f; }
    .risk-mid  .risk-note       { color:#92400e; }
    .risk-high { background:linear-gradient(135deg,#fff1f2,#ffe4e6); border:1.5px solid #fca5a5; }
    .risk-high .risk-badge      { background:#ffe4e6; color:#9f1239; }
    .risk-high .risk-level-text { color:#881337; }
    .risk-high .risk-note       { color:#9f1239; }

    /* ═══════════════════════════════
       CONFIDENCE CARD — fixed overflow
    ═══════════════════════════════ */
    .conf-wrap {
        background: rgba(255,255,255,0.88);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border);
        border-radius: var(--r);
        padding: 2rem 2rem;
        box-shadow: var(--sh-md);
        animation: slideUp 0.45s ease 0.1s both;
        /* key: fill full column height */
        height: 100%;
        min-height: 220px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .conf-top { flex: 1; }
    .conf-label-row {
        display: flex; justify-content: space-between;
        align-items: baseline; margin-bottom: 1rem;
    }
    .conf-title {
        font-size: 0.78rem; font-weight: 700;
        color: var(--mauve); letter-spacing: 0.10em; text-transform: uppercase;
    }
    .conf-pct {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.8rem !important; font-weight: 800 !important; color: var(--ink);
    }
    .conf-bar-bg {
        height: 11px; background: var(--rose-100);
        border-radius: 100px; overflow: hidden; margin-bottom: 0.9rem;
    }
    .conf-bar-fill {
        height: 100%; border-radius: 100px;
        transition: width 1.3s cubic-bezier(0.25,0.46,0.45,0.94);
    }
    .conf-fill-high { background: linear-gradient(90deg,#4ade80,#16a34a); }
    .conf-fill-mid  { background: linear-gradient(90deg,#fbbf24,#d97706); }
    .conf-fill-low  { background: linear-gradient(90deg,#fb7185,#e11d48); }
    .conf-level-badge {
        display: inline-block;
        font-size: 0.78rem; font-weight: 700;
        letter-spacing: 0.08em; text-transform: uppercase;
        border-radius: 100px; padding: 4px 15px;
        margin-bottom: 0.9rem;
    }
    .badge-high { background:#dcfce7; color:#15803d; }
    .badge-mid  { background:#fef3c7; color:#92400e; }
    .badge-low  { background:#ffe4e6; color:#9f1239; }
    .conf-note {
        font-size: 0.86rem; color: var(--ink-soft);
        line-height: 1.6; margin: 0;
    }

    /* ═══════════════════════════════
       CLINICAL SUMMARY
    ═══════════════════════════════ */
    .summary-card {
        background: linear-gradient(135deg,rgba(253,244,255,0.92),rgba(252,231,243,0.92));
        backdrop-filter: blur(8px);
        border: 1px solid #e9d5f5;
        border-radius: var(--r);
        padding: 2.2rem 2.6rem;
        box-shadow: var(--sh-sm);
        animation: slideUp 0.45s ease 0.15s both;
        margin-bottom: 1.4rem;
        position: relative;
        overflow: hidden;
    }
    /* decorative quote mark */
    .summary-card::before {
        content: '"';
        position: absolute;
        top: -10px; left: 20px;
        font-size: 8rem;
        color: rgba(167,139,250,0.12);
        font-family: 'Playfair Display', serif;
        line-height: 1;
        pointer-events: none;
    }
    .summary-label {
        font-size: 0.76rem; font-weight: 700;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: #7c3aed; margin-bottom: 0.9rem;
        display: flex; align-items: center; gap: 7px;
    }
    .summary-text {
        font-size: 1rem; line-height: 1.8;
        color: var(--ink); font-weight: 300;
        position: relative; z-index: 1;
    }
    .summary-text strong { font-weight: 600; color: var(--ink); }

    /* ═══════════════════════════════
       RECOMMENDATION CARD
    ═══════════════════════════════ */
    .rec-card {
        border-radius: var(--r);
        padding: 2.2rem 2.6rem;
        box-shadow: var(--sh-md);
        animation: slideUp 0.4s ease both;
        margin-bottom: 1.4rem;
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
    }
    .rec-low  { background:linear-gradient(135deg,#f0fdf4,#dcfce7); border:1.5px solid #a7f3d0; }
    .rec-mid  { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:1.5px solid #fcd34d; }
    .rec-high { background:linear-gradient(135deg,#fff1f2,#ffe4e6); border:1.5px solid #fca5a5; }
    .rec-urgency {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.35rem !important; font-weight: 800 !important;
        margin-bottom: 0.7rem;
    }
    .rec-low  .rec-urgency { color:#14532d; }
    .rec-mid  .rec-urgency { color:#78350f; }
    .rec-high .rec-urgency { color:#881337; }
    .rec-text { font-size: 0.98rem; line-height:1.7; font-weight:300; margin:0 0 1rem; }
    .rec-low  .rec-text { color:#166534; }
    .rec-mid  .rec-text { color:#92400e; }
    .rec-high .rec-text { color:#9f1239; }
    .rec-conf { font-size:0.85rem; color:var(--ink-soft); }
    .rec-conf strong { font-weight:600; color:var(--ink); }

    /* ═══════════════════════════════
       TIMESTAMP
    ═══════════════════════════════ */
    .timestamp-row {
        display: flex; align-items: center; gap: 8px;
        color: var(--ink-muted); font-size: 0.85rem;
        margin-top: 0.6rem; padding: 0.6rem 1rem;
        background: rgba(255,255,255,0.6);
        border-radius: 100px;
        width: fit-content;
        animation: slideUp 0.45s ease 0.2s both;
        border: 1px solid rgba(255,255,255,0.9);
    }

    /* ═══════════════════════════════
       DOWNLOAD BUTTON
    ═══════════════════════════════ */
    .stDownloadButton > button {
        background: white !important;
        color: var(--rose-600) !important;
        border: 2px solid var(--rose-300) !important;
        border-radius: 100px !important;
        padding: 0.75rem 2.4rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
        box-shadow: var(--sh-sm) !important;
    }
    .stDownloadButton > button:hover {
        background: var(--rose-50) !important;
        border-color: var(--rose-400) !important;
        box-shadow: 0 6px 20px rgba(225,29,72,0.18) !important;
        transform: translateY(-2px) !important;
    }

    /* ═══════════════════════════════
       REPORT CARD
    ═══════════════════════════════ */
    .report-card {
        background: rgba(255,255,255,0.85);
        border: 1px solid var(--border);
        border-radius: var(--r);
        padding: 2rem 2.4rem;
        box-shadow: var(--sh-md);
        margin-bottom: 1.4rem;
    }

    /* ═══════════════════════════════
       FOOTER
    ═══════════════════════════════ */
    .app-footer {
        text-align: center;
        padding: 3rem 1rem 2rem;
        color: var(--mauve);
        font-size: 0.84rem;
        letter-spacing: 0.03em;
        line-height: 2;
        border-top: 1px solid var(--mauve-lt);
        margin-top: 2rem;
    }

    /* ═══════════════════════════════
       RESPONSIVE
    ═══════════════════════════════ */
    @media (max-width: 768px) {
        .range-grid { grid-template-columns: repeat(2,1fr); }
        .hero-title  { font-size: 2.2rem !important; }
        .block-container { padding: 0 1rem 3rem !important; }
        .stats-strip { gap:1.5rem; padding:1.2rem 1.5rem; flex-wrap:wrap; }
        .hero-wrap::before, .hero-wrap::after { display:none; }
    }

    </style>
    """, unsafe_allow_html=True)

inject_styles()

# ═══════════════════════════════════════════════════════
#   HERO HEADER
# ═══════════════════════════════════════════════════════
import streamlit.components.v1 as components
components.html("""
<!DOCTYPE html>
<html>
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background: transparent; overflow: hidden; }
</style>
</head>
<body>
<div style="
    text-align:center;
    padding: 3.2rem 2rem 2.4rem;
    width:100%;
    display:flex;
    flex-direction:column;
    align-items:center;
    font-family:'DM Sans',sans-serif;
">
  <!-- Eyebrow badge -->
  <div style="
      display:inline-flex; align-items:center; gap:8px;
      background:rgba(255,228,233,0.9);
      color:#e11d48;
      font-size:0.72rem; font-weight:700;
      letter-spacing:0.15em; text-transform:uppercase;
      padding:7px 20px; border-radius:100px;
      margin-bottom:1.5rem;
      border:1px solid #fecdd6;
      box-shadow:0 2px 8px rgba(140,60,90,0.08);
  ">🌸 &nbsp; AI-Powered Clinical Decision Support</div>

  <!-- Main title -->
  <h1 style="
      font-family:'Playfair Display',serif;
      font-size:clamp(2.4rem,5vw,3.8rem);
      font-weight:900;
      color:#18080f;
      line-height:1.12;
      margin:0 auto 1.1rem;
      max-width:760px;
      text-align:center;
      letter-spacing:-0.01em;
  ">
      Maternal Health<br>
      <em style="
          font-style:italic;
          font-weight:700;
          background:linear-gradient(135deg,#f43f5e,#be123c);
          -webkit-background-clip:text;
          -webkit-text-fill-color:transparent;
          background-clip:text;
      ">Risk Prediction System</em>
  </h1>

  <!-- Subtitle -->
  <p style="
      font-size:1.05rem;
      color:#5c4a52;
      font-weight:300;
      max-width:600px;
      margin:0 auto 1.8rem;
      line-height:1.75;
      text-align:center;
  ">
      AI-powered system for predicting maternal health risk using key physiological parameters.
      It provides risk classification, confidence score, and clinical insights to support
      early detection and informed healthcare decisions.
  </p>

  <!-- Decorative divider only -->
  <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:48px;height:2px;background:linear-gradient(90deg,transparent,#fb7185);border-radius:4px;"></div>
      <div style="width:8px;height:8px;background:#fb7185;border-radius:50%;"></div>
      <div style="width:48px;height:2px;background:linear-gradient(90deg,#fb7185,transparent);border-radius:4px;"></div>
  </div>

</div>
</body>
</html>
""", height=380, scrolling=False)

# Stats strip — flat inline HTML, Streamlit-safe
st.markdown("""
<div style="display:flex;justify-content:center;max-width:560px;margin:-0.2rem auto 0.6rem;
            background:rgba(255,255,255,0.68);border:1px solid #ecdde3;
            border-radius:16px;box-shadow:0 2px 12px rgba(140,60,90,0.08);overflow:hidden;">
  <div style="flex:1;display:flex;flex-direction:column;align-items:center;
              padding:1rem 0.4rem;border-right:1px solid #ecdde3;">
    <span style="font-size:1.45rem;font-weight:800;color:#e11d48;line-height:1;">6</span>
    <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.09em;
                 text-transform:uppercase;color:#9b8a92;margin-top:3px;">Vital Parameters</span>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;align-items:center;
              padding:1rem 0.4rem;border-right:1px solid #ecdde3;">
    <span style="font-size:1.45rem;font-weight:800;color:#e11d48;line-height:1;">3</span>
    <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.09em;
                 text-transform:uppercase;color:#9b8a92;margin-top:3px;">Risk Levels</span>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;align-items:center;
              padding:1rem 0.4rem;border-right:1px solid #ecdde3;">
    <span style="font-size:1.45rem;font-weight:800;color:#e11d48;line-height:1;">AI</span>
    <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.09em;
                 text-transform:uppercase;color:#9b8a92;margin-top:3px;">SHAP Explained</span>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;align-items:center;
              padding:1rem 0.4rem;">
    <span style="font-size:1.45rem;font-weight:800;color:#e11d48;line-height:1;">PDF</span>
    <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.09em;
                 text-transform:uppercase;color:#9b8a92;margin-top:3px;">Clinical Report</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#   SECTION 1 — Patient Input
# ═══════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════
#   SECTION 2 — Clinical Reference Ranges
# ═══════════════════════════════════════════════════════
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
        <div class="range-pill">
            <span class="range-pill-label">Age</span>
            <span class="range-pill-value">18 – 35 years</span>
        </div>
        <div class="range-pill">
            <span class="range-pill-label">Systolic BP</span>
            <span class="range-pill-value">90 – 120 mmHg</span>
        </div>
        <div class="range-pill">
            <span class="range-pill-label">Diastolic BP</span>
            <span class="range-pill-value">60 – 80 mmHg</span>
        </div>
        <div class="range-pill">
            <span class="range-pill-label">Blood Sugar</span>
            <span class="range-pill-value">4.0 – 7.0 mmol/L</span>
        </div>
        <div class="range-pill">
            <span class="range-pill-label">Body Temperature</span>
            <span class="range-pill-value">36.5 – 37.5 °C</span>
        </div>
        <div class="range-pill">
            <span class="range-pill-label">Heart Rate</span>
            <span class="range-pill-value">60 – 100 bpm</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#   SECTION 3 — Predict Button
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="section-wrap">
    <div class="section-label">
        <div class="section-label-icon icon-rose">🔬</div>
        <span class="section-label-text">Risk Assessment</span>
    </div>
    <div class="section-rule"></div>
</div>
""", unsafe_allow_html=True)

predict_col, _ = st.columns([1, 2])
with predict_col:
    predict_clicked = st.button("🔍  Analyse & Predict Risk Level")

# ═══════════════════════════════════════════════════════
#   PREDICTION PIPELINE  [BACKEND — 100% UNCHANGED]
# ═══════════════════════════════════════════════════════
if predict_clicked:

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

    # 3. Prediction
    pred       = model.predict(scaled)[0]
    prob       = model.predict_proba(scaled)[0]
    risk       = label_encoder.inverse_transform([pred])[0]
    confidence = float(np.max(prob) * 100)
    timestamp  = datetime.now().strftime("%d %B %Y, %H:%M:%S")

    # 4. SHAP
    shap_values   = explainer(scaled)
    feature_names = ["Age","SystolicBP","DiastolicBP","BS","BodyTemp",
                     "HeartRate","PulsePressure","MAP","BP_Ratio"]
    shap_vals = shap_values.values[0][:, pred]
    shap_df   = pd.DataFrame({"Feature": feature_names, "Impact": shap_vals})
    shap_df["AbsImpact"] = shap_df["Impact"].abs()
    shap_df = shap_df.sort_values(by="AbsImpact", ascending=False)

    # Confidence level
    if confidence >= 85:
        confidence_level = "High Confidence"
    elif confidence >= 70:
        confidence_level = "Moderate Confidence"
    else:
        confidence_level = "Low Confidence"

    # Recommendation
    if risk.lower() == "low risk":
        recommendation = "Maintain regular prenatal check-ups and a healthy lifestyle. Continue routine monitoring."
        urgency = "Routine Care"
    elif risk.lower() == "mid risk":
        recommendation = "Increased monitoring is advised. Consult your healthcare provider for closer evaluation."
        urgency = "Moderate Attention Required"
    else:
        recommendation = "Immediate medical attention is recommended. Please consult a healthcare professional as soon as possible."
        urgency = "High Priority"

    # Risk display props
    risk_lower = risk.strip().lower()
    if "low" in risk_lower:
        card_class  = "risk-low";  rec_class = "rec-low"
        risk_icon   = "💚";        badge_label = "Low Risk"
        risk_note   = ("Your current vitals indicate a low maternal risk level. "
                       "Continue routine prenatal care and maintain healthy lifestyle habits. "
                       "Regular monitoring is still advised.")
    elif "high" in risk_lower:
        card_class  = "risk-high"; rec_class = "rec-high"
        risk_icon   = "🔴";        badge_label = "High Risk"
        risk_note   = ("Elevated risk indicators detected. Immediate consultation with your "
                       "obstetric care team is strongly recommended. Close monitoring and "
                       "possible medical intervention may be required.")
    else:
        card_class  = "risk-mid";  rec_class = "rec-mid"
        risk_icon   = "🟡";        badge_label = "Moderate Risk"
        risk_note   = ("Some risk indicators are outside the optimal range. Please schedule "
                       "a follow-up with your healthcare provider for further evaluation and "
                       "personalised guidance.")

    if confidence >= 85:
        bar_class = "conf-fill-high"; badge_cls = "badge-high"
    elif confidence >= 70:
        bar_class = "conf-fill-mid";  badge_cls = "badge-mid"
    else:
        bar_class = "conf-fill-low";  badge_cls = "badge-low"

    r_key = "low" if "low" in risk_lower else ("high" if "high" in risk_lower else "mid")

    # ────────────────────────────────────
    #  RESULT — Risk card + Confidence
    # ────────────────────────────────────
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-rose">📊</div>
            <span class="section-label-text">Prediction Result</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    res_col, conf_col = st.columns([3, 2], gap="large")

    with res_col:
        st.markdown(f"""
        <div class="risk-card {card_class}">
            <div class="risk-icon">{risk_icon}</div>
            <div style="flex:1;min-width:0;">
                <span class="risk-badge">{badge_label}</span>
                <div class="risk-level-text">{risk.title()}</div>
                <p class="risk-note">{risk_note}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with conf_col:
        st.markdown(f"""
        <div class="conf-wrap">
            <div class="conf-top">
                <div class="conf-label-row">
                    <span class="conf-title">Model Confidence</span>
                    <span class="conf-pct">{confidence:.1f}%</span>
                </div>
                <div class="conf-bar-bg">
                    <div class="conf-bar-fill {bar_class}" style="width:{confidence:.1f}%"></div>
                </div>
                <span class="conf-level-badge {badge_cls}">{confidence_level}</span>
            </div>
            <p class="conf-note">
                The model analysed 9 clinical parameters including derived cardiovascular
                indicators (Pulse Pressure, MAP, BP Ratio) using a trained machine learning classifier.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="timestamp-row">
        🕒 &nbsp; Assessment generated on &nbsp;<strong>{timestamp}</strong>
    </div>
    <br>
    """, unsafe_allow_html=True)

    # ────────────────────────────────────
    #  PARAMETER STATUS
    # ────────────────────────────────────
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-sage">📈</div>
            <span class="section-label-text">Parameter Status</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    def _param_status(value, low, high):
        if value < low:  return "below", "Below Normal"
        if value > high: return "above", "Above Normal"
        return "normal", "Normal"

    params = [
        ("Age",          age,       18,   35,   f"{int(age)} yrs"),
        ("Systolic BP",  systolic,  90,  120,   f"{int(systolic)} mmHg"),
        ("Diastolic BP", diastolic, 60,   80,   f"{int(diastolic)} mmHg"),
        ("Blood Sugar",  bs,        4.0,  7.0,  f"{bs:.1f} mmol/L"),
        ("Body Temp",    temp,      36.5, 37.5, f"{temp:.1f} °C"),
        ("Heart Rate",   hr,        60,  100,   f"{int(hr)} bpm"),
    ]

    for row_params in [params[:3], params[3:]]:
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

    # ────────────────────────────────────
    #  CLINICAL SUMMARY
    # ────────────────────────────────────
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-purple">🩺</div>
            <span class="section-label-text">Clinical Summary</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    abnormal_flags = []
    if systolic > 120 or systolic < 90:   abnormal_flags.append("blood pressure (systolic)")
    if diastolic > 80  or diastolic < 60: abnormal_flags.append("blood pressure (diastolic)")
    if bs > 7.0        or bs < 4.0:       abnormal_flags.append("blood sugar levels")
    if temp > 37.5     or temp < 36.5:    abnormal_flags.append("body temperature")
    if hr > 100        or hr < 60:        abnormal_flags.append("heart rate")
    if age < 18        or age > 35:       abnormal_flags.append("age-related risk factors")

    if abnormal_flags:
        joined = (", ".join(abnormal_flags[:-1]) + " and " + abnormal_flags[-1]) if len(abnormal_flags) > 1 else abnormal_flags[0]
        cause_sentence = f"The assessment highlights deviations in <strong>{joined}</strong>, which have contributed to the predicted risk classification."
    else:
        cause_sentence = "All measured parameters are within the expected clinical ranges, supporting a <strong>low-risk classification</strong>."

    summary_map = {
        "low":  (f"Based on the provided physiological parameters, the patient presents with <strong>stable and reassuring vital signs</strong>. "
                 f"{cause_sentence} Routine antenatal care, nutritional support, and scheduled follow-up appointments are recommended to maintain this favourable status."),
        "mid":  (f"Based on the provided physiological parameters, the patient demonstrates <strong>borderline clinical indicators</strong> warranting closer attention. "
                 f"{cause_sentence} A structured care plan with increased monitoring frequency is advised, along with consultation with the obstetric team for individualised management."),
        "high": (f"Based on the provided physiological parameters, the patient exhibits <strong>significant clinical risk indicators</strong> that require prompt evaluation. "
                 f"{cause_sentence} Immediate referral to an obstetrician or maternal-fetal medicine specialist is strongly recommended. Delay in intervention may pose risks to both maternal and fetal wellbeing."),
    }

    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-label">🩺 &nbsp; AI Clinical Interpretation</div>
        <p class="summary-text">{summary_map[r_key]}</p>
    </div>
    """, unsafe_allow_html=True)

    # ────────────────────────────────────
    #  CLINICAL RECOMMENDATION
    # ────────────────────────────────────
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-rose">🩺</div>
            <span class="section-label-text">Clinical Recommendation</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="rec-card {rec_class}">
        <div class="rec-urgency">{urgency}</div>
        <p class="rec-text">{recommendation}</p>
        <span class="rec-conf">
            Model Confidence: &nbsp;<strong>{confidence:.1f}% &nbsp;({confidence_level})</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ────────────────────────────────────
    #  AI SHAP EXPLANATION  — st.components.v1.html (self-contained)
    # ────────────────────────────────────
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-purple">🧠</div>
            <span class="section-label-text">AI Clinical Explanation</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    top_features = shap_df.head(6)
    max_impact   = top_features["AbsImpact"].max()

    shap_rows_html = ""
    for _, row in top_features.iterrows():
        feature = row["Feature"]
        impact  = row["Impact"]
        abs_imp = row["AbsImpact"]
        bar_pct = (abs_imp / max_impact * 100) if max_impact > 0 else 0

        if impact > 0:
            bar_color  = "linear-gradient(90deg,#fb7185,#e11d48)"
            dir_color  = "#be123c"
            dir_label  = "&#8593; Increases Risk"
        else:
            bar_color  = "linear-gradient(90deg,#4ade80,#16a34a)"
            dir_color  = "#15803d"
            dir_label  = "&#8595; Reduces Risk"

        shap_rows_html += f"""
        <div style="display:flex;align-items:center;gap:16px;padding:14px 0;
                    border-bottom:1px solid #ecdde3;font-family:'DM Sans',sans-serif;">
            <span style="width:155px;flex-shrink:0;font-size:15px;
                         font-weight:600;color:#1c1018;">{feature}</span>
            <div style="flex:1;height:10px;background:#f3f4f6;
                        border-radius:100px;overflow:hidden;">
                <div style="height:100%;width:{bar_pct:.1f}%;background:{bar_color};
                            border-radius:100px;"></div>
            </div>
            <span style="width:145px;flex-shrink:0;font-size:13px;font-weight:700;
                         text-align:right;color:{dir_color};">{dir_label}</span>
        </div>
        """

    shap_html = f"""
    <div style="background:rgba(255,255,255,0.9);border:1px solid #e8d8e0;
                border-radius:20px;padding:26px 30px;
                box-shadow:0 6px 24px rgba(140,60,90,0.11);
                font-family:'DM Sans',sans-serif;">
        <div style="display:flex;gap:28px;margin-bottom:16px;padding-bottom:12px;
                    border-bottom:2px solid #fff1f2;">
            <span style="display:inline-flex;align-items:center;gap:7px;
                         font-size:11px;font-weight:700;color:#be123c;
                         letter-spacing:0.10em;text-transform:uppercase;">
                <span style="width:12px;height:12px;border-radius:3px;flex-shrink:0;
                             background:linear-gradient(90deg,#fb7185,#e11d48);
                             display:inline-block;"></span>
                Increases Risk
            </span>
            <span style="display:inline-flex;align-items:center;gap:7px;
                         font-size:11px;font-weight:700;color:#15803d;
                         letter-spacing:0.10em;text-transform:uppercase;">
                <span style="width:12px;height:12px;border-radius:3px;flex-shrink:0;
                             background:linear-gradient(90deg,#4ade80,#16a34a);
                             display:inline-block;"></span>
                Reduces Risk
            </span>
        </div>
        {shap_rows_html}
        <p style="font-size:13px;color:#5c4a52;margin:16px 0 0;
                  line-height:1.7;font-style:italic;">
            Generated using SHAP (SHapley Additive exPlanations). Red bars indicate features
            that increase predicted risk; green bars indicate protective features.
            Bar length reflects the relative magnitude of each parameter's influence.
        </p>
    </div>
    """

    import streamlit.components.v1 as components
    components.html(shap_html, height=430, scrolling=False)

    st.markdown("<br>", unsafe_allow_html=True)

    # ────────────────────────────────────
    #  PDF REPORT
    # ────────────────────────────────────
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-amber">📄</div>
            <span class="section-label-text">Clinical Report</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    def generate_pdf():
        file_name = "Maternal_Risk_Report.pdf"
        doc = SimpleDocTemplate(
            file_name, pagesize=letter,
            rightMargin=0.9*inch, leftMargin=0.9*inch,
            topMargin=0.9*inch,  bottomMargin=0.9*inch
        )

        header_title_style = ParagraphStyle(
            "HeaderTitle", fontName="Helvetica-Bold", fontSize=16,
            textColor=colors.HexColor("#881337"), alignment=TA_CENTER,
            spaceAfter=8, leading=22,
        )
        header_sub_style = ParagraphStyle(
            "HeaderSub", fontName="Helvetica", fontSize=9.5,
            textColor=colors.HexColor("#9d6b7e"), alignment=TA_CENTER,
            spaceAfter=12, leading=14,
        )
        section_heading_style = ParagraphStyle(
            "SectionHeading", fontName="Helvetica-Bold", fontSize=10,
            textColor=colors.HexColor("#be123c"), spaceBefore=14, spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "Body", fontName="Helvetica", fontSize=9.5,
            textColor=colors.HexColor("#1c1018"), spaceAfter=5, leading=14,
        )
        caption_style = ParagraphStyle(
            "Caption", fontName="Helvetica-Oblique", fontSize=8.5,
            textColor=colors.HexColor("#5c4a52"), spaceAfter=4, leading=12,
        )
        ts_style = ParagraphStyle(
            "Timestamp", fontName="Helvetica", fontSize=8,
            textColor=colors.HexColor("#9d6b7e"), alignment=TA_RIGHT, spaceAfter=0,
        )

        story = []
        story.append(Spacer(1, 4))
        story.append(Paragraph("Maternal Health Risk Prediction System", header_title_style))
        story.append(Paragraph("AI-Powered Clinical Risk Assessment Report", header_sub_style))
        story.append(HRFlowable(width="100%", thickness=2,   color=colors.HexColor("#f43f5e"), spaceAfter=3))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#fecdd3"), spaceAfter=10))
        story.append(Paragraph(f"Report Generated: {timestamp}", ts_style))
        story.append(Spacer(1, 12))

        story.append(Paragraph("PATIENT VITALS &amp; PARAMETERS", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#ecdde3"), spaceAfter=8))

        def _status_text(val, lo, hi):
            if val < lo: return "Below Normal"
            if val > hi: return "Above Normal"
            return "Normal"

        patient_data = [
            ["Parameter",               "Recorded Value",    "Normal Range",      "Status"],
            ["Age",                     f"{age} years",      "18 – 35 yrs",       _status_text(age,      18,   35)],
            ["Systolic Blood Pressure", f"{systolic} mmHg",  "90 – 120 mmHg",     _status_text(systolic, 90,  120)],
            ["Diastolic Blood Pressure",f"{diastolic} mmHg", "60 – 80 mmHg",      _status_text(diastolic,60,   80)],
            ["Blood Sugar Level",       f"{bs:.1f} mmol/L",  "4.0 – 7.0 mmol/L",  _status_text(bs,       4.0,  7.0)],
            ["Body Temperature",        f"{temp:.1f} °C",    "36.5 – 37.5 °C",    _status_text(temp,     36.5,37.5)],
            ["Heart Rate",              f"{hr} bpm",         "60 – 100 bpm",       _status_text(hr,       60,  100)],
        ]

        pt = Table(patient_data, colWidths=[2.3*inch, 1.6*inch, 1.65*inch, 1.25*inch])
        pt.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), colors.HexColor("#fff1f2")),
            ("TEXTCOLOR",     (0,0),(-1,0), colors.HexColor("#be123c")),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,0), 8.5),
            ("TOPPADDING",    (0,0),(-1,0), 7), ("BOTTOMPADDING",(0,0),(-1,0),7),
            ("FONTNAME",      (0,1),(-1,-1),"Helvetica"),
            ("FONTSIZE",      (0,1),(-1,-1), 8.5),
            ("TEXTCOLOR",     (0,1),(-1,-1), colors.HexColor("#1c1018")),
            ("TOPPADDING",    (0,1),(-1,-1), 5), ("BOTTOMPADDING",(0,1),(-1,-1),5),
            ("BACKGROUND",    (0,2),(-1,2),  colors.HexColor("#fdf2f5")),
            ("BACKGROUND",    (0,4),(-1,4),  colors.HexColor("#fdf2f5")),
            ("BACKGROUND",    (0,6),(-1,6),  colors.HexColor("#fdf2f5")),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.HexColor("#ecdde3")),
            ("ALIGN",         (1,0),(-1,-1), "CENTER"),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ]))
        story.append(pt)
        story.append(Spacer(1, 14))

        story.append(Paragraph("RISK PREDICTION RESULT", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#ecdde3"), spaceAfter=8))

        r_color_map = {"low":"#14532d","mid":"#78350f","high":"#881337"}
        r_bg_map    = {"low":"#f0fdf4","mid":"#fffbeb","high":"#fff1f2"}
        r_color = r_color_map.get(r_key,"#881337")
        r_bg    = r_bg_map.get(r_key,"#fff1f2")

        rt = Table(
            [["Predicted Risk Level","Model Confidence","Confidence Label"],
             [risk.title(), f"{confidence:.1f}%", confidence_level]],
            colWidths=[2.3*inch, 2.3*inch, 2.3*inch]
        )
        rt.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), colors.HexColor("#fff1f2")),
            ("TEXTCOLOR",     (0,0),(-1,0), colors.HexColor("#9f1239")),
            ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0),(-1,0), 9),
            ("ALIGN",         (0,0),(-1,-1),"CENTER"),
            ("VALIGN",        (0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",    (0,0),(-1,-1), 9), ("BOTTOMPADDING",(0,0),(-1,-1),9),
            ("BACKGROUND",    (0,1),(-1,1),  colors.HexColor(r_bg)),
            ("TEXTCOLOR",     (0,1),(-1,1),  colors.HexColor(r_color)),
            ("FONTNAME",      (0,1),(-1,1),  "Helvetica-Bold"),
            ("FONTSIZE",      (0,1),(-1,1),  13),
            ("GRID",          (0,0),(-1,-1), 0.5, colors.HexColor("#ecdde3")),
            ("TOPPADDING",    (0,1),(-1,1),  12), ("BOTTOMPADDING",(0,1),(-1,1),12),
        ]))
        story.append(rt)
        story.append(Spacer(1, 14))

        story.append(Paragraph("CLINICAL INTERPRETATION", section_heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#ecdde3"), spaceAfter=8))
        interp_map = {
            "low":  ("The patient's vitals are within or close to the normal ranges for maternal health indicators. "
                     "The AI model classifies this case as <b>Low Risk</b>. Routine prenatal care and regular monitoring "
                     "are recommended. The patient should maintain a balanced diet, appropriate physical activity, and "
                     "attend all scheduled antenatal appointments."),
            "mid":  ("One or more of the patient's measured parameters fall outside the ideal reference range. "
                     "The AI model classifies this case as <b>Moderate Risk</b>. A prompt follow-up with the obstetric "
                     "care team is advised to assess potential complications. Lifestyle modifications and closer monitoring "
                     "frequency may be warranted."),
            "high": ("The patient's vitals indicate significant deviations from normal maternal health parameters. "
                     "The AI model classifies this case as <b>High Risk</b>. Immediate consultation with an obstetrician "
                     "or maternal-fetal medicine specialist is strongly recommended. Hospitalisation, medical intervention, "
                     "or intensified monitoring may be necessary to safeguard both maternal and fetal wellbeing."),
        }
        story.append(Paragraph(interp_map.get(r_key,""), body_style))
        story.append(Spacer(1, 10))

        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#ecdde3"), spaceAfter=6))
        story.append(Paragraph(
            "⚠  Disclaimer: This report is generated by an AI-based predictive model and is intended solely "
            "as a clinical decision-support tool. It does not constitute a medical diagnosis. All findings should "
            "be reviewed and validated by a qualified healthcare professional before any clinical action is taken.",
            caption_style
        ))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#fecdd3"), spaceAfter=5))
        story.append(Paragraph(
            "Maternal Health Risk Prediction System  ·  AI Clinical Assessment  ·  Confidential",
            ParagraphStyle("Footer", fontName="Helvetica", fontSize=7.5,
                           textColor=colors.HexColor("#9d6b7e"), alignment=TA_CENTER)
        ))

        doc.build(story)
        return file_name

    pdf_file = generate_pdf()

    st.markdown("""
    <div class="report-card">
        <p style="font-size:1rem;color:#5c4a52;margin:0 0 1.1rem;line-height:1.7;">
            A structured clinical PDF report has been generated based on the assessed parameters
            and predicted risk level. Download it for your records or to share with a healthcare provider.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📥  Download Clinical Report (PDF)",
            data=f,
            file_name="Maternal_Risk_Report.pdf",
            mime="application/pdf"
        )

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