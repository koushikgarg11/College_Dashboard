import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import re
from data_utils import load_data

st.set_page_config(
    page_title="India College Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background: #0f172a; }
    
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 13px; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; font-size: 28px; font-weight: 700; }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] { color: #4ade80 !important; }
    
    /* Page title */
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .page-subtitle { color: #64748b; font-size: 0.95rem; margin-bottom: 24px; }
    
    /* Section headers */
    .section-header {
        color: #e2e8f0;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 24px 0 12px 0;
        padding-left: 12px;
        border-left: 3px solid #6366f1;
    }
    
    /* Cards */
    .info-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
    }
    
    /* Table */
    [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
    
    /* Divider */
    hr { border-color: #334155; }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { background: #1e293b; border-radius: 8px; padding: 4px; gap: 4px; }
    .stTabs [data-baseweb="tab"] { color: #94a3b8; border-radius: 6px; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: #6366f1; color: white; }
    
    /* Streamlit selectbox / multiselect */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background: #1e293b;
        border-color: #334155;
        color: #e2e8f0;
    }
    
    h1, h2, h3, h4 { color: #e2e8f0; }
    p, li { color: #94a3b8; }
    
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
    }
    .badge-t1 { background: #1e3a5f; color: #60a5fa; border: 1px solid #2563eb; }
    .badge-t2 { background: #1a3340; color: #34d399; border: 1px solid #059669; }
    .badge-t3 { background: #2d1f3d; color: #a78bfa; border: 1px solid #7c3aed; }
</style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,23,42,0.8)",
    font=dict(family="Inter", color="#94a3b8"),
    title_font=dict(color="#e2e8f0", size=16, family="Inter"),
    legend=dict(bgcolor="rgba(30,41,59,0.8)", bordercolor="#334155", borderwidth=1, font=dict(color="#e2e8f0")),
    xaxis=dict(gridcolor="#1e293b", zerolinecolor="#334155", tickfont=dict(color="#64748b")),
    yaxis=dict(gridcolor="#1e293b", zerolinecolor="#334155", tickfont=dict(color="#64748b")),
    margin=dict(l=40, r=20, t=50, b=40),
)

COLOR_PALETTE = ["#6366f1", "#06b6d4", "#10b981", "#f59e0b", "#f43f5e", "#8b5cf6", "#ec4899", "#14b8a6"]
TIER_COLORS = {"Tier 1": "#6366f1", "Tier 2": "#06b6d4", "Tier 3": "#10b981"}

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 College Analytics")
    st.markdown("---")
    
    page = st.selectbox(
        "Navigate to Dashboard",
        [
            "🏆 Tier 1 College Dashboard",
            "🗺️ State-wise Distribution",
            "💼 Placement Analysis",
            "🤝 Recruiter Analytics",
            "⚖️ College Comparison",
            "💰 ROI Analysis"
        ]
    )
    
    st.markdown("---")
    st.markdown("### Filters")
    
    selected_states = st.multiselect(
        "States", sorted(df["State"].dropna().unique()), default=[]
    )
    selected_categories = st.multiselect(
        "College Category", sorted(df["Category"].dropna().unique()), default=[]
    )
    selected_ownership = st.multiselect(
        "Ownership Type", sorted(df["Ownership Type"].dropna().unique()), default=[]
    )
    
    st.markdown("---")
    st.caption("📊 Data: 45 Tier 1-3 Colleges")
    st.caption("🇮🇳 Covering 18 States")

# ── Filter data ──────────────────────────────────────────────────────────────
filtered_df = df.copy()
if selected_states:
    filtered_df = filtered_df[filtered_df["State"].isin(selected_states)]
if selected_categories:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
if selected_ownership:
    filtered_df = filtered_df[filtered_df["Ownership Type"].isin(selected_ownership)]


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 1 – TIER 1 COLLEGE DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
if page == "🏆 Tier 1 College Dashboard":
    st.markdown('<p class="page-title">🏆 Tier 1 College Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Deep analysis of India\'s premier educational institutions</p>', unsafe_allow_html=True)

    t1 = filtered_df[filtered_df["Tier"] == "Tier 1"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tier 1 Colleges", len(t1))
    col2.metric("Avg Placement %", f"{t1['Placement %'].mean():.1f}%" if len(t1) else "N/A")
    col3.metric("Avg Package (LPA)", f"₹{t1['Avg Pkg (LPA)'].mean():.1f}" if len(t1) else "N/A")
    col4.metric("Avg NIRF Rank", f"{t1['NIRF Rank'].mean():.1f}" if len(t1) else "N/A")

    st.markdown('<p class="section-header">Placement % vs Average Package</p>', unsafe_allow_html=True)
    
    if len(t1) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(
                t1, x="Avg Pkg (LPA)", y="Placement %",
                size="Student Intake", color="Category",
                hover_name="College Name",
                color_discrete_sequence=COLOR_PALETTE,
                title="Package vs Placement (bubble = student intake)",
                labels={"Avg Pkg (LPA)": "Avg Package (LPA)", "Placement %": "Placement %"}
            )
            fig.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig2 = px.bar(
                t1.sort_values("NIRF Rank").head(15),
                x="College Name", y="Placement %",
                color="Category", color_discrete_sequence=COLOR_PALETTE,
                title="Placement % – Top Tier 1 Colleges"
            )
            fig2.update_layout(**PLOTLY_LAYOUT)
            fig2.update_xaxes(tickangle=45)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<p class="section-header">NIRF Rankings & Package Distribution</p>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)

        with col3:
            fig3 = px.scatter(
                t1.dropna(subset=["NIRF Rank", "Avg Pkg (LPA)"]),
                x="NIRF Rank", y="Avg Pkg (LPA)",
                color="Category", hover_name="College Name",
                color_discrete_sequence=COLOR_PALETTE,
                title="NIRF Rank vs Avg Package (lower rank = better)",
                trendline="lowess"
            )
            fig3.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            fig4 = px.pie(
                t1, names="Category",
                color_discrete_sequence=COLOR_PALETTE,
                title="Category Breakdown – Tier 1"
            )
            fig4.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown('<p class="section-header">Tier 1 College Details</p>', unsafe_allow_html=True)
        display_cols = ["College Name", "Category", "State", "NIRF Rank", "NAAC/NBA Status",
                        "Placement %", "Avg Pkg", "Highest Pkg", "Student Intake"]
        st.dataframe(
            t1[display_cols].sort_values("NIRF Rank").reset_index(drop=True),
            use_container_width=True,
            height=400
        )
    else:
        st.info("No Tier 1 colleges match current filters.")


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 2 – STATE-WISE DISTRIBUTION
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🗺️ State-wise Distribution":
    st.markdown('<p class="page-title">🗺️ State-wise College Distribution</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Geographic spread of top colleges across India</p>', unsafe_allow_html=True)

    state_stats = (
        filtered_df.groupby("State")
        .agg(
            College_Count=("College Name", "count"),
            Avg_Placement=("Placement %", "mean"),
            Avg_Package=("Avg Pkg (LPA)", "mean"),
            Total_Intake=("Student Intake", "sum")
        )
        .reset_index()
        .round(2)
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("States Covered", len(state_stats))
    col2.metric("Total Colleges", len(filtered_df))
    col3.metric("Best Avg Placement", f"{state_stats['Avg_Placement'].max():.1f}%" if len(state_stats) else "N/A")
    col4.metric("Highest Avg Pkg", f"₹{state_stats['Avg_Package'].max():.1f} LPA" if len(state_stats) else "N/A")

    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            state_stats.sort_values("College_Count", ascending=True),
            x="College_Count", y="State", orientation="h",
            color="College_Count", color_continuous_scale="Viridis",
            title="Number of Colleges per State"
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            state_stats.sort_values("Avg_Placement", ascending=True),
            x="Avg_Placement", y="State", orientation="h",
            color="Avg_Placement", color_continuous_scale="Blues",
            title="Average Placement % by State"
        )
        fig2.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Package & Intake Distribution</p>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        fig3 = px.bar(
            state_stats.sort_values("Avg_Package", ascending=False),
            x="State", y="Avg_Package",
            color="Avg_Package", color_continuous_scale="Purples",
            title="Average Package by State (LPA)"
        )
        fig3.update_layout(**PLOTLY_LAYOUT)
        fig3.update_xaxes(tickangle=45)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        cat_state = filtered_df.groupby(["State", "Category"]).size().reset_index(name="Count")
        fig4 = px.bar(
            cat_state, x="State", y="Count", color="Category",
            color_discrete_sequence=COLOR_PALETTE,
            title="College Categories by State"
        )
        fig4.update_layout(**PLOTLY_LAYOUT)
        fig4.update_xaxes(tickangle=45)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<p class="section-header">State-wise Summary Table</p>', unsafe_allow_html=True)
    state_stats.columns = ["State", "College Count", "Avg Placement (%)", "Avg Package (LPA)", "Total Student Intake"]
    st.dataframe(state_stats.sort_values("College Count", ascending=False).reset_index(drop=True),
                 use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 3 – PLACEMENT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "💼 Placement Analysis":
    st.markdown('<p class="page-title">💼 Placement Analysis Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Comprehensive placement metrics across India\'s top colleges</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Placement %", f"{filtered_df['Placement %'].mean():.1f}%")
    col2.metric("Highest Placement", f"{filtered_df['Placement %'].max():.0f}%")
    col3.metric("Avg Package", f"₹{filtered_df['Avg Pkg (LPA)'].mean():.1f} LPA")
    col4.metric("Max Package", f"₹{filtered_df['Highest Pkg (LPA)'].max():.0f} LPA")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            filtered_df, x="Placement %", nbins=15,
            color="Tier", color_discrete_map=TIER_COLORS,
            title="Placement % Distribution by Tier",
            barmode="overlay", opacity=0.8
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        tier_avg = filtered_df.groupby("Tier").agg(
            Avg_Placement=("Placement %", "mean"),
            Avg_Package=("Avg Pkg (LPA)", "mean")
        ).reset_index()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Avg Placement %", x=tier_avg["Tier"], y=tier_avg["Avg_Placement"],
                              marker_color="#6366f1", yaxis="y"))
        fig2.add_trace(go.Bar(name="Avg Package (LPA)", x=tier_avg["Tier"], y=tier_avg["Avg_Package"],
                              marker_color="#06b6d4", yaxis="y2"))
        fig2.update_layout(
            **PLOTLY_LAYOUT,
            title="Placement % & Package by Tier",
            yaxis=dict(title="Placement %", gridcolor="#1e293b", tickfont=dict(color="#64748b")),
            yaxis2=dict(title="Avg Package (LPA)", overlaying="y", side="right", tickfont=dict(color="#64748b")),
            barmode="group"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Category-wise Placement Insights</p>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        cat_stats = filtered_df.groupby("Category").agg(
            Avg_Placement=("Placement %", "mean"),
            Avg_Package=("Avg Pkg (LPA)", "mean"),
            Count=("College Name", "count")
        ).reset_index()
        
        fig3 = px.scatter(
            cat_stats, x="Avg_Package", y="Avg_Placement",
            size="Count", color="Category",
            color_discrete_sequence=COLOR_PALETTE,
            text="Category",
            title="Category: Placement % vs Avg Package"
        )
        fig3.update_traces(textposition="top center")
        fig3.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        top20 = filtered_df.nlargest(20, "Placement %")
        fig4 = px.bar(
            top20.sort_values("Placement %"),
            x="Placement %", y="College Name", orientation="h",
            color="Tier", color_discrete_map=TIER_COLORS,
            title="Top 20 Colleges by Placement %"
        )
        fig4.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<p class="section-header">Package Range Analysis</p>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)

    with col5:
        fig5 = px.box(
            filtered_df.dropna(subset=["Avg Pkg (LPA)"]),
            x="Category", y="Avg Pkg (LPA)",
            color="Category", color_discrete_sequence=COLOR_PALETTE,
            title="Average Package Distribution by Category"
        )
        fig5.update_layout(**PLOTLY_LAYOUT)
        fig5.update_xaxes(tickangle=30)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        fig6 = px.scatter(
            filtered_df.dropna(subset=["Avg Pkg (LPA)", "Highest Pkg (LPA)"]),
            x="Avg Pkg (LPA)", y="Highest Pkg (LPA)",
            color="Tier", hover_name="College Name",
            color_discrete_map=TIER_COLORS,
            title="Avg Package vs Highest Package"
        )
        fig6.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig6, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 4 – RECRUITER ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🤝 Recruiter Analytics":
    st.markdown('<p class="page-title">🤝 Recruiter Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Top recruiters, industry partnerships & hiring patterns</p>', unsafe_allow_html=True)

    # Parse recruiters
    def split_list(val):
        if pd.isna(val):
            return []
        return [r.strip() for r in str(val).split(",") if r.strip()]

    all_recruiters = []
    for _, row in filtered_df.iterrows():
        all_recruiters.extend(split_list(row["Top Recruiters"]))
    
    all_partners = []
    for _, row in filtered_df.iterrows():
        all_partners.extend(split_list(row["Industry Partnerships"]))

    recruiter_counts = Counter(all_recruiters)
    partner_counts = Counter(all_partners)

    top_recruiters = pd.DataFrame(recruiter_counts.most_common(20), columns=["Recruiter", "College Count"])
    top_partners = pd.DataFrame(partner_counts.most_common(20), columns=["Partner", "College Count"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Unique Recruiters", len(recruiter_counts))
    col2.metric("Unique Industry Partners", len(partner_counts))
    col3.metric("Top Recruiter", recruiter_counts.most_common(1)[0][0] if recruiter_counts else "N/A")
    col4.metric("Colleges Analyzed", len(filtered_df))

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            top_recruiters.sort_values("College Count"),
            x="College Count", y="Recruiter", orientation="h",
            color="College Count", color_continuous_scale="Viridis",
            title="Top 20 Recruiters (by college presence)"
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            top_partners.sort_values("College Count"),
            x="College Count", y="Partner", orientation="h",
            color="College Count", color_continuous_scale="Plasma",
            title="Top 20 Industry Partners"
        )
        fig2.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Recruiter Reach by College Tier</p>', unsafe_allow_html=True)
    
    # Count recruiters per college
    filtered_df["Recruiter Count"] = filtered_df["Top Recruiters"].apply(
        lambda x: len(split_list(x))
    )
    filtered_df["Partner Count"] = filtered_df["Industry Partnerships"].apply(
        lambda x: len(split_list(x))
    )

    col3, col4 = st.columns(2)

    with col3:
        fig3 = px.scatter(
            filtered_df,
            x="Recruiter Count", y="Placement %",
            color="Tier", size="Avg Pkg (LPA)",
            hover_name="College Name",
            color_discrete_map=TIER_COLORS,
            title="Recruiter Count vs Placement %"
        )
        fig3.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        tier_rec = filtered_df.groupby("Tier")[["Recruiter Count", "Partner Count"]].mean().reset_index()
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Avg Recruiters", x=tier_rec["Tier"], y=tier_rec["Recruiter Count"], marker_color="#6366f1"))
        fig4.add_trace(go.Bar(name="Avg Partners", x=tier_rec["Tier"], y=tier_rec["Partner Count"], marker_color="#06b6d4"))
        fig4.update_layout(**PLOTLY_LAYOUT, title="Avg Recruiters & Partners by Tier", barmode="group")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<p class="section-header">Top 10 Recruiter Breakdown</p>', unsafe_allow_html=True)
    st.dataframe(
        top_recruiters.rename(columns={"College Count": "Number of Colleges Recruiting From"}),
        use_container_width=True
    )


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 5 – COLLEGE COMPARISON
# ═══════════════════════════════════════════════════════════════════════════
elif page == "⚖️ College Comparison":
    st.markdown('<p class="page-title">⚖️ College Comparison Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Compare colleges side-by-side across key metrics</p>', unsafe_allow_html=True)

    all_colleges = sorted(filtered_df["College Name"].dropna().unique())
    
    default_colleges = all_colleges[:min(5, len(all_colleges))]
    selected_colleges = st.multiselect(
        "Select Colleges to Compare (max 10)", all_colleges,
        default=default_colleges, max_selections=10
    )

    if selected_colleges:
        comp_df = filtered_df[filtered_df["College Name"].isin(selected_colleges)]

        st.markdown('<p class="section-header">Radar Chart – Multi-Metric Comparison</p>', unsafe_allow_html=True)

        metrics = ["Placement %", "Avg Pkg (LPA)", "Highest Pkg (LPA)", "Student Intake", "Alumni Network Strength"]
        
        # Normalize 0-100 for radar
        def normalize(series):
            mn, mx = series.min(), series.max()
            if mx == mn:
                return series * 0 + 50
            return (series - mn) / (mx - mn) * 100

        radar_df = comp_df[["College Name"] + [m for m in metrics if m in comp_df.columns]].copy()
        for m in metrics:
            if m in radar_df.columns:
                radar_df[m] = normalize(radar_df[m])

        fig_radar = go.Figure()
        for i, (_, row) in enumerate(radar_df.iterrows()):
            vals = [row[m] for m in metrics if m in row]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=metrics + [metrics[0]],
                fill="toself",
                name=row["College Name"],
                line=dict(color=COLOR_PALETTE[i % len(COLOR_PALETTE)])
            ))
        fig_radar.update_layout(
            **PLOTLY_LAYOUT,
            polar=dict(
                bgcolor="rgba(15,23,42,0.6)",
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color="#64748b")),
                angularaxis=dict(tickfont=dict(color="#94a3b8"))
            ),
            title="Normalized Multi-Metric Radar Comparison"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            fig2 = px.bar(
                comp_df.sort_values("Placement %", ascending=False),
                x="College Name", y="Placement %",
                color="College Name", color_discrete_sequence=COLOR_PALETTE,
                title="Placement % Comparison"
            )
            fig2.update_layout(**PLOTLY_LAYOUT)
            fig2.update_xaxes(tickangle=30)
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            fig3 = px.bar(
                comp_df.sort_values("Avg Pkg (LPA)", ascending=False),
                x="College Name", y="Avg Pkg (LPA)",
                color="College Name", color_discrete_sequence=COLOR_PALETTE,
                title="Average Package Comparison (LPA)"
            )
            fig3.update_layout(**PLOTLY_LAYOUT)
            fig3.update_xaxes(tickangle=30)
            st.plotly_chart(fig3, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            fig4 = px.bar(
                comp_df.dropna(subset=["Highest Pkg (LPA)"]).sort_values("Highest Pkg (LPA)", ascending=False),
                x="College Name", y="Highest Pkg (LPA)",
                color="College Name", color_discrete_sequence=COLOR_PALETTE,
                title="Highest Package Comparison (LPA)"
            )
            fig4.update_layout(**PLOTLY_LAYOUT)
            fig4.update_xaxes(tickangle=30)
            st.plotly_chart(fig4, use_container_width=True)

        with col4:
            fig5 = px.bar(
                comp_df.dropna(subset=["Student Intake"]).sort_values("Student Intake", ascending=False),
                x="College Name", y="Student Intake",
                color="Tier", color_discrete_map=TIER_COLORS,
                title="Student Intake Comparison"
            )
            fig5.update_layout(**PLOTLY_LAYOUT)
            fig5.update_xaxes(tickangle=30)
            st.plotly_chart(fig5, use_container_width=True)

        st.markdown('<p class="section-header">Detailed Comparison Table</p>', unsafe_allow_html=True)
        show_cols = ["College Name", "Category", "State", "Tier", "NIRF Rank",
                     "NAAC/NBA Status", "Placement %", "Avg Pkg", "Highest Pkg",
                     "Student Intake", "Ownership Type"]
        st.dataframe(comp_df[show_cols].reset_index(drop=True), use_container_width=True)
    else:
        st.info("Please select at least one college to compare.")


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE 6 – ROI ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "💰 ROI Analysis":
    st.markdown('<p class="page-title">💰 ROI Analysis Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Return on Investment — Placement outcomes vs education investment proxy</p>', unsafe_allow_html=True)

    roi_df = filtered_df.dropna(subset=["Avg Pkg (LPA)", "Placement %"]).copy()
    roi_df["ROI Score"] = (roi_df["Placement %"] * roi_df["Avg Pkg (LPA)"] / 100).round(2)
    roi_df["Placement Efficiency"] = (roi_df["Placement %"] / 100 * roi_df["Avg Pkg (LPA)"]).round(2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Top ROI Score", f"{roi_df['ROI Score'].max():.1f}")
    col2.metric("Avg ROI Score", f"{roi_df['ROI Score'].mean():.1f}")
    col3.metric("Best Value Tier", roi_df.groupby("Tier")["ROI Score"].mean().idxmax())
    col4.metric("Colleges Ranked", len(roi_df))

    st.markdown('<p class="section-header">ROI Leaderboard</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        top_roi = roi_df.nlargest(15, "ROI Score")
        fig = px.bar(
            top_roi.sort_values("ROI Score"),
            x="ROI Score", y="College Name", orientation="h",
            color="Tier", color_discrete_map=TIER_COLORS,
            title="Top 15 Colleges by ROI Score"
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(
            roi_df, x="Avg Pkg (LPA)", y="Placement %",
            size="ROI Score", color="Tier",
            hover_name="College Name",
            color_discrete_map=TIER_COLORS,
            title="ROI Matrix: Package vs Placement (bubble = ROI score)"
        )
        fig2.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">ROI by Category & Tier</p>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        cat_roi = roi_df.groupby("Category")["ROI Score"].mean().reset_index().sort_values("ROI Score", ascending=False)
        fig3 = px.bar(
            cat_roi, x="Category", y="ROI Score",
            color="ROI Score", color_continuous_scale="Viridis",
            title="Average ROI Score by Category"
        )
        fig3.update_layout(**PLOTLY_LAYOUT)
        fig3.update_xaxes(tickangle=30)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.box(
            roi_df, x="Tier", y="ROI Score",
            color="Tier", color_discrete_map=TIER_COLORS,
            title="ROI Score Distribution by Tier"
        )
        fig4.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<p class="section-header">ROI vs NIRF Rank</p>', unsafe_allow_html=True)
    fig5 = px.scatter(
        roi_df.dropna(subset=["NIRF Rank"]),
        x="NIRF Rank", y="ROI Score",
        color="Category", hover_name="College Name",
        color_discrete_sequence=COLOR_PALETTE,
        trendline="lowess",
        title="ROI Score vs NIRF Rank (lower rank = better ranked)"
    )
    fig5.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown('<p class="section-header">Full ROI Rankings Table</p>', unsafe_allow_html=True)
    roi_table = roi_df[["College Name", "Category", "State", "Tier", "Placement %",
                         "Avg Pkg (LPA)", "Highest Pkg (LPA)", "ROI Score", "NIRF Rank"]] \
        .sort_values("ROI Score", ascending=False).reset_index(drop=True)
    roi_table.index += 1
    st.dataframe(roi_table, use_container_width=True, height=450)

    st.markdown("""
    <div class="info-card" style="margin-top:16px;">
      <b style="color:#e2e8f0;">📌 ROI Score Methodology</b><br>
      <p>ROI Score = (Placement % × Avg Package LPA) / 100 — a composite proxy that rewards colleges 
      delivering both high placement rates AND competitive packages. A score of 25 means a college 
      placing 100% at 25 LPA average, or 83% at 30 LPA.</p>
    </div>
    """, unsafe_allow_html=True)
