# 🎓 India College Analytics Dashboard

A comprehensive multi-page Streamlit dashboard for analyzing India's top engineering and research colleges across placement, packages, recruiters, and ROI metrics.

## 📊 Dashboards Included

| Dashboard | Description |
|-----------|-------------|
| 🏆 **Tier 1 College Dashboard** | Deep dive into IITs, IISc, and premier institutions |
| 🗺️ **State-wise Distribution** | Geographic spread of colleges across Indian states |
| 💼 **Placement Analysis** | Placement %, package ranges, and category comparisons |
| 🤝 **Recruiter Analytics** | Top recruiters, industry partners, hiring patterns |
| ⚖️ **College Comparison** | Side-by-side radar and bar comparisons |
| 💰 **ROI Analysis** | Return on investment scoring and leaderboard |

## 🚀 Quick Start

### Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/college-analytics-dashboard.git
cd college-analytics-dashboard
pip install -r requirements.txt
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set `app.py` as main file
4. Click **Deploy!**

## 📁 Project Structure

```
college-analytics-dashboard/
├── app.py               # Main Streamlit application
├── data_utils.py        # Data loading & preprocessing
├── Final_Data_1.xlsx    # Source data (45 colleges, 17 metrics)
├── requirements.txt     # Python dependencies
└── README.md
```

## 📦 Data

- **45 colleges** across India (IITs, NITs, IIITs, Deemed Universities, State Universities)
- **17 metrics** per college including NIRF rank, placement %, packages, recruiters, and more
- **18 states** represented

## 🛠️ Tech Stack

- **Streamlit** – UI framework
- **Plotly** – Interactive charts
- **Pandas** – Data processing
- **OpenPyXL** – Excel reading

## 📸 Screenshots

Each dashboard features:
- Dark theme with gradient cards
- Interactive filters (State, Category, Ownership)
- 4 KPI metric cards at the top
- Multiple chart types (scatter, bar, radar, histogram, box)
- Sortable data tables

## 📄 License

MIT License
