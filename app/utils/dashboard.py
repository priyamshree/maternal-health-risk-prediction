"""
utils/dashboard.py
All dashboard analytics components: KPI cards, charts, insights, risk transitions.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_kpi_cards(history_df: pd.DataFrame, current_result: dict) -> None:
    """Render the 4 top KPI metric cards."""
    total_preds      = len(history_df)
    avg_confidence   = history_df["confidence"].mean() if total_preds else 0
    avg_clin_score   = history_df["clinical_score"].mean() if total_preds else 0
    most_common_risk = (
        history_df["risk"].mode()[0] if total_preds else current_result.get("risk", "—")
    )

    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-sage">📊</div>
            <span class="section-label-text">Session Analytics</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🔢</div>
            <div class="kpi-value">{total_preds}</div>
            <div class="kpi-label">Total Predictions</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🎯</div>
            <div class="kpi-value">{avg_confidence:.1f}%</div>
            <div class="kpi-label">Avg Confidence</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚖️</div>
            <div class="kpi-value">{avg_clin_score:.1f}</div>
            <div class="kpi-label">Avg Clinical Score</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        risk_icon_map = {"low risk": "💚", "mid risk": "🟡", "high risk": "🔴"}
        mc_icon = risk_icon_map.get(most_common_risk.lower(), "🔵")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{mc_icon}</div>
            <div class="kpi-value" style="font-size:1.3rem!important;">
                {most_common_risk.title()}
            </div>
            <div class="kpi-label">Most Common Risk</div>
        </div>
        """, unsafe_allow_html=True)


def render_charts(history_df: pd.DataFrame) -> None:
    """Render all 4 analytics charts in a 2×2 grid."""
    total_preds = len(history_df)
    if total_preds < 1:
        return

    color_map = {
        "Low Risk":  "#16a34a", "low risk":  "#16a34a",
        "Mid Risk":  "#d97706", "mid risk":  "#d97706",
        "High Risk": "#e11d48", "high risk": "#e11d48",
    }

    # ── Row 1 ──
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown("""
        <div class="section-wrap" style="margin-top:0;">
            <div class="section-label">
                <div class="section-label-icon icon-rose">🧾</div>
                <span class="section-label-text">Risk Distribution</span>
            </div>
            <div class="section-rule"></div>
        </div>
        """, unsafe_allow_html=True)
        risk_counts = history_df["risk"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Count"]
        risk_counts["Percentage"] = (risk_counts["Count"] / total_preds * 100).round(1)
        risk_counts["Label"] = risk_counts.apply(
            lambda x: f"{x['Count']} ({x['Percentage']}%)", axis=1
        )
        fig = px.bar(
            risk_counts, x="Risk Level", y="Count",
            text="Label", color="Risk Level",
            color_discrete_map=color_map
        )
        fig.update_traces(textposition="outside", marker_line_width=0, textfont=dict(size=13))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(t=10,b=10,l=0,r=0), height=300,
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="#f3e8ec", title="Count"),
            font=dict(family="DM Sans", size=13, color="#5c4a52"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("""
        <div class="section-wrap" style="margin-top:0;">
            <div class="section-label">
                <div class="section-label-icon icon-purple">📈</div>
                <span class="section-label-text">Confidence Over Time</span>
            </div>
            <div class="section-rule"></div>
        </div>
        """, unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            y=history_df["confidence"], mode="lines+markers",
            line=dict(color="#e11d48", width=2.5),
            marker=dict(size=8, color="#e11d48"),
            fill="tozeroy", fillcolor="rgba(225,29,72,0.07)",
            name="Confidence %"
        ))
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(t=10,b=10,l=0,r=0), height=300,
            xaxis=dict(showgrid=False, title="Prediction #"),
            yaxis=dict(showgrid=True, gridcolor="#f3e8ec", title="Confidence %", range=[0,105]),
            font=dict(family="DM Sans", size=13, color="#5c4a52"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Row 2 ──
    c3, c4 = st.columns(2, gap="large")

    with c3:
        st.markdown("""
        <div class="section-wrap" style="margin-top:0;">
            <div class="section-label">
                <div class="section-label-icon icon-amber">⚖️</div>
                <span class="section-label-text">Clinical Score Trend</span>
            </div>
            <div class="section-rule"></div>
        </div>
        """, unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            y=history_df["clinical_score"], mode="lines+markers",
            line=dict(color="#d97706", width=2.5),
            marker=dict(size=8, color="#d97706"),
            fill="tozeroy", fillcolor="rgba(217,119,6,0.08)",
            name="Clinical Score"
        ))
        fig3.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(t=10,b=10,l=0,r=0), height=300,
            xaxis=dict(showgrid=False, title="Prediction #"),
            yaxis=dict(showgrid=True, gridcolor="#f3e8ec", title="Clinical Score", range=[0,12]),
            font=dict(family="DM Sans", size=13, color="#5c4a52"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown("""
        <div class="section-wrap" style="margin-top:0;">
            <div class="section-label">
                <div class="section-label-icon icon-sage">🍩</div>
                <span class="section-label-text">Risk Composition</span>
            </div>
            <div class="section-rule"></div>
        </div>
        """, unsafe_allow_html=True)
        rc2 = history_df["risk"].value_counts()
        pie_colors = [
            "#16a34a" if "low" in k.lower() else
            "#d97706" if "mid" in k.lower() else "#e11d48"
            for k in rc2.index
        ]
        fig4 = go.Figure(go.Pie(
            labels=rc2.index, values=rc2.values, hole=0.55,
            marker_colors=pie_colors,
            textinfo="percent+label", textfont=dict(size=13, family="DM Sans"),
        ))
        fig4.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(t=10,b=10,l=0,r=0), height=300,
            font=dict(family="DM Sans", size=13, color="#5c4a52"),
        )
        st.plotly_chart(fig4, use_container_width=True)


