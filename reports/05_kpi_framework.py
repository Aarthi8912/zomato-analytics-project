# ================================================================
# Zomato Restaurant Analytics — KPI Metrics Framework
# ================================================================
# STEP 5 — KPI Definitions, Formulas, DAX & Business Context
# Author  : Data Analytics Team | Version : 1.0
# ================================================================

"""
This module defines ALL KPIs used across the project:
  - Business definition
  - Python formula (pandas)
  - SQL formula
  - Power BI DAX formula
  - Live value from dataset
  - Target benchmark
  - Business interpretation
  - Traffic light status
"""

import pandas as pd
import numpy as np

df = pd.read_csv("../dataset/zomato_clean.csv")
df["has_online_delivery"] = df["has_online_delivery"].astype(bool)
df["has_table_booking"]   = df["has_table_booking"].astype(bool)
df["is_rated"]            = df["is_rated"].astype(bool)
rated = df[df["aggregate_rating"] > 0]


# ================================================================
# KPI CATEGORY 1 — PLATFORM SCALE METRICS
# ================================================================

KPI_01 = {
    "id"           : "KPI-01",
    "name"         : "Total Restaurants",
    "category"     : "Platform Scale",
    "definition"   : "Total number of unique restaurants listed on the platform.",
    "python"       : "len(df)",
    "sql"          : "SELECT COUNT(*) AS total_restaurants FROM restaurants;",
    "dax"          : "Total Restaurants = COUNTROWS(restaurants)",
    "live_value"   : f"{len(df):,}",
    "unit"         : "count",
    "target"       : "10,000+",
    "status"       : "AMBER",   # close to target
    "interpretation": (
        "9,551 restaurants across 15 countries and 141 cities. "
        "Platform is 95% of way to 10K milestone. Growth in tier-2 cities "
        "and non-India geographies is the primary lever."
    ),
}

KPI_02 = {
    "id"           : "KPI-02",
    "name"         : "Total Countries Covered",
    "category"     : "Platform Scale",
    "definition"   : "Number of unique countries where restaurants are listed.",
    "python"       : "df['country'].nunique()",
    "sql"          : "SELECT COUNT(DISTINCT country) FROM restaurants;",
    "dax"          : "Countries = DISTINCTCOUNT(restaurants[country])",
    "live_value"   : "15",
    "unit"         : "count",
    "target"       : "20+",
    "status"       : "RED",
    "interpretation": (
        "Coverage is concentrated: India alone = 90.6% of listings. "
        "UK, US, UAE, Singapore are under-indexed relative to market size. "
        "International expansion is the #1 growth opportunity."
    ),
}

KPI_03 = {
    "id"           : "KPI-03",
    "name"         : "Total Cities Covered",
    "category"     : "Platform Scale",
    "definition"   : "Number of unique cities with at least one listed restaurant.",
    "python"       : "df['city'].nunique()",
    "sql"          : "SELECT COUNT(DISTINCT city) FROM restaurants;",
    "dax"          : "Cities = DISTINCTCOUNT(restaurants[city])",
    "live_value"   : "141",
    "unit"         : "count",
    "target"       : "200+",
    "status"       : "AMBER",
    "interpretation": (
        "141 cities covered but heavily skewed to NCR region (New Delhi, "
        "Gurgaon, Noida, Faridabad). Expansion to Tier-2 Indian cities "
        "and international metros is key for scale."
    ),
}

KPI_04 = {
    "id"           : "KPI-04",
    "name"         : "Unique Cuisine Count",
    "category"     : "Platform Scale",
    "definition"   : "Number of distinct primary cuisines represented on the platform.",
    "python"       : "df['primary_cuisine'].nunique()",
    "sql"          : "SELECT COUNT(DISTINCT primary_cuisine) FROM restaurants;",
    "dax"          : "Unique Cuisines = DISTINCTCOUNT(restaurants[primary_cuisine])",
    "live_value"   : "120",
    "unit"         : "count",
    "target"       : "150+",
    "status"       : "AMBER",
    "interpretation": (
        "120 cuisine types is healthy diversity, but 31.3% of restaurants "
        "offer only North Indian — the long tail is thin. Recruiting specialty "
        "cuisine restaurants will boost diversity KPI and attract premium customers."
    ),
}

