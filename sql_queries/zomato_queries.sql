-- ================================================================
-- Zomato Restaurant Analytics & Customer Insights Dashboard
-- ================================================================
-- STEP 4 — SQL Analysis (25+ Advanced Business Queries)
-- Database : SQLite (compatible with PostgreSQL / MySQL)
-- Author   : Data Analytics Team
-- Version  : 1.0
-- ================================================================


-- ================================================================
-- SECTION 0 — TABLE CREATION & DATA LOAD
-- ================================================================

CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id         INTEGER PRIMARY KEY,
    restaurant_name       TEXT    NOT NULL,
    country_code          INTEGER,
    country               TEXT,
    city                  TEXT,
    address               TEXT,
    locality              TEXT,
    longitude             REAL,
    latitude              REAL,
    cuisines              TEXT,
    primary_cuisine       TEXT,
    avg_cost_for_two      REAL,
    currency              TEXT,
    has_table_booking     INTEGER,   -- 1 = Yes, 0 = No
    has_online_delivery   INTEGER,   -- 1 = Yes, 0 = No
    is_delivering_now     INTEGER,
    price_range           INTEGER,   -- 1=Budget … 4=Premium
    aggregate_rating      REAL,
    rating_color          TEXT,
    rating_text           TEXT,
    rating_bucket         TEXT,
    cost_category         TEXT,
    votes                 INTEGER,
    is_rated              INTEGER,
    delivery_and_table    INTEGER,
    votes_per_rating      REAL
);

-- (Data loaded via Python script — see notebooks/02_eda.py)


-- ================================================================
-- SECTION 1 — FOUNDATIONAL KPI QUERIES
-- ================================================================

-- ── Q01: Executive KPI Dashboard ────────────────────────────────
-- Business: Single-row snapshot for the executive summary card
SELECT
    COUNT(*)                                              AS total_restaurants,
    COUNT(DISTINCT country)                               AS total_countries,
    COUNT(DISTINCT city)                                  AS total_cities,
    COUNT(DISTINCT primary_cuisine)                       AS unique_cuisines,
    ROUND(AVG(CASE WHEN aggregate_rating > 0
                   THEN aggregate_rating END), 2)         AS avg_rating,
    ROUND(AVG(avg_cost_for_two), 2)                       AS avg_cost_for_two,
    SUM(votes)                                            AS total_votes,
    ROUND(SUM(has_online_delivery) * 100.0 / COUNT(*), 1) AS online_delivery_pct,
    ROUND(SUM(has_table_booking)   * 100.0 / COUNT(*), 1) AS table_booking_pct,
    ROUND(SUM(CASE WHEN aggregate_rating >= 4.0 THEN 1 ELSE 0 END)
          * 100.0 / COUNT(*), 1)                          AS high_rated_pct
FROM restaurants;


-- ── Q02: Restaurant Count by Country ────────────────────────────
-- Business: Market size & geographic footprint
SELECT
    country,
    COUNT(*)                                        AS restaurant_count,
    ROUND(COUNT(*) * 100.0 /
          (SELECT COUNT(*) FROM restaurants), 2)    AS market_share_pct,
    ROUND(AVG(CASE WHEN aggregate_rating > 0
                   THEN aggregate_rating END), 2)   AS avg_rating,
    ROUND(AVG(avg_cost_for_two), 0)                 AS avg_cost,
    SUM(votes)                                      AS total_votes
FROM restaurants
GROUP BY country
ORDER BY restaurant_count DESC;


-- ── Q03: Top 20 Cities by Restaurant Count ──────────────────────
-- Business: Identify saturated vs emerging markets
SELECT
    city,
    country,
    COUNT(*)                                            AS restaurant_count,
    ROUND(AVG(CASE WHEN aggregate_rating > 0
                   THEN aggregate_rating END), 2)       AS avg_rating,
    ROUND(AVG(avg_cost_for_two), 0)                     AS avg_cost,
    ROUND(SUM(has_online_delivery) * 100.0 / COUNT(*), 1) AS delivery_pct
FROM restaurants
GROUP BY city, country
ORDER BY restaurant_count DESC
LIMIT 20;


