"""
=============================================================
Zomato Restaurant Analytics & Customer Insights Dashboard
=============================================================
STEP 2 — Data Cleaning & Feature Engineering
Author  : Data Analytics Team
Version : 1.0
=============================================================

Production-quality data cleaning pipeline for the Zomato
restaurant dataset. Follows PEP-8 and modular architecture.
"""

import pandas as pd
import numpy as np
import warnings
import os
import logging

warnings.filterwarnings("ignore")

# ── Logging Configuration ──────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Paths ──────────────────────────────────────────────────
RAW_PATH    = os.path.join(os.path.dirname(__file__), "../dataset/zomato.csv")
CLEAN_PATH  = os.path.join(os.path.dirname(__file__), "../dataset/zomato_clean.csv")


# ==============================================================
# 1. LOAD DATA
# ==============================================================
def load_data(path: str) -> pd.DataFrame:
    """Load raw CSV with latin-1 encoding (handles special characters)."""
    log.info("Loading dataset from: %s", path)
    df = pd.read_csv(path, encoding="latin-1")
    log.info("Raw shape: %s rows × %s columns", *df.shape)
    return df


# ==============================================================
# 2. COLUMN STANDARDISATION
# ==============================================================
def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns to snake_case for consistent programmatic access.
    Original names preserved in comments for traceability.
    """
    rename_map = {
        "Restaurant ID"       : "restaurant_id",
        "Restaurant Name"     : "restaurant_name",
        "Country Code"        : "country_code",
        "City"                : "city",
        "Address"             : "address",
        "Locality"            : "locality",
        "Locality Verbose"    : "locality_verbose",
        "Longitude"           : "longitude",
        "Latitude"            : "latitude",
        "Cuisines"            : "cuisines",
        "Average Cost for two": "avg_cost_for_two",
        "Currency"            : "currency",
        "Has Table booking"   : "has_table_booking",
        "Has Online delivery" : "has_online_delivery",
        "Is delivering now"   : "is_delivering_now",
        "Switch to order menu": "switch_to_order_menu",
        "Price range"         : "price_range",
        "Aggregate rating"    : "aggregate_rating",
        "Rating color"        : "rating_color",
        "Rating text"         : "rating_text",
        "Votes"               : "votes",
    }
    df = df.rename(columns=rename_map)
    log.info("Columns standardised to snake_case.")
    return df


# ==============================================================
# 3. MISSING VALUE ANALYSIS & TREATMENT
# ==============================================================
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strategy:
      - cuisines   : fill with 'Unknown' (categorical – mode imputation
                     would bias towards North Indian in India-heavy data)
      - rating = 0 : means 'Not rated'; keep as-is but flag with a boolean
      - All other  : assess and document
    """
    log.info("=== Missing Value Report ===")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    report = pd.DataFrame({"missing_count": missing, "missing_%": missing_pct})
    report = report[report["missing_count"] > 0]
    log.info("\n%s", report.to_string())

    # Cuisines — fill unknown
    null_cuisines = df["cuisines"].isnull().sum()
    if null_cuisines > 0:
        df["cuisines"] = df["cuisines"].fillna("Unknown")
        log.info("Filled %d null cuisines with 'Unknown'.", null_cuisines)

    return df


# ==============================================================
# 4. DUPLICATE DETECTION & REMOVAL
# ==============================================================
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows; log count for audit trail."""
    before = len(df)
    df = df.drop_duplicates(subset=["restaurant_id"], keep="first")
    removed = before - len(df)
    log.info("Duplicates removed: %d  (rows remaining: %d)", removed, len(df))
    return df


# ==============================================================
# 5. DATA TYPE CONVERSION
# ==============================================================
def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enforce correct dtypes for downstream analysis:
      - Boolean  : Yes/No columns → bool
      - Numeric  : already correct but validated
      - String   : object columns stripped of whitespace
    """
    # Yes/No → bool
    bool_cols = [
        "has_table_booking",
        "has_online_delivery",
        "is_delivering_now",
        "switch_to_order_menu",
    ]
    for col in bool_cols:
        df[col] = df[col].str.strip().map({"Yes": True, "No": False})
        df[col] = df[col].astype(bool)

    # Strip whitespace from all string columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # Ensure numeric types
    df["avg_cost_for_two"]  = pd.to_numeric(df["avg_cost_for_two"],  errors="coerce")
    df["aggregate_rating"]  = pd.to_numeric(df["aggregate_rating"],  errors="coerce")
    df["votes"]             = pd.to_numeric(df["votes"],              errors="coerce")

    log.info("Dtypes converted successfully.")
    return df