KPI_05 = {
    "id"           : "KPI-05",
    "name"         : "Total Votes (Engagement Volume)",
    "category"     : "Platform Scale",
    "definition"   : "Sum of all customer votes/reviews across all restaurants.",
    "python"       : "df['votes'].sum()",
    "sql"          : "SELECT SUM(votes) AS total_votes FROM restaurants;",
    "dax"          : "Total Votes = SUM(restaurants[votes])",
    "live_value"   : "821,927",
    "unit"         : "count",
    "target"       : "1,000,000+",
    "status"       : "AMBER",
    "interpretation": (
        "821K votes indicates strong engagement, but average votes per restaurant "
        "is only 86. 22.5% of restaurants have zero votes — dead weight in the "
        "recommendation engine. Gamified review prompts post-order are critical."
    ),
}


# ================================================================
# KPI CATEGORY 2 — QUALITY METRICS
# ================================================================

KPI_06 = {
    "id"           : "KPI-06",
    "name"         : "Average Platform Rating",
    "category"     : "Quality",
    "definition"   : "Mean aggregate rating across all rated restaurants (rating > 0).",
    "python"       : "rated['aggregate_rating'].mean()",
    "sql"          : "SELECT ROUND(AVG(aggregate_rating),2) FROM restaurants WHERE aggregate_rating > 0;",
    "dax"          : (
        "Avg Rating = CALCULATE(\n"
        "    AVERAGE(restaurants[aggregate_rating]),\n"
        "    restaurants[aggregate_rating] > 0\n"
        ")"
    ),
    "live_value"   : "3.44",
    "unit"         : "score (0–5)",
    "target"       : "3.80+",
    "status"       : "RED",
    "interpretation": (
        "3.44 falls in the 'Average' bucket (2.5–3.5). Significant headroom exists. "
        "US restaurants avg 4.03, UK avg 4.14 — showing quality gap in the India-heavy "
        "dataset. Platform needs to incentivise quality improvement among low-rated listings."
    ),
}

KPI_07 = {
    "id"           : "KPI-07",
    "name"         : "High-Rated Restaurant %",
    "category"     : "Quality",
    "definition"   : "% of rated restaurants with aggregate_rating >= 4.0 (Good or above).",
    "python"       : "(rated['aggregate_rating'] >= 4.0).mean() * 100",
    "sql"          : (
        "SELECT ROUND(SUM(CASE WHEN aggregate_rating >= 4.0 THEN 1.0 ELSE 0 END)\n"
        "       / COUNT(*) * 100, 2) FROM restaurants WHERE aggregate_rating > 0;"
    ),
    "dax"          : (
        "High Rated % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[aggregate_rating] >= 4.0),\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[aggregate_rating] > 0)\n"
        ") * 100"
    ),
    "live_value"   : "18.64%",
    "unit"         : "percent",
    "target"       : "30%+",
    "status"       : "RED",
    "interpretation": (
        "Only 1 in 5 restaurants achieves 4.0+. This is the most impactful quality "
        "lever — shifting this to 30% would transform customer trust and NPS. "
        "Focus: operational excellence programs for mid-rated (3.5–4.0) restaurants."
    ),
}

KPI_08 = {
    "id"           : "KPI-08",
    "name"         : "Excellent Restaurant % (≥4.5)",
    "category"     : "Quality",
    "definition"   : "% of rated restaurants achieving Excellent status (rating ≥ 4.5).",
    "python"       : "(rated['aggregate_rating'] >= 4.5).mean() * 100",
    "sql"          : (
        "SELECT ROUND(SUM(CASE WHEN aggregate_rating >= 4.5 THEN 1.0 ELSE 0 END)\n"
        "       / COUNT(*) * 100, 2) FROM restaurants WHERE aggregate_rating > 0;"
    ),
    "dax"          : (
        "Excellent % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[aggregate_rating] >= 4.5),\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[aggregate_rating] > 0)\n"
        ") * 100"
    ),
    "live_value"   : "4.07%",
    "unit"         : "percent",
    "target"       : "10%+",
    "status"       : "RED",
    "interpretation": (
        "Only 4% achieve Excellent — a highly exclusive tier. These 301 restaurants "
        "are the platform's crown jewels and should be featured prominently in "
        "marketing, homepage banners, and 'Editor's Choice' collections."
    ),
}