-- ================================================================
-- SECTION 2 — CUISINE ANALYSIS
-- ================================================================

-- ── Q04: Top Cuisines by Restaurant Count & Avg Rating ──────────
-- Business: Identify dominant cuisines and their quality scores
SELECT
    primary_cuisine,
    COUNT(*)                                          AS restaurant_count,
    ROUND(COUNT(*) * 100.0 /
          (SELECT COUNT(*) FROM restaurants), 2)      AS market_share_pct,
    ROUND(AVG(CASE WHEN aggregate_rating > 0
                   THEN aggregate_rating END), 2)     AS avg_rating,
    ROUND(AVG(avg_cost_for_two), 0)                   AS avg_cost,
    SUM(votes)                                        AS total_votes,
    ROUND(AVG(votes), 0)                              AS avg_votes_per_restaurant
FROM restaurants
WHERE primary_cuisine != 'Unknown'
GROUP BY primary_cuisine
HAVING COUNT(*) >= 20
ORDER BY restaurant_count DESC
LIMIT 20;


-- ── Q05: Best-Rated Cuisines (min 50 restaurants) ───────────────
-- Business: Quality benchmark by cuisine for marketing campaigns
SELECT
    primary_cuisine,
    COUNT(*)                                          AS restaurant_count,
    ROUND(AVG(aggregate_rating), 2)                   AS avg_rating,
    MAX(aggregate_rating)                             AS max_rating,
    MIN(aggregate_rating)                             AS min_rating,
    ROUND(AVG(avg_cost_for_two), 0)                   AS avg_cost
FROM restaurants
WHERE aggregate_rating > 0
  AND primary_cuisine != 'Unknown'
GROUP BY primary_cuisine
HAVING COUNT(*) >= 50
ORDER BY avg_rating DESC
LIMIT 15;


-- ── Q06: Cuisine Performance by Price Tier (Pivot-style) ────────
-- Business: Find the best cuisine-price combinations
SELECT
    primary_cuisine,
    ROUND(AVG(CASE WHEN cost_category = 'Budget'
                   THEN aggregate_rating END), 2)     AS budget_rating,
    ROUND(AVG(CASE WHEN cost_category = 'Affordable'
                   THEN aggregate_rating END), 2)     AS affordable_rating,
    ROUND(AVG(CASE WHEN cost_category = 'Mid-Range'
                   THEN aggregate_rating END), 2)     AS midrange_rating,
    ROUND(AVG(CASE WHEN cost_category = 'Premium'
                   THEN aggregate_rating END), 2)     AS premium_rating,
    COUNT(*)                                          AS total_count
FROM restaurants
WHERE aggregate_rating > 0
  AND primary_cuisine != 'Unknown'
GROUP BY primary_cuisine
HAVING COUNT(*) >= 30
ORDER BY COALESCE(
    AVG(CASE WHEN cost_category = 'Mid-Range' THEN aggregate_rating END), 0
) DESC
LIMIT 15;


-- ================================================================
-- SECTION 3 — RATING ANALYSIS
-- ================================================================

-- ── Q07: Rating Distribution (Bucket Summary) ───────────────────
-- Business: Understand quality spread across the platform
SELECT
    rating_bucket,
    COUNT(*)                                          AS restaurant_count,
    ROUND(COUNT(*) * 100.0 /
          (SELECT COUNT(*) FROM restaurants), 2)      AS pct_of_total,
    ROUND(AVG(avg_cost_for_two), 0)                   AS avg_cost,
    ROUND(AVG(votes), 0)                              AS avg_votes
FROM restaurants
GROUP BY rating_bucket
ORDER BY
    CASE rating_bucket
        WHEN 'Excellent (≥ 4.5)'    THEN 1
        WHEN 'Very Good (4.0–4.5)'  THEN 2
        WHEN 'Good (3.5–4.0)'       THEN 3
        WHEN 'Average (2.5–3.5)'    THEN 4
        WHEN 'Poor (< 2.5)'         THEN 5
        ELSE 6
    END;


