import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from data_utils import load_data

st.set_page_config(
    page_title="India College Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 13px; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; font-size: 26px; font-weight: 700; }
.page-title {
    font-size: 2rem; font-weight: 700;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.page-subtitle { color: #64748b; font-size: 0.95rem; margin-bottom: 24px; }
.section-header {
    color: #e2e8f0; font-size: 1.05rem; font-weight: 600;
    margin: 24px 0 12px 0; padding-left: 12px;
    border-left: 3px solid #6366f1;
}
.info-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155; border-radius: 12px;
    padding: 20px; margin: 8px 0;
}
h1, h2, h3, h4 { color: #e2e8f0; }
p, li { color: #94a3b8; }
.stTabs [data-baseweb="tab-list"] { background: #1e293b; border-radius: 8px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { color: #94a3b8; border-radius: 6px; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background: #6366f1; color: white; }
</style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,23,42,0.8)",
    font=dict(family="Inter", color="#94a3b8"),
    title_font=dict(color="#e2e8f0", size=15, family="Inter"),
    legend=dict(bgcolor="rgba(30,41,59,0.8)", bordercolor="#334155", borderwidth=1, font=dict(color="#e2e8f0")),
    xaxis=dict(gridcolor="#1e293b", zerolinecolor="#334155", tickfont=dict(color="#64748b")),
    yaxis=dict(gridcolor="#1e293b", zerolinecolor="#334155", tickfont=dict(color="#64748b")),
    margin=dict(l=40, r=20, t=50, b=40),
)

COLORS = ["#6366f1","#06b6d4","#10b981","#f59e0b","#f43f5e","#8b5cf6","#ec4899","#14b8a6","#f97316","#84cc16"]
TIER_COLORS = {"Tier 1": "#6366f1", "Tier 2": "#06b6d4", "Tier 3": "#10b981"}

def apply_layout(fig, extra=None):
    layout = dict(PLOTLY_LAYOUT)
    if extra:
        layout.update(extra)
    fig.update_layout(**layout)
    return fig

@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 College Analytics")
    st.markdown("---")
    page = st.selectbox("Navigate to Dashboard", [
        "🏆 Tier 1 College Dashboard",
        "🗺️ State-wise Distribution",
        "💼 Placement Analysis",
        "🤝 Recruiter Analytics",
        "⚖️ College Comparison",
        "💰 ROI Analysis"
    ])
    st.markdown("---")
    st.markdown("### Filters")
    sel_states = st.multiselect("States", sorted(df["State"].dropna().unique()))
    sel_cats   = st.multiselect("College Category", sorted(df["Category"].dropna().unique()))
    sel_own    = st.multiselect("Ownership Type", sorted(df["Ownership Type"].dropna().unique()))
    st.markdown("---")
    st.caption(f"📊 {len(df)} Colleges  |  🇮🇳 {df['State'].nunique()} States")

fdf = df.copy()
if sel_states: fdf = fdf[fdf["State"].isin(sel_states)]
if sel_cats:   fdf = fdf[fdf["Category"].isin(sel_cats)]
if sel_own:    fdf = fdf[fdf["Ownership Type"].isin(sel_own)]

def kpi(cols, values):
    for c, (label, val) in zip(cols, values):
        c.metric(label, val)

# ═══════════════════════════════════════════════════════════════
# PAGE 1 – TIER 1 COLLEGE DASHBOARD
# ═══════════════════════════════════════════════════════════════
if page == "🏆 Tier 1 College Dashboard":
    st.markdown('<p class="page-title">🏆 Tier 1 College Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Deep analysis of India\'s premier educational institutions</p>', unsafe_allow_html=True)

    t1 = fdf[fdf["Tier"] == "Tier 1"].copy()

    c1, c2, c3, c4 = st.columns(4)
    kpi([c1,c2,c3,c4], [
        ("Tier 1 Colleges", len(t1)),
        ("Avg Placement %", f"{t1['Placement %'].mean():.1f}%" if len(t1) else "N/A"),
        ("Avg Package (LPA)", f"₹{t1['Avg Pkg (LPA)'].mean():.1f}" if len(t1) else "N/A"),
        ("Avg NIRF Rank", f"{t1['NIRF Rank'].mean():.0f}" if len(t1) else "N/A"),
    ])

    if len(t1) == 0:
        st.info("No Tier 1 colleges match current filters.")
        st.stop()

    st.markdown('<p class="section-header">Placement % vs Average Package</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig = px.scatter(
            t1, x="Avg Pkg (LPA)", y="Placement %",
            size="Student Intake", color="Category",
            hover_name="College Name",
            color_discrete_sequence=COLORS,
            title="Package vs Placement (bubble = student intake)"
        )
        st.plotly_chart(apply_layout(fig), use_container_width=True)

    with c2:
        top15 = t1.sort_values("NIRF Rank").head(15)
        fig2 = px.bar(
            top15, x="College Name", y="Placement %",
            color="Category", color_discrete_sequence=COLORS,
            title="Placement % – Top Tier 1 Colleges"
        )
        fig2.update_xaxes(tickangle=45)
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    st.markdown('<p class="section-header">NIRF Rankings & Package Distribution</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        nirf_df = t1.dropna(subset=["NIRF Rank", "Avg Pkg (LPA)"])
        fig3 = px.scatter(
            nirf_df, x="NIRF Rank", y="Avg Pkg (LPA)",
            color="Category", hover_name="College Name",
            color_discrete_sequence=COLORS,
            title="NIRF Rank vs Avg Package"
        )
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

    with c4:
        fig4 = px.pie(
            t1, names="Category",
            color_discrete_sequence=COLORS,
            title="Category Breakdown – Tier 1"
        )
        fig4.update_traces(textfont_color="#e2e8f0")
        st.plotly_chart(apply_layout(fig4), use_container_width=True)

    st.markdown('<p class="section-header">Ownership & Location Analysis</p>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)

    with c5:
        own_df = t1.groupby("Ownership Type").agg(
            Count=("College Name","count"),
            Avg_Placement=("Placement %","mean"),
            Avg_Package=("Avg Pkg (LPA)","mean")
        ).reset_index()
        fig5 = px.bar(
            own_df, x="Ownership Type", y="Avg_Placement",
            color="Ownership Type", color_discrete_sequence=COLORS,
            title="Avg Placement % by Ownership Type",
            text="Count"
        )
        st.plotly_chart(apply_layout(fig5), use_container_width=True)

    with c6:
        loc_df = t1.groupby("Location Type")["Placement %"].mean().reset_index()
        fig6 = px.bar(
            loc_df, x="Location Type", y="Placement %",
            color="Location Type", color_discrete_sequence=COLORS,
            title="Avg Placement % by Location Type"
        )
        st.plotly_chart(apply_layout(fig6), use_container_width=True)

    st.markdown('<p class="section-header">Tier 1 College Details</p>', unsafe_allow_html=True)
    show = ["College Name","Category","State","NIRF Rank","NAAC/NBA Status",
            "Placement %","Avg Pkg","Highest Pkg","Student Intake","Ownership Type"]
    st.dataframe(t1[show].sort_values("NIRF Rank").reset_index(drop=True), use_container_width=True, height=400)


# ═══════════════════════════════════════════════════════════════
# PAGE 2 – STATE-WISE DISTRIBUTION
# ═══════════════════════════════════════════════════════════════
elif page == "🗺️ State-wise Distribution":
    st.markdown('<p class="page-title">🗺️ State-wise College Distribution</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Geographic spread of top colleges across India</p>', unsafe_allow_html=True)

    ss = fdf.groupby("State").agg(
        College_Count=("College Name","count"),
        Avg_Placement=("Placement %","mean"),
        Avg_Package=("Avg Pkg (LPA)","mean"),
        Total_Intake=("Student Intake","sum")
    ).reset_index().round(2)

    c1, c2, c3, c4 = st.columns(4)
    kpi([c1,c2,c3,c4], [
        ("States Covered", len(ss)),
        ("Total Colleges", len(fdf)),
        ("Best Avg Placement", f"{ss['Avg_Placement'].max():.1f}%" if len(ss) else "N/A"),
        ("Highest Avg Package", f"₹{ss['Avg_Package'].max():.1f} LPA" if len(ss) else "N/A"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            ss.sort_values("College_Count"),
            x="College_Count", y="State", orientation="h",
            color="College_Count", color_continuous_scale="Viridis",
            title="Number of Colleges per State"
        )
        st.plotly_chart(apply_layout(fig), use_container_width=True)

    with c2:
        fig2 = px.bar(
            ss.sort_values("Avg_Placement"),
            x="Avg_Placement", y="State", orientation="h",
            color="Avg_Placement", color_continuous_scale="Blues",
            title="Average Placement % by State"
        )
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    st.markdown('<p class="section-header">Package & Category Distribution</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        fig3 = px.bar(
            ss.sort_values("Avg_Package", ascending=False),
            x="State", y="Avg_Package",
            color="Avg_Package", color_continuous_scale="Purples",
            title="Average Package by State (LPA)"
        )
        fig3.update_xaxes(tickangle=45)
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

    with c4:
        cat_state = fdf.groupby(["State","Category"]).size().reset_index(name="Count")
        fig4 = px.bar(
            cat_state, x="State", y="Count", color="Category",
            color_discrete_sequence=COLORS,
            title="College Categories by State"
        )
        fig4.update_xaxes(tickangle=45)
        st.plotly_chart(apply_layout(fig4), use_container_width=True)

    st.markdown('<p class="section-header">Tier Distribution by State</p>', unsafe_allow_html=True)
    tier_state = fdf.groupby(["State","Tier"]).size().reset_index(name="Count")
    fig5 = px.bar(
        tier_state, x="State", y="Count", color="Tier",
        color_discrete_map=TIER_COLORS,
        title="Tier Distribution Across States"
    )
    fig5.update_xaxes(tickangle=45)
    st.plotly_chart(apply_layout(fig5), use_container_width=True)

    st.markdown('<p class="section-header">State-wise Summary Table</p>', unsafe_allow_html=True)
    ss.columns = ["State","College Count","Avg Placement (%)","Avg Package (LPA)","Total Student Intake"]
    st.dataframe(ss.sort_values("College Count", ascending=False).reset_index(drop=True), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 3 – PLACEMENT ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif page == "💼 Placement Analysis":
    st.markdown('<p class="page-title">💼 Placement Analysis Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Comprehensive placement metrics across India\'s top colleges</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    kpi([c1,c2,c3,c4], [
        ("Avg Placement %", f"{fdf['Placement %'].mean():.1f}%"),
        ("Highest Placement", f"{fdf['Placement %'].max():.0f}%"),
        ("Avg Package (LPA)", f"₹{fdf['Avg Pkg (LPA)'].mean():.1f}"),
        ("Max Package (LPA)", f"₹{fdf['Highest Pkg (LPA)'].max():.0f}"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(
            fdf, x="Placement %", nbins=12,
            color="Tier", color_discrete_map=TIER_COLORS,
            title="Placement % Distribution by Tier",
            barmode="overlay", opacity=0.8
        )
        st.plotly_chart(apply_layout(fig), use_container_width=True)

    with c2:
        tier_avg = fdf.groupby("Tier").agg(
            Avg_Placement=("Placement %","mean"),
            Avg_Package=("Avg Pkg (LPA)","mean")
        ).reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Avg Placement %", x=tier_avg["Tier"], y=tier_avg["Avg_Placement"].round(1), marker_color="#6366f1"))
        fig2.add_trace(go.Bar(name="Avg Package (LPA)", x=tier_avg["Tier"], y=tier_avg["Avg_Package"].round(1), marker_color="#06b6d4"))
        fig2.update_layout(barmode="group", title="Placement & Package by Tier")
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    st.markdown('<p class="section-header">Category-wise Insights</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        cat_stats = fdf.groupby("Category").agg(
            Avg_Placement=("Placement %","mean"),
            Avg_Package=("Avg Pkg (LPA)","mean"),
            Count=("College Name","count")
        ).reset_index()
        fig3 = px.scatter(
            cat_stats, x="Avg_Package", y="Avg_Placement",
            size="Count", color="Category",
            color_discrete_sequence=COLORS,
            text="Category",
            title="Category: Placement % vs Avg Package"
        )
        fig3.update_traces(textposition="top center")
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

    with c4:
        top20 = fdf.nlargest(20,"Placement %")
        fig4 = px.bar(
            top20.sort_values("Placement %"),
            x="Placement %", y="College Name", orientation="h",
            color="Tier", color_discrete_map=TIER_COLORS,
            title="Top 20 Colleges by Placement %"
        )
        st.plotly_chart(apply_layout(fig4), use_container_width=True)

    st.markdown('<p class="section-header">Package Range Analysis</p>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)

    with c5:
        box_df = fdf.dropna(subset=["Avg Pkg (LPA)"])
        fig5 = px.box(
            box_df, x="Category", y="Avg Pkg (LPA)",
            color="Category", color_discrete_sequence=COLORS,
            title="Avg Package Distribution by Category"
        )
        fig5.update_xaxes(tickangle=30)
        st.plotly_chart(apply_layout(fig5), use_container_width=True)

    with c6:
        pkg_df = fdf.dropna(subset=["Avg Pkg (LPA)","Highest Pkg (LPA)"])
        fig6 = px.scatter(
            pkg_df, x="Avg Pkg (LPA)", y="Highest Pkg (LPA)",
            color="Tier", hover_name="College Name",
            color_discrete_map=TIER_COLORS,
            title="Avg Package vs Highest Package (LPA)"
        )
        st.plotly_chart(apply_layout(fig6), use_container_width=True)

    st.markdown('<p class="section-header">Placement % by Ownership Type</p>', unsafe_allow_html=True)
    own_p = fdf.groupby("Ownership Type")["Placement %"].mean().reset_index().sort_values("Placement %", ascending=False)
    fig7 = px.bar(
        own_p, x="Ownership Type", y="Placement %",
        color="Ownership Type", color_discrete_sequence=COLORS,
        title="Average Placement % by Ownership Type"
    )
    st.plotly_chart(apply_layout(fig7), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 4 – RECRUITER ANALYTICS
# ═══════════════════════════════════════════════════════════════
elif page == "🤝 Recruiter Analytics":
    st.markdown('<p class="page-title">🤝 Recruiter Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Top recruiters, industry partnerships & hiring patterns</p>', unsafe_allow_html=True)

    def split_col(val):
        if pd.isna(val): return []
        return [x.strip() for x in str(val).split(",") if x.strip()]

    all_rec  = []
    all_part = []
    for _, row in fdf.iterrows():
        all_rec.extend(split_col(row["Top Recruiters"]))
        all_part.extend(split_col(row["Industry Partnerships"]))

    rec_counts  = Counter(all_rec)
    part_counts = Counter(all_part)
    top_rec  = pd.DataFrame(rec_counts.most_common(20),  columns=["Recruiter","College Count"])
    top_part = pd.DataFrame(part_counts.most_common(20), columns=["Partner","College Count"])

    fdf2 = fdf.copy()
    fdf2["Recruiter Count"] = fdf2["Top Recruiters"].apply(lambda x: len(split_col(x)))
    fdf2["Partner Count"]   = fdf2["Industry Partnerships"].apply(lambda x: len(split_col(x)))

    c1, c2, c3, c4 = st.columns(4)
    kpi([c1,c2,c3,c4], [
        ("Unique Recruiters", len(rec_counts)),
        ("Unique Industry Partners", len(part_counts)),
        ("Most Common Recruiter", rec_counts.most_common(1)[0][0] if rec_counts else "N/A"),
        ("Colleges Analyzed", len(fdf2)),
    ])

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            top_rec.sort_values("College Count"),
            x="College Count", y="Recruiter", orientation="h",
            color="College Count", color_continuous_scale="Viridis",
            title="Top 20 Recruiters (college presence)"
        )
        st.plotly_chart(apply_layout(fig), use_container_width=True)

    with c2:
        fig2 = px.bar(
            top_part.sort_values("College Count"),
            x="College Count", y="Partner", orientation="h",
            color="College Count", color_continuous_scale="Plasma",
            title="Top 20 Industry Partners"
        )
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    st.markdown('<p class="section-header">Recruiter Reach by Tier</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        fig3 = px.scatter(
            fdf2, x="Recruiter Count", y="Placement %",
            color="Tier", hover_name="College Name",
            size="Avg Pkg (LPA)",
            color_discrete_map=TIER_COLORS,
            title="Recruiter Count vs Placement %"
        )
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

    with c4:
        tier_rec = fdf2.groupby("Tier")[["Recruiter Count","Partner Count"]].mean().reset_index()
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Avg Recruiters", x=tier_rec["Tier"], y=tier_rec["Recruiter Count"].round(1), marker_color="#6366f1"))
        fig4.add_trace(go.Bar(name="Avg Partners",   x=tier_rec["Tier"], y=tier_rec["Partner Count"].round(1),   marker_color="#06b6d4"))
        fig4.update_layout(barmode="group", title="Avg Recruiters & Partners by Tier")
        st.plotly_chart(apply_layout(fig4), use_container_width=True)

    st.markdown('<p class="section-header">Recruiter Count vs Average Package</p>', unsafe_allow_html=True)
    fig5 = px.scatter(
        fdf2.dropna(subset=["Avg Pkg (LPA)"]),
        x="Recruiter Count", y="Avg Pkg (LPA)",
        color="Category", hover_name="College Name",
        color_discrete_sequence=COLORS,
        title="More Recruiters → Higher Package?"
    )
    st.plotly_chart(apply_layout(fig5), use_container_width=True)

    st.markdown('<p class="section-header">Top Recruiters Table</p>', unsafe_allow_html=True)
    st.dataframe(
        top_rec.rename(columns={"College Count":"Number of Colleges"}),
        use_container_width=True
    )


# ═══════════════════════════════════════════════════════════════
# PAGE 5 – COLLEGE COMPARISON
# ═══════════════════════════════════════════════════════════════
elif page == "⚖️ College Comparison":
    st.markdown('<p class="page-title">⚖️ College Comparison Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Compare colleges side-by-side across key metrics</p>', unsafe_allow_html=True)

    all_colleges = sorted(fdf["College Name"].dropna().unique())
    default_sel  = all_colleges[:min(5, len(all_colleges))]
    sel_colleges = st.multiselect("Select Colleges to Compare (max 10)", all_colleges, default=default_sel, max_selections=10)

    if not sel_colleges:
        st.info("Please select at least one college to compare.")
        st.stop()

    cdf = fdf[fdf["College Name"].isin(sel_colleges)].copy()

    st.markdown('<p class="section-header">Radar Chart – Multi-Metric Comparison</p>', unsafe_allow_html=True)

    radar_metrics = ["Placement %", "Avg Pkg (LPA)", "Highest Pkg (LPA)", "Student Intake"]
    radar_df = cdf[["College Name"] + radar_metrics].dropna().copy()

    def normalize(s):
        mn, mx = s.min(), s.max()
        if mx == mn: return s * 0 + 50
        return (s - mn) / (mx - mn) * 100

    for m in radar_metrics:
        radar_df[m] = normalize(radar_df[m])

    fig_r = go.Figure()
    for i, (_, row) in enumerate(radar_df.iterrows()):
        vals = [row[m] for m in radar_metrics]
        fig_r.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=radar_metrics + [radar_metrics[0]],
            fill="toself",
            name=row["College Name"],
            line=dict(color=COLORS[i % len(COLORS)])
        ))
    fig_r.update_layout(
        **PLOTLY_LAYOUT,
        polar=dict(
            bgcolor="rgba(15,23,42,0.6)",
            radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color="#64748b")),
            angularaxis=dict(tickfont=dict(color="#94a3b8"))
        ),
        title="Normalized Multi-Metric Radar Comparison"
    )
    st.plotly_chart(fig_r, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig2 = px.bar(
            cdf.sort_values("Placement %", ascending=False),
            x="College Name", y="Placement %",
            color="College Name", color_discrete_sequence=COLORS,
            title="Placement % Comparison"
        )
        fig2.update_xaxes(tickangle=30)
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    with c2:
        fig3 = px.bar(
            cdf.sort_values("Avg Pkg (LPA)", ascending=False),
            x="College Name", y="Avg Pkg (LPA)",
            color="College Name", color_discrete_sequence=COLORS,
            title="Average Package Comparison (LPA)"
        )
        fig3.update_xaxes(tickangle=30)
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        hp_df = cdf.dropna(subset=["Highest Pkg (LPA)"])
        fig4 = px.bar(
            hp_df.sort_values("Highest Pkg (LPA)", ascending=False),
            x="College Name", y="Highest Pkg (LPA)",
            color="College Name", color_discrete_sequence=COLORS,
            title="Highest Package Comparison (LPA)"
        )
        fig4.update_xaxes(tickangle=30)
        st.plotly_chart(apply_layout(fig4), use_container_width=True)

    with c4:
        si_df = cdf.dropna(subset=["Student Intake"])
        fig5 = px.bar(
            si_df.sort_values("Student Intake", ascending=False),
            x="College Name", y="Student Intake",
            color="Tier", color_discrete_map=TIER_COLORS,
            title="Student Intake Comparison"
        )
        fig5.update_xaxes(tickangle=30)
        st.plotly_chart(apply_layout(fig5), use_container_width=True)

    st.markdown('<p class="section-header">NIRF Rank Comparison</p>', unsafe_allow_html=True)
    nirf_df = cdf.dropna(subset=["NIRF Rank"])
    if len(nirf_df):
        fig6 = px.bar(
            nirf_df.sort_values("NIRF Rank"),
            x="College Name", y="NIRF Rank",
            color="Category", color_discrete_sequence=COLORS,
            title="NIRF Rank (lower = better)"
        )
        fig6.update_xaxes(tickangle=30)
        st.plotly_chart(apply_layout(fig6), use_container_width=True)

    st.markdown('<p class="section-header">Detailed Comparison Table</p>', unsafe_allow_html=True)
    show = ["College Name","Category","State","Tier","NIRF Rank","NAAC/NBA Status",
            "Placement %","Avg Pkg","Highest Pkg","Student Intake","Ownership Type"]
    st.dataframe(cdf[show].reset_index(drop=True), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 6 – ROI ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif page == "💰 ROI Analysis":
    st.markdown('<p class="page-title">💰 ROI Analysis Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Return on Investment — placement outcomes vs education investment</p>', unsafe_allow_html=True)

    roi_df = fdf.dropna(subset=["Avg Pkg (LPA)","Placement %"]).copy()
    roi_df["ROI Score"] = (roi_df["Placement %"] * roi_df["Avg Pkg (LPA)"] / 100).round(2)

    c1, c2, c3, c4 = st.columns(4)
    kpi([c1,c2,c3,c4], [
        ("Top ROI Score", f"{roi_df['ROI Score'].max():.1f}"),
        ("Avg ROI Score", f"{roi_df['ROI Score'].mean():.1f}"),
        ("Best Value Tier", roi_df.groupby("Tier")["ROI Score"].mean().idxmax()),
        ("Colleges Ranked", len(roi_df)),
    ])

    st.markdown('<p class="section-header">ROI Leaderboard</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        top_roi = roi_df.nlargest(15,"ROI Score")
        fig = px.bar(
            top_roi.sort_values("ROI Score"),
            x="ROI Score", y="College Name", orientation="h",
            color="Tier", color_discrete_map=TIER_COLORS,
            title="Top 15 Colleges by ROI Score"
        )
        st.plotly_chart(apply_layout(fig), use_container_width=True)

    with c2:
        fig2 = px.scatter(
            roi_df, x="Avg Pkg (LPA)", y="Placement %",
            size="ROI Score", color="Tier",
            hover_name="College Name",
            color_discrete_map=TIER_COLORS,
            title="ROI Matrix: Package vs Placement (bubble = ROI score)"
        )
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    st.markdown('<p class="section-header">ROI by Category & Tier</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        cat_roi = roi_df.groupby("Category")["ROI Score"].mean().reset_index().sort_values("ROI Score", ascending=False)
        fig3 = px.bar(
            cat_roi, x="Category", y="ROI Score",
            color="ROI Score", color_continuous_scale="Viridis",
            title="Average ROI Score by Category"
        )
        fig3.update_xaxes(tickangle=30)
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

    with c4:
        fig4 = px.box(
            roi_df, x="Tier", y="ROI Score",
            color="Tier", color_discrete_map=TIER_COLORS,
            title="ROI Score Distribution by Tier"
        )
        st.plotly_chart(apply_layout(fig4), use_container_width=True)

    st.markdown('<p class="section-header">ROI vs NIRF Rank</p>', unsafe_allow_html=True)
    nirf_roi = roi_df.dropna(subset=["NIRF Rank"])
    fig5 = px.scatter(
        nirf_roi, x="NIRF Rank", y="ROI Score",
        color="Category", hover_name="College Name",
        color_discrete_sequence=COLORS,
        size="Avg Pkg (LPA)",
        title="ROI Score vs NIRF Rank (lower rank = better)"
    )
    st.plotly_chart(apply_layout(fig5), use_container_width=True)

    st.markdown('<p class="section-header">ROI by State</p>', unsafe_allow_html=True)
    state_roi = roi_df.groupby("State")["ROI Score"].mean().reset_index().sort_values("ROI Score", ascending=False)
    fig6 = px.bar(
        state_roi, x="State", y="ROI Score",
        color="ROI Score", color_continuous_scale="Plasma",
        title="Average ROI Score by State"
    )
    fig6.update_xaxes(tickangle=45)
    st.plotly_chart(apply_layout(fig6), use_container_width=True)

    st.markdown('<p class="section-header">Full ROI Rankings Table</p>', unsafe_allow_html=True)
    roi_table = roi_df[["College Name","Category","State","Tier","Placement %",
                         "Avg Pkg (LPA)","Highest Pkg (LPA)","ROI Score","NIRF Rank"]] \
        .sort_values("ROI Score", ascending=False).reset_index(drop=True)
    roi_table.index += 1
    st.dataframe(roi_table, use_container_width=True, height=450)

    st.markdown("""
    <div class="info-card" style="margin-top:16px;">
      <b style="color:#e2e8f0;">📌 ROI Score Methodology</b><br>
      <p style="margin-top:8px;">ROI Score = (Placement % × Avg Package LPA) / 100 — a composite metric rewarding 
      colleges that deliver both high placement rates AND competitive packages. 
      A score of 25 = placing 100% students at ₹25 LPA average, or 83% at ₹30 LPA.</p>
    </div>
    """, unsafe_allow_html=True)