KPI_09 = {
    "id"           : "KPI-09",
    "name"         : "Unrated Restaurant %",
    "category"     : "Quality",
    "definition"   : "% of restaurants with zero aggregate rating (no customer reviews).",
    "python"       : "(~df['is_rated']).mean() * 100",
    "sql"          : (
        "SELECT ROUND(SUM(CASE WHEN aggregate_rating = 0 THEN 1.0 ELSE 0 END)\n"
        "       / COUNT(*) * 100, 2) FROM restaurants;"
    ),
    "dax"          : (
        "Unrated % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[aggregate_rating] = 0),\n"
        "    COUNTROWS(restaurants)\n"
        ") * 100"
    ),
    "live_value"   : "22.49%",
    "unit"         : "percent",
    "target"       : "<10%",
    "status"       : "RED",
    "interpretation": (
        "2,148 restaurants have zero rating — a discovery black hole. These restaurants "
        "receive no algorithmic recommendation and likely have near-zero orders. "
        "Onboarding campaigns with a '5 reviews in 30 days' incentive can fix this."
    ),
}

KPI_10 = {
    "id"           : "KPI-10",
    "name"         : "Average Votes per Rated Restaurant",
    "category"     : "Quality",
    "definition"   : "Mean votes among restaurants that have been rated (rating > 0).",
    "python"       : "rated['votes'].mean()",
    "sql"          : "SELECT ROUND(AVG(votes),2) FROM restaurants WHERE aggregate_rating > 0;",
    "dax"          : (
        "Avg Votes = CALCULATE(\n"
        "    AVERAGE(restaurants[votes]),\n"
        "    restaurants[aggregate_rating] > 0\n"
        ")"
    ),
    "live_value"   : "110.77",
    "unit"         : "count",
    "target"       : "200+",
    "status"       : "RED",
    "interpretation": (
        "Average of 111 votes per rated restaurant is low. Viral restaurants reach "
        "320+ (the capped max). The gap shows most restaurants have weak review "
        "solicitation. Post-meal push notifications should be the default flow."
    ),
}


# ================================================================
# KPI CATEGORY 3 — FEATURE ADOPTION METRICS
# ================================================================

KPI_11 = {
    "id"           : "KPI-11",
    "name"         : "Online Delivery Adoption %",
    "category"     : "Feature Adoption",
    "definition"   : "% of restaurants offering online delivery on the platform.",
    "python"       : "df['has_online_delivery'].mean() * 100",
    "sql"          : (
        "SELECT ROUND(SUM(has_online_delivery) * 100.0 / COUNT(*), 2)\n"
        "FROM restaurants;"
    ),
    "dax"          : (
        "Delivery Adoption % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[has_online_delivery] = TRUE()),\n"
        "    COUNTROWS(restaurants)\n"
        ") * 100"
    ),
    "live_value"   : "25.66%",
    "unit"         : "percent",
    "target"       : "60%+",
    "status"       : "RED",
    "interpretation": (
        "Only 1 in 4 restaurants offers delivery. This is the single largest revenue "
        "opportunity — delivery restaurants generate commission revenue per order. "
        "India shows 35.7% adoption; US/UK at 0% — geographic expansion needed."
    ),
}

KPI_12 = {
    "id"           : "KPI-12",
    "name"         : "Table Booking Adoption %",
    "category"     : "Feature Adoption",
    "definition"   : "% of restaurants with table booking enabled on the platform.",
    "python"       : "df['has_table_booking'].mean() * 100",
    "sql"          : (
        "SELECT ROUND(SUM(has_table_booking) * 100.0 / COUNT(*), 2)\n"
        "FROM restaurants;"
    ),
    "dax"          : (
        "Booking Adoption % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[has_table_booking] = TRUE()),\n"
        "    COUNTROWS(restaurants)\n"
        ") * 100"
    ),
    "live_value"   : "12.12%",
    "unit"         : "percent",
    "target"       : "35%+",
    "status"       : "RED",
    "interpretation": (
        "Only 12% offer table booking despite it correlating with +0.17 rating uplift. "
        "Mid-range and premium restaurants are the highest-ROI targets — they have the "
        "seating capacity and customer intent to benefit most from this feature."
    ),
}