-- ── Q08: Top 10 Highest-Rated Restaurants (min 100 votes) ───────
-- Business: Showcase restaurant excellence for platform promotion
SELECT
    restaurant_name,
    city,
    country,
    primary_cuisine,
    aggregate_rating,
    votes,
    avg_cost_for_two,
    cost_category,
    CASE WHEN has_online_delivery = 1 THEN 'Yes' ELSE 'No' END AS delivery,
    CASE WHEN has_table_booking   = 1 THEN 'Yes' ELSE 'No' END AS table_booking
FROM restaurants
WHERE aggregate_rating >= 4.5
  AND votes >= 100
ORDER BY aggregate_rating DESC, votes DESC
LIMIT 10;


-- ── Q09: City-Level Rating Benchmarks ───────────────────────────
-- Business: Identify over/underperforming cities vs global avg
WITH global_avg AS (
    SELECT AVG(aggregate_rating) AS global_mean
    FROM restaurants
    WHERE aggregate_rating > 0
)
SELECT
    city,
    country,
    COUNT(*)                                              AS restaurant_count,
    ROUND(AVG(aggregate_rating), 2)                       AS city_avg_rating,
    ROUND(AVG(aggregate_rating) -
          (SELECT global_mean FROM global_avg), 2)        AS vs_global_avg,
    CASE
        WHEN AVG(aggregate_rating) >
             (SELECT global_mean FROM global_avg) + 0.2  THEN 'Outperforming'
        WHEN AVG(aggregate_rating) <
             (SELECT global_mean FROM global_avg) - 0.2  THEN 'Underperforming'
        ELSE 'On Par'
    END                                                   AS performance_flag
FROM restaurants
WHERE aggregate_rating > 0
GROUP BY city, country
HAVING COUNT(*) >= 30
ORDER BY city_avg_rating DESC
LIMIT 20;


-- ================================================================
-- SECTION 4 — DELIVERY & BOOKING ANALYSIS
-- ================================================================

-- ── Q10: Online Delivery Adoption by Country ────────────────────
-- Business: Delivery market maturity by geography
SELECT
    country,
    COUNT(*)                                              AS total_restaurants,
    SUM(has_online_delivery)                              AS delivery_restaurants,
    ROUND(SUM(has_online_delivery) * 100.0 / COUNT(*), 1) AS delivery_adoption_pct,
    ROUND(AVG(CASE WHEN has_online_delivery = 1
                   THEN aggregate_rating END), 2)         AS delivery_avg_rating,
    ROUND(AVG(CASE WHEN has_online_delivery = 0
                   THEN aggregate_rating END), 2)         AS no_delivery_avg_rating
FROM restaurants
WHERE aggregate_rating > 0
GROUP BY country
ORDER BY delivery_adoption_pct DESC;


-- ── Q11: Feature Combo Impact on Rating ─────────────────────────
-- Business: Quantify business value of each feature combination
SELECT
    CASE
        WHEN has_online_delivery = 1 AND has_table_booking = 1
             THEN 'Delivery + Table Booking'
        WHEN has_online_delivery = 1 AND has_table_booking = 0
             THEN 'Delivery Only'
        WHEN has_online_delivery = 0 AND has_table_booking = 1
             THEN 'Table Booking Only'
        ELSE 'Neither'
    END                                                   AS feature_combo,
    COUNT(*)                                              AS restaurant_count,
    ROUND(AVG(CASE WHEN aggregate_rating > 0
                   THEN aggregate_rating END), 2)         AS avg_rating,
    ROUND(AVG(votes), 0)                                  AS avg_votes,
    ROUND(AVG(avg_cost_for_two), 0)                       AS avg_cost
FROM restaurants
GROUP BY feature_combo
ORDER BY avg_rating DESC;


