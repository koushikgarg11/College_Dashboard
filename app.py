import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import re
from data_utils import load_data

st.set_page_config(
    page_title="NexusIQ — India's Tier 1 Engineering Intelligence Vault",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: #060b18;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(6,182,212,0.06) 0%, transparent 50%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1526 0%, #060b18 100%);
    border-right: 1px solid rgba(99,102,241,0.2);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: rgba(30,41,59,0.8);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 8px;
    color: #e2e8f0 !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px;
    padding: 20px 16px;
    backdrop-filter: blur(10px);
    transition: border-color 0.3s;
}
[data-testid="metric-container"]:hover { border-color: rgba(99,102,241,0.6); }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { color: #f8fafc !important; font-size: 28px !important; font-weight: 800 !important; font-family: 'Space Grotesk', sans-serif !important; }
[data-testid="stMetricDelta"] { color: #4ade80 !important; }

/* ── Page header ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(6,182,212,0.1) 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at top left, rgba(99,102,241,0.12), transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem; font-weight: 700;
    background: linear-gradient(135deg, #a5b4fc, #67e8f9, #a5b4fc);
    background-size: 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 6px 0;
}
.hero-subtitle { color: #64748b; font-size: 0.9rem; margin: 0; }
.hero-badge {
    display: inline-block; padding: 4px 12px;
    background: rgba(99,102,241,0.2); border: 1px solid rgba(99,102,241,0.4);
    border-radius: 20px; font-size: 11px; color: #a5b4fc;
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;
    margin-bottom: 10px;
}

/* ── Section headers ── */
.section-hdr {
    display: flex; align-items: center; gap: 10px;
    color: #e2e8f0; font-size: 1rem; font-weight: 600;
    margin: 28px 0 14px 0;
}
.section-hdr::before {
    content: ''; width: 4px; height: 20px;
    background: linear-gradient(180deg, #6366f1, #06b6d4);
    border-radius: 2px; flex-shrink: 0;
}

/* ── Stat pill ── */
.stat-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
.stat-pill {
    background: rgba(30,41,59,0.8); border: 1px solid rgba(99,102,241,0.2);
    border-radius: 24px; padding: 6px 16px;
    font-size: 12px; color: #94a3b8; font-weight: 500;
}
.stat-pill span { color: #a5b4fc; font-weight: 700; }

/* ── Tables ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid rgba(99,102,241,0.15); }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.8); border-radius: 10px;
    padding: 4px; gap: 4px;
    border: 1px solid rgba(99,102,241,0.15);
}
.stTabs [data-baseweb="tab"] { color: #64748b; border-radius: 7px; font-size: 13px; }
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white !important;
}

/* ── Insight card ── */
.insight-card {
    background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 14px; padding: 18px 20px; margin: 6px 0;
}
.insight-card h4 { color: #a5b4fc; font-size: 13px; font-weight: 600; margin: 0 0 6px 0; text-transform: uppercase; letter-spacing: 0.05em; }
.insight-card p  { color: #94a3b8; font-size: 13px; margin: 0; line-height: 1.6; }
.insight-card .big-num { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #f1f5f9; }

/* ── Recruiter chip ── */
.chip-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.chip {
    padding: 5px 13px; border-radius: 20px; font-size: 12px; font-weight: 600;
    border: 1px solid; cursor: default;
}
.chip-blue  { background: rgba(99,102,241,0.12); color: #a5b4fc; border-color: rgba(99,102,241,0.3); }
.chip-cyan  { background: rgba(6,182,212,0.12);  color: #67e8f9; border-color: rgba(6,182,212,0.3);  }
.chip-green { background: rgba(16,185,129,0.12); color: #6ee7b7; border-color: rgba(16,185,129,0.3); }
.chip-amber { background: rgba(245,158,11,0.12); color: #fcd34d; border-color: rgba(245,158,11,0.3); }

h1,h2,h3,h4 { color: #e2e8f0; }
p, li { color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ── Plotly defaults ────────────────────────────────────────────────────────
BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(6,11,24,0.6)",
    font=dict(family="Inter", color="#94a3b8", size=12),
    title_font=dict(color="#e2e8f0", size=14, family="Space Grotesk"),
    legend=dict(bgcolor="rgba(15,23,42,0.8)", bordercolor="rgba(99,102,241,0.2)",
                borderwidth=1, font=dict(color="#cbd5e1", size=11)),
    xaxis=dict(gridcolor="rgba(30,41,59,0.8)", zerolinecolor="rgba(99,102,241,0.2)",
               tickfont=dict(color="#475569", size=11)),
    yaxis=dict(gridcolor="rgba(30,41,59,0.8)", zerolinecolor="rgba(99,102,241,0.2)",
               tickfont=dict(color="#475569", size=11)),
    margin=dict(l=40, r=20, t=48, b=40),
    hoverlabel=dict(bgcolor="rgba(15,23,42,0.95)", bordercolor="rgba(99,102,241,0.4)",
                    font=dict(color="#e2e8f0", size=12)),
)

GRAD  = ["#6366f1","#06b6d4","#10b981","#f59e0b","#f43f5e","#8b5cf6","#ec4899","#14b8a6","#f97316","#84cc16"]
TIER_C = {"Tier 1":"#6366f1","Tier 2":"#06b6d4","Tier 3":"#10b981"}
CAT_C  = {
    "IIT":"#6366f1","NIT":"#06b6d4","IIIT":"#10b981",
    "Deemed University":"#f59e0b","Research Institute":"#f43f5e",
    "State University":"#8b5cf6","Engineering College":"#ec4899","University":"#14b8a6"
}

def L(fig, **kw):
    d = dict(BASE); d.update(kw)
    fig.update_layout(**d)
    return fig

def section(text):
    st.markdown(f'<div class="section-hdr">{text}</div>', unsafe_allow_html=True)

def hero(title, subtitle, badge="LIVE DASHBOARD"):
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-badge">{badge}</div>
        <p class="hero-title">{title}</p>
        <p class="hero-subtitle">{subtitle}</p>
    </div>""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    df = load_data()
    # Parse alumni count
    def alumni_num(v):
        if pd.isna(v): return None
        nums = re.findall(r'[\d,]+', str(v))
        if nums:
            return int(nums[0].replace(',',''))
        return None
    df["Alumni Count"] = df["Alumni Network Strength"].apply(alumni_num)

    # Parse internship companies
    def intern_cos(v):
        if pd.isna(v): return []
        m = re.search(r'\|(.*)', str(v))
        if m: return [x.strip() for x in m.group(1).split(',') if x.strip()]
        return []
    df["Internship Companies"] = df["Internship Opportunities"].apply(intern_cos)
    df["Internship Count"] = df["Internship Companies"].apply(len)

    # Recruiter count
    def split_c(v):
        if pd.isna(v): return []
        return [x.strip() for x in str(v).split(',') if x.strip()]
    df["Recruiter List"] = df["Top Recruiters"].apply(split_c)
    df["Recruiter Count"] = df["Recruiter List"].apply(len)
    df["Partner List"]    = df["Industry Partnerships"].apply(split_c)
    df["Partner Count"]   = df["Partner List"].apply(len)
    return df

df = get_data()

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 8px 0 16px 0;'>
        <div style='font-family:Space Grotesk; font-size:1.2rem; font-weight:700;
             background:linear-gradient(135deg,#a5b4fc,#67e8f9);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            🔬 NexusIQ
        </div>
        <div style='font-size:11px; color:#475569; margin-top:2px;'>India's Tier 1 Engineering Intelligence Vault</div>
    </div>""", unsafe_allow_html=True)

    page = st.selectbox("📊 Dashboard", [
        "🏠 Overview & Highlights",
        "🏆 Tier 1 College Deep Dive",
        "🗺️ State-wise Distribution",
        "💼 Placement Analysis",
        "🤝 Recruiter & Industry Network",
        "⚖️ College Comparison Tool",
        "💰 ROI & Value Analysis",
    ])
    st.markdown("---")
    st.markdown("**🔍 Global Filters**")
    sel_tier  = st.multiselect("Tier", sorted(df["Tier"].unique()))
    sel_states= st.multiselect("State", sorted(df["State"].dropna().unique()))
    sel_cats  = st.multiselect("Category", sorted(df["Category"].dropna().unique()))
    sel_own   = st.multiselect("Ownership", sorted(df["Ownership Type"].dropna().unique()))
    sel_naac  = st.multiselect("Accreditation", sorted(df["NAAC/NBA Status"].dropna().unique()))
    st.markdown("---")
    pkg_min, pkg_max = int(df["Avg Pkg (LPA)"].min()), int(df["Avg Pkg (LPA)"].max())
    pkg_range = st.slider("Avg Package (LPA)", pkg_min, pkg_max, (pkg_min, pkg_max))
    pl_min, pl_max = int(df["Placement %"].min()), int(df["Placement %"].max())
    pl_range = st.slider("Placement %", pl_min, pl_max, (pl_min, pl_max))
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center;'>
        <div style='font-size:11px; color:#475569;'>Showing data for</div>
        <div style='font-family:Space Grotesk; font-size:1.5rem; font-weight:700; color:#a5b4fc;'>{len(df)}</div>
        <div style='font-size:11px; color:#475569;'>colleges across {df['State'].nunique()} states</div>
    </div>""", unsafe_allow_html=True)

# ── Apply filters ──────────────────────────────────────────────────────────
fdf = df.copy()
if sel_tier:   fdf = fdf[fdf["Tier"].isin(sel_tier)]
if sel_states: fdf = fdf[fdf["State"].isin(sel_states)]
if sel_cats:   fdf = fdf[fdf["Category"].isin(sel_cats)]
if sel_own:    fdf = fdf[fdf["Ownership Type"].isin(sel_own)]
if sel_naac:   fdf = fdf[fdf["NAAC/NBA Status"].isin(sel_naac)]
fdf = fdf[(fdf["Avg Pkg (LPA)"] >= pkg_range[0]) & (fdf["Avg Pkg (LPA)"] <= pkg_range[1])]
fdf = fdf[(fdf["Placement %"] >= pl_range[0]) & (fdf["Placement %"] <= pl_range[1])]

def safe_metric(label, val, delta=None):
    if delta: st.metric(label, val, delta)
    else: st.metric(label, val)

# ═══════════════════════════════════════════════════════════════
# PAGE 0 – OVERVIEW & HIGHLIGHTS
# ═══════════════════════════════════════════════════════════════
if page == "🏠 Overview & Highlights":
    hero("NexusIQ — India's Tier 1 Engineering Intelligence Vault",
         "The definitive database of India's premier engineering colleges — placements, packages, recruiters & ROI, all in one place",
         "TIER 1 ENGINEERING DATABASE")

    # Top KPIs
    all_rec = [r for lst in fdf["Recruiter List"] for r in lst]
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Colleges", len(fdf))
    c2.metric("States", fdf["State"].nunique())
    c3.metric("Avg Placement", f"{fdf['Placement %'].mean():.1f}%")
    c4.metric("Avg Package", f"₹{fdf['Avg Pkg (LPA)'].mean():.1f} LPA")
    c5.metric("Top Package", f"₹{fdf['Highest Pkg (LPA)'].max():.0f} LPA")
    c6.metric("Unique Recruiters", len(set(all_rec)))

    st.markdown("")

    # ── Row 1 ──
    section("Tier & Category Breakdown")
    c1, c2, c3 = st.columns([1.2, 1.2, 1])

    with c1:
        tier_df = fdf.groupby("Tier").agg(
            Count=("College Name","count"),
            Avg_Placement=("Placement %","mean"),
            Avg_Package=("Avg Pkg (LPA)","mean")
        ).reset_index()
        fig = go.Figure()
        for i, row in tier_df.iterrows():
            fig.add_trace(go.Bar(
                name=row["Tier"], x=[row["Tier"]],
                y=[row["Count"]],
                marker=dict(color=TIER_C[row["Tier"]], opacity=0.85,
                            line=dict(color=TIER_C[row["Tier"]], width=1)),
                text=[f"{int(row['Count'])} colleges"],
                textposition="outside", textfont=dict(color="#e2e8f0"),
                hovertemplate=f"<b>{row['Tier']}</b><br>Colleges: {int(row['Count'])}<br>"
                              f"Avg Placement: {row['Avg_Placement']:.1f}%<br>"
                              f"Avg Package: ₹{row['Avg_Package']:.1f} LPA<extra></extra>"
            ))
        fig.update_layout(**BASE, title="Colleges by Tier", showlegend=False)
        fig.update_yaxes(title_text="Count")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        cat_df = fdf.groupby("Category").size().reset_index(name="Count").sort_values("Count", ascending=False)
        fig2 = px.bar(cat_df, x="Category", y="Count",
                      color="Category",
                      color_discrete_map=CAT_C,
                      title="Colleges by Category",
                      text="Count")
        fig2.update_traces(textposition="outside", textfont_color="#e2e8f0")
        fig2.update_xaxes(tickangle=30)
        st.plotly_chart(L(fig2, showlegend=False), use_container_width=True)

    with c3:
        naac_df = fdf.groupby("NAAC/NBA Status").size().reset_index(name="Count")
        fig3 = px.pie(naac_df, names="NAAC/NBA Status", values="Count",
                      color_discrete_sequence=GRAD,
                      title="Accreditation Split", hole=0.45)
        fig3.update_traces(textfont_color="#e2e8f0", textfont_size=11)
        st.plotly_chart(L(fig3), use_container_width=True)

    # ── Row 2 ──
    section("Placement & Package Landscape")
    c1, c2 = st.columns(2)

    with c1:
        fig4 = px.scatter(
            fdf, x="Avg Pkg (LPA)", y="Placement %",
            color="Tier", size="Student Intake",
            hover_name="College Name",
            color_discrete_map=TIER_C,
            size_max=30,
            title="Placement % vs Avg Package (bubble = intake)",
            labels={"Avg Pkg (LPA)":"Avg Package (LPA)","Placement %":"Placement %"}
        )
        fig4.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="rgba(255,255,255,0.2)")))
        st.plotly_chart(L(fig4), use_container_width=True)

    with c2:
        # Heatmap: state vs category count
        pivot = fdf.groupby(["State","Tier"]).agg(Avg_Pkg=("Avg Pkg (LPA)","mean")).reset_index()
        pivot_wide = pivot.pivot(index="State", columns="Tier", values="Avg_Pkg").fillna(0)
        fig5 = go.Figure(go.Heatmap(
            z=pivot_wide.values,
            x=pivot_wide.columns.tolist(),
            y=pivot_wide.index.tolist(),
            colorscale=[[0,"#060b18"],[0.5,"#312e81"],[1,"#a5b4fc"]],
            hoverongaps=False,
            text=[[f"₹{v:.1f}" if v else "" for v in row] for row in pivot_wide.values],
            texttemplate="%{text}",
            textfont=dict(size=10, color="#e2e8f0"),
            showscale=True,
            colorbar=dict(tickfont=dict(color="#64748b"))
        ))
        fig5.update_layout(**BASE, title="Avg Package (LPA) — State × Tier Heatmap")
        fig5.update_xaxes(title_text="")
        fig5.update_yaxes(title_text="")
        st.plotly_chart(fig5, use_container_width=True)

    # ── Row 3 – Quick Insights ──
    section("🔥 Quick Insights")
    top_place = fdf.nlargest(1,"Placement %").iloc[0]
    top_pkg   = fdf.nlargest(1,"Avg Pkg (LPA)").iloc[0]
    top_roi   = fdf.nlargest(1,"ROI Score").iloc[0]
    top_nirf  = fdf.dropna(subset=["NIRF Rank"]).nsmallest(1,"NIRF Rank").iloc[0]

    c1,c2,c3,c4 = st.columns(4)
    cards = [
        (c1,"🎯 Best Placement",  top_place["College Name"], f"{top_place['Placement %']:.0f}%", "placement rate"),
        (c2,"💰 Highest Package", top_pkg["College Name"],   f"₹{top_pkg['Avg Pkg (LPA)']:.0f} LPA", "average package"),
        (c3,"📈 Best ROI",        top_roi["College Name"],   f"{top_roi['ROI Score']:.1f}", "ROI score"),
        (c4,"🏅 Top NIRF Rank",   top_nirf["College Name"],  f"#{int(top_nirf['NIRF Rank'])}", "national rank"),
    ]
    for col, title, name, val, lbl in cards:
        with col:
            st.markdown(f"""
            <div class="insight-card">
                <h4>{title}</h4>
                <div class="big-num">{val}</div>
                <p style="margin-top:4px;font-size:11px;">{lbl}</p>
                <p style="color:#6366f1;font-size:12px;font-weight:600;margin-top:8px;">{name}</p>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 1 – TIER 1 DEEP DIVE
# ═══════════════════════════════════════════════════════════════
elif page == "🏆 Tier 1 College Deep Dive":
    hero("Tier 1 College Deep Dive",
         "IITs, IISc & top research institutions — premium analytics on India's best colleges",
         "TIER 1 ANALYSIS")

    t1 = fdf[fdf["Tier"] == "Tier 1"].copy()
    if len(t1) == 0:
        st.info("No Tier 1 colleges match the current filters."); st.stop()

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Tier 1 Colleges", len(t1))
    c2.metric("Avg Placement %", f"{t1['Placement %'].mean():.1f}%")
    c3.metric("Avg Package", f"₹{t1['Avg Pkg (LPA)'].mean():.1f} LPA")
    c4.metric("Best Package", f"₹{t1['Highest Pkg (LPA)'].max():.0f} LPA")
    c5.metric("Avg NIRF Rank", f"#{t1['NIRF Rank'].mean():.0f}")

    tabs = st.tabs(["📊 Performance", "📍 Geography", "🎓 Academics", "📋 Full Data"])

    # ── Tab 1: Performance ──
    with tabs[0]:
        section("NIRF Rank vs Package vs Placement")
        sorted_t1 = t1.sort_values("NIRF Rank").head(16)
        fig = px.scatter(
            t1, x="NIRF Rank", y="Placement %",
            size="Avg Pkg (LPA)", color="Category",
            hover_name="College Name",
            color_discrete_map=CAT_C,
            size_max=35,
            title="NIRF Rank vs Placement % (bubble = Avg Package)"
        )
        fig.update_traces(marker=dict(opacity=0.85, line=dict(width=1, color="rgba(255,255,255,0.15)")))
        st.plotly_chart(L(fig), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            fig2 = px.bar(
                sorted_t1, x="College Name", y=["Avg Pkg (LPA)","Highest Pkg (LPA)"],
                barmode="group", title="Avg vs Highest Package",
                color_discrete_sequence=["#6366f1","#06b6d4"],
                labels={"value":"Package (LPA)","variable":""}
            )
            fig2.update_xaxes(tickangle=40)
            st.plotly_chart(L(fig2), use_container_width=True)

        with c2:
            fig3 = px.bar(
                sorted_t1.sort_values("Placement %", ascending=True),
                x="Placement %", y="College Name", orientation="h",
                color="Category", color_discrete_map=CAT_C,
                title="Placement % Ranking"
            )
            st.plotly_chart(L(fig3), use_container_width=True)

    # ── Tab 2: Geography ──
    with tabs[1]:
        section("Geographic Distribution")
        c1, c2 = st.columns(2)
        with c1:
            state_t1 = t1.groupby("State").agg(Count=("College Name","count"),
                                                Avg_Pkg=("Avg Pkg (LPA)","mean")).reset_index()
            fig4 = px.bar(state_t1.sort_values("Count", ascending=True),
                          x="Count", y="State", orientation="h",
                          color="Avg_Pkg", color_continuous_scale="Viridis",
                          title="Tier 1 Colleges per State",
                          text="Count")
            fig4.update_traces(textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig4), use_container_width=True)

        with c2:
            loc_df = t1.groupby("Location Type").agg(Count=("College Name","count"),
                                                      Avg_Place=("Placement %","mean")).reset_index()
            fig5 = px.pie(loc_df, names="Location Type", values="Count",
                          color_discrete_sequence=GRAD, hole=0.4,
                          title="Urban vs Semi-Urban Distribution")
            fig5.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(L(fig5), use_container_width=True)

    # ── Tab 3: Academics ──
    with tabs[2]:
        section("Alumni Network & Student Intake")
        c1, c2 = st.columns(2)
        with c1:
            alumni_df = t1.dropna(subset=["Alumni Count"]).sort_values("Alumni Count", ascending=True)
            fig6 = px.bar(alumni_df, x="Alumni Count", y="College Name", orientation="h",
                          color="Alumni Count", color_continuous_scale="Purples",
                          title="Alumni Network Size")
            st.plotly_chart(L(fig6), use_container_width=True)
        with c2:
            fig7 = px.scatter(t1, x="Student Intake", y="Placement %",
                              color="Category", hover_name="College Name",
                              color_discrete_map=CAT_C, size="Avg Pkg (LPA)", size_max=28,
                              title="Student Intake vs Placement %")
            st.plotly_chart(L(fig7), use_container_width=True)

        section("Accreditation Distribution")
        naac_t1 = t1.groupby("NAAC/NBA Status").size().reset_index(name="Count")
        fig8 = px.bar(naac_t1, x="NAAC/NBA Status", y="Count",
                      color="NAAC/NBA Status", color_discrete_sequence=GRAD,
                      title="NAAC/NBA Accreditation – Tier 1 Colleges", text="Count")
        fig8.update_traces(textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig8, showlegend=False), use_container_width=True)

    # ── Tab 4: Data ──
    with tabs[3]:
        section("Complete Tier 1 Dataset")
        cols = ["College Name","Category","State","City","NIRF Rank","NAAC/NBA Status",
                "Ownership Type","Placement %","Avg Pkg","Highest Pkg","Student Intake","ROI Score"]
        st.dataframe(t1[cols].sort_values("NIRF Rank").reset_index(drop=True),
                     use_container_width=True, height=500)


# ═══════════════════════════════════════════════════════════════
# PAGE 2 – STATE-WISE DISTRIBUTION
# ═══════════════════════════════════════════════════════════════
elif page == "🗺️ State-wise Distribution":
    hero("State-wise College Distribution",
         "Geographic intelligence — how top colleges are distributed across India's states",
         "GEO ANALYTICS")

    ss = fdf.groupby("State").agg(
        Count=("College Name","count"),
        Avg_Placement=("Placement %","mean"),
        Avg_Package=("Avg Pkg (LPA)","mean"),
        Total_Intake=("Student Intake","sum"),
        Tier1=("Tier", lambda x: (x=="Tier 1").sum()),
        Tier2=("Tier", lambda x: (x=="Tier 2").sum()),
        Tier3=("Tier", lambda x: (x=="Tier 3").sum()),
    ).reset_index().round(2)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("States", len(ss))
    c2.metric("Total Colleges", len(fdf))
    c3.metric("Best Placement State", ss.loc[ss["Avg_Placement"].idxmax(),"State"])
    c4.metric("Best Package State",   ss.loc[ss["Avg_Package"].idxmax(),"State"])

    tabs = st.tabs(["📊 Distribution", "💰 Package Map", "🎯 Placement Map", "📋 State Table"])

    with tabs[0]:
        section("College Count & Tier Mix by State")
        tier_state = fdf.groupby(["State","Tier"]).size().reset_index(name="Count")
        fig = px.bar(tier_state.sort_values("Count", ascending=False),
                     x="State", y="Count", color="Tier",
                     color_discrete_map=TIER_C,
                     title="Stacked Tier Distribution by State")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(L(fig), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            fig2 = px.bar(ss.sort_values("Count", ascending=True),
                          x="Count", y="State", orientation="h",
                          color="Count", color_continuous_scale="Blues",
                          title="Number of Colleges per State", text="Count")
            fig2.update_traces(textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig2), use_container_width=True)
        with c2:
            cat_state = fdf.groupby(["State","Category"]).size().reset_index(name="Count")
            fig3 = px.bar(cat_state, x="State", y="Count", color="Category",
                          color_discrete_map=CAT_C,
                          title="Category Mix by State")
            fig3.update_xaxes(tickangle=45)
            st.plotly_chart(L(fig3), use_container_width=True)

    with tabs[1]:
        section("Average Package by State")
        fig4 = px.bar(ss.sort_values("Avg_Package", ascending=False),
                      x="State", y="Avg_Package",
                      color="Avg_Package", color_continuous_scale="Viridis",
                      title="Average Package (LPA) — State Ranking",
                      text=ss.sort_values("Avg_Package", ascending=False)["Avg_Package"].apply(lambda x: f"₹{x}"))
        fig4.update_traces(textposition="outside", textfont_color="#e2e8f0")
        fig4.update_xaxes(tickangle=45)
        st.plotly_chart(L(fig4), use_container_width=True)

        fig5 = px.scatter(ss, x="Avg_Package", y="Count",
                          size="Total_Intake", text="State",
                          color="Avg_Placement", color_continuous_scale="Plasma",
                          title="Package vs College Count (bubble = total intake, color = avg placement)")
        fig5.update_traces(textposition="top center", textfont=dict(color="#e2e8f0", size=10))
        st.plotly_chart(L(fig5), use_container_width=True)

    with tabs[2]:
        section("Placement Performance by State")
        fig6 = px.bar(ss.sort_values("Avg_Placement", ascending=True),
                      x="Avg_Placement", y="State", orientation="h",
                      color="Avg_Placement", color_continuous_scale="Teal",
                      title="Average Placement % by State",
                      text=ss.sort_values("Avg_Placement")["Avg_Placement"].apply(lambda x: f"{x:.1f}%"))
        fig6.update_traces(textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig6), use_container_width=True)

    with tabs[3]:
        section("State-wise Summary")
        ss_display = ss.copy()
        ss_display.columns = ["State","Colleges","Avg Placement (%)","Avg Package (LPA)",
                               "Total Intake","Tier 1","Tier 2","Tier 3"]
        st.dataframe(ss_display.sort_values("Colleges", ascending=False).reset_index(drop=True),
                     use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 3 – PLACEMENT ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif page == "💼 Placement Analysis":
    hero("Placement Analysis Dashboard",
         "Deep dive into placement rates, salary packages & employment trends across colleges",
         "PLACEMENT INTELLIGENCE")

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Avg Placement %", f"{fdf['Placement %'].mean():.1f}%")
    c2.metric("100% Placed Colleges", len(fdf[fdf["Placement %"]==100]))
    c3.metric("Avg Package", f"₹{fdf['Avg Pkg (LPA)'].mean():.1f} LPA")
    c4.metric("Max Package", f"₹{fdf['Highest Pkg (LPA)'].max():.0f} LPA")
    c5.metric("Median Package", f"₹{fdf['Avg Pkg (LPA)'].median():.1f} LPA")

    tabs = st.tabs(["📈 Distributions","🏆 Rankings","📊 Comparisons","🔗 Correlations"])

    with tabs[0]:
        section("Placement % & Package Distributions")
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(fdf, x="Placement %", nbins=10,
                               color="Tier", color_discrete_map=TIER_C,
                               barmode="overlay", opacity=0.75,
                               title="Placement % Distribution by Tier",
                               marginal="rug")
            st.plotly_chart(L(fig), use_container_width=True)
        with c2:
            fig2 = px.histogram(fdf.dropna(subset=["Avg Pkg (LPA)"]),
                                x="Avg Pkg (LPA)", nbins=12,
                                color="Category", color_discrete_map=CAT_C,
                                barmode="overlay", opacity=0.75,
                                title="Avg Package Distribution by Category",
                                marginal="box")
            st.plotly_chart(L(fig2), use_container_width=True)

        section("Package Range — Box Plots")
        c1, c2 = st.columns(2)
        with c1:
            fig3 = px.box(fdf.dropna(subset=["Avg Pkg (LPA)"]),
                          x="Tier", y="Avg Pkg (LPA)",
                          color="Tier", color_discrete_map=TIER_C,
                          points="all", hover_name="College Name",
                          title="Avg Package Distribution by Tier")
            st.plotly_chart(L(fig3), use_container_width=True)
        with c2:
            fig4 = px.box(fdf.dropna(subset=["Avg Pkg (LPA)"]),
                          x="Category", y="Avg Pkg (LPA)",
                          color="Category", color_discrete_map=CAT_C,
                          points="all", hover_name="College Name",
                          title="Avg Package Distribution by Category")
            fig4.update_xaxes(tickangle=30)
            st.plotly_chart(L(fig4), use_container_width=True)

    with tabs[1]:
        section("Top 20 Colleges by Placement %")
        top20p = fdf.nlargest(20,"Placement %")
        fig5 = px.bar(top20p.sort_values("Placement %"),
                      x="Placement %", y="College Name", orientation="h",
                      color="Tier", color_discrete_map=TIER_C,
                      text="Placement %",
                      title="Top 20 Colleges — Placement %")
        fig5.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig5), use_container_width=True)

        section("Top 20 Colleges by Average Package")
        top20k = fdf.nlargest(20,"Avg Pkg (LPA)")
        fig6 = px.bar(top20k.sort_values("Avg Pkg (LPA)"),
                      x="Avg Pkg (LPA)", y="College Name", orientation="h",
                      color="Category", color_discrete_map=CAT_C,
                      text="Avg Pkg (LPA)",
                      title="Top 20 Colleges — Avg Package (LPA)")
        fig6.update_traces(texttemplate="₹%{text}", textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig6), use_container_width=True)

    with tabs[2]:
        section("Tier & Ownership Comparisons")
        c1, c2 = st.columns(2)
        with c1:
            tier_agg = fdf.groupby("Tier").agg(
                Avg_P=("Placement %","mean"),
                Avg_K=("Avg Pkg (LPA)","mean"),
                Max_K=("Highest Pkg (LPA)","mean")
            ).reset_index()
            fig7 = go.Figure()
            fig7.add_trace(go.Bar(name="Avg Placement %", x=tier_agg["Tier"],
                                  y=tier_agg["Avg_P"].round(1), marker_color="#6366f1",
                                  yaxis="y", text=tier_agg["Avg_P"].round(1),
                                  texttemplate="%{text}%", textposition="outside",
                                  textfont=dict(color="#e2e8f0")))
            fig7.add_trace(go.Bar(name="Avg Package (LPA)", x=tier_agg["Tier"],
                                  y=tier_agg["Avg_K"].round(1), marker_color="#06b6d4",
                                  yaxis="y2", text=tier_agg["Avg_K"].round(1),
                                  texttemplate="₹%{text}", textposition="outside",
                                  textfont=dict(color="#e2e8f0")))
            fig7.update_layout(**BASE, title="Tier: Placement % vs Package",
                               barmode="group",
                               yaxis2=dict(title="Package (LPA)", overlaying="y", side="right",
                                           tickfont=dict(color="#475569")))
            fig7.update_yaxes(title_text="Placement %", secondary_y=False)
            st.plotly_chart(fig7, use_container_width=True)

        with c2:
            own_agg = fdf.groupby("Ownership Type").agg(
                Avg_P=("Placement %","mean"),
                Avg_K=("Avg Pkg (LPA)","mean"),
                Count=("College Name","count")
            ).reset_index()
            fig8 = px.scatter(own_agg, x="Avg_K", y="Avg_P",
                              size="Count", color="Ownership Type",
                              color_discrete_sequence=GRAD,
                              text="Ownership Type",
                              title="Ownership Type: Package vs Placement")
            fig8.update_traces(textposition="top center", textfont=dict(color="#e2e8f0", size=10))
            st.plotly_chart(L(fig8), use_container_width=True)

    with tabs[3]:
        section("Correlation: What drives placement?")
        corr_df = fdf[["Placement %","Avg Pkg (LPA)","Highest Pkg (LPA)",
                        "Student Intake","NIRF Rank","Recruiter Count",
                        "Partner Count","Alumni Count"]].dropna()
        corr = corr_df.corr().round(2)
        fig9 = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.index,
            colorscale=[[0,"#f43f5e"],[0.5,"#060b18"],[1,"#6366f1"]],
            zmid=0, text=corr.values,
            texttemplate="%{text}", textfont=dict(size=10, color="#e2e8f0"),
            showscale=True,
            colorbar=dict(tickfont=dict(color="#64748b"))
        ))
        fig9.update_layout(**BASE, title="Correlation Matrix — Key Metrics")
        fig9.update_xaxes(tickangle=30)
        st.plotly_chart(fig9, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 4 – RECRUITER & INDUSTRY NETWORK
# ═══════════════════════════════════════════════════════════════
elif page == "🤝 Recruiter & Industry Network":
    hero("Recruiter & Industry Network",
         "Who's hiring from India's top colleges — recruiter frequency, reach & hiring patterns",
         "RECRUITER INTELLIGENCE")

    all_rec  = [r for lst in fdf["Recruiter List"]  for r in lst]
    all_part = [r for lst in fdf["Partner List"]     for r in lst]
    rec_ctr  = Counter(all_rec)
    part_ctr = Counter(all_part)
    top_rec  = pd.DataFrame(rec_ctr.most_common(25),  columns=["Company","Colleges"])
    top_part = pd.DataFrame(part_ctr.most_common(25), columns=["Company","Colleges"])

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Unique Recruiters",       len(rec_ctr))
    c2.metric("Unique Industry Partners",len(part_ctr))
    c3.metric("Top Recruiter",           rec_ctr.most_common(1)[0][0])
    c4.metric("Avg Recruiters/College",  f"{fdf['Recruiter Count'].mean():.1f}")

    tabs = st.tabs(["🏢 Top Recruiters","🤝 Industry Partners","📊 Network Analysis","🔬 Internships"])

    with tabs[0]:
        section("Top 25 Recruiters by College Reach")
        fig = px.bar(top_rec.sort_values("Colleges"),
                     x="Colleges", y="Company", orientation="h",
                     color="Colleges", color_continuous_scale="Viridis",
                     title="Top 25 Recruiters (number of colleges they recruit from)",
                     text="Colleges")
        fig.update_traces(textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig), use_container_width=True)

        # Chip display
        section("🔥 Top 15 Most Active Recruiters")
        chip_colors = ["chip-blue","chip-cyan","chip-green","chip-amber"]
        chips = "".join([
            f'<span class="chip {chip_colors[i%4]}">{r} <b>({c})</b></span>'
            for i,(r,c) in enumerate(rec_ctr.most_common(15))
        ])
        st.markdown(f'<div class="chip-grid">{chips}</div>', unsafe_allow_html=True)

    with tabs[1]:
        section("Top 25 Industry Partners")
        fig2 = px.bar(top_part.sort_values("Colleges"),
                      x="Colleges", y="Company", orientation="h",
                      color="Colleges", color_continuous_scale="Plasma",
                      title="Top 25 Industry Partners",
                      text="Colleges")
        fig2.update_traces(textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig2), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            fig3 = px.pie(top_rec.head(10), names="Company", values="Colleges",
                          color_discrete_sequence=GRAD, hole=0.4,
                          title="Top 10 Recruiter Share")
            fig3.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(L(fig3), use_container_width=True)
        with c2:
            fig4 = px.pie(top_part.head(10), names="Company", values="Colleges",
                          color_discrete_sequence=GRAD, hole=0.4,
                          title="Top 10 Partner Share")
            fig4.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(L(fig4), use_container_width=True)

    with tabs[2]:
        section("Recruiter Network vs Placement Outcomes")
        c1, c2 = st.columns(2)
        with c1:
            fig5 = px.scatter(fdf, x="Recruiter Count", y="Placement %",
                              color="Tier", hover_name="College Name",
                              size="Avg Pkg (LPA)", size_max=28,
                              color_discrete_map=TIER_C,
                              title="Recruiter Count vs Placement %")
            fig5.update_traces(marker=dict(opacity=0.85))
            st.plotly_chart(L(fig5), use_container_width=True)
        with c2:
            fig6 = px.scatter(fdf, x="Partner Count", y="Avg Pkg (LPA)",
                              color="Tier", hover_name="College Name",
                              size="Placement %", size_max=28,
                              color_discrete_map=TIER_C,
                              title="Industry Partners vs Avg Package")
            st.plotly_chart(L(fig6), use_container_width=True)

        section("Recruiter & Partner Count by Tier")
        tier_net = fdf.groupby("Tier")[["Recruiter Count","Partner Count"]].mean().reset_index()
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(name="Avg Recruiters", x=tier_net["Tier"],
                              y=tier_net["Recruiter Count"].round(1),
                              marker_color="#6366f1", text=tier_net["Recruiter Count"].round(1),
                              textposition="outside", textfont=dict(color="#e2e8f0")))
        fig7.add_trace(go.Bar(name="Avg Partners", x=tier_net["Tier"],
                              y=tier_net["Partner Count"].round(1),
                              marker_color="#06b6d4", text=tier_net["Partner Count"].round(1),
                              textposition="outside", textfont=dict(color="#e2e8f0")))
        fig7.update_layout(**BASE, barmode="group", title="Network Depth by Tier")
        st.plotly_chart(fig7, use_container_width=True)

    with tabs[3]:
        section("Internship Ecosystem")
        all_intern = [c for lst in fdf["Internship Companies"] for c in lst]
        intern_ctr = Counter(all_intern)
        intern_df  = pd.DataFrame(intern_ctr.most_common(20), columns=["Company","Count"])
        c1, c2 = st.columns(2)
        with c1:
            fig8 = px.bar(intern_df.sort_values("Count"),
                          x="Count", y="Company", orientation="h",
                          color="Count", color_continuous_scale="Teal",
                          title="Top 20 Internship Providers", text="Count")
            fig8.update_traces(textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig8), use_container_width=True)
        with c2:
            fig9 = px.scatter(fdf, x="Internship Count", y="Placement %",
                              color="Tier", hover_name="College Name",
                              color_discrete_map=TIER_C, size="Avg Pkg (LPA)", size_max=25,
                              title="Internship Variety vs Placement %")
            st.plotly_chart(L(fig9), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 5 – COLLEGE COMPARISON TOOL
# ═══════════════════════════════════════════════════════════════
elif page == "⚖️ College Comparison Tool":
    hero("College Comparison Tool",
         "Select any colleges and compare them side-by-side across every dimension",
         "COMPARISON ENGINE")

    all_colleges = sorted(fdf["College Name"].dropna().unique())
    defaults     = all_colleges[:min(5, len(all_colleges))]
    sel = st.multiselect("🔍 Select colleges to compare (up to 10)", all_colleges,
                         default=defaults, max_selections=10)
    if not sel:
        st.info("Select at least 2 colleges above to begin comparison.")
        st.stop()

    cdf = fdf[fdf["College Name"].isin(sel)].copy()

    # ── Summary pills ──
    st.markdown('<div class="stat-row">' + "".join([
        f'<div class="stat-pill"><span>{r["College Name"].split("(")[0].strip()}</span> — {r["Tier"]} | ₹{r["Avg Pkg (LPA)"]} LPA | {r["Placement %"]}% placed</div>'
        for _, r in cdf.iterrows()
    ]) + '</div>', unsafe_allow_html=True)

    tabs = st.tabs(["🕸️ Radar View","📊 Bar Charts","📈 Scatter","📋 Data Table"])

    with tabs[0]:
        section("Multi-Metric Radar Comparison")
        metrics = ["Placement %","Avg Pkg (LPA)","Highest Pkg (LPA)","Student Intake","Recruiter Count","Partner Count"]
        rdf = cdf[["College Name"]+metrics].dropna().copy()
        def norm(s):
            mn,mx = s.min(), s.max()
            return (s-mn)/(mx-mn)*100 if mx!=mn else s*0+50
        for m in metrics:
            rdf[m] = norm(rdf[m])

        fig = go.Figure()
        for i, (_, row) in enumerate(rdf.iterrows()):
            v = [row[m] for m in metrics]
            fig.add_trace(go.Scatterpolar(
                r=v+[v[0]], theta=metrics+[metrics[0]],
                fill="toself", name=row["College Name"],
                line=dict(color=GRAD[i % len(GRAD)], width=2),
                fillcolor=GRAD[i % len(GRAD)].replace(")", ",0.12)").replace("rgb","rgba") if "rgb" in GRAD[i%len(GRAD)] else GRAD[i%len(GRAD)]+"20"
            ))
        fig.update_layout(
            **BASE,
            polar=dict(
                bgcolor="rgba(6,11,24,0.8)",
                radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color="#475569"), gridcolor="rgba(99,102,241,0.15)"),
                angularaxis=dict(tickfont=dict(color="#94a3b8"), gridcolor="rgba(99,102,241,0.15)")
            ),
            title="Normalised Multi-Metric Radar (100 = best in selection)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        section("Side-by-Side Bar Comparisons")
        metrics_bar = {
            "Placement %": ("Placement %","Placement %"),
            "Avg Package (LPA)": ("Avg Pkg (LPA)","₹ LPA"),
            "Highest Package (LPA)": ("Highest Pkg (LPA)","₹ LPA"),
            "Student Intake": ("Student Intake","Students"),
        }
        cols_iter = iter(st.columns(2))
        for label, (col, unit) in metrics_bar.items():
            c = next(cols_iter, None)
            if c is None:
                cols_iter = iter(st.columns(2)); c = next(cols_iter)
            with c:
                d = cdf.dropna(subset=[col]).sort_values(col, ascending=False)
                fig = px.bar(d, x="College Name", y=col,
                             color="College Name", color_discrete_sequence=GRAD,
                             title=label, text=col)
                fig.update_traces(texttemplate="%{text:.1f}", textposition="outside",
                                  textfont_color="#e2e8f0")
                fig.update_xaxes(tickangle=30)
                st.plotly_chart(L(fig, showlegend=False), use_container_width=True)

    with tabs[2]:
        section("Placement vs Package Scatter")
        fig2 = px.scatter(cdf, x="Avg Pkg (LPA)", y="Placement %",
                          color="College Name", color_discrete_sequence=GRAD,
                          size="Student Intake", size_max=40,
                          hover_name="College Name",
                          text="College Name",
                          title="Package vs Placement (bubble = intake)")
        fig2.update_traces(textposition="top center", textfont=dict(size=9, color="#e2e8f0"),
                           marker=dict(opacity=0.85))
        st.plotly_chart(L(fig2), use_container_width=True)

        section("NIRF Rank vs ROI Score")
        nirf_cdf = cdf.dropna(subset=["NIRF Rank"])
        if len(nirf_cdf):
            fig3 = px.scatter(nirf_cdf, x="NIRF Rank", y="ROI Score",
                              color="College Name", color_discrete_sequence=GRAD,
                              size="Avg Pkg (LPA)", size_max=35,
                              hover_name="College Name",
                              title="NIRF Rank vs ROI Score")
            st.plotly_chart(L(fig3), use_container_width=True)

    with tabs[3]:
        section("Full Comparison Table")
        show = ["College Name","Tier","Category","State","NIRF Rank","NAAC/NBA Status",
                "Placement %","Avg Pkg (LPA)","Highest Pkg (LPA)","Student Intake",
                "Recruiter Count","Partner Count","ROI Score","Ownership Type"]
        st.dataframe(cdf[show].set_index("College Name"), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 6 – ROI & VALUE ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif page == "💰 ROI & Value Analysis":
    hero("ROI & Value Analysis",
         "Which colleges deliver the best return on your educational investment?",
         "VALUE INTELLIGENCE")

    roi_df = fdf.dropna(subset=["Avg Pkg (LPA)","Placement %"]).copy()
    roi_df["ROI Score"] = (roi_df["Placement %"] * roi_df["Avg Pkg (LPA)"] / 100).round(2)
    roi_df["Value Grade"] = pd.cut(roi_df["ROI Score"],
                                   bins=[0,10,16,22,30],
                                   labels=["C — Fair","B — Good","A — Great","S — Exceptional"])

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Top ROI Score",    f"{roi_df['ROI Score'].max():.1f}")
    c2.metric("Avg ROI Score",    f"{roi_df['ROI Score'].mean():.1f}")
    c3.metric("S-Grade Colleges", len(roi_df[roi_df["Value Grade"]=="S — Exceptional"]))
    c4.metric("Best Value Tier",  roi_df.groupby("Tier")["ROI Score"].mean().idxmax())
    c5.metric("Best Value State", roi_df.groupby("State")["ROI Score"].mean().idxmax())

    tabs = st.tabs(["🏆 Leaderboard","📊 Grade Analysis","🗺️ State ROI","🔗 ROI Matrix","📋 Full Table"])

    with tabs[0]:
        section("ROI Leaderboard — Top 20 Colleges")
        top_roi = roi_df.nlargest(20,"ROI Score")
        fig = px.bar(top_roi.sort_values("ROI Score"),
                     x="ROI Score", y="College Name", orientation="h",
                     color="Value Grade",
                     color_discrete_map={
                         "S — Exceptional":"#6366f1","A — Great":"#06b6d4",
                         "B — Good":"#10b981","C — Fair":"#f59e0b"
                     },
                     text="ROI Score",
                     title="Top 20 Colleges by ROI Score")
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside",
                          textfont_color="#e2e8f0")
        st.plotly_chart(L(fig), use_container_width=True)

        section("ROI Bubble Matrix")
        fig2 = px.scatter(roi_df, x="Avg Pkg (LPA)", y="Placement %",
                          size="ROI Score", color="Tier",
                          hover_name="College Name",
                          color_discrete_map=TIER_C, size_max=45,
                          title="ROI Matrix: Package vs Placement (bubble = ROI score)")
        fig2.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="rgba(255,255,255,0.15)")))
        st.plotly_chart(L(fig2), use_container_width=True)

    with tabs[1]:
        section("Value Grade Distribution")
        c1, c2 = st.columns(2)
        with c1:
            grade_df = roi_df.groupby("Value Grade").size().reset_index(name="Count")
            fig3 = px.pie(grade_df, names="Value Grade", values="Count",
                          color_discrete_map={
                              "S — Exceptional":"#6366f1","A — Great":"#06b6d4",
                              "B — Good":"#10b981","C — Fair":"#f59e0b"
                          }, hole=0.5,
                          title="Colleges by Value Grade")
            fig3.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(L(fig3), use_container_width=True)
        with c2:
            cat_roi = roi_df.groupby("Category")["ROI Score"].mean().reset_index().sort_values("ROI Score", ascending=True)
            fig4 = px.bar(cat_roi, x="ROI Score", y="Category", orientation="h",
                          color="ROI Score", color_continuous_scale="Viridis",
                          title="Average ROI Score by Category", text="ROI Score")
            fig4.update_traces(texttemplate="%{text:.1f}", textposition="outside",
                               textfont_color="#e2e8f0")
            st.plotly_chart(L(fig4), use_container_width=True)

        section("ROI Score Distribution by Tier")
        fig5 = px.box(roi_df, x="Tier", y="ROI Score",
                      color="Tier", color_discrete_map=TIER_C,
                      points="all", hover_name="College Name",
                      title="ROI Score Spread by Tier")
        st.plotly_chart(L(fig5), use_container_width=True)

    with tabs[2]:
        section("State-wise ROI Performance")
        state_roi = roi_df.groupby("State").agg(
            Avg_ROI=("ROI Score","mean"),
            Max_ROI=("ROI Score","max"),
            Count=("College Name","count")
        ).reset_index().sort_values("Avg_ROI", ascending=False)

        fig6 = px.bar(state_roi, x="State", y="Avg_ROI",
                      color="Avg_ROI", color_continuous_scale="Plasma",
                      title="Average ROI Score by State",
                      text=state_roi["Avg_ROI"].round(1))
        fig6.update_traces(textposition="outside", textfont_color="#e2e8f0")
        fig6.update_xaxes(tickangle=45)
        st.plotly_chart(L(fig6), use_container_width=True)

        fig7 = px.scatter(state_roi, x="Count", y="Avg_ROI",
                          size="Max_ROI", text="State",
                          color="Avg_ROI", color_continuous_scale="Viridis",
                          title="State: College Count vs Avg ROI (bubble = best ROI in state)")
        fig7.update_traces(textposition="top center", textfont=dict(color="#e2e8f0", size=10))
        st.plotly_chart(L(fig7), use_container_width=True)

    with tabs[3]:
        section("ROI vs NIRF Rank")
        nirf_roi = roi_df.dropna(subset=["NIRF Rank"])
        fig8 = px.scatter(nirf_roi, x="NIRF Rank", y="ROI Score",
                          color="Category", size="Avg Pkg (LPA)",
                          hover_name="College Name",
                          color_discrete_map=CAT_C, size_max=30,
                          title="ROI Score vs NIRF Rank (lower rank = better nationally ranked)")
        fig8.update_traces(marker=dict(opacity=0.85))
        st.plotly_chart(L(fig8), use_container_width=True)

        section("ROI vs Alumni Network")
        alumni_roi = roi_df.dropna(subset=["Alumni Count"])
        fig9 = px.scatter(alumni_roi, x="Alumni Count", y="ROI Score",
                          color="Tier", size="Placement %", size_max=25,
                          hover_name="College Name",
                          color_discrete_map=TIER_C,
                          title="Alumni Network Size vs ROI Score")
        st.plotly_chart(L(fig9), use_container_width=True)

    with tabs[4]:
        section("Complete ROI Rankings")
        table = roi_df[["College Name","Tier","Category","State","Placement %",
                         "Avg Pkg (LPA)","Highest Pkg (LPA)","ROI Score","Value Grade","NIRF Rank"]] \
            .sort_values("ROI Score", ascending=False).reset_index(drop=True)
        table.index += 1
        st.dataframe(table, use_container_width=True, height=500)

        st.markdown("""
        <div class="insight-card" style="margin-top:16px;">
          <h4>📌 ROI Score Methodology</h4>
          <p>
            <b style="color:#a5b4fc;">ROI Score = (Placement % × Avg Package LPA) / 100</b><br><br>
            A composite metric rewarding colleges that deliver both high placement rates AND competitive salaries.
            Grading: <b style="color:#6366f1;">S (&gt;22)</b> Exceptional &nbsp;|&nbsp;
            <b style="color:#06b6d4;">A (16–22)</b> Great &nbsp;|&nbsp;
            <b style="color:#10b981;">B (10–16)</b> Good &nbsp;|&nbsp;
            <b style="color:#f59e0b;">C (&lt;10)</b> Fair
          </p>
        </div>""", unsafe_allow_html=True)