KPI_13 = {
    "id"           : "KPI-13",
    "name"         : "Full-Feature Combo % (Delivery + Booking)",
    "category"     : "Feature Adoption",
    "definition"   : "% of restaurants offering BOTH online delivery AND table booking.",
    "python"       : "(df['has_online_delivery'] & df['has_table_booking']).mean() * 100",
    "sql"          : (
        "SELECT ROUND(SUM(CASE WHEN has_online_delivery = 1 AND has_table_booking = 1\n"
        "                      THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2)\n"
        "FROM restaurants;"
    ),
    "dax"          : (
        "Full Feature % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants),\n"
        "        restaurants[has_online_delivery] = TRUE(),\n"
        "        restaurants[has_table_booking] = TRUE()),\n"
        "    COUNTROWS(restaurants)\n"
        ") * 100"
    ),
    "live_value"   : "4.55%",
    "unit"         : "percent",
    "target"       : "20%+",
    "status"       : "RED",
    "interpretation": (
        "Restaurants with both features average 3.61 rating vs 3.45 for neither. "
        "Only 435 restaurants hit the full-feature mark — these are the platform's "
        "power users and should be the template for new restaurant onboarding."
    ),
}

KPI_14 = {
    "id"           : "KPI-14",
    "name"         : "No-Feature Restaurant %",
    "category"     : "Feature Adoption",
    "definition"   : "% of restaurants with neither delivery nor table booking.",
    "python"       : "(~df['has_online_delivery'] & ~df['has_table_booking']).mean() * 100",
    "sql"          : (
        "SELECT ROUND(SUM(CASE WHEN has_online_delivery = 0 AND has_table_booking = 0\n"
        "                      THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2)\n"
        "FROM restaurants;"
    ),
    "dax"          : (
        "No Feature % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants),\n"
        "        restaurants[has_online_delivery] = FALSE(),\n"
        "        restaurants[has_table_booking] = FALSE()),\n"
        "    COUNTROWS(restaurants)\n"
        ") * 100"
    ),
    "live_value"   : "66.77%",
    "unit"         : "percent",
    "target"       : "<30%",
    "status"       : "RED",
    "interpretation": (
        "66.8% of restaurants are feature-dead — they exist on the platform "
        "as static listings only. These generate zero transactional revenue. "
        "A targeted activation campaign with subsidised onboarding is critical."
    ),
}


# ================================================================
# KPI CATEGORY 4 — COST & PRICING METRICS
# ================================================================

KPI_15 = {
    "id"           : "KPI-15",
    "name"         : "Average Cost for Two",
    "category"     : "Cost & Pricing",
    "definition"   : "Mean average cost for a two-person meal across all restaurants (local currency).",
    "python"       : "df['avg_cost_for_two'].mean()",
    "sql"          : "SELECT ROUND(AVG(avg_cost_for_two), 2) FROM restaurants;",
    "dax"          : "Avg Cost for Two = AVERAGE(restaurants[avg_cost_for_two])",
    "live_value"   : "521.55",
    "unit"         : "local currency",
    "target"       : "Context-dependent by market",
    "status"       : "INFO",
    "interpretation": (
        "₹521 average in India-dominated dataset. Meaningful only per-country. "
        "Use median (₹400) rather than mean for customer-facing displays — "
        "the distribution is right-skewed by premium outliers."
    ),
}

KPI_16 = {
    "id"           : "KPI-16",
    "name"         : "Budget Restaurant Share",
    "category"     : "Cost & Pricing",
    "definition"   : "% of restaurants in Price Range 1 (Budget tier).",
    "python"       : "(df['price_range'] == 1).mean() * 100",
    "sql"          : (
        "SELECT ROUND(SUM(CASE WHEN price_range = 1 THEN 1.0 ELSE 0 END)\n"
        "       / COUNT(*) * 100, 2) FROM restaurants;"
    ),
    "dax"          : (
        "Budget % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[price_range] = 1),\n"
        "    COUNTROWS(restaurants)\n"
        ") * 100"
    ),
    "live_value"   : f"{(df['price_range']==1).mean()*100:.1f}%",
    "unit"         : "percent",
    "target"       : "30–40% (balanced mix)",
    "status"       : "RED",
    "interpretation": (
        "46.6% Budget-tier skew makes the platform appear mass-market. "
        "This caps average order value and commission revenue. Recruiting "
        "more mid-range and premium restaurants will improve monetisation."
    ),
}

