
# 🍽️ Zomato Restaurant Analytics & Customer Insights Dashboard

## 📌 Project Overview

This project delivers a complete restaurant intelligence platform built on the Zomato dataset. It follows the full data analytics lifecycle — from raw CSV ingestion to an interactive Streamlit web app, with SQL analysis, Power BI dashboard design, machine learning, and board-ready business recommendations.



---

## 🎯 Business Problem

Zomato operates in a highly competitive food-tech market. Key business questions this project answers:

- Which markets are saturated and which offer growth potential?
- What drives restaurant ratings — and can we predict them?
- Why is online delivery adoption at only 25.7% when it drives 22% more engagement?
- Where are the 543 "Hidden Gem" restaurants the platform should be promoting?
- What is the platform's overall health score and where are the critical gaps?

---

## 📂 Project Structure

```
Zomato-Analytics-Project/
│
├── dataset/
│   ├── zomato.csv                  ← Raw dataset (9,551 restaurants)
│   └── zomato_clean.csv            ← Cleaned dataset (28 columns, 0 nulls)
│
├── notebooks/
│   ├── 01_data_cleaning.py         ← 10-function production cleaning pipeline
│   ├── 02_eda.py                   ← 9 EDA analyses with charts + insights
│   └── 03_ml_model.py              ← 4-model ML pipeline + evaluation
│
├── sql_queries/
│   ├── zomato_analysis.sql         ← 30 advanced SQL queries
│   └── run_queries.py              ← SQLite query runner
│
├── powerbi_dashboard/
│   └── dashboard_spec.md           ← 5-page dashboard specification
│
├── reports/
│   ├── 05_kpi_framework.py         ← 20 KPI definitions with DAX formulas
│   └── 07_08_insights_recommendations.py ← 9 insights + 16 recommendations
│
├── screenshots/                    ← All generated chart images
│
├── app/
│   ├── streamlit_app.py            ← 5-tab interactive web dashboard
│   ├── rating_predictor.pkl        ← Saved champion ML model
│   └── scaler.pkl                  ← Feature scaler
│
├── README.md
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| **Data Processing** | Python, Pandas, NumPy |
| **Visualisation** | Matplotlib, Seaborn |
| **SQL Analysis** | SQLite (PostgreSQL-compatible syntax) |
| **Machine Learning** | Scikit-Learn (GBR, RF, Ridge, Linear) |
| **Web App** | Streamlit |
| **BI Dashboard** | Power BI (5-page specification) |
| **Version Control** | Git / GitHub |

---

## 📊 Dataset

| Field | Description |
|---|---|
| Source | Zomato Restaurant Dataset (Kaggle) |
| Rows | 9,551 restaurants |
| Countries | 15 |
| Cities | 141 |
| Raw Columns | 21 |
| Engineered Columns | 7 (primary_cuisine, rating_bucket, cost_category, is_rated, delivery_and_table, votes_per_rating, country) |
| Final Columns | 28 |
| Null values (post-clean) | 0 |

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/Aarthi8912/zomato-analytics-project.git
cd zomato-analytics-project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run data cleaning pipeline
python notebooks/01_data_cleaning.py

# 5. Run EDA (generates 9 charts in /screenshots)
python notebooks/02_eda.py

# 6. Run ML pipeline
python notebooks/03_ml_model.py

# 7. Run SQL analysis
python sql_queries/run_queries.py

# 8. Launch Streamlit app
streamlit run app/streamlit_app.py
```

---

## 📈 Key Results

### Data Quality
- **0 nulls** remaining after cleaning pipeline
- **0 duplicates** (deduplicated by restaurant_id)
- **853** cost outliers and **1,126** vote outliers winsorized via IQR
- **7 new features** engineered for analysis and ML

### EDA — Top Findings

| Finding | Metric |
|---|---|
| New Delhi concentration | 57.3% of all restaurants |
| Top 3 cities combined | 80.3% of dataset |
| North Indian cuisine share | 31.3% (market monopoly) |
| Platform avg rating | 3.44 / 5.0 |
| Unrated restaurants | 22.5% (2,148 restaurants) |
| Online delivery adoption | 25.7% |
| Table booking lift | +0.18 rating points |
| Hidden gems identified | 543 restaurants |

### SQL — Advanced Queries (30 total)

Techniques used: `CTE`, `Window Functions`, `RANK / DENSE_RANK / NTILE`, `PERCENT_RANK`, `ROW_NUMBER`, `CASE WHEN`, `HAVING`, `Self-JOIN`, `Cross-JOIN`, `Subqueries`, `HHI Market Index`, `Composite Scoring`

### ML Model — Rating Predictor