def render_smart_insights(history_df: pd.DataFrame, current_result: dict) -> None:
    """Generate and render the Smart Insights Engine."""
    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-purple">🧠</div>
            <span class="section-label-text">Smart Insights</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    insights = []
    total    = len(history_df)

    if total > 0:
        risk_pcts = (history_df["risk"].value_counts(normalize=True) * 100).round(1)
        for risk_lvl, pct in risk_pcts.items():
            if pct >= 50:
                insights.append((
                    f"Majority of cases ({pct:.0f}%) fall under <strong>{risk_lvl.title()}</strong> — review care protocols accordingly.",
                    "#7c3aed"
                ))
        if total >= 3:
            recent_conf = history_df["confidence"].tail(3).tolist()
            if recent_conf[-1] < recent_conf[0] - 5:
                insights.append(("⬇️ Model confidence is <strong>declining</strong> — parameter variability may be increasing.", "#92400e"))
            elif recent_conf[-1] > recent_conf[0] + 5:
                insights.append(("⬆️ Model confidence is <strong>improving</strong> — recent vitals are more decisive.", "#15803d"))

            recent_scores = history_df["clinical_score"].tail(3).tolist()
            if all(recent_scores[i] <= recent_scores[i+1] for i in range(len(recent_scores)-1)):
                insights.append(("📈 Clinical score trend is <strong>increasing</strong> — potential deterioration. Closer monitoring recommended.", "#9f1239"))
            elif all(recent_scores[i] >= recent_scores[i+1] for i in range(len(recent_scores)-1)):
                insights.append(("📉 Clinical score trend is <strong>decreasing</strong> — clinical context appears to be improving.", "#14532d"))

        if total >= 2:
            recent_risks = history_df["risk"].tail(3).str.lower().tolist()
            if recent_risks.count("high risk") >= 2:
                insights.append(("🚨 <strong>High-risk cases are recurring</strong> — systemic review recommended.", "#9f1239"))

        adj = current_result.get("adjustment_made", "unchanged")
        if adj == "escalated":
            insights.append(("⚠️ The latest case was <strong>escalated by clinical context</strong> — ML prediction alone underestimated patient risk.", "#92400e"))
        elif adj == "upgraded":
            insights.append(("📋 Clinical history <strong>upgraded</strong> the latest case from Low to Moderate Risk.", "#92400e"))

    if not insights:
        insights.append(("✅ Insufficient data for trend analysis. Run more predictions to generate meaningful insights.", "#6b7280"))

    palette = ["#8b5cf6","#ec4899","#3b82f6","#10b981","#f59e0b"]
    for i, (text, _) in enumerate(insights):
        dot_color = palette[i % len(palette)]
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-dot" style="background:{dot_color};"></div>
            <span class="insight-text">{text}</span>
        </div>
        """, unsafe_allow_html=True)


def render_risk_transitions(history_df: pd.DataFrame) -> None:
    """Detect and display risk level transitions across predictions."""
    if len(history_df) < 2:
        return

    st.markdown("""
    <div class="section-wrap">
        <div class="section-label">
            <div class="section-label-icon icon-amber">🔄</div>
            <span class="section-label-text">Risk Transition Tracking</span>
        </div>
        <div class="section-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    risk_order  = {"low risk": 0, "mid risk": 1, "high risk": 2}
    risks_list  = history_df["risk"].str.lower().tolist()
    transitions = []
    for i in range(1, len(risks_list)):
        prev = risks_list[i-1]; curr = risks_list[i]
        if prev != curr:
            icon = "⬆️" if risk_order.get(curr, 1) > risk_order.get(prev, 1) else "⬇️"
            transitions.append((i, prev.title(), curr.title(), icon))

    if transitions:
        rows_html = ""
        for idx, frm, to, icon in transitions[-5:]:
            rows_html += f"""
            <div style="display:flex;align-items:center;gap:12px;padding:10px 0;
                        border-bottom:1px solid #fde68a;font-family:'DM Sans',sans-serif;">
                <span style="font-size:0.75rem;font-weight:700;color:#92400e;width:90px;">#{idx}→#{idx+1}</span>
                <span style="font-size:0.9rem;font-weight:600;color:#78350f;">{frm}</span>
                <span style="font-size:1.1rem;">{icon}</span>
                <span style="font-size:0.9rem;font-weight:600;color:#78350f;">{to}</span>
            </div>"""
        st.markdown(f"""
        <div class="transition-card">
            <div style="font-size:0.75rem;font-weight:700;letter-spacing:0.12em;
                        text-transform:uppercase;color:#92400e;margin-bottom:0.6rem;">
                🔄 &nbsp; Risk Level Transitions Detected
            </div>
            {rows_html}
            <p style="font-size:0.84rem;color:#92400e;margin-top:0.8rem;font-style:italic;">
                Risk transitions indicate changing patient condition and require clinical attention.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="transition-card">
            <p style="font-size:0.9rem;color:#92400e;margin:0;">
                ✅ No risk transitions detected — risk classification has remained consistent.
            </p>
        </div>
        """, unsafe_allow_html=True)