# ==============================================================
# 6. OUTLIER DETECTION (IQR Method)
# ==============================================================
def detect_and_cap_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Use IQR method to detect outliers in cost and votes.
    Strategy: CAP (Winsorize) rather than drop — preserves data
    volume while limiting distortion in aggregations.
    """
    numeric_cols = ["avg_cost_for_two", "votes"]

    for col in numeric_cols:
        q1  = df[col].quantile(0.25)
        q3  = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        n_out = ((df[col] < lower) | (df[col] > upper)).sum()
        df[col] = df[col].clip(lower=lower, upper=upper)
        log.info("%-22s | IQR [%.1f – %.1f] | %d outliers capped",
                 col, lower, upper, n_out)

    return df


# ==============================================================
# 7. DATA VALIDATION
# ==============================================================
def validate_data(df: pd.DataFrame) -> None:
    """
    Sanity checks post-cleaning. Raises ValueError on critical
    failures to prevent silent bad data flowing downstream.
    """
    # Rating must be in [0, 5]
    invalid_rating = df[~df["aggregate_rating"].between(0, 5)]
    if not invalid_rating.empty:
        log.warning("Found %d rows with aggregate_rating outside [0,5].",
                    len(invalid_rating))

    # Cost cannot be negative
    neg_cost = df[df["avg_cost_for_two"] < 0]
    if not neg_cost.empty:
        raise ValueError(f"{len(neg_cost)} rows have negative avg_cost_for_two!")

    # Votes cannot be negative
    neg_votes = df[df["votes"] < 0]
    if not neg_votes.empty:
        raise ValueError(f"{len(neg_votes)} rows have negative votes!")

    log.info("Data validation passed ✓")


# ==============================================================
# 8. FEATURE ENGINEERING
# ==============================================================
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create derived columns that enrich analysis:
      1. primary_cuisine    — first cuisine listed (most representative)
      2. rating_bucket      — ordinal grouping of aggregate_rating
      3. cost_category      — affordability tier
      4. is_rated           — flag: restaurant has at least 1 review
      5. delivery_and_table — both features enabled (premium UX flag)
      6. votes_per_rating   — engagement intensity metric
    """

    # 1. Primary cuisine (first in comma-separated list)
    df["primary_cuisine"] = df["cuisines"].str.split(",").str[0].str.strip()

    # 2. Rating bucket
    def rating_bucket(r):
        if r == 0:      return "Not Rated"
        elif r < 2.5:   return "Poor (< 2.5)"
        elif r < 3.5:   return "Average (2.5–3.5)"
        elif r < 4.0:   return "Good (3.5–4.0)"
        elif r < 4.5:   return "Very Good (4.0–4.5)"
        else:           return "Excellent (≥ 4.5)"

    df["rating_bucket"] = df["aggregate_rating"].apply(rating_bucket)

    # 3. Cost category (based on price_range 1–4)
    cost_map = {1: "Budget", 2: "Affordable", 3: "Mid-Range", 4: "Premium"}
    df["cost_category"] = df["price_range"].map(cost_map)

    # 4. Is rated
    df["is_rated"] = df["aggregate_rating"] > 0

    # 5. Both delivery & table booking
    df["delivery_and_table"] = df["has_online_delivery"] & df["has_table_booking"]

    # 6. Votes per rating point (engagement intensity)
    df["votes_per_rating"] = np.where(
        df["aggregate_rating"] > 0,
        (df["votes"] / df["aggregate_rating"]).round(2),
        0,
    )

    log.info("Feature engineering complete. New columns: %s",
             ["primary_cuisine", "rating_bucket", "cost_category",
              "is_rated", "delivery_and_table", "votes_per_rating"])

    return df


# ==============================================================
# 9. COUNTRY CODE MAPPING
# ==============================================================
def map_country_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map Zomato's numeric Country Code → human-readable country name.
    Source: Zomato's public country code reference.
    """
    country_map = {
        1:   "India",
        14:  "Australia",
        30:  "Brazil",
        37:  "Canada",
        94:  "Indonesia",
        148: "New Zealand",
        162: "Philippines",
        166: "Qatar",
        184: "Singapore",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "UAE",
        215: "United Kingdom",
        216: "United States",
    }
    df["country"] = df["country_code"].map(country_map).fillna("Other")
    log.info("Country names mapped.")
    return df


# ==============================================================
# 10. SAVE CLEAN DATASET
# ==============================================================
def save_clean_data(df: pd.DataFrame, path: str) -> None:
    """Persist the cleaned DataFrame as UTF-8 CSV."""
    df.to_csv(path, index=False, encoding="utf-8")
    log.info("Clean dataset saved → %s  (%d rows × %d cols)", path, *df.shape)


# ==============================================================
# PIPELINE ORCHESTRATOR
# ==============================================================
def run_cleaning_pipeline(raw_path: str = RAW_PATH,
                          clean_path: str = CLEAN_PATH) -> pd.DataFrame:
    """
    Executes the full data cleaning pipeline end-to-end.
    Returns the cleaned DataFrame for immediate downstream use.
    """
    log.info("══════════════════════════════════════════")
    log.info("  ZOMATO DATA CLEANING PIPELINE — START")
    log.info("══════════════════════════════════════════")

    df = load_data(raw_path)
    df = standardise_columns(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = convert_dtypes(df)
    df = detect_and_cap_outliers(df)
    validate_data(df)
    df = engineer_features(df)
    df = map_country_names(df)
    save_clean_data(df, clean_path)

    log.info("══════════════════════════════════════════")
    log.info("  PIPELINE COMPLETE ✓  Final shape: %d × %d", *df.shape)
    log.info("══════════════════════════════════════════")
    return df


# ==============================================================
# ENTRY POINT
# ==============================================================
if __name__ == "__main__":
    cleaned_df = run_cleaning_pipeline()

    # Quick summary report
    print("\n" + "═" * 55)
    print("  DATA QUALITY SUMMARY")
    print("═" * 55)
    print(f"  Total Restaurants  : {len(cleaned_df):,}")
    print(f"  Total Countries    : {cleaned_df['country'].nunique()}")
    print(f"  Total Cities       : {cleaned_df['city'].nunique()}")
    print(f"  Unique Cuisines    : {cleaned_df['primary_cuisine'].nunique()}")
    print(f"  Avg Rating         : {cleaned_df[cleaned_df['aggregate_rating']>0]['aggregate_rating'].mean():.2f}")
    print(f"  Online Delivery %  : {cleaned_df['has_online_delivery'].mean()*100:.1f}%")
    print(f"  Table Booking %    : {cleaned_df['has_table_booking'].mean()*100:.1f}%")
    print(f"  Null Values Left   : {cleaned_df.isnull().sum().sum()}")
    print("═" * 55)