-- ── Q12: Delivery Impact on Rating (Statistical) ────────────────
-- Business: Evidence-based decision for platform delivery push
SELECT
    has_online_delivery,
    COUNT(*)                                              AS count,
    ROUND(AVG(aggregate_rating), 2)                       AS avg_rating,
    ROUND(AVG(votes), 0)                                  AS avg_votes,
    ROUND(AVG(avg_cost_for_two), 0)                       AS avg_cost,
    ROUND(100.0 * SUM(CASE WHEN aggregate_rating >= 4.0
                           THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_high_rated
FROM restaurants
WHERE aggregate_rating > 0
GROUP BY has_online_delivery;


-- ================================================================
-- SECTION 5 — COST & PRICING ANALYSIS
-- ================================================================

-- ── Q13: Avg Cost by Price Range & Country ──────────────────────
-- Business: Pricing strategy benchmarks across markets
SELECT
    country,
    cost_category,
    price_range,
    COUNT(*)                                              AS restaurant_count,
    ROUND(AVG(avg_cost_for_two), 0)                       AS avg_cost,
    ROUND(MIN(avg_cost_for_two), 0)                       AS min_cost,
    ROUND(MAX(avg_cost_for_two), 0)                       AS max_cost,
    ROUND(AVG(aggregate_rating), 2)                       AS avg_rating
FROM restaurants
WHERE aggregate_rating > 0
GROUP BY country, cost_category, price_range
ORDER BY country, price_range;


-- ── Q14: Cost vs Rating Segments (CASE-based segmentation) ──────
-- Business: Identify value-for-money vs overpriced restaurants
SELECT
    CASE
        WHEN avg_cost_for_two <= 300  AND aggregate_rating >= 4.0
             THEN 'Hidden Gem (Low Cost, High Rating)'
        WHEN avg_cost_for_two >  800  AND aggregate_rating >= 4.0
             THEN 'Luxury Winner (High Cost, High Rating)'
        WHEN avg_cost_for_two >  800  AND aggregate_rating <  3.5
             THEN 'Overpriced (High Cost, Low Rating)'
        WHEN avg_cost_for_two <= 300  AND aggregate_rating <  3.0
             THEN 'Budget & Poor'
        ELSE 'Mid Segment'
    END                                                   AS segment,
    COUNT(*)                                              AS restaurant_count,
    ROUND(AVG(aggregate_rating), 2)                       AS avg_rating,
    ROUND(AVG(avg_cost_for_two), 0)                       AS avg_cost,
    ROUND(AVG(votes), 0)                                  AS avg_votes
FROM restaurants
WHERE aggregate_rating > 0
GROUP BY segment
ORDER BY avg_rating DESC;


-- ── Q15: Premium vs Budget Restaurant Profile ───────────────────
-- Business: Understand what separates top-tier from budget dining
SELECT
    cost_category,
    COUNT(*)                                              AS count,
    ROUND(AVG(aggregate_rating), 2)                       AS avg_rating,
    ROUND(AVG(votes), 0)                                  AS avg_votes,
    ROUND(SUM(has_online_delivery) * 100.0 / COUNT(*), 1) AS delivery_pct,
    ROUND(SUM(has_table_booking)   * 100.0 / COUNT(*), 1) AS booking_pct,
    ROUND(AVG(avg_cost_for_two), 0)                       AS avg_cost
FROM restaurants
WHERE cost_category IS NOT NULL
GROUP BY cost_category
ORDER BY
    CASE cost_category
        WHEN 'Budget'     THEN 1
        WHEN 'Affordable' THEN 2
        WHEN 'Mid-Range'  THEN 3
        WHEN 'Premium'    THEN 4
    END;


-- ================================================================
-- SECTION 6 — WINDOW FUNCTIONS & RANKING
-- ================================================================

-- ── Q16: Restaurant Rank within Each City ───────────────────────
-- Business: Leaderboard of top restaurants per city
SELECT
    city,
    restaurant_name,
    primary_cuisine,
    aggregate_rating,
    votes,
    RANK()       OVER (PARTITION BY city ORDER BY aggregate_rating DESC,
                       votes DESC)                       AS city_rank,
    DENSE_RANK() OVER (PARTITION BY city ORDER BY aggregate_rating DESC)
                                                         AS city_dense_rank,
    NTILE(4)     OVER (PARTITION BY city ORDER BY aggregate_rating DESC)
                                                         AS quartile
FROM restaurants
WHERE aggregate_rating > 0
  AND votes >= 50
ORDER BY city, city_rank
LIMIT 40;


-- ── Q17: Running Total of Restaurants by Country ────────────────
-- Business: Cumulative market share analysis
SELECT
    country,
    restaurant_count,
    SUM(restaurant_count) OVER (
        ORDER BY restaurant_count DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                                     AS cumulative_count,
    ROUND(SUM(restaurant_count) OVER (
        ORDER BY restaurant_count DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) * 100.0 / SUM(restaurant_count) OVER (), 2)         AS cumulative_pct
FROM (
    SELECT country, COUNT(*) AS restaurant_count
    FROM restaurants
    GROUP BY country
) sub
ORDER BY restaurant_count DESC;


-- ── Q18: Rolling Average Rating by Price Range ──────────────────
-- Business: Price-tier quality trends for competitive positioning
WITH city_price_rating AS (
    SELECT
        city,
        price_range,
        ROUND(AVG(aggregate_rating), 2) AS avg_rating,
        COUNT(*)                         AS count
    FROM restaurants
    WHERE aggregate_rating > 0
    GROUP BY city, price_range
    HAVING COUNT(*) >= 5
)
SELECT
    city,
    price_range,
    avg_rating,
    count,
    ROUND(AVG(avg_rating) OVER (
        PARTITION BY price_range
        ORDER BY avg_rating DESC
        ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
    ), 2)                                                 AS smoothed_avg_rating
FROM city_price_rating
ORDER BY price_range, avg_rating DESC
LIMIT 30;


-- ── Q19: Top Restaurant per Country (Window Function) ───────────
-- Business: Country-level ambassador restaurants for marketing
WITH ranked AS (
    SELECT
        country,
        restaurant_name,
        city,
        primary_cuisine,
        aggregate_rating,
        votes,
        avg_cost_for_two,
        ROW_NUMBER() OVER (
            PARTITION BY country
            ORDER BY aggregate_rating DESC, votes DESC
        ) AS rn
    FROM restaurants
    WHERE aggregate_rating > 0 AND votes >= 50
)
SELECT
    country,
    restaurant_name,
    city,
    primary_cuisine,
    aggregate_rating,
    votes,
    avg_cost_for_two
FROM ranked
WHERE rn = 1
ORDER BY aggregate_rating DESC;


-- ── Q20: Percentile Rank of Each Restaurant ─────────────────────
-- Business: Know exactly where each restaurant stands on the platform
SELECT
    restaurant_name,
    city,
    primary_cuisine,
    aggregate_rating,
    votes,
    ROUND(PERCENT_RANK() OVER (ORDER BY aggregate_rating) * 100, 1)
                                                          AS rating_percentile,
    ROUND(PERCENT_RANK() OVER (ORDER BY votes) * 100, 1)
                                                          AS votes_percentile,
    CASE
        WHEN PERCENT_RANK() OVER (ORDER BY aggregate_rating) >= 0.90
             THEN 'Top 10%'
        WHEN PERCENT_RANK() OVER (ORDER BY aggregate_rating) >= 0.75
             THEN 'Top 25%'
        WHEN PERCENT_RANK() OVER (ORDER BY aggregate_rating) >= 0.50
             THEN 'Top 50%'
        ELSE 'Bottom 50%'
    END                                                   AS performance_tier
FROM restaurants
WHERE aggregate_rating > 0
ORDER BY rating_percentile DESC
LIMIT 20;


-- ================================================================
-- SECTION 7 — SUBQUERIES & CTEs
-- ================================================================

-- ── Q21: Cities Above the National Average Rating ───────────────
-- Business: Identify quality clusters for platform promotion
WITH country_avg AS (
    SELECT
        country,
        AVG(aggregate_rating) AS country_mean
    FROM restaurants
    WHERE aggregate_rating > 0
    GROUP BY country
),
city_avg AS (
    SELECT
        city,
        country,
        AVG(aggregate_rating) AS city_mean,
        COUNT(*)               AS count
    FROM restaurants
    WHERE aggregate_rating > 0
    GROUP BY city, country
    HAVING COUNT(*) >= 20
)
SELECT
    ca.city,
    ca.country,
    ROUND(ca.city_mean, 2)                                AS city_avg_rating,
    ROUND(co.country_mean, 2)                             AS country_avg_rating,
    ROUND(ca.city_mean - co.country_mean, 2)              AS delta,
    ca.count                                              AS restaurant_count
FROM city_avg ca
JOIN country_avg co ON ca.country = co.country
WHERE ca.city_mean > co.country_mean
ORDER BY delta DESC
LIMIT 20;


-- ── Q22: Cuisine Market Concentration (HHI Index) ───────────────
-- Business: Measure how concentrated the cuisine market is per city
-- HHI > 2500 = highly concentrated; < 1500 = competitive
WITH cuisine_share AS (
    SELECT
        city,
        primary_cuisine,
        COUNT(*) AS cnt
    FROM restaurants
    GROUP BY city, primary_cuisine
),
city_total AS (
    SELECT city, COUNT(*) AS total
    FROM restaurants
    GROUP BY city
),
shares AS (
    SELECT
        cs.city,
        cs.primary_cuisine,
        ROUND(cs.cnt * 100.0 / ct.total, 2)  AS share_pct
    FROM cuisine_share cs
    JOIN city_total ct ON cs.city = ct.city
)
SELECT
    city,
    ROUND(SUM(share_pct * share_pct), 0)                  AS hhi_index,
    CASE
        WHEN SUM(share_pct * share_pct) > 2500 THEN 'Highly Concentrated'
        WHEN SUM(share_pct * share_pct) > 1500 THEN 'Moderately Competitive'
        ELSE 'Highly Competitive'
    END                                                    AS market_type,
    COUNT(DISTINCT primary_cuisine)                        AS unique_cuisines
FROM shares
GROUP BY city
ORDER BY hhi_index DESC
LIMIT 20;


-- ── Q23: Restaurants with Below-Average Cost but Above-Average Rating ──
-- Business: Discover "value champions" — best marketing assets
WITH benchmarks AS (
    SELECT
        AVG(avg_cost_for_two) AS avg_cost,
        AVG(aggregate_rating) AS avg_rating
    FROM restaurants
    WHERE aggregate_rating > 0
)
SELECT
    r.restaurant_name,
    r.city,
    r.country,
    r.primary_cuisine,
    r.avg_cost_for_two,
    r.aggregate_rating,
    r.votes,
    ROUND(r.avg_cost_for_two / b.avg_cost, 2)             AS cost_ratio,
    ROUND(r.aggregate_rating - b.avg_rating, 2)           AS rating_delta
FROM restaurants r
CROSS JOIN benchmarks b
WHERE r.avg_cost_for_two < b.avg_cost
  AND r.aggregate_rating > b.avg_rating
  AND r.votes >= 100
ORDER BY r.aggregate_rating DESC, r.votes DESC
LIMIT 20;


-- ── Q24: Delivery Penetration CTE — City Level ──────────────────
-- Business: Which cities should be targeted for delivery expansion?
WITH city_metrics AS (
    SELECT
        city,
        country,
        COUNT(*)                                              AS total,
        SUM(has_online_delivery)                              AS delivery_count,
        ROUND(SUM(has_online_delivery) * 100.0 / COUNT(*), 1) AS delivery_pct,
        ROUND(AVG(aggregate_rating), 2)                       AS avg_rating,
        ROUND(AVG(votes), 0)                                  AS avg_votes
    FROM restaurants
    GROUP BY city, country
    HAVING COUNT(*) >= 20
),
national_delivery AS (
    SELECT
        country,
        ROUND(AVG(delivery_pct), 1) AS national_delivery_avg
    FROM city_metrics
    GROUP BY country
)
SELECT
    cm.city,
    cm.country,
    cm.total,
    cm.delivery_pct,
    nd.national_delivery_avg,
    ROUND(cm.delivery_pct - nd.national_delivery_avg, 1)  AS vs_national,
    CASE
        WHEN cm.delivery_pct < nd.national_delivery_avg - 10
             THEN 'High Expansion Opportunity'
        WHEN cm.delivery_pct < nd.national_delivery_avg
             THEN 'Moderate Opportunity'
        ELSE 'Saturated'
    END                                                    AS expansion_flag,
    cm.avg_votes
FROM city_metrics cm
JOIN national_delivery nd ON cm.country = nd.country
ORDER BY vs_national ASC
LIMIT 25;


-- ── Q25: Restaurant Success Score (Composite KPI) ───────────────
-- Business: Unified performance score for each restaurant
-- Score = normalised(rating) * 0.5 + normalised(votes) * 0.3
--         + delivery_bonus * 0.1 + booking_bonus * 0.1
WITH stats AS (
    SELECT
        MAX(aggregate_rating) AS max_rating,
        MIN(aggregate_rating) AS min_rating,
        MAX(votes)            AS max_votes,
        MIN(votes)            AS min_votes
    FROM restaurants
    WHERE aggregate_rating > 0 AND votes > 0
)
SELECT
    r.restaurant_id,
    r.restaurant_name,
    r.city,
    r.primary_cuisine,
    r.aggregate_rating,
    r.votes,
    r.has_online_delivery,
    r.has_table_booking,
    ROUND(
        -- Normalised rating (0–1) × weight 50%
        ((r.aggregate_rating - s.min_rating) /
         NULLIF(s.max_rating - s.min_rating, 0)) * 0.50
        -- Normalised votes (0–1) × weight 30%
      + ((CAST(r.votes AS REAL) - s.min_votes) /
         NULLIF(s.max_votes - s.min_votes, 0)) * 0.30
        -- Delivery bonus × weight 10%
      + (r.has_online_delivery * 0.10)
        -- Table booking bonus × weight 10%
      + (r.has_table_booking   * 0.10),
    4)                                                      AS success_score,
    NTILE(5) OVER (
        ORDER BY
            ((r.aggregate_rating - s.min_rating) /
             NULLIF(s.max_rating - s.min_rating, 0)) * 0.50
          + ((CAST(r.votes AS REAL) - s.min_votes) /
             NULLIF(s.max_votes - s.min_votes, 0)) * 0.30
          + r.has_online_delivery * 0.10
          + r.has_table_booking   * 0.10
        DESC
    )                                                       AS success_tier
FROM restaurants r
CROSS JOIN stats s
WHERE r.aggregate_rating > 0 AND r.votes > 0
ORDER BY success_score DESC
LIMIT 30;


-- ── Q26: Month-over-Month Style Comparison (Price Tier Shifts) ──
-- Business: Analyse how restaurant mix differs across price tiers
WITH tier_stats AS (
    SELECT
        cost_category,
        primary_cuisine,
        COUNT(*)                        AS count,
        ROUND(AVG(aggregate_rating), 2) AS avg_rating,
        ROUND(AVG(votes), 0)            AS avg_votes
    FROM restaurants
    WHERE aggregate_rating > 0
      AND cost_category IS NOT NULL
    GROUP BY cost_category, primary_cuisine
),
tier_totals AS (
    SELECT cost_category, SUM(count) AS tier_total
    FROM tier_stats
    GROUP BY cost_category
)
SELECT
    ts.cost_category,
    ts.primary_cuisine,
    ts.count,
    ROUND(ts.count * 100.0 / tt.tier_total, 2)            AS within_tier_share_pct,
    ts.avg_rating,
    ts.avg_votes
FROM tier_stats ts
JOIN tier_totals tt ON ts.cost_category = tt.cost_category
ORDER BY ts.cost_category, ts.count DESC;


-- ── Q27: HAVING Clause — Cities with High Avg Cost & Low Rating ─
-- Business: Flag potential customer satisfaction risks in premium markets
SELECT
    city,
    country,
    COUNT(*)                                              AS restaurant_count,
    ROUND(AVG(avg_cost_for_two), 0)                       AS avg_cost,
    ROUND(AVG(aggregate_rating), 2)                       AS avg_rating,
    ROUND(AVG(votes), 0)                                  AS avg_votes
FROM restaurants
WHERE aggregate_rating > 0
GROUP BY city, country
HAVING COUNT(*) >= 15
   AND AVG(avg_cost_for_two) > (SELECT AVG(avg_cost_for_two) FROM restaurants)
   AND AVG(aggregate_rating) < (SELECT AVG(aggregate_rating)
                                FROM restaurants WHERE aggregate_rating > 0)
ORDER BY avg_cost DESC, avg_rating ASC
LIMIT 15;


-- ── Q28: Self-JOIN — Restaurants in the Same City & Cuisine ─────
-- Business: Competitive landscape — direct competitors per restaurant
SELECT
    a.restaurant_name                                      AS restaurant,
    b.restaurant_name                                      AS competitor,
    a.city,
    a.primary_cuisine,
    a.aggregate_rating                                     AS restaurant_rating,
    b.aggregate_rating                                     AS competitor_rating,
    ROUND(b.aggregate_rating - a.aggregate_rating, 2)      AS rating_gap,
    a.avg_cost_for_two                                     AS restaurant_cost,
    b.avg_cost_for_two                                     AS competitor_cost
FROM restaurants a
JOIN restaurants b
    ON  a.city           = b.city
    AND a.primary_cuisine = b.primary_cuisine
    AND a.restaurant_id  != b.restaurant_id
    AND a.aggregate_rating > 0
    AND b.aggregate_rating > 0
WHERE a.aggregate_rating < b.aggregate_rating      -- show only where competitor wins
ORDER BY a.city, a.primary_cuisine, rating_gap DESC
LIMIT 30;


-- ── Q29: Cuisine Diversity Index per City ───────────────────────
-- Business: Identify gastronomically diverse cities for food tourism
SELECT
    city,
    country,
    COUNT(*)                          AS total_restaurants,
    COUNT(DISTINCT primary_cuisine)   AS unique_cuisines,
    ROUND(
        COUNT(DISTINCT primary_cuisine) * 1.0 / COUNT(*), 4
    )                                 AS diversity_index,
    ROUND(AVG(aggregate_rating), 2)   AS avg_rating
FROM restaurants
WHERE aggregate_rating > 0
GROUP BY city, country
HAVING COUNT(*) >= 20
ORDER BY diversity_index DESC
LIMIT 15;


-- ── Q30: Platform Health Scorecard (Final Executive Query) ───────
-- Business: One query to assess platform-wide health across 5 KPIs
WITH kpis AS (
    SELECT
        COUNT(*)                                                    AS total_restaurants,
        ROUND(AVG(CASE WHEN aggregate_rating > 0 THEN aggregate_rating END), 2)
                                                                    AS avg_platform_rating,
        ROUND(SUM(has_online_delivery) * 100.0 / COUNT(*), 1)      AS delivery_adoption_pct,
        ROUND(SUM(has_table_booking)   * 100.0 / COUNT(*), 1)      AS booking_adoption_pct,
        ROUND(SUM(CASE WHEN aggregate_rating >= 4.0 THEN 1 ELSE 0 END)
              * 100.0 / NULLIF(SUM(CASE WHEN aggregate_rating > 0 THEN 1 ELSE 0 END), 0), 1)
                                                                    AS pct_high_quality,
        ROUND(SUM(CASE WHEN votes = 0 THEN 1 ELSE 0 END)
              * 100.0 / COUNT(*), 1)                                AS pct_zero_votes,
        COUNT(DISTINCT country)                                     AS countries_covered,
        COUNT(DISTINCT city)                                        AS cities_covered
    FROM restaurants
)
SELECT
    total_restaurants,
    avg_platform_rating,
    delivery_adoption_pct,
    booking_adoption_pct,
    pct_high_quality,
    pct_zero_votes,
    countries_covered,
    cities_covered,
    -- Health score out of 100
    ROUND(
        (CASE WHEN avg_platform_rating >= 4.0 THEN 25
              WHEN avg_platform_rating >= 3.5 THEN 18
              ELSE 10 END)
      + (CASE WHEN delivery_adoption_pct >= 50 THEN 25
              WHEN delivery_adoption_pct >= 25 THEN 15
              ELSE 8 END)
      + (CASE WHEN pct_high_quality >= 40 THEN 25
              WHEN pct_high_quality >= 20 THEN 15
              ELSE 8 END)
      + (CASE WHEN pct_zero_votes <= 10 THEN 25
              WHEN pct_zero_votes <= 25 THEN 15
              ELSE 8 END),
    0)                                                              AS platform_health_score
FROM kpis;
