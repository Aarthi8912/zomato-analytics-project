"""
Loads clean CSV into SQLite and runs all 30 SQL queries.
Prints formatted results for verification.
"""
import sqlite3, pandas as pd, textwrap, os, re

BASE    = os.path.join(os.path.dirname(__file__), "..")
DATA    = os.path.join(BASE, "dataset", "zomato_clean.csv")
SQL_FILE= os.path.join(BASE, "sql_queries", "zomato_analysis.sql")
DB_PATH = ":memory:"   # in-memory SQLite

con = sqlite3.connect(DB_PATH)

# ── Load CSV → SQLite ──────────────────────────────────────────
df = pd.read_csv(DATA)
df["has_table_booking"]   = df["has_table_booking"].astype(int)
df["has_online_delivery"] = df["has_online_delivery"].astype(int)
df["is_rated"]            = df["is_rated"].astype(int)
df["delivery_and_table"]  = df["delivery_and_table"].astype(int)
df.to_sql("restaurants", con, if_exists="replace", index=False)
print(f"Loaded {len(df):,} rows into SQLite\n")

# ── Parse SQL file into individual queries ─────────────────────
with open(SQL_FILE) as f:
    raw = f.read()

# Split on query header comments (-- ── Q...)
blocks = re.split(r"(-- ── Q\d+:.*)", raw)
queries = []
current_label = ""
for block in blocks:
    if re.match(r"-- ── Q\d+:", block):
        current_label = block.strip()
    elif current_label and block.strip():
        # grab the first SELECT statement
        stmts = [s.strip() for s in block.split(";") if "SELECT" in s.upper()]
        if stmts:
            queries.append((current_label, stmts[0] + ";"))
            current_label = ""

print(f"Found {len(queries)} queries to execute\n")
print("═" * 70)

# ── Execute each query ─────────────────────────────────────────
for label, sql in queries:
    q_num = re.search(r"Q(\d+)", label).group(0)
    title = label.replace("-- ── ", "").strip()
    print(f"\n{'━'*70}")
    print(f"  {title}")
    print(f"{'━'*70}")
    try:
        result = pd.read_sql_query(sql, con)
        if result.empty:
            print("  (no rows returned)")
        else:
            # limit display to 8 rows, truncate wide cols
            display = result.head(8).copy()
            for col in display.select_dtypes(include="object").columns:
                display[col] = display[col].str[:28]
            pd.set_option("display.max_columns", 12)
            pd.set_option("display.width", 120)
            pd.set_option("display.float_format", "{:.2f}".format)
            print(display.to_string(index=False))
            if len(result) > 8:
                print(f"  ... and {len(result)-8} more rows")
    except Exception as e:
        print(f"  ERROR: {e}")

print(f"\n{'═'*70}")
print("  ALL QUERIES EXECUTED ✓")
print(f"{'═'*70}")
con.close()