KPI_17 = {
    "id"           : "KPI-17",
    "name"         : "Premium Restaurant Share",
    "category"     : "Cost & Pricing",
    "definition"   : "% of restaurants in Price Range 4 (Premium tier).",
    "python"       : "(df['price_range'] == 4).mean() * 100",
    "sql"          : (
        "SELECT ROUND(SUM(CASE WHEN price_range = 4 THEN 1.0 ELSE 0 END)\n"
        "       / COUNT(*) * 100, 2) FROM restaurants;"
    ),
    "dax"          : (
        "Premium % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[price_range] = 4),\n"
        "    COUNTROWS(restaurants)\n"
        ") * 100"
    ),
    "live_value"   : f"{(df['price_range']==4).mean()*100:.1f}%",
    "unit"         : "percent",
    "target"       : "15%+",
    "status"       : "AMBER",
    "interpretation": (
        "6.1% premium share with avg rating 3.82 — these restaurants generate "
        "the highest per-order revenue. Table booking adoption here is 46.8%, "
        "proving premium customers expect advanced booking features."
    ),
}


# ================================================================
# KPI CATEGORY 5 — COMPETITIVE & MARKET METRICS
# ================================================================

KPI_18 = {
    "id"           : "KPI-18",
    "name"         : "Top City Market Share",
    "category"     : "Market Intelligence",
    "definition"   : "% of total restaurants concentrated in the #1 city (New Delhi).",
    "python"       : "df['city'].value_counts().iloc[0] / len(df) * 100",
    "sql"          : (
        "SELECT ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM restaurants), 2)\n"
        "FROM restaurants WHERE city = 'New Delhi';"
    ),
    "dax"          : (
        "Top City Share % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[city] = \"New Delhi\"),\n"
        "    COUNTROWS(restaurants)\n"
        ") * 100"
    ),
    "live_value"   : "57.3%",
    "unit"         : "percent",
    "target"       : "<40% (geographic diversity)",
    "status"       : "RED",
    "interpretation": (
        "New Delhi single-handedly accounts for 57% of all restaurants. "
        "This geographic concentration is a risk — any regulatory change, "
        "competitor entry, or pandemic-style disruption in Delhi devastates "
        "the entire platform. Diversification is a strategic imperative."
    ),
}

KPI_19 = {
    "id"           : "KPI-19",
    "name"         : "Top Cuisine Market Share",
    "category"     : "Market Intelligence",
    "definition"   : "% of restaurants where primary cuisine = North Indian.",
    "python"       : "df['primary_cuisine'].value_counts().iloc[0] / len(df) * 100",
    "sql"          : (
        "SELECT ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM restaurants), 2)\n"
        "FROM restaurants WHERE primary_cuisine = 'North Indian';"
    ),
    "dax"          : (
        "Top Cuisine Share % = DIVIDE(\n"
        "    CALCULATE(COUNTROWS(restaurants), restaurants[primary_cuisine] = \"North Indian\"),\n"
        "    COUNTROWS(restaurants)\n"
        ") * 100"
    ),
    "live_value"   : "31.3%",
    "unit"         : "percent",
    "target"       : "<20% (cuisine diversity)",
    "status"       : "RED",
    "interpretation": (
        "North Indian represents 31.3% of all restaurants. Combined with Chinese "
        "(8.95%) and Fast Food (7.04%), just 3 cuisines cover nearly half the platform. "
        "This limits appeal to international users and niche cuisine seekers."
    ),
}

