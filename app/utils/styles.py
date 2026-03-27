import streamlit as st


def inject_styles():
    """Injects the full premium CSS for the entire app."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

    :root {
        --rose-50:#fff1f3;--rose-100:#ffe4e9;--rose-200:#fecdd6;
        --rose-300:#fda4b5;--rose-400:#fb7185;--rose-500:#f43f5e;
        --rose-600:#e11d48;--rose-700:#be123c;
        --mauve:#9d6b7e;--mauve-lt:#e8d5dc;
        --sage-lt:#d9ede0;--amber-lt:#fef3c7;--purple-lt:#ede9fe;
        --ink:#18080f;--ink-soft:#5c4a52;--ink-muted:#9b8a92;
        --surface:#fdfafc;--border:#e8d8e0;--white:#ffffff;
        --sh-sm:0 2px 8px rgba(140,60,90,0.07);
        --sh-md:0 6px 24px rgba(140,60,90,0.11),0 2px 8px rgba(140,60,90,0.06);
        --sh-lg:0 16px 48px rgba(140,60,90,0.15),0 4px 16px rgba(140,60,90,0.09);
        --r:20px;--r-sm:12px;
    }
    html,body{font-size:17px!important;}
    .stApp,.stApp*{font-family:'DM Sans',sans-serif!important;}
    .stMarkdown p,div[data-testid="stMarkdownContainer"] p{font-size:1.05rem!important;line-height:1.78!important;}
    .stNumberInput input{font-size:1.05rem!important;}
    label[data-testid="stWidgetLabel"] p,.stNumberInput label{font-size:0.82rem!important;font-weight:700!important;color:var(--ink-soft)!important;letter-spacing:0.05em!important;text-transform:uppercase!important;}
    .stButton>button,.stDownloadButton>button{font-size:1rem!important;}
    p{font-size:1.05rem;line-height:1.78;}
    #MainMenu,footer,header{visibility:hidden;}
    .stCustomComponentV1,.stCustomComponentV1>div,.stCustomComponentV1 iframe{background:transparent!important;background-color:transparent!important;}
    iframe{background-color:transparent!important;}
    @keyframes gradientBreath{0%{background-position:0% 50%;}33%{background-position:100% 50%;}66%{background-position:50% 100%;}100%{background-position:0% 50%;}}
    .stApp{background:linear-gradient(-45deg,#fdf0f4,#fff0f6,#fce8f5,#f5eeff,#ede8fe,#fce4f0,#fff1f3);background-size:600% 600%;animation:gradientBreath 24s ease infinite;min-height:100vh;position:relative;overflow-x:hidden;}
    .stApp::before{content:'';position:fixed;top:-120px;left:-160px;width:520px;height:520px;background:radial-gradient(circle,rgba(244,63,94,0.12) 0%,transparent 70%);border-radius:50%;pointer-events:none;z-index:0;filter:blur(40px);}
    .stApp::after{content:'';position:fixed;bottom:-100px;right:-140px;width:560px;height:560px;background:radial-gradient(circle,rgba(139,92,246,0.10) 0%,transparent 70%);border-radius:50%;pointer-events:none;z-index:0;filter:blur(50px);}
    .block-container{padding:0 3rem 6rem 3rem!important;max-width:1160px!important;margin-left:auto!important;margin-right:auto!important;position:relative;z-index:1;}
    @keyframes slideUp{from{opacity:0;transform:translateY(22px);}to{opacity:1;transform:translateY(0);}}
    @keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
    .hero-wrap{text-align:center;padding:4rem 1rem 2.5rem;width:100%;display:flex;flex-direction:column;align-items:center;animation:fadeIn 0.8s ease both;position:relative;}
    .hero-wrap::before,.hero-wrap::after{content:'✦';position:absolute;top:50%;font-size:1.4rem;color:var(--rose-300);opacity:0.5;transform:translateY(-50%);}
    .hero-wrap::before{left:0;}.hero-wrap::after{right:0;}
    .hero-title{font-family:'Playfair Display',serif!important;font-size:clamp(2.6rem,5.5vw,4rem)!important;font-weight:900!important;color:var(--ink)!important;line-height:1.12!important;margin:0 auto 1.1rem!important;max-width:780px!important;text-align:center!important;letter-spacing:-0.01em!important;}
    .hero-title em{font-style:italic!important;font-weight:700!important;background:linear-gradient(135deg,var(--rose-500),var(--rose-700));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
    .hero-sub{font-size:1.1rem!important;color:var(--ink-soft);font-weight:300;max-width:620px;margin:0 auto 1.8rem;line-height:1.75;text-align:center;}
    .section-wrap{position:relative;margin-top:2.4rem;margin-bottom:1rem;}
    .section-label{display:flex;align-items:center;gap:12px;}
    .section-label-icon{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;box-shadow:var(--sh-sm);}
    .icon-rose{background:linear-gradient(135deg,#fff0f2,#ffd6de);border:1px solid var(--rose-200);}
    .icon-sage{background:linear-gradient(135deg,#f0fdf4,#d9ede0);border:1px solid #bbf7d0;}
    .icon-amber{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1px solid #fde68a;}
    .icon-purple{background:linear-gradient(135deg,#faf5ff,#ede9fe);border:1px solid #ddd6fe;}
    .section-label-text{font-family:'Playfair Display',serif!important;font-size:1.4rem!important;color:var(--ink);font-weight:700;}
    .section-rule{height:1px;background:linear-gradient(90deg,var(--border),transparent);margin-top:0.7rem;margin-bottom:1rem;}
    .card{background:rgba(255,255,255,0.82);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.95);border-radius:var(--r);padding:2rem 2.4rem;box-shadow:var(--sh-md);margin-bottom:1.4rem;transition:box-shadow 0.3s ease,transform 0.25s ease;width:100%;max-width:100%;box-sizing:border-box;}
    .card:hover{box-shadow:var(--sh-lg);transform:translateY(-2px);}
    .stNumberInput div[data-testid="InputInstructions"],.stNumberInput>div>div>div>small,div[data-testid="stNumberInput"] small,div[data-testid="stNumberInputContainer"]~small,.stNumberInput small{display:none!important;visibility:hidden!important;height:0!important;margin:0!important;padding:0!important;}
    [data-testid="stHorizontalBlock"]{background:rgba(255,255,255,0.82)!important;backdrop-filter:blur(10px)!important;border:1px solid rgba(255,255,255,0.95)!important;border-radius:var(--r)!important;padding:2rem 2rem 1rem!important;box-shadow:var(--sh-md)!important;margin-bottom:1.4rem!important;transition:box-shadow 0.3s ease!important;}
    [data-testid="stHorizontalBlock"]:hover{box-shadow:var(--sh-lg)!important;}
    [data-testid="column"]{gap:0!important;}
    [data-testid="stHorizontalBlock"]:has(.risk-card){align-items:stretch!important;}
    .stNumberInput>div>div>input{border:1.5px solid var(--border)!important;border-radius:var(--r-sm)!important;background:rgba(253,250,252,0.9)!important;color:var(--ink)!important;font-size:1.05rem!important;padding:0.65rem 1rem!important;transition:border-color 0.2s,box-shadow 0.2s!important;}
    .stNumberInput>div>div>input:focus{border-color:var(--rose-400)!important;box-shadow:0 0 0 3px rgba(244,63,94,0.10)!important;outline:none!important;background:#fff!important;}
    .range-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0.9rem;}
    .range-pill{background:rgba(253,250,252,0.9);border:1px solid var(--border);border-radius:var(--r-sm);padding:1rem 1.2rem;display:flex;flex-direction:column;gap:4px;transition:border-color 0.2s,transform 0.2s;}
    .range-pill:hover{border-color:var(--rose-300);transform:translateY(-1px);}
    .range-pill-label{font-size:0.72rem;font-weight:700;color:var(--mauve);letter-spacing:0.09em;text-transform:uppercase;}
    .range-pill-value{font-size:1rem;color:var(--ink);font-weight:400;}
    .param-card{border-radius:var(--r-sm);padding:1.1rem 1.3rem;display:flex;flex-direction:column;gap:6px;animation:slideUp 0.35s ease both;margin-bottom:0.8rem;transition:transform 0.2s;}
    .param-card:hover{transform:translateY(-2px);}
    .param-card.normal{background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1.5px solid #a7f3d0;}
    .param-card.above{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1.5px solid #fcd34d;}
    .param-card.high{background:linear-gradient(135deg,#fff1f2,#ffe4e6);border:1.5px solid #fca5a5;}
    .param-card.below{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1.5px solid #93c5fd;}
    .param-name{font-size:0.73rem;font-weight:700;letter-spacing:0.09em;text-transform:uppercase;color:var(--ink-soft);}
    .param-value{font-family:'Playfair Display',serif!important;font-size:1.3rem;font-weight:700;}
    .param-card.normal .param-value{color:#14532d;}.param-card.above .param-value{color:#92400e;}.param-card.high .param-value{color:#881337;}.param-card.below .param-value{color:#1e40af;}
    .param-status{font-size:0.77rem;font-weight:700;border-radius:100px;padding:3px 11px;display:inline-block;width:fit-content;}
    .param-card.normal .param-status{background:#dcfce7;color:#15803d;}.param-card.above .param-status{background:#fef3c7;color:#92400e;}.param-card.high .param-status{background:#ffe4e6;color:#9f1239;}.param-card.below .param-status{background:#dbeafe;color:#1d4ed8;}
    .stButton>button{background:linear-gradient(135deg,#f43f5e 0%,#be123c 100%)!important;color:white!important;border:none!important;border-radius:100px!important;padding:0.85rem 3rem!important;font-size:1.05rem!important;font-weight:600!important;letter-spacing:0.03em!important;box-shadow:0 6px 24px rgba(225,29,72,0.35)!important;transition:all 0.25s ease!important;width:100%!important;height:3.5rem!important;}
    .stButton>button:hover{transform:translateY(-3px)!important;box-shadow:0 10px 32px rgba(225,29,72,0.42)!important;}
    .stButton>button:active{transform:translateY(0)!important;}
    .risk-card{border-radius:var(--r);padding:2.2rem 2.4rem;display:flex;align-items:flex-start;gap:1.6rem;flex-wrap:wrap;box-shadow:var(--sh-md);animation:slideUp 0.4s ease both;width:100%;box-sizing:border-box;height:100%;}
    .risk-icon{font-size:3rem;line-height:1;flex-shrink:0;margin-top:3px;}
    .risk-badge{font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;border-radius:100px;padding:4px 13px;display:inline-block;margin-bottom:7px;}
    .risk-level-text{font-family:'Playfair Display',serif!important;font-size:2rem!important;font-weight:800!important;line-height:1.1;margin:3px 0 10px;}
    .risk-note{font-size:0.96rem;line-height:1.65;font-weight:300;margin:0;}
    .risk-low{background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1.5px solid #a7f3d0;}
    .risk-low .risk-badge{background:#dcfce7;color:#15803d;}.risk-low .risk-level-text{color:#14532d;}.risk-low .risk-note{color:#166534;}
    .risk-mid{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1.5px solid #fcd34d;}
    .risk-mid .risk-badge{background:#fef3c7;color:#92400e;}.risk-mid .risk-level-text{color:#78350f;}.risk-mid .risk-note{color:#92400e;}
    .risk-high{background:linear-gradient(135deg,#fff1f2,#ffe4e6);border:1.5px solid #fca5a5;}
    .risk-high .risk-badge{background:#ffe4e6;color:#9f1239;}.risk-high .risk-level-text{color:#881337;}.risk-high .risk-note{color:#9f1239;}
    .conf-wrap{background:rgba(255,255,255,0.88);backdrop-filter:blur(10px);border:1px solid var(--border);border-radius:var(--r);padding:2rem;box-shadow:var(--sh-md);animation:slideUp 0.45s ease 0.1s both;height:100%;min-height:220px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;}
    .conf-top{flex:1;}
    .conf-label-row{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1rem;}
    .conf-title{font-size:0.78rem;font-weight:700;color:var(--mauve);letter-spacing:0.10em;text-transform:uppercase;}
    .conf-pct{font-family:'Playfair Display',serif!important;font-size:1.8rem!important;font-weight:800!important;color:var(--ink);}
    .conf-bar-bg{height:11px;background:var(--rose-100);border-radius:100px;overflow:hidden;margin-bottom:0.9rem;}
    .conf-bar-fill{height:100%;border-radius:100px;transition:width 1.3s cubic-bezier(0.25,0.46,0.45,0.94);}
    .conf-fill-high{background:linear-gradient(90deg,#4ade80,#16a34a);}
    .conf-fill-mid{background:linear-gradient(90deg,#fbbf24,#d97706);}
    .conf-fill-low{background:linear-gradient(90deg,#fb7185,#e11d48);}
    .conf-level-badge{display:inline-block;font-size:0.78rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;border-radius:100px;padding:4px 15px;margin-bottom:0.9rem;}
    .badge-high{background:#dcfce7;color:#15803d;}.badge-mid{background:#fef3c7;color:#92400e;}.badge-low{background:#ffe4e6;color:#9f1239;}
    .conf-note{font-size:0.86rem;color:var(--ink-soft);line-height:1.6;margin:0;}
    .summary-card{background:linear-gradient(135deg,rgba(253,244,255,0.92),rgba(252,231,243,0.92));backdrop-filter:blur(8px);border:1px solid #e9d5f5;border-radius:var(--r);padding:2.2rem 2.6rem;box-shadow:var(--sh-sm);animation:slideUp 0.45s ease 0.15s both;margin-bottom:1.4rem;position:relative;overflow:hidden;}
    .summary-card::before{content:'"';position:absolute;top:-10px;left:20px;font-size:8rem;color:rgba(167,139,250,0.12);font-family:'Playfair Display',serif;line-height:1;pointer-events:none;}
    .summary-label{font-size:0.76rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#7c3aed;margin-bottom:0.9rem;display:flex;align-items:center;gap:7px;}
    .summary-text{font-size:1rem;line-height:1.8;color:var(--ink);font-weight:300;position:relative;z-index:1;}
    .summary-text strong{font-weight:600;color:var(--ink);}
    .rec-card{border-radius:var(--r);padding:2.2rem 2.6rem;box-shadow:var(--sh-md);animation:slideUp 0.4s ease both;margin-bottom:1.4rem;box-sizing:border-box;position:relative;overflow:hidden;}
    .rec-low{background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1.5px solid #a7f3d0;}
    .rec-mid{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1.5px solid #fcd34d;}
    .rec-high{background:linear-gradient(135deg,#fff1f2,#ffe4e6);border:1.5px solid #fca5a5;}
    .rec-urgency{font-family:'Playfair Display',serif!important;font-size:1.35rem!important;font-weight:800!important;margin-bottom:0.7rem;}
    .rec-low .rec-urgency{color:#14532d;}.rec-mid .rec-urgency{color:#78350f;}.rec-high .rec-urgency{color:#881337;}
    .rec-text{font-size:0.98rem;line-height:1.7;font-weight:300;margin:0 0 1rem;}
    .rec-low .rec-text{color:#166534;}.rec-mid .rec-text{color:#92400e;}.rec-high .rec-text{color:#9f1239;}
    .rec-conf{font-size:0.85rem;color:var(--ink-soft);}.rec-conf strong{font-weight:600;color:var(--ink);}
    .clinical-score-wrap{background:rgba(255,255,255,0.88);border:1px solid var(--border);border-radius:var(--r);padding:1.8rem 2.2rem;box-shadow:var(--sh-md);animation:slideUp 0.4s ease both;margin-bottom:1.4rem;}
    .score-row{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;}
    .score-number{font-family:'Playfair Display',serif!important;font-size:3rem!important;font-weight:900!important;line-height:1;}
    .score-low{color:#14532d;}.score-mid{color:#78350f;}.score-high{color:#881337;}
    .score-breakdown{flex:1;min-width:200px;display:flex;flex-direction:column;gap:6px;}
    .score-item{display:flex;align-items:center;gap:10px;font-size:0.9rem;color:var(--ink-soft);}
    .score-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
    .score-dot.active{background:#e11d48;}.score-dot.inactive{background:#d1d5db;}
    .adjustment-badge{display:inline-flex;align-items:center;gap:6px;font-size:0.78rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;border-radius:100px;padding:5px 14px;margin-top:0.6rem;}
    .adj-upgraded{background:#fef3c7;color:#92400e;border:1px solid #fcd34d;}
    .adj-escalated{background:#ffe4e6;color:#9f1239;border:1px solid #fca5a5;}
    .adj-unchanged{background:#dcfce7;color:#15803d;border:1px solid #a7f3d0;}
    .projection-card{background:linear-gradient(135deg,rgba(239,246,255,0.92),rgba(219,234,254,0.92));border:1.5px solid #93c5fd;border-radius:var(--r);padding:2rem 2.4rem;box-shadow:var(--sh-sm);animation:slideUp 0.4s ease both;margin-bottom:1.4rem;}
    .proj-label{font-size:0.75rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#1d4ed8;margin-bottom:0.8rem;}
    .proj-row{display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap;}
    .proj-arrow{font-size:1.4rem;color:#3b82f6;}
    .proj-item{display:flex;flex-direction:column;gap:3px;}
    .proj-item-label{font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6b7280;}
    .proj-item-value{font-family:'Playfair Display',serif!important;font-size:1.2rem!important;font-weight:700!important;color:#1e40af;}
    .proj-note{font-size:0.85rem;color:#3b82f6;margin-top:0.9rem;line-height:1.6;font-style:italic;}
    .transparency-card{background:linear-gradient(135deg,rgba(245,243,255,0.92),rgba(237,233,254,0.92));border:1.5px solid #c4b5fd;border-radius:var(--r);padding:2.2rem 2.6rem;box-shadow:var(--sh-sm);animation:slideUp 0.4s ease both;margin-bottom:1.4rem;}
    .trans-label{font-size:0.75rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#6d28d9;margin-bottom:1rem;}
    .trans-flow{display:flex;align-items:center;gap:0.8rem;flex-wrap:wrap;margin:1rem 0;}
    .trans-node{background:white;border:1.5px solid #c4b5fd;border-radius:var(--r-sm);padding:0.6rem 1rem;font-size:0.84rem;font-weight:600;color:#4c1d95;text-align:center;}
    .trans-arrow{font-size:1rem;color:#8b5cf6;font-weight:700;}
    .trans-text{font-size:0.95rem;line-height:1.75;color:var(--ink-soft);font-weight:300;}
    .trans-text strong{font-weight:600;color:var(--ink);}
    .stSelectbox>div>div{border:1.5px solid var(--border)!important;border-radius:var(--r-sm)!important;background:rgba(253,250,252,0.9)!important;font-size:1rem!important;transition:border-color 0.2s!important;}
    .stSelectbox>div>div:focus-within{border-color:var(--rose-400)!important;box-shadow:0 0 0 3px rgba(244,63,94,0.10)!important;}
    .stSelectbox label{font-size:0.82rem!important;font-weight:700!important;color:var(--ink-soft)!important;letter-spacing:0.05em!important;text-transform:uppercase!important;}
    .report-card{background:rgba(255,255,255,0.85);border:1px solid var(--border);border-radius:var(--r);padding:2rem 2.4rem;box-shadow:var(--sh-md);margin-bottom:1.4rem;}
    .timestamp-row{display:flex;align-items:center;gap:8px;color:var(--ink-muted);font-size:0.85rem;margin-top:0.6rem;padding:0.6rem 1rem;background:rgba(255,255,255,0.6);border-radius:100px;width:fit-content;animation:slideUp 0.45s ease 0.2s both;border:1px solid rgba(255,255,255,0.9);}
    .stDownloadButton>button{background:white!important;color:var(--rose-600)!important;border:2px solid var(--rose-300)!important;border-radius:100px!important;padding:0.75rem 2.4rem!important;font-size:1rem!important;font-weight:600!important;transition:all 0.25s ease!important;width:100%!important;box-shadow:var(--sh-sm)!important;}
    .stDownloadButton>button:hover{background:var(--rose-50)!important;border-color:var(--rose-400)!important;box-shadow:0 6px 20px rgba(225,29,72,0.18)!important;transform:translateY(-2px)!important;}
    .kpi-card{background:rgba(255,255,255,0.88);backdrop-filter:blur(10px);border:1px solid var(--border);border-radius:var(--r);padding:1.6rem 1.8rem;box-shadow:var(--sh-md);animation:slideUp 0.4s ease both;text-align:center;transition:transform 0.2s,box-shadow 0.2s;}
    .kpi-card:hover{transform:translateY(-3px);box-shadow:var(--sh-lg);}
    .kpi-icon{font-size:1.8rem;margin-bottom:0.5rem;}
    .kpi-value{font-family:'Playfair Display',serif!important;font-size:2.2rem!important;font-weight:900!important;color:var(--rose-600);line-height:1;}
    .kpi-label{font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:var(--ink-muted);margin-top:0.4rem;}
    .alert-banner{display:flex;align-items:flex-start;gap:12px;padding:1rem 1.4rem;border-radius:var(--r-sm);margin-bottom:0.7rem;animation:slideUp 0.3s ease both;}
    .alert-critical{background:#fff1f2;border:1.5px solid #fca5a5;}
    .alert-warning{background:#fffbeb;border:1.5px solid #fcd34d;}
    .alert-info{background:#eff6ff;border:1.5px solid #93c5fd;}
    .alert-icon{font-size:1.1rem;flex-shrink:0;margin-top:1px;}
    .alert-text{font-size:0.92rem;line-height:1.55;}
    .alert-critical .alert-text{color:#9f1239;}.alert-warning .alert-text{color:#92400e;}.alert-info .alert-text{color:#1d4ed8;}
    .case-summary{background:linear-gradient(135deg,rgba(255,241,242,0.92),rgba(255,228,230,0.92));border:1.5px solid #fda4b5;border-radius:var(--r);padding:1.6rem 2rem;box-shadow:var(--sh-sm);margin-bottom:1.4rem;display:flex;align-items:center;flex-wrap:wrap;gap:1.2rem;animation:slideUp 0.35s ease both;}
    .case-chip{background:white;border:1px solid #fecdd6;border-radius:100px;padding:4px 14px;font-size:0.82rem;font-weight:600;color:var(--rose-700);}
    .insight-card{background:linear-gradient(135deg,rgba(250,245,255,0.92),rgba(237,233,254,0.92));border:1px solid #c4b5fd;border-radius:var(--r-sm);padding:1rem 1.4rem;margin-bottom:0.7rem;display:flex;align-items:flex-start;gap:10px;animation:slideUp 0.35s ease both;}
    .insight-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;margin-top:5px;}
    .insight-text{font-size:0.94rem;color:#4c1d95;line-height:1.6;}
    .transition-card{background:linear-gradient(135deg,rgba(255,251,235,0.92),rgba(254,243,199,0.92));border:1.5px solid #fcd34d;border-radius:var(--r);padding:1.6rem 2rem;margin-bottom:1.4rem;}
    .app-footer{text-align:center;padding:3rem 1rem 2rem;color:var(--mauve);font-size:0.84rem;letter-spacing:0.03em;line-height:2;border-top:1px solid var(--mauve-lt);margin-top:2rem;}
    @media(max-width:768px){.range-grid{grid-template-columns:repeat(2,1fr);}.hero-title{font-size:2.2rem!important;}.block-container{padding:0 1rem 3rem!important;}.hero-wrap::before,.hero-wrap::after{display:none;}}
    /* ── NAV BUTTON — never wrap text ── */
    [data-testid="stHorizontalBlock"] .stButton > button {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        padding: 0.6rem 1rem !important;
        height: 2.8rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        border-radius: 100px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* ── IMAGE INSIGHT CARDS ── */
    .insight-img-card {
        background: rgba(255,255,255,0.88);
        border: 1px solid var(--border);
        border-radius: var(--r);
        padding: 1rem;
        box-shadow: var(--sh-md);
        margin-bottom: 0.6rem;
        transition: box-shadow 0.25s ease, transform 0.2s ease;
    }
    .insight-img-card:hover {
        box-shadow: var(--sh-lg);
        transform: translateY(-2px);
    }
    .insight-img-caption {
        text-align: center;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: var(--ink-muted);
        margin-top: 0.6rem;
        margin-bottom: 0.8rem;
    }

    /* Override Streamlit's image container inside our card ── */
    .insight-img-card [data-testid="stImage"],
    .insight-img-card img {
        border-radius: 12px;
        width: 100% !important;
    }

    </style>
    """, unsafe_allow_html=True)