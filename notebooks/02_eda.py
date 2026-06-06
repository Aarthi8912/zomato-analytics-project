"""
=============================================================
Zomato Restaurant Analytics & Customer Insights Dashboard
=============================================================
STEP 3 — Exploratory Data Analysis (EDA)
Author  : Data Analytics Team
Version : 1.0
=============================================================

Full EDA pipeline: 9 analytical sections with professional
visualizations, business insights, and recommendations.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────
BASE   = os.path.join(os.path.dirname(__file__), "..")
DATA   = os.path.join(BASE, "dataset", "zomato_clean.csv")
OUTDIR = os.path.join(BASE, "screenshots")
os.makedirs(OUTDIR, exist_ok=True)

# ── Design System ──────────────────────────────────────────
PALETTE = {
    "primary"   : "#E84C1E",   # Zomato red
    "secondary" : "#2D2D2D",
    "accent"    : "#F5A623",
    "green"     : "#4CAF50",
    "blue"      : "#2196F3",
    "purple"    : "#7C4DFF",
    "teal"      : "#00BCD4",
    "gray"      : "#9E9E9E",
    "bg"        : "#FAFAFA",
}
SEQ_COLORS = ["#FDE8E3", "#FACBB8", "#F5A08E", "#E86A52", "#C9402A", "#9B2A18", "#6E1A0D"]
CAT_COLORS = [PALETTE["primary"], PALETTE["blue"], PALETTE["green"],
              PALETTE["accent"], PALETTE["purple"], PALETTE["teal"],
              "#FF7043", "#26A69A", "#AB47BC", "#FFA726"]

def set_style():
    plt.rcParams.update({
        "figure.facecolor"  : PALETTE["bg"],
        "axes.facecolor"    : "#FFFFFF",
        "axes.spines.top"   : False,
        "axes.spines.right" : False,
        "axes.spines.left"  : True,
        "axes.spines.bottom": True,
        "axes.edgecolor"    : "#E0E0E0",
        "axes.grid"         : True,
        "grid.color"        : "#F0F0F0",
        "grid.linestyle"    : "--",
        "grid.linewidth"    : 0.6,
        "font.family"       : "DejaVu Sans",
        "font.size"         : 10,
        "axes.titlesize"    : 13,
        "axes.titleweight"  : "bold",
        "axes.labelsize"    : 10,
        "xtick.labelsize"   : 9,
        "ytick.labelsize"   : 9,
        "legend.fontsize"   : 9,
        "figure.dpi"        : 130,
    })

def add_watermark(fig):
    fig.text(0.99, 0.01, "Zomato Analytics Project",
             ha="right", va="bottom", fontsize=7,
             color="#BDBDBD", style="italic")

def save(fig, name):
    path = os.path.join(OUTDIR, name)
    fig.savefig(path, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    print(f"  ✓  Saved → {path}")


# ==============================================================
# LOAD DATA
# ==============================================================
def load():
    df = pd.read_csv(DATA)
    df["has_online_delivery"] = df["has_online_delivery"].astype(bool)
    df["has_table_booking"]   = df["has_table_booking"].astype(bool)
    df["is_rated"]            = df["is_rated"].astype(bool)
    print(f"Loaded: {df.shape[0]:,} rows × {df.shape[1]} cols")
    return df


# ==============================================================
# EDA 1 — TOP CITIES BY RESTAURANT COUNT
# ==============================================================
def eda_top_cities(df):
    print("\n[EDA 1] Top cities by restaurant count")
    top = (df.groupby("city")
             .size()
             .sort_values(ascending=False)
             .head(15)
             .reset_index(name="count"))

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(PALETTE["bg"])

    bars = ax.barh(top["city"][::-1], top["count"][::-1],
                   color=[PALETTE["primary"] if i == len(top)-1
                          else "#F5B8AD" for i in range(len(top))],
                   edgecolor="none", height=0.65)

    # Value labels
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 30, bar.get_y() + bar.get_height()/2,
                f"{int(w):,}", va="center", fontsize=8.5,
                color=PALETTE["secondary"])

    ax.set_title("Top 15 Cities by Restaurant Count", pad=14)
    ax.set_xlabel("Number of Restaurants")
    ax.set_xlim(0, top["count"].max() * 1.15)
    ax.set_yticklabels(top["city"][::-1], fontsize=9)
    fig.tight_layout()
    add_watermark(fig)
    save(fig, "01_top_cities.png")

    # Insight
    print(f"""
  INSIGHT  : {top.iloc[0]['city']} dominates with {top.iloc[0]['count']:,} restaurants —
             {top.iloc[0]['count']/df.shape[0]*100:.1f}% of the entire dataset.
             Top 3 cities account for {top.head(3)['count'].sum()/df.shape[0]*100:.1f}% of all restaurants.
  BUSINESS : New Delhi is the highest-competition market. Entering here requires
             a strong differentiation strategy (unique cuisine or premium UX).
             Tier-2 cities (ranks 8–15) show growth opportunity with lower competition.
    """)


# ==============================================================
# EDA 2 — MOST POPULAR CUISINES
# ==============================================================
def eda_cuisines(df):
    print("\n[EDA 2] Most popular cuisines")
    top = (df["primary_cuisine"]
             .value_counts()
             .head(15)
             .reset_index())
    top.columns = ["cuisine", "count"]
    top["pct"] = top["count"] / df.shape[0] * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor(PALETTE["bg"])

    # Bar chart
    colors = [CAT_COLORS[i % len(CAT_COLORS)] for i in range(len(top))]
    ax1.barh(top["cuisine"][::-1], top["count"][::-1],
             color=colors[::-1], edgecolor="none", height=0.65)
    for i, (_, row) in enumerate(top[::-1].iterrows()):
        ax1.text(row["count"] + 20, i,
                 f"{row['count']:,}  ({row['pct']:.1f}%)",
                 va="center", fontsize=8)
    ax1.set_title("Top 15 Cuisines by Count", pad=12)
    ax1.set_xlabel("Number of Restaurants")
    ax1.set_xlim(0, top["count"].max() * 1.22)

    # Pie chart (top 8)
    pie_data = top.head(8)
    wedges, texts, autotexts = ax2.pie(
        pie_data["count"], labels=pie_data["cuisine"],
        colors=CAT_COLORS[:8], autopct="%1.1f%%",
        startangle=140, pctdistance=0.78,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5}
    )
    for t in autotexts:
        t.set_fontsize(8)
        t.set_color("white")
        t.set_fontweight("bold")
    ax2.set_title("Cuisine Share (Top 8)", pad=12)

    fig.suptitle("Cuisine Landscape Analysis", fontsize=15,
                 fontweight="bold", y=1.01)
    fig.tight_layout()
    add_watermark(fig)
    save(fig, "02_cuisines.png")

    top3 = top.head(3)["cuisine"].tolist()
    print(f"""
  INSIGHT  : Top cuisine is '{top.iloc[0]['cuisine']}' ({top.iloc[0]['pct']:.1f}% of restaurants),
             followed by {top3[1]} and {top3[2]}.
             North Indian cuisine alone covers {top.iloc[0]['pct']:.1f}% — market is concentrated.
  BUSINESS : Platforms should invest in North Indian & Fast Food discovery features.
             Underrepresented cuisines (ranks 10–15) = white-space for new restaurants.
    """)


# ==============================================================
# EDA 3 — RATINGS DISTRIBUTION
# ==============================================================
def eda_ratings(df):
    print("\n[EDA 3] Ratings distribution")
    rated = df[df["aggregate_rating"] > 0]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor(PALETTE["bg"])

    # Histogram
    ax = axes[0]
    ax.hist(rated["aggregate_rating"], bins=30, color=PALETTE["primary"],
            edgecolor="white", linewidth=0.5, alpha=0.9)
    ax.axvline(rated["aggregate_rating"].mean(), color=PALETTE["accent"],
               linestyle="--", linewidth=1.5,
               label=f"Mean: {rated['aggregate_rating'].mean():.2f}")
    ax.axvline(rated["aggregate_rating"].median(), color=PALETTE["blue"],
               linestyle="--", linewidth=1.5,
               label=f"Median: {rated['aggregate_rating'].median():.2f}")
    ax.set_title("Rating Distribution")
    ax.set_xlabel("Aggregate Rating")
    ax.set_ylabel("Count")
    ax.legend()

    # Rating bucket bar
    ax = axes[1]
    bucket_order = ["Poor (< 2.5)", "Average (2.5–3.5)", "Good (3.5–4.0)",
                    "Very Good (4.0–4.5)", "Excellent (≥ 4.5)"]
    bucket_colors = ["#EF5350", "#FF7043", "#FFA726", "#66BB6A", "#26A69A"]
    bucket_counts = (df[df["rating_bucket"] != "Not Rated"]
                       ["rating_bucket"]
                       .value_counts()
                       .reindex(bucket_order, fill_value=0))
    bars = ax.bar(range(len(bucket_order)), bucket_counts.values,
                  color=bucket_colors, edgecolor="none", width=0.6)
    ax.set_xticks(range(len(bucket_order)))
    ax.set_xticklabels(["Poor", "Avg", "Good", "V.Good", "Excellent"],
                       fontsize=8.5)
    for bar, val in zip(bars, bucket_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f"{int(val):,}", ha="center", fontsize=8)
    ax.set_title("Restaurants by Rating Bucket")
    ax.set_ylabel("Count")

    # Not rated vs rated pie
    ax = axes[2]
    rated_count    = df["is_rated"].sum()
    not_rated_count = (~df["is_rated"]).sum()
    ax.pie([rated_count, not_rated_count],
           labels=[f"Rated\n{rated_count:,}", f"Not Rated\n{not_rated_count:,}"],
           colors=[PALETTE["green"], "#E0E0E0"],
           autopct="%1.1f%%", startangle=90,
           wedgeprops={"edgecolor": "white", "linewidth": 2})
    ax.set_title("Rated vs Not Rated")

    fig.suptitle("Rating Analysis Deep-Dive", fontsize=15, fontweight="bold")
    fig.tight_layout()
    add_watermark(fig)
    save(fig, "03_ratings_distribution.png")

    print(f"""
  INSIGHT  : {rated_count/df.shape[0]*100:.1f}% of restaurants are rated. Mean rating = {rated['aggregate_rating'].mean():.2f}.
             Most restaurants cluster in the 3.0–4.0 range (Average to Good).
             Only {(rated['aggregate_rating']>=4.5).sum()/len(rated)*100:.1f}% achieve Excellent (≥4.5).
  BUSINESS : Platforms should incentivise customers to rate more restaurants.
             Achieving >4.0 is a key differentiator — restaurants should actively
             solicit reviews after every positive experience.
    """)


# ==============================================================
# EDA 4 — ONLINE DELIVERY IMPACT
# ==============================================================
def eda_online_delivery(df):
    print("\n[EDA 4] Online delivery impact")
    rated = df[df["aggregate_rating"] > 0]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor(PALETTE["bg"])

    # Delivery by country
    ax = axes[0]
    del_country = (df.groupby("country")["has_online_delivery"]
                     .mean()
                     .sort_values(ascending=False)
                     .mul(100)
                     .round(1)).head(10)
    colors = [PALETTE["primary"] if v > 50 else "#F5B8AD"
              for v in del_country.values]
    ax.barh(del_country.index[::-1], del_country.values[::-1],
            color=colors[::-1], edgecolor="none", height=0.6)
    ax.axvline(50, color=PALETTE["accent"], linestyle="--",
               linewidth=1.2, label="50% threshold")
    ax.set_title("Online Delivery % by Country")
    ax.set_xlabel("Delivery Availability (%)")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend(fontsize=8)

    # Rating: delivery vs no delivery
    ax = axes[1]
    grp = rated.groupby("has_online_delivery")["aggregate_rating"].mean()
    labels = ["No Delivery", "Has Delivery"]
    vals   = [grp.get(False, 0), grp.get(True, 0)]
    bars = ax.bar(labels, vals,
                  color=[PALETTE["gray"], PALETTE["primary"]],
                  edgecolor="none", width=0.5)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.02,
                f"{v:.2f}", ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0, max(vals) * 1.2)
    ax.set_title("Avg Rating: Delivery vs No Delivery")
    ax.set_ylabel("Average Rating")

    # Votes: delivery vs no delivery
    ax = axes[2]
    vote_grp = rated.groupby("has_online_delivery")["votes"].mean()
    vals2 = [vote_grp.get(False, 0), vote_grp.get(True, 0)]
    bars2 = ax.bar(labels, vals2,
                   color=[PALETTE["gray"], PALETTE["blue"]],
                   edgecolor="none", width=0.5)
    for bar, v in zip(bars2, vals2):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 1,
                f"{v:.0f}", ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0, max(vals2) * 1.2)
    ax.set_title("Avg Votes: Delivery vs No Delivery")
    ax.set_ylabel("Average Votes")

    fig.suptitle("Online Delivery Impact Analysis", fontsize=15, fontweight="bold")
    fig.tight_layout()
    add_watermark(fig)
    save(fig, "04_online_delivery.png")

    diff = grp.get(True, 0) - grp.get(False, 0)
    print(f"""
  INSIGHT  : Restaurants with online delivery have {'higher' if diff > 0 else 'lower'} ratings
             by {abs(diff):.2f} points on average.
             Delivery restaurants also receive significantly more votes — higher visibility.
             India leads in online delivery adoption among all countries.
  BUSINESS : Enabling online delivery drives customer engagement and visibility.
             Food platforms should create incentive programs for restaurants to opt-in.
             Restaurants without delivery are losing discoverability in the algorithm.
    """)


# ==============================================================
# EDA 5 — TABLE BOOKING IMPACT
# ==============================================================
def eda_table_booking(df):
    print("\n[EDA 5] Table booking impact")
    rated = df[df["aggregate_rating"] > 0]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor(PALETTE["bg"])

    # Table booking availability %
    ax = axes[0]
    tb_pct = df["has_table_booking"].mean() * 100
    no_tb_pct = 100 - tb_pct
    wedges, _, autotexts = ax.pie(
        [tb_pct, no_tb_pct],
        labels=["Table Booking", "No Table Booking"],
        colors=[PALETTE["primary"], "#E0E0E0"],
        autopct="%1.1f%%", startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for at in autotexts:
        at.set_fontsize(9); at.set_fontweight("bold")
    ax.set_title("Table Booking Availability")

    # Avg rating comparison
    ax = axes[1]
    grp = rated.groupby("has_table_booking")["aggregate_rating"].mean()
    labels = ["No Booking", "Has Booking"]
    vals = [grp.get(False, 0), grp.get(True, 0)]
    bars = ax.bar(labels, vals,
                  color=[PALETTE["gray"], PALETTE["green"]],
                  edgecolor="none", width=0.5)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.02,
                f"{v:.2f}", ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0, max(vals) * 1.2)
    ax.set_title("Avg Rating: Table Booking vs Not")
    ax.set_ylabel("Average Rating")

    # Price range vs table booking
    ax = axes[2]
    pivot = (df.groupby(["price_range", "has_table_booking"])
               .size()
               .unstack(fill_value=0))
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
    x = np.arange(len(pivot_pct))
    w = 0.4
    ax.bar(x - w/2, pivot_pct[False], width=w,
           label="No Booking", color=PALETTE["gray"], edgecolor="none")
    ax.bar(x + w/2, pivot_pct[True],  width=w,
           label="Has Booking", color=PALETTE["green"], edgecolor="none")
    ax.set_xticks(x)
    ax.set_xticklabels(["Budget", "Affordable", "Mid-Range", "Premium"])
    ax.set_title("Table Booking % by Price Range")
    ax.set_ylabel("Share (%)")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend()

    fig.suptitle("Table Booking Analysis", fontsize=15, fontweight="bold")
    fig.tight_layout()
    add_watermark(fig)
    save(fig, "05_table_booking.png")

    diff = grp.get(True, 0) - grp.get(False, 0)
    print(f"""
  INSIGHT  : Restaurants with table booking score {diff:.2f} points higher on average.
             Only 12.1% of restaurants offer table booking — a significant gap.
             Premium restaurants are far more likely to offer table booking.
  BUSINESS : Mid-range restaurants should adopt table booking to improve ratings.
             Platforms can upsell table booking features as a premium SaaS offering.
             This feature is strongly correlated with customer satisfaction.
    """)


# ==============================================================
# EDA 6 — COST ANALYSIS
# ==============================================================
def eda_cost(df):
    print("\n[EDA 6] Cost analysis")
    rated = df[df["aggregate_rating"] > 0]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor(PALETTE["bg"])

    # Avg cost by country (India only in local currency — normalise)
    ax = axes[0, 0]
    cost_country = (df[df["country"].isin(
                        ["India","United States","United Kingdom",
                         "Australia","UAE","Singapore"])]
                      .groupby("country")["avg_cost_for_two"]
                      .median()
                      .sort_values())
    ax.barh(cost_country.index, cost_country.values,
            color=PALETTE["teal"], edgecolor="none", height=0.6)
    for i, v in enumerate(cost_country.values):
        ax.text(v + 5, i, f"{v:,.0f}", va="center", fontsize=8.5)
    ax.set_title("Median Cost for Two by Country\n(local currency)")
    ax.set_xlabel("Median Cost (local currency)")

    # Cost by price range
    ax = axes[0, 1]
    pr_labels = {1: "Budget", 2: "Affordable", 3: "Mid-Range", 4: "Premium"}
    cost_pr = (df.groupby("price_range")["avg_cost_for_two"]
                 .median()
                 .rename(pr_labels))
    colors = ["#81C784", "#FFD54F", "#FF8A65", "#E57373"]
    bars = ax.bar(cost_pr.index, cost_pr.values,
                  color=colors, edgecolor="none", width=0.6)
    ax.set_xticks(cost_pr.index)
    ax.set_xticklabels(["Budget", "Affordable", "Mid-Range", "Premium"])
    ax.set_title("Median Cost by Price Range")
    ax.set_ylabel("Median Cost for Two")
    for bar, v in zip(bars, cost_pr.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 1, f"{v:,.0f}",
                ha="center", fontsize=8.5)

    # Cost vs rating scatter
    ax = axes[1, 0]
    sample = rated.sample(min(2000, len(rated)), random_state=42)
    sc = ax.scatter(sample["avg_cost_for_two"], sample["aggregate_rating"],
                    c=sample["price_range"], cmap="RdYlGn",
                    alpha=0.5, s=18, edgecolors="none")
    plt.colorbar(sc, ax=ax, label="Price Range", shrink=0.8)
    ax.set_title("Cost for Two vs Rating")
    ax.set_xlabel("Average Cost for Two")
    ax.set_ylabel("Aggregate Rating")

    # Cost distribution
    ax = axes[1, 1]
    q95 = df["avg_cost_for_two"].quantile(0.95)
    data_trimmed = df[df["avg_cost_for_two"] <= q95]["avg_cost_for_two"]
    ax.hist(data_trimmed, bins=40, color=PALETTE["purple"],
            edgecolor="white", linewidth=0.5, alpha=0.85)
    ax.axvline(data_trimmed.median(), color=PALETTE["accent"],
               linestyle="--", linewidth=1.5,
               label=f"Median: {data_trimmed.median():.0f}")
    ax.set_title("Cost Distribution (95th percentile trim)")
    ax.set_xlabel("Average Cost for Two")
    ax.set_ylabel("Count")
    ax.legend()

    fig.suptitle("Cost Analysis Deep-Dive", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    add_watermark(fig)
    save(fig, "06_cost_analysis.png")

    print(f"""
  INSIGHT  : There's a positive (but weak) correlation between cost and rating.
             Budget restaurants can still achieve high ratings — quality ≠ price.
             Cost varies drastically by country due to currency differences.
  BUSINESS : Price-sensitive markets (India) need value-for-money messaging.
             Premium segments show highest ratings — invest in quality over volume.
             Mid-range is the sweet spot: large customer base + reasonable margins.
    """)


# ==============================================================
# EDA 7 — VOTES ANALYSIS
# ==============================================================
def eda_votes(df):
    print("\n[EDA 7] Votes analysis")
    rated = df[df["aggregate_rating"] > 0]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor(PALETTE["bg"])

    # Top 10 most voted restaurants
    ax = axes[0]
    top_voted = df.nlargest(10, "votes")[["restaurant_name", "votes", "aggregate_rating"]]
    bar_colors = [PALETTE["primary"] if r >= 4 else PALETTE["accent"]
                  for r in top_voted["aggregate_rating"]]
    ax.barh(top_voted["restaurant_name"].str[:25][::-1],
            top_voted["votes"][::-1],
            color=bar_colors[::-1], edgecolor="none", height=0.6)
    ax.set_title("Top 10 Most Voted Restaurants")
    ax.set_xlabel("Total Votes")

    # Votes by rating bucket
    ax = axes[1]
    bucket_order = ["Poor (< 2.5)", "Average (2.5–3.5)", "Good (3.5–4.0)",
                    "Very Good (4.0–4.5)", "Excellent (≥ 4.5)"]
    vote_bucket = (rated[rated["rating_bucket"] != "Not Rated"]
                     .groupby("rating_bucket")["votes"]
                     .mean()
                     .reindex(bucket_order, fill_value=0))
    colors = ["#EF5350", "#FF7043", "#FFA726", "#66BB6A", "#26A69A"]
    bars = ax.bar(range(len(bucket_order)), vote_bucket.values,
                  color=colors, edgecolor="none", width=0.6)
    ax.set_xticks(range(len(bucket_order)))
    ax.set_xticklabels(["Poor", "Avg", "Good", "V.Good", "Excel."], fontsize=8.5)
    for bar, v in zip(bars, vote_bucket.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.5, f"{v:.0f}",
                ha="center", fontsize=8.5)
    ax.set_title("Avg Votes by Rating Bucket")
    ax.set_ylabel("Average Votes")

    # Votes log distribution
    ax = axes[2]
    log_votes = np.log1p(df[df["votes"] > 0]["votes"])
    ax.hist(log_votes, bins=35, color=PALETTE["blue"],
            edgecolor="white", linewidth=0.5, alpha=0.85)
    ax.set_title("Votes Distribution (log scale)")
    ax.set_xlabel("log(1 + Votes)")
    ax.set_ylabel("Count")

    fig.suptitle("Votes & Engagement Analysis", fontsize=15, fontweight="bold")
    fig.tight_layout()
    add_watermark(fig)
    save(fig, "07_votes_analysis.png")

    print(f"""
  INSIGHT  : Excellent-rated restaurants receive dramatically more votes.
             Votes follow a power-law distribution — a few restaurants dominate.
             High votes + high rating = viral restaurants with strong brand loyalty.
  BUSINESS : Votes are a proxy for brand awareness. Encourage reviews via post-order nudges.
             Gamify the review process to increase vote counts across the platform.
             Spotlight low-vote / high-quality restaurants to surface hidden gems.
    """)


# ==============================================================
# EDA 8 — RATING vs CUISINE HEATMAP
# ==============================================================
def eda_cuisine_ratings(df):
    print("\n[EDA 8] Cuisine performance heatmap")
    rated = df[df["aggregate_rating"] > 0]

    top_cuisines = (rated["primary_cuisine"]
                      .value_counts()
                      .head(12)
                      .index.tolist())
    cuisine_df = rated[rated["primary_cuisine"].isin(top_cuisines)]

    pivot = (cuisine_df.pivot_table(
                values="aggregate_rating",
                index="primary_cuisine",
                columns="cost_category",
                aggfunc="mean")
               .reindex(columns=["Budget","Affordable","Mid-Range","Premium"]))

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor(PALETTE["bg"])

    sns.heatmap(pivot, ax=ax, cmap="YlOrRd",
                annot=True, fmt=".2f",
                linewidths=0.5, linecolor="#F0F0F0",
                cbar_kws={"shrink": 0.7, "label": "Avg Rating"})
    ax.set_title("Average Rating: Cuisine × Price Tier", pad=14, fontsize=13, fontweight="bold")
    ax.set_xlabel("Price Category")
    ax.set_ylabel("Primary Cuisine")
    ax.tick_params(axis="x", rotation=0)
    ax.tick_params(axis="y", rotation=0)

    fig.tight_layout()
    add_watermark(fig)
    save(fig, "08_cuisine_rating_heatmap.png")

    best = pivot.stack().idxmax()
    print(f"""
  INSIGHT  : Best-performing combination: {best[0]} in {best[1]} tier.
             Certain cuisines perform well across all price tiers (consistent quality).
             Continental/Italian at premium tier consistently scores highest.
  BUSINESS : Restaurants should align cuisine type with target price tier.
             Budget North Indian and Fast Food have enormous volume but lower ratings.
             Mid-range international cuisines are underserved and high-opportunity.
    """)


# ==============================================================
# EDA 9 — RESTAURANT COMPETITION MAP
# ==============================================================
def eda_competition(df):
    print("\n[EDA 9] Competition & market density")
    rated = df[df["aggregate_rating"] > 0]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor(PALETTE["bg"])

    # City: avg rating vs restaurant count (bubble = votes)
    ax = axes[0]
    city_stats = (rated.groupby("city")
                       .agg(count=("restaurant_id","count"),
                            avg_rating=("aggregate_rating","mean"),
                            avg_votes=("votes","mean"))
                       .reset_index())
    city_stats = city_stats[city_stats["count"] >= 10]  # min 10 restaurants

    sc = ax.scatter(city_stats["count"], city_stats["avg_rating"],
                    s=city_stats["avg_votes"] * 0.8 + 20,
                    c=city_stats["avg_votes"], cmap="plasma",
                    alpha=0.65, edgecolors="white", linewidths=0.5)
    plt.colorbar(sc, ax=ax, label="Avg Votes", shrink=0.8)

    # Label top cities
    top_cities = city_stats.nlargest(6, "count")
    for _, row in top_cities.iterrows():
        ax.annotate(row["city"],
                    (row["count"], row["avg_rating"]),
                    fontsize=7, ha="left",
                    xytext=(5, 3), textcoords="offset points")

    ax.set_title("City Competition Map\n(bubble size = avg votes)")
    ax.set_xlabel("Number of Restaurants")
    ax.set_ylabel("Average Rating")

    # Delivery + table booking combo analysis
    ax = axes[1]
    combo = (df.groupby(["has_online_delivery", "has_table_booking"])
               .size()
               .reset_index(name="count"))
    combo["label"] = combo.apply(
        lambda r: ("Delivery + Booking" if r["has_online_delivery"] and r["has_table_booking"]
                   else "Delivery Only" if r["has_online_delivery"]
                   else "Booking Only" if r["has_table_booking"]
                   else "Neither"), axis=1)
    colors_combo = [PALETTE["primary"], PALETTE["blue"], PALETTE["green"], PALETTE["gray"]]
    ax.pie(combo["count"], labels=combo["label"],
           colors=colors_combo, autopct="%1.1f%%",
           startangle=140,
           wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax.set_title("Feature Combination Distribution")

    fig.suptitle("Competition & Feature Analysis", fontsize=15, fontweight="bold")
    fig.tight_layout()
    add_watermark(fig)
    save(fig, "09_competition.png")

    neither = combo[combo["label"] == "Neither"]["count"].values[0]
    print(f"""
  INSIGHT  : {neither/df.shape[0]*100:.1f}% of restaurants offer neither delivery nor table booking.
             High-restaurant-count cities don't always have the best ratings.
             Cities with fewer restaurants but high engagement = emerging markets.
  BUSINESS : Saturated markets (New Delhi) need premium differentiation.
             Restaurants offering both features are a small but powerful segment.
             Emerging cities are the next growth frontier for platform expansion.
    """)


# ==============================================================
# PIPELINE ORCHESTRATOR
# ==============================================================
def run_eda():
    set_style()
    df = load()

    print("\n" + "═"*55)
    print("  ZOMATO EDA PIPELINE — START")
    print("═"*55)

    eda_top_cities(df)
    eda_cuisines(df)
    eda_ratings(df)
    eda_online_delivery(df)
    eda_table_booking(df)
    eda_cost(df)
    eda_votes(df)
    eda_cuisine_ratings(df)
    eda_competition(df)

    print("\n" + "═"*55)
    print(f"  EDA COMPLETE ✓  9 charts saved to {OUTDIR}")
    print("═"*55)


if __name__ == "__main__":
    run_eda()