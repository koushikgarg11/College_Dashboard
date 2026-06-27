# 🔬 NexusIQ — India's Tier 1 Engineering Intelligence Vault

> Built by **Koushik Garg** · Data & Buisness Analyst Intern @ Analytics Career Connect (ACC)

A comprehensive multi-page Streamlit dashboard for analyzing India's top engineering colleges across placements, packages, recruiters, and ROI metrics.

## 🌐 Live Demo
👉 **[collegedashboard.streamlit.app](https://collegedashboard.streamlit.app/)**

---

## 📊 Dashboards Included

| Dashboard | Description |
|---|---|
| 🏠 **Overview & Highlights** | KPIs, tier breakdown, placement landscape & quick insights |
| 🏆 **Tier 1 College Deep Dive** | IITs, IISc & premier institutions — performance, geography, academics |
| 🗺️ **State-wise Distribution** | Geographic spread of colleges across India's states |
| 💼 **Placement Analysis** | Distributions, rankings, comparisons & correlation matrix |
| 🤝 **Recruiter & Industry Network** | Top recruiters, industry partners, internship ecosystem |
| ⚖️ **College Comparison Tool** | Side-by-side radar, bar & scatter comparison of any colleges |
| 💰 **ROI & Value Analysis** | Return on investment scoring, grading & leaderboard |

---

## 🚀 Quick Start

### Local Setup

```bash
git clone https://github.com/koushikgarg11/College_Dashboard.git
cd College_Dashboard
pip install -r requirements.txt
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select repo → set `app.py` as main file
4. Click **Deploy!**

---

## 📁 Project Structure

```
College_Dashboard/
├── app.py               # Main Streamlit application (7 pages, 1100+ lines)
├── data_utils.py        # Data loading, cleaning & feature engineering
├── Final_Data_1.xlsx    # Source dataset (45 colleges, 17 metrics)
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 📦 Dataset

- **45 colleges** across India — IITs, NITs, IIITs, Deemed Universities, State Universities
- **17 raw metrics** per college including NIRF rank, placement %, packages, recruiters, industry partners, alumni network
- **18 states** represented
- **Engineered features**: ROI Score, Tier classification, Alumni Count (numeric), Recruiter Count, Internship Count

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Streamlit** | UI framework & deployment |
| **Plotly** | Interactive charts (scatter, bar, heatmap, radar, pie, histogram, box) |
| **Pandas** | Data processing & aggregation |
| **OpenPyXL** | Excel file reading |

---

## ✨ Key Features

- 🌙 Dark navy theme with gradient accents — consistent across all 7 pages
- 🔍 Global sidebar filters — Tier, State, Category, Ownership, Accreditation, Package range, Placement %
- 📊 25+ interactive Plotly charts with hover tooltips
- 🧮 ROI Score model — composite metric (Placement % × Avg Package / 100)
- 🏷️ Value grading system — S / A / B / C grades per college
- 📋 Full sortable data tables on every page
- ⚡ `@st.cache_data` for fast repeated loads

---

## 👤 About

**Koushik Garg**
Data & Business Analyst Intern @ Analytics Career Connect (ACC) |B.Com (Hons), Aryabhatta College, University of Delhi | IIT Madras Diploma in Data Science
Entry-level Data Analyst with hands-on experience in data wrangling, statistical analysis, demand forecasting, and machine learning. Improved demand forecast accuracy by 15–20% using ARIMA time-series models; reduced ML threat-detection false positives by ~18% on a 100K+ record dataset. Proficient in Python, SQL, Power BI, and Tableau, with experience building automated reporting pipelines, ETL workflows, and executive dashboards.

- 🔗 [LinkedIn](https://www.linkedin.com/in/koushikgarg11)
- 💻 [GitHub](https://github.com/koushikgarg11)
- 🌐 [Live App](https://collegedashboard.streamlit.app)