| Model | MAE | RMSE | R² | MAPE |
|---|---|---|---|---|
| Linear Regression | 0.2275 | 0.2891 | 0.730 | 6.90% |
| Ridge Regression | 0.2273 | 0.2893 | 0.730 | 6.90% |
| Random Forest | 0.1371 | 0.2057 | 0.863 | 4.25% |
| **Gradient Boosting ⭐** | **0.0584** | **0.0841** | **0.977** | **1.75%** |

**Champion Model: Gradient Boosting Regressor**
- R² = 0.9771 (explains 97.7% of rating variance)
- MAE = 0.058 rating points (predicts within ±0.06 stars)
- Top feature: `votes` (56.7% importance)

---

## 💡 Business Insights

> *9 data-verified insights from real analysis*

1. **🔴 CRITICAL** — New Delhi accounts for 57.3% of all restaurants — extreme concentration risk
2. **🟠 HIGH** — North Indian cuisine = 31.3%; top-3 cuisines cover 47.3% of the platform
3. **🔴 CRITICAL** — Platform avg rating = 3.44 ("Average" bucket); 22.5% of restaurants unrated
4. **🔴 CRITICAL** — Delivery adoption at 25.7%; UK and US at 0% despite 4.0+ avg ratings
5. **🟠 HIGH** — Table booking at 12.1% despite proven +0.18 rating uplift
6. **🟡 MEDIUM** — Price-quality correlation weak (r ≈ 0.22) — 543 hidden gems identified
7. **🟡 MEDIUM** — Votes follow a power law — Excellent restaurants get 6× more votes than Average
8. **🟠 HIGH** — UK (4.14 avg) and US (4.03 avg) have zero delivery — highest ROI expansion
9. **✅ OPPORTUNITY** — 543 hidden gems average 4.33★ at below-average cost — prime for promotion

---

## 🎯 Strategic Recommendations

**16 recommendations across 5 audiences:**

- **Restaurant Owners** — Enable delivery, activate table booking, solicit reviews
- **Delivery Platforms** — Activate 6,377 no-feature restaurants; build Hidden Gems feature
- **Marketing Teams** — 'Rate your meal' campaign; monthly cuisine spotlights; UAE case study
- **Pricing** — Flag 284 overpriced restaurants; dynamic pricing benchmark dashboards
- **Retention** — Personalised feed by rating + cost preference; Power Reviewer loyalty tier

---

## 📊 Power BI Dashboard

5-page interactive dashboard:

| Page | Focus |
|---|---|
| Executive Summary | KPI cards, city map, price tier mix, country share |
| Customer Insights | Rating distribution, feature combo impact, engagement |
| Cuisine Analysis | Top cuisines, rating × price heatmap, diversity index |
| Cost & Ratings | Price tier analysis, votes by bucket, value segments |
| Restaurant Performance | Composite score leaderboard, segmentation, drill-through |

---

## 🤖 ML Model Details

**Problem type:** Regression (predict aggregate_rating from 10 features)

**Features used:**
- `has_online_delivery`, `has_table_booking` — feature flags
- `price_range`, `avg_cost_for_two` — pricing signals
- `votes`, `votes_per_rating` — engagement metrics
- `cuisine_le`, `country_le`, `city_le` — encoded categoricals
- `delivery_and_table` — combined feature flag

**Feature Importance (Gradient Boosting):**
1. `votes` — 56.7%
2. `votes_per_rating` — 31.5%
3. `city_le` — 7.8%
4. `country_le` — 1.4%
5. All others — combined 2.6%

---

## 📸 Screenshots

| EDA Charts | ML Evaluation |
|---|---|
| Top cities | Model comparison |
| Cuisine distribution | Feature importance |
| Rating distribution | Actual vs predicted |
| Online delivery impact | Residuals |
| Cost analysis heatmap | MAE by bucket |

*(See `/screenshots/` directory)*

---

## 🔮 Future Improvements

- [ ] Sentiment analysis on restaurant reviews (NLP)
- [ ] Time-series analysis of restaurant growth trends
- [ ] Geospatial mapping with Folium/Plotly
- [ ] Restaurant recommendation engine (collaborative filtering)
- [ ] Real-time data pipeline with Zomato API
- [ ] Docker containerisation for Streamlit app
- [ ] CI/CD pipeline for automated model retraining

---

## 👤 Author

** Data Analyzer **

- 📧 aarthia776@gmail.com.com
- 💼 [LinkedIn](https://linkedin.com/in/s-aarthi-825a29262)
- 🐙 [GitHub](https://github.com/Aarthi8912)

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.

---

<div align="center">

⭐ **Star this repo if it helped you!** ⭐

*Built with real data · Real insights · Real business thinking*

</div>