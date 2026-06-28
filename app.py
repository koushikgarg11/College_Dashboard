import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from data_utils import load_data

st.set_page_config(
    page_title="NexusIQ — India's Tier 1 Engineering Intelligence Vault",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
}
[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px; padding: 20px 16px;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.06em; }
[data-testid="stMetricValue"] { color: #f8fafc !important; font-size: 26px !important; font-weight: 800 !important; font-family: 'Space Grotesk', sans-serif !important; }
.hero-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(6,182,212,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.2); border-radius: 20px;
    padding: 28px 32px; margin-bottom: 24px;
}
.hero-badge {
    display: inline-block; padding: 4px 12px;
    background: rgba(99,102,241,0.2); border: 1px solid rgba(99,102,241,0.4);
    border-radius: 20px; font-size: 10px; color: #a5b4fc;
    font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif; font-size: 1.85rem; font-weight: 700;
    background: linear-gradient(135deg, #a5b4fc, #67e8f9);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 6px 0;
}
.hero-subtitle { color: #64748b; font-size: 0.88rem; margin: 0; }
.sec-hdr {
    display: flex; align-items: center; gap: 10px;
    color: #e2e8f0; font-size: 0.95rem; font-weight: 600;
    margin: 26px 0 14px 0;
}
.sec-hdr::before {
    content: ''; width: 4px; height: 20px;
    background: linear-gradient(180deg, #6366f1, #06b6d4);
    border-radius: 2px; flex-shrink: 0;
}
.insight-card {
    background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9));
    border: 1px solid rgba(99,102,241,0.2); border-radius: 14px;
    padding: 18px 20px; margin: 4px 0;
}
.insight-card h4 { color: #a5b4fc; font-size: 11px; font-weight: 700; margin: 0 0 6px 0; text-transform: uppercase; letter-spacing: 0.06em; }
.insight-card .big { font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 700; color: #f1f5f9; }
.insight-card .name { color: #6366f1; font-size: 12px; font-weight: 600; margin-top: 6px; }
.insight-card .sub { color: #64748b; font-size: 11px; margin: 2px 0 0 0; }
.chip-wrap { display: flex; flex-wrap: wrap; gap: 8px; }
.chip { padding: 5px 13px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid; }
.c1 { background: rgba(99,102,241,0.12); color: #a5b4fc; border-color: rgba(99,102,241,0.3); }
.c2 { background: rgba(6,182,212,0.12);  color: #67e8f9; border-color: rgba(6,182,212,0.3);  }
.c3 { background: rgba(16,185,129,0.12); color: #6ee7b7; border-color: rgba(16,185,129,0.3); }
.c4 { background: rgba(245,158,11,0.12); color: #fcd34d; border-color: rgba(245,158,11,0.3); }
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid rgba(99,102,241,0.15); }
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.8); border-radius: 10px; padding: 4px; gap: 4px;
    border: 1px solid rgba(99,102,241,0.15);
}
.stTabs [data-baseweb="tab"] { color: #64748b; border-radius: 7px; font-size: 13px; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background: linear-gradient(135deg,#6366f1,#4f46e5); color: white !important; }
h1,h2,h3,h4 { color: #e2e8f0; }
p, li { color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ── Theme constants ──────────────────────────────────────────────────────────
BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(6,11,24,0.6)",
    font=dict(family="Inter", color="#94a3b8", size=11),
    title_font=dict(color="#e2e8f0", size=14, family="Space Grotesk"),
    legend=dict(bgcolor="rgba(15,23,42,0.85)", bordercolor="rgba(99,102,241,0.2)",
                borderwidth=1, font=dict(color="#cbd5e1", size=11)),
    xaxis=dict(gridcolor="rgba(30,41,59,0.9)", zerolinecolor="rgba(99,102,241,0.15)",
               tickfont=dict(color="#475569", size=10)),
    yaxis=dict(gridcolor="rgba(30,41,59,0.9)", zerolinecolor="rgba(99,102,241,0.15)",
               tickfont=dict(color="#475569", size=10)),
    margin=dict(l=40, r=20, t=48, b=40),
    hoverlabel=dict(bgcolor="rgba(15,23,42,0.95)", bordercolor="rgba(99,102,241,0.4)",
                    font=dict(color="#e2e8f0", size=12)),
)
COLORS = ["#6366f1","#06b6d4","#10b981","#f59e0b","#f43f5e","#8b5cf6","#ec4899","#14b8a6","#f97316","#84cc16"]
TIER_C = {"Tier 1":"#6366f1","Tier 2":"#06b6d4","Tier 3":"#10b981"}
CAT_C  = {
    "IIT":"#6366f1","Research Institute":"#a78bfa","IIIT":"#06b6d4","NIT":"#10b981",
    "Deemed University":"#f59e0b","State University":"#f43f5e",
    "Engineering College":"#ec4899","University":"#14b8a6",
}
GRADE_C = {
    "S — Exceptional": "#6366f1",
    "A — Great":       "#06b6d4",
    "B — Good":        "#10b981",
    "C — Fair":        "#f59e0b",
}


def L(fig, **kw):
    d = dict(BASE); d.update(kw); fig.update_layout(**d); return fig


def sec(txt):
    st.markdown(f'<div class="sec-hdr">{txt}</div>', unsafe_allow_html=True)


def hero(title, subtitle, badge):
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-badge">{badge}</div>
        <p class="hero-title">{title}</p>
        <p class="hero-subtitle">{subtitle}</p>
    </div>""", unsafe_allow_html=True)


# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:8px 0 16px 0;'>
      <div style='font-family:Space Grotesk;font-size:1.15rem;font-weight:700;
           background:linear-gradient(135deg,#a5b4fc,#67e8f9);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
        🔬 NexusIQ
      </div>
      <div style='font-size:10px;color:#475569;margin-top:3px;'>
        India's Engineering Intelligence Vault
      </div>
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
    sel_tier   = st.multiselect("Tier",          sorted(df["Tier"].dropna().unique()))
    sel_states = st.multiselect("State",         sorted(df["State"].dropna().unique()))
    sel_cats   = st.multiselect("Category",      sorted(df["Category"].dropna().unique()))
    sel_own    = st.multiselect("Ownership",     sorted(df["Ownership Type"].dropna().unique()))
    sel_naac   = st.multiselect("Accreditation", sorted(df["NAAC/NBA Status"].dropna().unique()))
    st.markdown("---")

    _pkg_min = int(df["Avg Pkg (LPA)"].min(skipna=True))
    _pkg_max = int(df["Avg Pkg (LPA)"].max(skipna=True))
    pkg_rng  = st.slider("Avg Package (LPA)", _pkg_min, _pkg_max, (_pkg_min, _pkg_max))

    _pl_min = int(df["Placement %"].min())
    _pl_max = int(df["Placement %"].max())
    pl_rng  = st.slider("Placement %", _pl_min, _pl_max, (_pl_min, _pl_max))

    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center;'>
      <div style='font-size:10px;color:#475569;'>Showing</div>
      <div style='font-family:Space Grotesk;font-size:1.6rem;font-weight:700;color:#a5b4fc;'>{len(df)}</div>
      <div style='font-size:10px;color:#475569;'>colleges across {df['State'].nunique()} states</div>
    </div>""", unsafe_allow_html=True)


# ── Filter ────────────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_tier:   fdf = fdf[fdf["Tier"].isin(sel_tier)]
if sel_states: fdf = fdf[fdf["State"].isin(sel_states)]
if sel_cats:   fdf = fdf[fdf["Category"].isin(sel_cats)]
if sel_own:    fdf = fdf[fdf["Ownership Type"].isin(sel_own)]
if sel_naac:   fdf = fdf[fdf["NAAC/NBA Status"].isin(sel_naac)]
fdf = fdf[
    (fdf["Avg Pkg (LPA)"].fillna(0) >= pkg_rng[0]) &
    (fdf["Avg Pkg (LPA)"].fillna(0) <= pkg_rng[1])
]
fdf = fdf[
    (fdf["Placement %"] >= pl_rng[0]) &
    (fdf["Placement %"] <= pl_rng[1])
]

if len(fdf) == 0:
    st.warning("⚠️ No colleges match your current filters. Please adjust the sidebar filters.")
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 0 – OVERVIEW & HIGHLIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview & Highlights":
    hero(
        "NexusIQ — India's Engineering Intelligence Vault",
        "The definitive database of India's top engineering colleges — placements, packages, recruiters, ROI & more",
        "OVERVIEW DASHBOARD",
    )

    all_rec = [r for lst in fdf["Recruiter List"] for r in lst]
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Colleges",    len(fdf))
    c2.metric("States Covered",    fdf["State"].nunique())
    c3.metric("Avg Placement",     f"{fdf['Placement %'].mean():.1f}%")
    c4.metric("Avg Package",       f"₹{fdf['Avg Pkg (LPA)'].mean():.1f} LPA")
    c5.metric("Top Pkg (Domestic)",f"₹{fdf['Highest Pkg (LPA)'].max():.0f} LPA")
    c6.metric("Unique Recruiters", len(set(all_rec)))

    # ── Tier & Category Breakdown ──
    sec("Tier & Category Breakdown")
    c1, c2, c3 = st.columns([1.1, 1.1, 0.9])

    with c1:
        tier_agg = fdf.groupby("Tier").agg(Count=("College Name", "count")).reset_index()
        fig = px.bar(tier_agg, x="Tier", y="Count",
                     color="Tier", color_discrete_map=TIER_C,
                     text="Count", title="Colleges by Tier")
        fig.update_traces(textposition="outside", textfont_color="#e2e8f0", marker_line_width=0)
        st.plotly_chart(L(fig, showlegend=False), use_container_width=True)

    with c2:
        cat_agg = (fdf.groupby("Category").size()
                   .reset_index(name="Count")
                   .sort_values("Count", ascending=False))
        fig2 = px.bar(cat_agg, x="Category", y="Count",
                      color="Category", color_discrete_map=CAT_C,
                      text="Count", title="Colleges by Category")
        fig2.update_traces(textposition="outside", textfont_color="#e2e8f0", marker_line_width=0)
        fig2.update_xaxes(tickangle=30)
        st.plotly_chart(L(fig2, showlegend=False), use_container_width=True)

    with c3:
        naac_agg = fdf.groupby("NAAC/NBA Status").size().reset_index(name="Count")
        fig3 = px.pie(naac_agg, names="NAAC/NBA Status", values="Count",
                      color_discrete_sequence=COLORS, hole=0.48,
                      title="Accreditation Split")
        fig3.update_traces(textfont_color="#e2e8f0", textfont_size=10)
        st.plotly_chart(L(fig3), use_container_width=True)

    # ── Placement & Package Landscape ──
    sec("Placement & Package Landscape")
    c1, c2 = st.columns(2)

    with c1:
        fig4 = px.scatter(
            fdf.dropna(subset=["Avg Pkg (LPA)", "Placement %", "Student Intake"]),
            x="Avg Pkg (LPA)", y="Placement %",
            color="Tier", size="Student Intake",
            hover_name="College Name",
            hover_data={"Avg Pkg Range": True, "Category": True, "NIRF Rank": True, "Tier": False},
            color_discrete_map=TIER_C, size_max=30,
            title="Placement % vs Avg Package (bubble = student intake)",
        )
        fig4.update_traces(marker=dict(opacity=0.85, line=dict(width=1, color="rgba(255,255,255,0.15)")))
        st.plotly_chart(L(fig4), use_container_width=True)

    with c2:
        pivot = (fdf.groupby(["State", "Tier"])["Avg Pkg (LPA)"].mean().reset_index())
        pivot_w = pivot.pivot(index="State", columns="Tier", values="Avg Pkg (LPA)").fillna(0)
        fig5 = go.Figure(go.Heatmap(
            z=pivot_w.values, x=pivot_w.columns.tolist(), y=pivot_w.index.tolist(),
            colorscale=[[0, "#060b18"], [0.5, "#312e81"], [1, "#a5b4fc"]],
            hoverongaps=False,
            text=[[f"₹{v:.1f}" if v else "" for v in row] for row in pivot_w.values],
            texttemplate="%{text}", textfont=dict(size=10, color="#e2e8f0"),
            showscale=True, colorbar=dict(tickfont=dict(color="#64748b")),
        ))
        fig5.update_layout(**BASE, title="Avg Package (LPA) — State × Tier Heatmap")
        st.plotly_chart(fig5, use_container_width=True)

    # ── Quick Insights ──
    sec("🔥 Quick Insights")
    tp = fdf.nlargest(1, "Placement %").iloc[0]
    tk = fdf.dropna(subset=["Avg Pkg (LPA)"]).nlargest(1, "Avg Pkg (LPA)").iloc[0]
    tr = fdf.dropna(subset=["ROI Score"]).nlargest(1, "ROI Score").iloc[0]
    tn = fdf.dropna(subset=["NIRF Rank"]).nsmallest(1, "NIRF Rank").iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    for col, badge, val, sub, name in [
        (c1, "🎯 Best Placement",   f"{tp['Placement %']:.0f}%",         "placement rate", tp["College Name"]),
        (c2, "💰 Highest Avg Pkg",  f"₹{tk['Avg Pkg (LPA)']:.0f} LPA",  "avg package",    tk["College Name"]),
        (c3, "📈 Best ROI Score",   f"{tr['ROI Score']:.1f}",             "ROI score",      tr["College Name"]),
        (c4, "🏅 Top NIRF Rank",    f"#{int(tn['NIRF Rank'])}",           "national rank",  tn["College Name"]),
    ]:
        with col:
            st.markdown(f"""
            <div class="insight-card">
                <h4>{badge}</h4>
                <div class="big">{val}</div>
                <p class="sub">{sub}</p>
                <p class="name">{name}</p>
            </div>""", unsafe_allow_html=True)

    # ── Top 10 by Package ──
    sec("Top 10 Colleges by Average Package")
    top10 = fdf.dropna(subset=["Avg Pkg (LPA)"]).nlargest(10, "Avg Pkg (LPA)").sort_values("Avg Pkg (LPA)")
    fig6 = px.bar(
        top10, x="Avg Pkg (LPA)", y="College Name", orientation="h",
        color="Tier", color_discrete_map=TIER_C,
        text="Avg Pkg Range",
        title="Top 10 — Average Package (LPA midpoint)",
        hover_data={"Placement %": True, "Category": True},
    )
    fig6.update_traces(textposition="outside", textfont_color="#e2e8f0")
    st.plotly_chart(L(fig6), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 – TIER 1 DEEP DIVE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Tier 1 College Deep Dive":
    hero(
        "Tier 1 College Deep Dive",
        "IITs & IISc — the gold standard of Indian engineering education. Every metric, every insight.",
        "TIER 1 ANALYSIS",
    )

    t1 = fdf[fdf["Tier"] == "Tier 1"].copy()
    if len(t1) == 0:
        st.info("No Tier 1 colleges match current filters."); st.stop()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Tier 1 Colleges",  len(t1))
    c2.metric("Avg Placement %",  f"{t1['Placement %'].mean():.1f}%")
    c3.metric("Avg Package",      f"₹{t1['Avg Pkg (LPA)'].mean():.1f} LPA")
    c4.metric("Highest Package",  f"₹{t1['Highest Pkg (LPA)'].max():.0f} LPA")
    c5.metric("Avg NIRF Rank",    f"#{t1['NIRF Rank'].mean():.0f}")

    tabs = st.tabs(["📊 Performance", "📦 Package Details", "📍 Geography", "🎓 Network & Intake", "📋 Full Data"])

    # ── Tab 0: Performance ──────────────────────────────────────────────────
    with tabs[0]:
        sec("NIRF Rank vs Placement %")
        fig = px.scatter(
            t1.dropna(subset=["NIRF Rank", "Avg Pkg (LPA)"]),
            x="NIRF Rank", y="Placement %",
            color="Category", size="Avg Pkg (LPA)",
            hover_name="College Name",
            hover_data={"Avg Pkg Range": True, "State": True, "NIRF Rank": True},
            color_discrete_map=CAT_C, size_max=35,
            title="NIRF Rank vs Placement % (bubble size = avg package)",
        )
        fig.update_traces(marker=dict(opacity=0.85, line=dict(width=1, color="rgba(255,255,255,0.12)")))
        fig.update_xaxes(autorange="reversed", title_text="NIRF Rank (lower = better)")
        st.plotly_chart(L(fig), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            fig2 = px.bar(
                t1.sort_values("Placement %", ascending=True),
                x="Placement %", y="College Name", orientation="h",
                color="Category", color_discrete_map=CAT_C,
                text="Placement %",
                title="Placement % — All Tier 1 Colleges",
                hover_data={"Avg Pkg Range": True},
            )
            fig2.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig2), use_container_width=True)

        with c2:
            fig3 = px.bar(
                t1.dropna(subset=["Avg Pkg (LPA)"]).sort_values("Avg Pkg (LPA)", ascending=True),
                x="Avg Pkg (LPA)", y="College Name", orientation="h",
                color="Category", color_discrete_map=CAT_C,
                text="Avg Pkg Range",
                title="Average Package — All Tier 1 Colleges",
            )
            fig3.update_traces(textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig3), use_container_width=True)

    # ── Tab 1: Package Details ───────────────────────────────────────────────
    with tabs[1]:
        sec("Domestic vs International Highest Package Comparison")
        pkg_df = t1.dropna(subset=["Intl Pkg (LPA)", "Highest Pkg (LPA)"]).copy()
        if len(pkg_df):
            fig4 = go.Figure()
            fig4.add_trace(go.Bar(
                name="Domestic Highest (LPA)",
                y=pkg_df["College Name"], x=pkg_df["Highest Pkg (LPA)"],
                orientation="h", marker_color="#06b6d4",
                text=pkg_df["Highest Pkg (LPA)"].apply(lambda x: f"₹{x:.0f}"),
                textposition="outside", textfont=dict(color="#e2e8f0"),
            ))
            fig4.add_trace(go.Bar(
                name="International Highest (LPA)",
                y=pkg_df["College Name"], x=pkg_df["Intl Pkg (LPA)"],
                orientation="h", marker_color="#6366f1",
                text=pkg_df["Intl Pkg (LPA)"].apply(lambda x: f"₹{x:.0f}"),
                textposition="outside", textfont=dict(color="#e2e8f0"),
            ))
            fig4.update_layout(**BASE, barmode="group",
                               title="Domestic vs International Highest Package (LPA)")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No colleges with both domestic and international package data.")

        sec("Avg Package vs Highest Package (Domestic)")
        fig5 = px.scatter(
            t1.dropna(subset=["Avg Pkg (LPA)", "Highest Pkg (LPA)"]),
            x="Avg Pkg (LPA)", y="Highest Pkg (LPA)",
            color="Category", hover_name="College Name",
            color_discrete_map=CAT_C, size="Placement %", size_max=28,
            hover_data={"Avg Pkg Range": True, "Placement %": True},
            title="Avg Package vs Highest Package (domestic)",
        )
        fig5.update_traces(marker=dict(opacity=0.85))
        st.plotly_chart(L(fig5), use_container_width=True)

        sec("Package Raw Data")
        pkg_show = t1[["College Name", "Category", "Avg Pkg", "Highest Pkg",
                        "Avg Pkg (LPA)", "Highest Pkg (LPA)", "Intl Pkg (LPA)"]]\
            .sort_values("Avg Pkg (LPA)", ascending=False).reset_index(drop=True)
        st.dataframe(pkg_show, use_container_width=True)

    # ── Tab 2: Geography ─────────────────────────────────────────────────────
    with tabs[2]:
        sec("State-wise Distribution of Tier 1 Colleges")
        c1, c2 = st.columns(2)
        with c1:
            state_t1 = t1.groupby("State").agg(
                Count=("College Name", "count"),
                Avg_K=("Avg Pkg (LPA)", "mean"),
            ).reset_index()
            fig6 = px.bar(
                state_t1.sort_values("Count", ascending=True),
                x="Count", y="State", orientation="h",
                color="Avg_K", color_continuous_scale="Viridis",
                text="Count", title="Tier 1 Colleges per State (color = avg pkg)",
            )
            fig6.update_traces(textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig6), use_container_width=True)

        with c2:
            own_t1 = t1.groupby("Ownership Type").size().reset_index(name="Count")
            fig7 = px.pie(own_t1, names="Ownership Type", values="Count",
                          color_discrete_sequence=COLORS, hole=0.45,
                          title="Ownership Type Distribution")
            fig7.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(L(fig7), use_container_width=True)

    # ── Tab 3: Network & Intake ───────────────────────────────────────────────
    with tabs[3]:
        sec("Alumni Network Size")
        alumni_df = t1.dropna(subset=["Alumni Count"]).sort_values("Alumni Count", ascending=True)
        fig8 = px.bar(
            alumni_df, x="Alumni Count", y="College Name", orientation="h",
            color="Alumni Count", color_continuous_scale="Purples",
            text=alumni_df["Alumni Count"].apply(lambda x: f"{x/1000:.0f}K"),
            title="Alumni Network Size (Tier 1 Colleges)",
        )
        fig8.update_traces(textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig8), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            fig9 = px.bar(
                t1.dropna(subset=["Student Intake"]).sort_values("Student Intake", ascending=True),
                x="Student Intake", y="College Name", orientation="h",
                color="Student Intake", color_continuous_scale="Blues",
                text="Student Intake", title="Annual Student Intake",
            )
            fig9.update_traces(textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig9), use_container_width=True)

        with c2:
            naac_t1 = t1.groupby("NAAC/NBA Status").size().reset_index(name="Count")
            fig10 = px.pie(naac_t1, names="NAAC/NBA Status", values="Count",
                           color_discrete_sequence=COLORS, hole=0.45,
                           title="Accreditation — Tier 1 Colleges")
            fig10.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(L(fig10), use_container_width=True)

    # ── Tab 4: Full Data ──────────────────────────────────────────────────────
    with tabs[4]:
        sec("Complete Tier 1 Dataset")
        show = ["College Name", "Category", "State", "City", "NIRF Rank", "NAAC/NBA Status",
                "Ownership Type", "Placement %", "Avg Pkg", "Highest Pkg",
                "Student Intake", "Recruiter Count", "Partner Count", "ROI Score"]
        st.dataframe(t1[show].sort_values("NIRF Rank").reset_index(drop=True),
                     use_container_width=True, height=520)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 – STATE-WISE DISTRIBUTION
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ State-wise Distribution":
    hero(
        "State-wise College Distribution",
        "How India's premier engineering colleges are spread across states",
        "GEO ANALYTICS",
    )

    ss = fdf.groupby("State").agg(
        Colleges=("College Name", "count"),
        Avg_Placement=("Placement %", "mean"),
        Avg_Package=("Avg Pkg (LPA)", "mean"),
        Total_Intake=("Student Intake", "sum"),
        Tier1=("Tier", lambda x: (x == "Tier 1").sum()),
        Tier2=("Tier", lambda x: (x == "Tier 2").sum()),
        Tier3=("Tier", lambda x: (x == "Tier 3").sum()),
    ).reset_index().round(2)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("States Covered",    len(ss))
    c2.metric("Total Colleges",    len(fdf))
    c3.metric("Top State (Pkg)",   ss.loc[ss["Avg_Package"].idxmax(), "State"])
    c4.metric("Top State (Plcmt)", ss.loc[ss["Avg_Placement"].idxmax(), "State"])

    tabs = st.tabs(["📊 Distribution", "💰 Package by State", "🎯 Placement by State", "📋 State Table"])

    with tabs[0]:
        sec("Tier Mix by State")
        tier_state = fdf.groupby(["State", "Tier"]).size().reset_index(name="Count")
        fig = px.bar(tier_state, x="State", y="Count", color="Tier",
                     color_discrete_map=TIER_C,
                     title="Stacked Tier Distribution by State")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(L(fig), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            fig2 = px.bar(ss.sort_values("Colleges", ascending=True),
                          x="Colleges", y="State", orientation="h",
                          color="Colleges", color_continuous_scale="Blues",
                          text="Colleges", title="Colleges per State")
            fig2.update_traces(textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig2), use_container_width=True)

        with c2:
            cat_state = fdf.groupby(["State", "Category"]).size().reset_index(name="Count")
            fig3 = px.bar(cat_state, x="State", y="Count", color="Category",
                          color_discrete_map=CAT_C, title="Category Mix by State")
            fig3.update_xaxes(tickangle=45)
            st.plotly_chart(L(fig3), use_container_width=True)

    with tabs[1]:
        sec("Average Package by State")
        ss_sorted = ss.sort_values("Avg_Package", ascending=False)
        fig4 = px.bar(ss_sorted, x="State", y="Avg_Package",
                      color="Avg_Package", color_continuous_scale="Viridis",
                      text=ss_sorted["Avg_Package"].apply(lambda x: f"₹{x:.1f}"),
                      title="Average Package (LPA) — State Ranking")
        fig4.update_traces(textposition="outside", textfont_color="#e2e8f0")
        fig4.update_xaxes(tickangle=45)
        st.plotly_chart(L(fig4), use_container_width=True)

        fig5 = px.scatter(ss, x="Avg_Package", y="Colleges",
                          size="Total_Intake", text="State",
                          color="Avg_Placement", color_continuous_scale="Plasma",
                          title="Package vs College Count (bubble = intake, color = avg placement%)")
        fig5.update_traces(textposition="top center", textfont=dict(color="#e2e8f0", size=10))
        st.plotly_chart(L(fig5), use_container_width=True)

    with tabs[2]:
        sec("Placement % by State")
        ss_pl = ss.sort_values("Avg_Placement", ascending=True)
        fig6 = px.bar(ss_pl, x="Avg_Placement", y="State", orientation="h",
                      color="Avg_Placement", color_continuous_scale="Teal",
                      text=ss_pl["Avg_Placement"].apply(lambda x: f"{x:.1f}%"),
                      title="Average Placement % — State Ranking")
        fig6.update_traces(textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig6), use_container_width=True)

    with tabs[3]:
        sec("State Summary Table")
        ss.columns = ["State", "Colleges", "Avg Placement (%)", "Avg Package (LPA)",
                      "Total Intake", "Tier 1", "Tier 2", "Tier 3"]
        st.dataframe(ss.sort_values("Colleges", ascending=False).reset_index(drop=True),
                     use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – PLACEMENT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💼 Placement Analysis":
    hero(
        "Placement Analysis Dashboard",
        "Placement rates, salary ranges, category benchmarks — every data point from the actual database",
        "PLACEMENT INTELLIGENCE",
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Avg Placement %",   f"{fdf['Placement %'].mean():.1f}%")
    c2.metric("Highest Placement", f"{fdf['Placement %'].max():.0f}%")
    c3.metric("Avg Package",       f"₹{fdf['Avg Pkg (LPA)'].mean():.1f} LPA")
    c4.metric("Highest Pkg (Dom)", f"₹{fdf['Highest Pkg (LPA)'].max():.0f} LPA")
    c5.metric("Median Package",    f"₹{fdf['Avg Pkg (LPA)'].median():.1f} LPA")

    tabs = st.tabs(["📈 Distributions", "🏆 Rankings", "📊 Category Benchmarks", "🔗 Correlations"])

    with tabs[0]:
        sec("Placement % Distribution")
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(fdf, x="Placement %", nbins=10,
                               color="Tier", color_discrete_map=TIER_C,
                               barmode="overlay", opacity=0.78,
                               title="Placement % Distribution by Tier", marginal="rug")
            st.plotly_chart(L(fig), use_container_width=True)
        with c2:
            fig2 = px.histogram(fdf.dropna(subset=["Avg Pkg (LPA)"]),
                                x="Avg Pkg (LPA)", nbins=12,
                                color="Category", color_discrete_map=CAT_C,
                                barmode="overlay", opacity=0.75,
                                title="Avg Package Distribution by Category", marginal="box")
            st.plotly_chart(L(fig2), use_container_width=True)

        sec("Package Range Box Plots")
        c1, c2 = st.columns(2)
        with c1:
            fig3 = px.box(fdf.dropna(subset=["Avg Pkg (LPA)"]),
                          x="Tier", y="Avg Pkg (LPA)",
                          color="Tier", color_discrete_map=TIER_C,
                          points="all", hover_name="College Name",
                          hover_data={"Avg Pkg Range": True},
                          title="Avg Package Spread by Tier")
            st.plotly_chart(L(fig3), use_container_width=True)
        with c2:
            fig4 = px.box(fdf.dropna(subset=["Avg Pkg (LPA)"]),
                          x="Category", y="Avg Pkg (LPA)",
                          color="Category", color_discrete_map=CAT_C,
                          points="all", hover_name="College Name",
                          hover_data={"Avg Pkg Range": True},
                          title="Avg Package Spread by Category")
            fig4.update_xaxes(tickangle=30)
            st.plotly_chart(L(fig4), use_container_width=True)

    with tabs[1]:
        sec("Top 20 by Placement %")
        top20p = fdf.nlargest(20, "Placement %")
        fig5 = px.bar(
            top20p.sort_values("Placement %"),
            x="Placement %", y="College Name", orientation="h",
            color="Tier", color_discrete_map=TIER_C,
            text="Placement %",
            hover_data={"Avg Pkg Range": True, "Category": True},
            title="Top 20 Colleges — Placement %",
        )
        fig5.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig5), use_container_width=True)

        sec("Top 20 by Average Package")
        top20k = fdf.dropna(subset=["Avg Pkg (LPA)"]).nlargest(20, "Avg Pkg (LPA)")
        fig6 = px.bar(
            top20k.sort_values("Avg Pkg (LPA)"),
            x="Avg Pkg (LPA)", y="College Name", orientation="h",
            color="Category", color_discrete_map=CAT_C,
            text="Avg Pkg Range",
            title="Top 20 Colleges — Average Package (actual range shown)",
        )
        fig6.update_traces(textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig6), use_container_width=True)

    with tabs[2]:
        sec("Category Benchmarks")
        cat_agg = fdf.groupby("Category").agg(
            Avg_P=("Placement %", "mean"),
            Avg_K=("Avg Pkg (LPA)", "mean"),
            Count=("College Name", "count"),
        ).reset_index()

        c1, c2 = st.columns(2)
        with c1:
            fig7 = px.scatter(
                cat_agg.dropna(), x="Avg_K", y="Avg_P",
                size="Count", color="Category",
                color_discrete_map=CAT_C, text="Category",
                title="Category: Placement % vs Avg Package", size_max=40,
            )
            fig7.update_traces(textposition="top center", textfont=dict(color="#e2e8f0", size=10))
            st.plotly_chart(L(fig7), use_container_width=True)

        with c2:
            ca = cat_agg.dropna().copy()
            fig8 = go.Figure()
            fig8.add_trace(go.Bar(
                name="Avg Placement %", x=ca["Category"], y=ca["Avg_P"].round(1),
                marker_color="#6366f1",
                text=ca["Avg_P"].round(1), texttemplate="%{text}%",
                textposition="outside", textfont=dict(color="#e2e8f0"),
            ))
            fig8.add_trace(go.Bar(
                name="Avg Package (LPA)", x=ca["Category"], y=ca["Avg_K"].round(1),
                marker_color="#06b6d4",
                text=ca["Avg_K"].round(1), texttemplate="₹%{text}",
                textposition="outside", textfont=dict(color="#e2e8f0"), yaxis="y2",
            ))
            fig8.update_layout(
                **BASE, barmode="group",
                title="Category: Placement % & Avg Package",
                yaxis2=dict(title="Package (LPA)", overlaying="y", side="right",
                            tickfont=dict(color="#475569")),
            )
            fig8.update_xaxes(tickangle=30)
            st.plotly_chart(fig8, use_container_width=True)

    with tabs[3]:
        sec("Correlation Matrix — What Drives Placement?")
        corr_df = fdf[["Placement %", "Avg Pkg (LPA)", "Highest Pkg (LPA)",
                        "Student Intake", "NIRF Rank", "Recruiter Count",
                        "Partner Count", "Alumni Count"]].dropna()
        corr = corr_df.corr().round(2)
        fig9 = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
            colorscale=[[0, "#f43f5e"], [0.5, "#060b18"], [1, "#6366f1"]],
            zmid=0,
            text=corr.values, texttemplate="%{text}",
            textfont=dict(size=10, color="#e2e8f0"),
            showscale=True, colorbar=dict(tickfont=dict(color="#64748b")),
        ))
        fig9.update_layout(**BASE, title="Correlation Matrix — Key Metrics")
        fig9.update_xaxes(tickangle=30)
        st.plotly_chart(fig9, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 – RECRUITER & INDUSTRY NETWORK
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🤝 Recruiter & Industry Network":
    hero(
        "Recruiter & Industry Network",
        "Every recruiter, every industry partner — parsed directly from the database",
        "RECRUITER INTELLIGENCE",
    )

    all_rec  = [r for lst in fdf["Recruiter List"]  for r in lst]
    all_part = [r for lst in fdf["Partner List"]    for r in lst]
    rec_ctr  = Counter(all_rec)
    part_ctr = Counter(all_part)
    top_rec  = pd.DataFrame(rec_ctr.most_common(25),  columns=["Company", "Colleges"])
    top_part = pd.DataFrame(part_ctr.most_common(25), columns=["Company", "Colleges"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Unique Recruiters",        len(rec_ctr))
    c2.metric("Unique Industry Partners", len(part_ctr))
    c3.metric("Most Active Recruiter",    rec_ctr.most_common(1)[0][0])
    c4.metric("Avg Recruiters/College",   f"{fdf['Recruiter Count'].mean():.1f}")

    tabs = st.tabs(["🏢 Top Recruiters", "🤝 Industry Partners", "📊 Network vs Outcomes", "🔬 Internships"])

    with tabs[0]:
        sec("Top 25 Recruiters by College Reach")
        fig = px.bar(
            top_rec.sort_values("Colleges"),
            x="Colleges", y="Company", orientation="h",
            color="Colleges", color_continuous_scale="Viridis",
            text="Colleges",
            title="Top 25 Recruiters — How many colleges they recruit from",
        )
        fig.update_traces(textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig), use_container_width=True)

        sec("🔥 Top 15 Most Active Recruiters")
        cls = ["c1", "c2", "c3", "c4"]
        chips = "".join([
            f'<span class="chip {cls[i % 4]}">{r} <b>({c})</b></span>'
            for i, (r, c) in enumerate(rec_ctr.most_common(15))
        ])
        st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)

    with tabs[1]:
        sec("Top 25 Industry Partners")
        fig2 = px.bar(
            top_part.sort_values("Colleges"),
            x="Colleges", y="Company", orientation="h",
            color="Colleges", color_continuous_scale="Plasma",
            text="Colleges", title="Top 25 Industry Partners",
        )
        fig2.update_traces(textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig2), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            fig3 = px.pie(top_rec.head(10), names="Company", values="Colleges",
                          color_discrete_sequence=COLORS, hole=0.42,
                          title="Top 10 Recruiter Share")
            fig3.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(L(fig3), use_container_width=True)
        with c2:
            fig4 = px.pie(top_part.head(10), names="Company", values="Colleges",
                          color_discrete_sequence=COLORS, hole=0.42,
                          title="Top 10 Partner Share")
            fig4.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(L(fig4), use_container_width=True)

    with tabs[2]:
        sec("Network Size vs Placement Outcomes")
        c1, c2 = st.columns(2)
        with c1:
            fig5 = px.scatter(
                fdf.dropna(subset=["Avg Pkg (LPA)"]),
                x="Recruiter Count", y="Placement %",
                color="Tier", hover_name="College Name",
                size="Avg Pkg (LPA)", size_max=28,
                color_discrete_map=TIER_C,
                hover_data={"Avg Pkg Range": True, "Category": True},
                title="Recruiter Count vs Placement %",
            )
            st.plotly_chart(L(fig5), use_container_width=True)
        with c2:
            fig6 = px.scatter(
                fdf.dropna(subset=["Avg Pkg (LPA)"]),
                x="Partner Count", y="Avg Pkg (LPA)",
                color="Tier", hover_name="College Name",
                size="Placement %", size_max=28,
                color_discrete_map=TIER_C,
                hover_data={"Avg Pkg Range": True, "Category": True},
                title="Industry Partners vs Avg Package",
            )
            st.plotly_chart(L(fig6), use_container_width=True)

        sec("Recruiter & Partner Count by Tier")
        tier_net = fdf.groupby("Tier")[["Recruiter Count", "Partner Count"]].mean().reset_index()
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(
            name="Avg Recruiters", x=tier_net["Tier"],
            y=tier_net["Recruiter Count"].round(1),
            marker_color="#6366f1",
            text=tier_net["Recruiter Count"].round(1),
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig7.add_trace(go.Bar(
            name="Avg Partners", x=tier_net["Tier"],
            y=tier_net["Partner Count"].round(1),
            marker_color="#06b6d4",
            text=tier_net["Partner Count"].round(1),
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig7.update_layout(**BASE, barmode="group", title="Network Depth by Tier")
        st.plotly_chart(fig7, use_container_width=True)

    with tabs[3]:
        sec("Internship Ecosystem")
        all_intern = [c for lst in fdf["Internship Companies"] for c in lst]
        intern_ctr = Counter(all_intern)
        intern_df  = pd.DataFrame(intern_ctr.most_common(20), columns=["Company", "Count"])

        c1, c2 = st.columns(2)
        with c1:
            fig8 = px.bar(
                intern_df.sort_values("Count"),
                x="Count", y="Company", orientation="h",
                color="Count", color_continuous_scale="Teal",
                text="Count", title="Top 20 Internship Providers",
            )
            fig8.update_traces(textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig8), use_container_width=True)
        with c2:
            fig9 = px.scatter(
                fdf.dropna(subset=["Avg Pkg (LPA)"]),
                x="Internship Count", y="Placement %",
                color="Tier", hover_name="College Name",
                color_discrete_map=TIER_C, size="Avg Pkg (LPA)", size_max=25,
                title="Internship Company Variety vs Placement %",
            )
            st.plotly_chart(L(fig9), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 – COLLEGE COMPARISON TOOL
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⚖️ College Comparison Tool":
    hero(
        "College Comparison Tool",
        "Select any colleges from the database and compare them across every available metric",
        "COMPARISON ENGINE",
    )

    all_colleges = sorted(fdf["College Name"].dropna().unique())
    defaults     = all_colleges[:min(5, len(all_colleges))]
    sel = st.multiselect("🔍 Select colleges to compare (up to 10)",
                         all_colleges, default=defaults, max_selections=10)

    if not sel:
        st.info("Select at least 2 colleges to begin."); st.stop()

    cdf = fdf[fdf["College Name"].isin(sel)].copy()

    pills = "".join([
        f'<span style="display:inline-block;padding:5px 14px;border-radius:20px;font-size:12px;'
        f'font-weight:600;background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.3);'
        f'color:#a5b4fc;margin:3px;">'
        f'{r["College Name"].split("(")[0].strip()} — {r["Tier"]} | '
        f'{r["Avg Pkg Range"]} | {r["Placement %"]:.0f}% placed</span>'
        for _, r in cdf.iterrows()
    ])
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:16px;">{pills}</div>',
                unsafe_allow_html=True)

    tabs = st.tabs(["🕸️ Radar View", "📊 Bar Charts", "📋 Data Table"])

    with tabs[0]:
        sec("Multi-Metric Radar Comparison (normalised 0–100)")
        metrics = ["Placement %", "Avg Pkg (LPA)", "Highest Pkg (LPA)",
                   "Student Intake", "Recruiter Count", "Partner Count"]
        rdf = cdf[["College Name"] + metrics].dropna().copy()

        def norm(s):
            mn, mx = s.min(), s.max()
            return (s - mn) / (mx - mn) * 100 if mx != mn else s * 0 + 50

        for m in metrics:
            rdf[m] = norm(rdf[m])

        fig = go.Figure()
        for i, (_, row) in enumerate(rdf.iterrows()):
            v = [row[m] for m in metrics]
            fig.add_trace(go.Scatterpolar(
                r=v + [v[0]], theta=metrics + [metrics[0]],
                fill="toself", name=row["College Name"],
                line=dict(color=COLORS[i % len(COLORS)], width=2),
                opacity=0.8,
            ))
        fig.update_layout(
            **BASE,
            polar=dict(
                bgcolor="rgba(6,11,24,0.8)",
                radialaxis=dict(visible=True, range=[0, 100],
                                tickfont=dict(color="#475569"),
                                gridcolor="rgba(99,102,241,0.15)"),
                angularaxis=dict(tickfont=dict(color="#94a3b8"),
                                 gridcolor="rgba(99,102,241,0.15)"),
            ),
            title="Radar — Normalised Comparison (100 = best in selection)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        sec("Side-by-Side Bar Comparisons")
        metrics_bar = [
            ("Placement %",       "Placement %",           "%{text}%"),
            ("Avg Pkg (LPA)",     "Avg Package (LPA)",     "₹%{text}"),
            ("Highest Pkg (LPA)", "Highest Package (LPA)", "₹%{text}"),
            ("Student Intake",    "Student Intake",         "%{text}"),
            ("Recruiter Count",   "Recruiter Count",        "%{text}"),
            ("NIRF Rank",         "NIRF Rank",             "#%{text}"),
        ]
        for i in range(0, len(metrics_bar), 2):
            c1, c2 = st.columns(2)
            for col, (ycol, title, tpl) in zip([c1, c2], metrics_bar[i:i+2]):
                with col:
                    d = cdf.dropna(subset=[ycol]).sort_values(ycol, ascending=False)
                    fig2 = px.bar(d, x="College Name", y=ycol,
                                  color="College Name", color_discrete_sequence=COLORS,
                                  title=title, text=ycol)
                    fig2.update_traces(texttemplate=tpl, textposition="outside",
                                       textfont_color="#e2e8f0")
                    fig2.update_xaxes(tickangle=30)
                    st.plotly_chart(L(fig2, showlegend=False), use_container_width=True)

    with tabs[2]:
        sec("Full Comparison Table")
        show = ["College Name", "Tier", "Category", "State", "NIRF Rank", "NAAC/NBA Status",
                "Placement %", "Avg Pkg", "Highest Pkg", "Avg Pkg (LPA)", "Highest Pkg (LPA)",
                "Student Intake", "Recruiter Count", "Partner Count", "ROI Score", "Ownership Type"]
        st.dataframe(cdf[show].set_index("College Name"), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 – ROI & VALUE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💰 ROI & Value Analysis":
    hero(
        "ROI & Value Analysis",
        "Which college gives the best return on your investment? Rankings based on real placement & package data.",
        "VALUE INTELLIGENCE",
    )

    roi_df = fdf.dropna(subset=["Avg Pkg (LPA)", "Placement %"]).copy()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Top ROI Score",    f"{roi_df['ROI Score'].max():.1f}")
    c2.metric("Avg ROI Score",    f"{roi_df['ROI Score'].mean():.1f}")
    c3.metric("S-Grade Colleges", len(roi_df[roi_df["Value Grade"] == "S — Exceptional"]))
    c4.metric("Best Value Tier",  roi_df.groupby("Tier")["ROI Score"].mean().idxmax())
    c5.metric("Best Value State", roi_df.groupby("State")["ROI Score"].mean().idxmax())

    tabs = st.tabs(["🏆 Leaderboard", "📊 Grade Analysis", "🗺️ State ROI", "📋 Full Rankings"])

    with tabs[0]:
        sec("ROI Leaderboard — Top 20 Colleges")
        top_roi = roi_df.nlargest(20, "ROI Score")
        fig = px.bar(
            top_roi.sort_values("ROI Score"),
            x="ROI Score", y="College Name", orientation="h",
            color="Value Grade", color_discrete_map=GRADE_C,
            text="ROI Score",
            hover_data={"Avg Pkg Range": True, "Placement %": True, "Tier": True},
            title="Top 20 Colleges by ROI Score",
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside", textfont_color="#e2e8f0")
        st.plotly_chart(L(fig), use_container_width=True)

        sec("ROI Bubble Matrix")
        fig2 = px.scatter(
            roi_df, x="Avg Pkg (LPA)", y="Placement %",
            size="ROI Score", color="Tier",
            hover_name="College Name",
            color_discrete_map=TIER_C, size_max=45,
            hover_data={"Avg Pkg Range": True, "ROI Score": True, "Category": True},
            title="ROI Matrix: Avg Package vs Placement % (bubble = ROI score)",
        )
        fig2.update_traces(marker=dict(opacity=0.82, line=dict(width=1, color="rgba(255,255,255,0.12)")))
        st.plotly_chart(L(fig2), use_container_width=True)

    with tabs[1]:
        sec("Value Grade Distribution")
        c1, c2 = st.columns(2)
        with c1:
            gd = roi_df.groupby("Value Grade").size().reset_index(name="Count")
            fig3 = px.pie(gd, names="Value Grade", values="Count",
                          color_discrete_map=GRADE_C, hole=0.48,
                          title="Colleges by Value Grade")
            fig3.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(L(fig3), use_container_width=True)

        with c2:
            cat_roi = (roi_df.groupby("Category")["ROI Score"].mean()
                       .reset_index().sort_values("ROI Score", ascending=True))
            fig4 = px.bar(cat_roi, x="ROI Score", y="Category", orientation="h",
                          color="ROI Score", color_continuous_scale="Viridis",
                          text="ROI Score", title="Average ROI Score by Category")
            fig4.update_traces(texttemplate="%{text:.1f}", textposition="outside", textfont_color="#e2e8f0")
            st.plotly_chart(L(fig4), use_container_width=True)

        sec("ROI Score Distribution by Tier")
        fig5 = px.box(
            roi_df, x="Tier", y="ROI Score",
            color="Tier", color_discrete_map=TIER_C,
            points="all", hover_name="College Name",
            hover_data={"Avg Pkg Range": True, "Placement %": True},
            title="ROI Score Spread by Tier",
        )
        st.plotly_chart(L(fig5), use_container_width=True)

    with tabs[2]:
        sec("State-wise ROI Performance")
        state_roi = roi_df.groupby("State").agg(
            Avg_ROI=("ROI Score", "mean"),
            Max_ROI=("ROI Score", "max"),
            Count=("College Name", "count"),
        ).reset_index().sort_values("Avg_ROI", ascending=False)

        fig6 = px.bar(
            state_roi, x="State", y="Avg_ROI",
            color="Avg_ROI", color_continuous_scale="Plasma",
            text=state_roi["Avg_ROI"].round(1),
            title="Average ROI Score by State",
        )
        fig6.update_traces(textposition="outside", textfont_color="#e2e8f0")
        fig6.update_xaxes(tickangle=45)
        st.plotly_chart(L(fig6), use_container_width=True)

        fig7 = px.scatter(
            state_roi, x="Count", y="Avg_ROI",
            size="Max_ROI", text="State",
            color="Avg_ROI", color_continuous_scale="Viridis",
            title="State: College Count vs Avg ROI (bubble = best ROI in state)",
        )
        fig7.update_traces(textposition="top center", textfont=dict(color="#e2e8f0", size=10))
        st.plotly_chart(L(fig7), use_container_width=True)

    with tabs[3]:
        sec("Complete ROI Rankings Table")
        table = roi_df[["College Name", "Tier", "Category", "State", "Placement %",
                         "Avg Pkg", "Avg Pkg (LPA)", "Highest Pkg", "Highest Pkg (LPA)",
                         "ROI Score", "Value Grade", "NIRF Rank"]]\
            .sort_values("ROI Score", ascending=False).reset_index(drop=True)
        table.index += 1
        st.dataframe(table, use_container_width=True, height=520)

        st.markdown("""
        <div class="insight-card" style="margin-top:16px;">
          <h4>📌 ROI Score Methodology</h4>
          <p style="margin-top:8px;">
            <b style="color:#a5b4fc;">ROI Score = (Placement % × Avg Package LPA midpoint) / 100</b><br><br>
            Uses the <b>midpoint</b> of the actual package range from the database (e.g. "21–25 LPA" → 23 LPA).<br>
            Grading: &nbsp;
            <b style="color:#6366f1;">S (&gt;22)</b> Exceptional &nbsp;|&nbsp;
            <b style="color:#06b6d4;">A (16–22)</b> Great &nbsp;|&nbsp;
            <b style="color:#10b981;">B (10–16)</b> Good &nbsp;|&nbsp;
            <b style="color:#f59e0b;">C (&lt;10)</b> Fair
          </p>
        </div>""", unsafe_allow_html=True)
