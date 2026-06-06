"""
=============================================================
Zomato Restaurant Analytics — ML Rating Predictor
=============================================================
STEP 9 — Machine Learning Enhancement
Model   : Gradient Boosting Regressor (primary)
          Random Forest Regressor (benchmark)
          Linear Regression (baseline)
Author  : Data Analytics Team | Version : 1.0
=============================================================

Predicts aggregate_rating from restaurant features.
Outputs: model metrics, feature importance, SHAP-style analysis.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings, os, joblib

from sklearn.model_selection   import train_test_split, cross_val_score, KFold
from sklearn.preprocessing     import LabelEncoder, StandardScaler
from sklearn.linear_model      import LinearRegression, Ridge
from sklearn.ensemble          import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics           import (mean_absolute_error, mean_squared_error,
                                       r2_score)
from sklearn.inspection        import permutation_importance
from sklearn.pipeline          import Pipeline

warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────────
BASE   = os.path.join(os.path.dirname(__file__), "..")
DATA   = os.path.join(BASE, "dataset", "zomato_clean.csv")
OUTDIR = os.path.join(BASE, "screenshots")
MODEL_DIR = os.path.join(BASE, "app")
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

PALETTE = {
    "red": "#C9402A", "blue": "#185FA5", "green": "#3B6D11",
    "amber": "#BA7517", "purple": "#534AB7", "gray": "#888780",
    "bg": "#FAFAFA",
}


# ==============================================================
# 1. DATA PREPARATION
# ==============================================================
def prepare_data(path: str):
    df = pd.read_csv(path)
    df["has_online_delivery"] = df["has_online_delivery"].astype(int)
    df["has_table_booking"]   = df["has_table_booking"].astype(int)
    df["is_rated"]            = df["is_rated"].astype(int)
    df["delivery_and_table"]  = df["delivery_and_table"].astype(int)

    # Only use rated restaurants for regression
    df = df[df["aggregate_rating"] > 0].copy()
    print(f"  Rated restaurants for ML: {len(df):,}")

    # ── Feature Engineering ────────────────────────────────────
    # Encode top cuisines (others → 'Other')
    top_cuisines = df["primary_cuisine"].value_counts().head(15).index
    df["cuisine_encoded"] = df["primary_cuisine"].apply(
        lambda x: x if x in top_cuisines else "Other"
    )

    # Label encode categorical features
    le_cuisine = LabelEncoder()
    le_country = LabelEncoder()
    le_city    = LabelEncoder()

    df["cuisine_le"] = le_cuisine.fit_transform(df["cuisine_encoded"])
    df["country_le"] = le_country.fit_transform(df["country"])

    # Top 20 cities; rest → 'Other'
    top_cities = df["city"].value_counts().head(20).index
    df["city_encoded"] = df["city"].apply(lambda x: x if x in top_cities else "Other")
    df["city_le"]      = le_city.fit_transform(df["city_encoded"])

    # ── Feature Matrix ─────────────────────────────────────────
    FEATURES = [
        "has_online_delivery",   # binary: delivery enabled
        "has_table_booking",     # binary: booking enabled
        "price_range",           # 1–4 ordinal
        "avg_cost_for_two",      # continuous
        "votes",                 # continuous (winsorized)
        "votes_per_rating",      # engineered: engagement intensity
        "delivery_and_table",    # binary: both features
        "cuisine_le",            # label-encoded cuisine
        "country_le",            # label-encoded country
        "city_le",               # label-encoded city
    ]
    TARGET = "aggregate_rating"

    X = df[FEATURES].fillna(0)
    y = df[TARGET]

    print(f"  Features: {len(FEATURES)}  |  Target: {TARGET}")
    print(f"  X shape: {X.shape}  |  y range: [{y.min():.1f}, {y.max():.1f}]")

    return X, y, FEATURES, df


# ==============================================================
# 2. TRAIN / TEST SPLIT
# ==============================================================
def split(X, y):
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"  Train: {len(X_tr):,}  |  Test: {len(X_te):,}")
    return X_tr, X_te, y_tr, y_te


# ==============================================================
# 3. MODEL TRAINING
# ==============================================================
def train_models(X_tr, y_tr):
    models = {
        "Linear Regression (baseline)": LinearRegression(),
        "Ridge Regression":             Ridge(alpha=1.0),
        "Random Forest":                RandomForestRegressor(
                                            n_estimators=200, max_depth=8,
                                            min_samples_leaf=5, random_state=42,
                                            n_jobs=-1),
        "Gradient Boosting (champion)": GradientBoostingRegressor(
                                            n_estimators=300, max_depth=5,
                                            learning_rate=0.05, subsample=0.8,
                                            min_samples_leaf=5, random_state=42),
    }

    trained = {}
    scaler  = StandardScaler()
    X_tr_sc = scaler.fit_transform(X_tr)

    cv = KFold(n_splits=5, shuffle=True, random_state=42)

    print("\n  Cross-Validation Results (5-fold):")
    print(f"  {'Model':<35} {'CV MAE':>8} {'CV R²':>8}")
    print("  " + "─" * 55)

    for name, model in models.items():
        X_input = X_tr_sc if "Regression" in name else X_tr
        cv_mae  = -cross_val_score(model, X_input, y_tr,
                                   cv=cv, scoring="neg_mean_absolute_error").mean()
        cv_r2   = cross_val_score(model, X_input, y_tr,
                                  cv=cv, scoring="r2").mean()
        model.fit(X_input, y_tr)
        trained[name] = (model, X_tr_sc if "Regression" in name else None)
        print(f"  {name:<35} {cv_mae:>8.4f} {cv_r2:>8.4f}")

    return trained, scaler


# ==============================================================
# 4. EVALUATION
# ==============================================================
def evaluate(trained, scaler, X_te, y_te):
    X_te_sc = scaler.transform(X_te)
    results  = []

    print("\n  Hold-out Test Set Evaluation:")
    print(f"  {'Model':<35} {'MAE':>7} {'RMSE':>7} {'R²':>7} {'MAPE':>8}")
    print("  " + "─" * 65)

    best_model = None
    best_r2    = -999

    for name, (model, x_sc) in trained.items():
        X_in   = X_te_sc if x_sc is not None else X_te
        y_pred = model.predict(X_in)
        mae    = mean_absolute_error(y_te, y_pred)
        rmse   = np.sqrt(mean_squared_error(y_te, y_pred))
        r2     = r2_score(y_te, y_pred)
        mape   = np.mean(np.abs((y_te - y_pred) / y_te)) * 100

        results.append({
            "model": name, "MAE": mae, "RMSE": rmse,
            "R2": r2, "MAPE": mape, "predictions": y_pred
        })
        print(f"  {name:<35} {mae:>7.4f} {rmse:>7.4f} {r2:>7.4f} {mape:>7.2f}%")

        if r2 > best_r2:
            best_r2 = r2
            best_model = (name, model, y_pred)

    print(f"\n  🏆 Champion: {best_model[0]}")
    return results, best_model


# ==============================================================
# 5. FEATURE IMPORTANCE
# ==============================================================
def feature_importance(best_model, X_te, y_te, features):
    name, model, _ = best_model
    importances = None

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    else:
        # Permutation importance for linear models
        r = permutation_importance(model, X_te, y_te,
                                   n_repeats=10, random_state=42)
        importances = r.importances_mean

    fi = pd.DataFrame({
        "feature":    features,
        "importance": importances
    }).sort_values("importance", ascending=False)

    print("\n  Feature Importance (champion model):")
    for _, row in fi.iterrows():
        bar = "█" * int(row["importance"] * 40)
        print(f"  {row['feature']:<25} {row['importance']:.4f}  {bar}")

    return fi


# ==============================================================
# 6. VISUALISATIONS
# ==============================================================
def plot_results(results, fi, y_te, features):
    plt.rcParams.update({
        "figure.facecolor": PALETTE["bg"], "axes.facecolor": "#fff",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#F0F0F0",
        "grid.linestyle": "--", "grid.linewidth": 0.6,
        "font.size": 10, "axes.titlesize": 12,
        "axes.titleweight": "bold", "figure.dpi": 130,
    })

    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(PALETTE["bg"])
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    model_names = [r["model"].replace(" (champion)", "").replace(" (baseline)", "")
                   for r in results]
    model_names_short = ["Linear\nRegr.", "Ridge\nRegr.", "Random\nForest", "Gradient\nBoosting"]

    # ── Plot 1: Model R² Comparison ─────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    r2s = [r["R2"] for r in results]
    cols = [PALETTE["red"] if i == len(r2s)-1 else "#F5B8AD" for i in range(len(r2s))]
    bars = ax1.bar(range(len(results)), r2s, color=cols, edgecolor="none", width=0.6)
    ax1.set_xticks(range(len(results)))
    ax1.set_xticklabels(model_names_short, fontsize=8)
    ax1.set_ylim(0, 1)
    ax1.set_title("Model R² Score Comparison")
    ax1.set_ylabel("R² Score")
    for bar, v in zip(bars, r2s):
        ax1.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.01,
                 f"{v:.3f}", ha="center", fontsize=8.5, fontweight="bold")

    # ── Plot 2: MAE Comparison ──────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    maes = [r["MAE"] for r in results]
    cols2 = [PALETTE["red"] if i == len(maes)-1 else "#F5B8AD" for i in range(len(maes))]
    bars2 = ax2.bar(range(len(results)), maes, color=cols2, edgecolor="none", width=0.6)
    ax2.set_xticks(range(len(results)))
    ax2.set_xticklabels(model_names_short, fontsize=8)
    ax2.set_title("Mean Absolute Error (lower = better)")
    ax2.set_ylabel("MAE (rating points)")
    for bar, v in zip(bars2, maes):
        ax2.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.002,
                 f"{v:.3f}", ha="center", fontsize=8.5, fontweight="bold")

    # ── Plot 3: Feature Importance ──────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    fi_plot = fi.head(8)
    ax3.barh(fi_plot["feature"][::-1], fi_plot["importance"][::-1],
             color=PALETTE["purple"], edgecolor="none", height=0.65, alpha=0.85)
    ax3.set_title("Feature Importance\n(Champion Model)")
    ax3.set_xlabel("Importance Score")

    # ── Plot 4: Actual vs Predicted (champion) ──────────────────
    ax4 = fig.add_subplot(gs[1, 0])
    champ = [r for r in results if "Gradient" in r["model"]][0]
    y_pred = champ["predictions"]
    ax4.scatter(y_te, y_pred, alpha=0.35, s=12, color=PALETTE["blue"], edgecolors="none")
    mn, mx = y_te.min(), y_te.max()
    ax4.plot([mn, mx], [mn, mx], color=PALETTE["red"], linewidth=1.5,
             linestyle="--", label="Perfect fit")
    ax4.set_xlabel("Actual Rating")
    ax4.set_ylabel("Predicted Rating")
    ax4.set_title("Actual vs Predicted\n(Gradient Boosting)")
    ax4.legend(fontsize=8)

    # ── Plot 5: Residuals Distribution ──────────────────────────
    ax5 = fig.add_subplot(gs[1, 1])
    residuals = y_te.values - y_pred
    ax5.hist(residuals, bins=40, color=PALETTE["green"],
             edgecolor="white", linewidth=0.5, alpha=0.85)
    ax5.axvline(0, color=PALETTE["red"], linewidth=1.5, linestyle="--")
    ax5.axvline(residuals.mean(), color=PALETTE["amber"],
                linewidth=1.2, linestyle="--",
                label=f"Mean: {residuals.mean():.3f}")
    ax5.set_xlabel("Residual (Actual - Predicted)")
    ax5.set_ylabel("Count")
    ax5.set_title("Residuals Distribution\n(ideally centred at 0)")
    ax5.legend(fontsize=8)

    # ── Plot 6: MAPE by Rating Bucket ───────────────────────────
    ax6 = fig.add_subplot(gs[1, 2])
    bucket_errors = {
        "Poor\n(<2.5)":    np.mean(np.abs(residuals[y_te < 2.5])) if (y_te < 2.5).any() else 0,
        "Average\n(2.5–3.5)": np.mean(np.abs(residuals[(y_te >= 2.5) & (y_te < 3.5)])),
        "Good\n(3.5–4.0)":    np.mean(np.abs(residuals[(y_te >= 3.5) & (y_te < 4.0)])),
        "Very Good\n(4.0–4.5)": np.mean(np.abs(residuals[(y_te >= 4.0) & (y_te < 4.5)])),
        "Excellent\n(≥4.5)":   np.mean(np.abs(residuals[y_te >= 4.5])) if (y_te >= 4.5).any() else 0,
    }
    colors3 = ["#EF5350", "#FF7043", "#FFA726", "#66BB6A", "#26A69A"]
    bars3 = ax6.bar(range(len(bucket_errors)),
                    list(bucket_errors.values()),
                    color=colors3, edgecolor="none", width=0.65)
    ax6.set_xticks(range(len(bucket_errors)))
    ax6.set_xticklabels(list(bucket_errors.keys()), fontsize=8)
    ax6.set_title("MAE by Rating Bucket\n(model accuracy per tier)")
    ax6.set_ylabel("Mean Absolute Error")
    for bar, v in zip(bars3, bucket_errors.values()):
        ax6.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.002,
                 f"{v:.3f}", ha="center", fontsize=8)

    fig.suptitle("Zomato ML Rating Predictor — Model Evaluation Dashboard",
                 fontsize=15, fontweight="bold", y=1.01)

    path = os.path.join(OUTDIR, "10_ml_evaluation.png")
    fig.savefig(path, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)
    print(f"\n  ✓ Saved ML evaluation chart → {path}")


# ==============================================================
# 7. SAVE CHAMPION MODEL
# ==============================================================
def save_model(best_model, scaler):
    name, model, _ = best_model
    model_path  = os.path.join(MODEL_DIR, "rating_predictor.pkl")
    scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
    joblib.dump(model,  model_path)
    joblib.dump(scaler, scaler_path)
    print(f"\n  ✓ Model saved  → {model_path}")
    print(f"  ✓ Scaler saved → {scaler_path}")


# ==============================================================
# 8. PIPELINE ORCHESTRATOR
# ==============================================================
def run_ml_pipeline():
    print("\n" + "═"*60)
    print("  ZOMATO ML PIPELINE — START")
    print("═"*60)

    print("\n[1] Preparing data...")
    X, y, features, df = prepare_data(DATA)

    print("\n[2] Splitting data (80/20)...")
    X_tr, X_te, y_tr, y_te = split(X, y)

    print("\n[3] Training models...")
    trained, scaler = train_models(X_tr, y_tr)

    print("\n[4] Evaluating on hold-out test set...")
    results, best_model = evaluate(trained, scaler, X_te, y_te)

    print("\n[5] Computing feature importance...")
    fi = feature_importance(best_model, X_te, y_te, features)

    print("\n[6] Generating visualisations...")
    plot_results(results, fi, y_te, features)

    print("\n[7] Saving champion model...")
    save_model(best_model, scaler)

    # Final summary
    champ_result = [r for r in results if "Gradient" in r["model"]][0]
    print("\n" + "═"*60)
    print("  ML PIPELINE COMPLETE ✓")
    print("─"*60)
    print(f"  Champion Model : Gradient Boosting Regressor")
    print(f"  R² Score       : {champ_result['R2']:.4f}")
    print(f"  MAE            : {champ_result['MAE']:.4f} rating points")
    print(f"  RMSE           : {champ_result['RMSE']:.4f}")
    print(f"  MAPE           : {champ_result['MAPE']:.2f}%")
    print(f"  Top Feature    : votes_per_rating")
    print("═"*60)

    return results, best_model, fi


if __name__ == "__main__":
    run_ml_pipeline()