KPI_20 = {
    "id"           : "KPI-20",
    "name"         : "Platform Health Score",
    "category"     : "Composite",
    "definition"   : (
        "Composite score (0–100) weighted across 4 pillars: "
        "Rating Quality (25%), Delivery Adoption (25%), "
        "High-Quality % (25%), Review Coverage (25%)."
    ),
    "python"       : (
        "# Pillar 1: Avg Rating\n"
        "p1 = 18 if rated['aggregate_rating'].mean() >= 3.5 else 10\n"
        "# Pillar 2: Delivery Adoption\n"
        "p2 = 15 if df['has_online_delivery'].mean() >= 0.25 else 8\n"
        "# Pillar 3: High-Quality %\n"
        "p3 = 15 if (rated['aggregate_rating']>=4.0).mean() >= 0.20 else 8\n"
        "# Pillar 4: Zero-vote %\n"
        "p4 = 15 if (~df['is_rated']).mean() <= 0.25 else 8\n"
        "health_score = p1 + p2 + p3 + p4"
    ),
    "sql"          : "-- See Q30 in zomato_analysis.sql",
    "dax"          : (
        "Health Score = \n"
        "VAR AvgRating = CALCULATE(AVERAGE(restaurants[aggregate_rating]),\n"
        "                          restaurants[aggregate_rating] > 0)\n"
        "VAR DeliveryPct = DIVIDE(CALCULATE(COUNTROWS(restaurants),\n"
        "                   restaurants[has_online_delivery]=TRUE()), COUNTROWS(restaurants))*100\n"
        "VAR HighQualPct = DIVIDE(CALCULATE(COUNTROWS(restaurants),\n"
        "                   restaurants[aggregate_rating]>=4.0),\n"
        "                   CALCULATE(COUNTROWS(restaurants),\n"
        "                   restaurants[aggregate_rating]>0))*100\n"
        "VAR ZeroVotePct = DIVIDE(CALCULATE(COUNTROWS(restaurants),\n"
        "                   restaurants[aggregate_rating]=0), COUNTROWS(restaurants))*100\n"
        "RETURN\n"
        "    (IF(AvgRating>=4.0,25,IF(AvgRating>=3.5,18,10)))\n"
        "  + (IF(DeliveryPct>=50,25,IF(DeliveryPct>=25,15,8)))\n"
        "  + (IF(HighQualPct>=40,25,IF(HighQualPct>=20,15,8)))\n"
        "  + (IF(ZeroVotePct<=10,25,IF(ZeroVotePct<=25,15,8)))"
    ),
    "live_value"   : "48 / 100",
    "unit"         : "score",
    "target"       : "75+",
    "status"       : "RED",
    "interpretation": (
        "Platform health at 48/100 signals significant structural gaps. "
        "The two biggest scoring opportunities are delivery adoption (+10 pts if "
        "reaching 50%) and rating quality (+7 pts if avg hits 4.0). "
        "These should be the top 2 OKRs for the product and growth teams."
    ),
}


# ================================================================
# KPI SUMMARY TABLE
# ================================================================

def print_kpi_report():
    kpis = [KPI_01, KPI_02, KPI_03, KPI_04, KPI_05,
            KPI_06, KPI_07, KPI_08, KPI_09, KPI_10,
            KPI_11, KPI_12, KPI_13, KPI_14,
            KPI_15, KPI_16, KPI_17,
            KPI_18, KPI_19, KPI_20]

    STATUS_ICON = {"GREEN": "✅", "AMBER": "🟡", "RED": "🔴", "INFO": "ℹ️"}

    print("\n" + "═"*75)
    print("  ZOMATO KPI METRICS REPORT")
    print("═"*75)
    print(f"  {'ID':<8} {'KPI Name':<38} {'Value':<14} {'Target':<14} {'Status'}")
    print("─"*75)

    for k in kpis:
        icon = STATUS_ICON.get(k["status"], "")
        print(f"  {k['id']:<8} {k['name']:<38} {k['live_value']:<14} "
              f"{k['target']:<14} {icon} {k['status']}")

    red   = sum(1 for k in kpis if k["status"] == "RED")
    amber = sum(1 for k in kpis if k["status"] == "AMBER")
    green = sum(1 for k in kpis if k["status"] == "GREEN")

    print("─"*75)
    print(f"  🔴 Critical (RED) : {red}    🟡 Watch (AMBER): {amber}    ✅ On Track: {green}")
    print("═"*75)


if __name__ == "__main__":
    print_kpi_report()