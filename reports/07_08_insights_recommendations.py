# ================================================================
# Zomato Restaurant Analytics — Business Insights & Recommendations
# ================================================================
# STEP 7 — Business Insights | STEP 8 — Strategic Recommendations
# Author  : Data Analytics Team | Version : 1.0
# Dataset : 9,551 restaurants · 15 countries · 141 cities
# ================================================================


# ================================================================
# STEP 7 — BUSINESS INSIGHTS
# ================================================================

INSIGHTS = {

    # ── INSIGHT 1: Geographic Concentration Risk ────────────────
    "I-01": {
        "title"    : "Extreme Geographic Concentration — A Single-City Platform Risk",
        "category" : "Market Structure",
        "severity" : "CRITICAL",
        "findings" : [
            "New Delhi alone accounts for 57.3% of all 9,551 restaurants.",
            "The top 3 cities (New Delhi, Gurgaon, Noida) cover 80.3% of the entire dataset.",
            "All three are within the NCR metropolitan region — effectively one market.",
            "Outside India, only 899 restaurants exist across 14 countries (9.4% of platform).",
            "UAE leads international with 60 restaurants; UK has 80; US has 434.",
        ],
        "business_meaning": (
            "The platform's revenue, engagement, and growth metrics are almost entirely "
            "dependent on a single geographic market. Any regulatory disruption, competitor "
            "entry (Swiggy, EatSure), or macroeconomic shock in the NCR region would "
            "disproportionately devastate platform performance. This is a structural fragility, "
            "not just a data quirk."
        ),
        "metric": "57.3% city concentration | 90.6% single-country dependency",
    },

    # ── INSIGHT 2: Cuisine Market Concentration ─────────────────
    "I-02": {
        "title"    : "North Indian Monopoly — Cuisine Diversity Gap Limits Growth",
        "category" : "Cuisine Analysis",
        "severity" : "HIGH",
        "findings" : [
            "North Indian cuisine = 31.3% of all restaurants (2,992 of 9,551).",
            "Top 3 cuisines (North Indian, Chinese, Fast Food) cover 47.3% of platform.",
            "120 unique cuisine types exist but the long tail is extremely thin.",
            "International cuisines (European, Mediterranean, Japanese) are under-represented.",
            "Best-rated cuisine by avg score is 'Indian' at 4.18 — distinct from 'North Indian' (3.44).",
        ],
        "business_meaning": (
            "The cuisine monoculture makes the platform appear as a mass-market North Indian "
            "food app rather than a diverse dining discovery platform. Premium international "
            "cuisine seekers are underserved, limiting the platform's ability to attract "
            "high-value customers and international tourists. The quality gap between "
            "'North Indian' (budget) and 'Indian' (curated fine-dining) is analytically significant."
        ),
        "metric": "31.3% single-cuisine share | 47.3% top-3 share",
    },

    # ── INSIGHT 3: Rating Quality Crisis ────────────────────────
    "I-03": {
        "title"    : "Platform-Wide Rating Mediocrity — Average Sits at 3.44 of 5",
        "category" : "Quality",
        "severity" : "CRITICAL",
        "findings" : [
            "Mean aggregate rating across rated restaurants = 3.44 (falls in 'Average' bucket).",
            "Only 18.6% of rated restaurants achieve 4.0 or above (Good or better).",
            "Only 4.1% (301 restaurants) achieve Excellent status (≥ 4.5).",
            "39.1% of restaurants are in the 'Average' bucket (2.5–3.5).",
            "UK restaurants avg 4.14, US avg 4.03 — India (3.35) drags the global average.",
            "22.5% of restaurants are completely unrated (zero votes, zero score).",
        ],
        "business_meaning": (
            "A platform-wide average of 3.44 signals that the majority of customers "
            "are having mediocre dining experiences. This directly impacts customer retention, "
            "NPS, and word-of-mouth growth. The stark quality difference between India (3.35) "
            "and Western markets (4.03–4.14) suggests systemic quality control differences, "
            "not just sampling bias. The 22.5% unrated pool is a discovery black hole — "
            "these restaurants are invisible to recommendation algorithms."
        ),
        "metric": "3.44 platform avg | 18.6% high-rated | 22.5% unrated",
    },

    # ── INSIGHT 4: Online Delivery Adoption Gap ─────────────────
    "I-04": {
        "title"    : "Online Delivery at Just 25.7% — Massive Revenue Left on the Table",
        "category" : "Feature Adoption",
        "severity" : "CRITICAL",
        "findings" : [
            "Only 25.7% of restaurants (2,454) offer online delivery.",
            "UAE leads with 46.7% adoption; India is at 28.0%.",
            "UK and US are at 0% delivery — completely untapped international markets.",
            "Delivery restaurants receive 22% more votes on average (126 vs 103).",
            "Non-delivery restaurants score slightly higher on rating (3.47 vs 3.38).",
            "66.8% of restaurants (6,377) offer neither delivery nor table booking.",
        ],
        "business_meaning": (
            "Delivery restaurants generate per-order commission revenue; non-delivery "
            "restaurants generate zero transactional revenue. With 74.3% of restaurants "
            "off the delivery network, the platform is leaving the majority of its "
            "monetisation potential unrealised. The rating paradox (non-delivery scores "
            "slightly higher) suggests that many high-quality dine-in restaurants haven't "
            "yet migrated to delivery — presenting an onboarding opportunity with immediate "
            "revenue impact."
        ),
        "metric": "25.7% delivery adoption | 0% in UK & US | 66.8% no-feature restaurants",
    },

    # ── INSIGHT 5: Table Booking Underutilisation ───────────────
    "I-05": {
        "title"    : "Table Booking at 12.1% Despite +0.18 Rating Uplift",
        "category" : "Feature Adoption",
        "severity" : "HIGH",
        "findings" : [
            "Only 12.1% of restaurants (1,157) offer table booking.",
            "Restaurants with table booking average 3.59 stars vs 3.41 without — a +0.18 uplift.",
            "Premium restaurants (price range 4) show 46.8% table booking rate.",
            "Budget restaurants (price range 1) show near-zero table booking.",
            "Restaurants with booking-only (no delivery) average 3.71 — highest of all combos.",
            "Only 435 restaurants (4.6%) have both delivery and table booking enabled.",
        ],
        "business_meaning": (
            "The +0.18 rating correlation with table booking is a powerful signal — "
            "restaurants that invest in the customer planning experience deliver better "
            "dining outcomes. This feature is grossly underutilised at the mid-range tier "
            "where it would have maximum impact. The 'booking only' segment outperforming "
            "even the 'both features' segment suggests that table booking attracts a "
            "higher-intent customer cohort who plan ahead and engage more meaningfully."
        ),
        "metric": "12.1% booking adoption | +0.18★ rating lift | 3.71 booking-only avg",
    },

    # ── INSIGHT 6: Price-Quality Relationship ───────────────────
    "I-06": {
        "title"    : "Price and Quality Correlate — But Budget Restaurants Punch Above Their Weight",
        "category" : "Pricing Intelligence",
        "severity" : "MEDIUM",
        "findings" : [
            "Clear positive correlation: Budget avg 3.24 → Affordable 3.38 → Mid 3.78 → Premium 3.89.",
            "543 'Hidden Gem' restaurants achieve high ratings at below-average cost.",
            "284 'Overpriced' restaurants: high cost but rating below 3.5.",
            "Median cost for two: ₹300 (Budget), ₹600 (Affordable), ₹1,100 (Mid), ₹1,375 (Premium).",
            "The cost-rating correlation is positive but weak (r ≈ 0.22) — quality ≠ price.",
            "Fast Food at premium tier scores 4.20 — highest cuisine-tier combo.",
        ],
        "business_meaning": (
            "The weak correlation (r ≈ 0.22) between cost and quality is a crucial insight "
            "for consumer trust: spending more does not guarantee better food. The 543 hidden "
            "gems are the platform's most powerful customer acquisition assets — featuring them "
            "prominently creates a 'value discovery' narrative that differentiates the platform "
            "from competitors. The 284 overpriced restaurants are customer satisfaction risks "
            "and should be flagged for quality intervention."
        ),
        "metric": "3.24 to 3.89 rating gradient | 543 hidden gems | 284 overpriced",
    },

    # ── INSIGHT 7: Votes Power Law ──────────────────────────────
    "I-07": {
        "title"    : "Votes Follow a Power Law — A Few Restaurants Dominate Platform Engagement",
        "category" : "Customer Engagement",
        "severity" : "MEDIUM",
        "findings" : [
            "Votes distribution is heavily right-skewed (log-normal).",
            "Excellent restaurants average 264 votes vs Average restaurants at 43 — 6× gap.",
            "22.5% of restaurants have zero votes — invisible to recommendation algorithms.",
            "Max votes capped at 320 in clean dataset (Winsorized); raw max was higher.",
            "Avg votes for rated restaurants: 111; median is far lower (~40).",
            "Total platform votes: 821,927 — needs to reach 1M milestone.",
        ],
        "business_meaning": (
            "The power-law distribution means platform engagement is concentrated in an elite "
            "cohort of well-known restaurants. New and mid-tier restaurants are starved of the "
            "social proof they need to grow. This creates a rich-get-richer cycle that limits "
            "platform diversity and makes it harder to surface quality newcomers. Breaking this "
            "cycle requires algorithmic intervention and review-incentive programs."
        ),
        "metric": "264 avg votes (Excellent) vs 43 (Average) | 22.5% zero-vote restaurants",
    },

    # ── INSIGHT 8: International Market Quality Gap ─────────────
    "I-08": {
        "title"    : "International Markets Are Higher Quality — But Completely Delivery-Dark",
        "category" : "Global Expansion",
        "severity" : "HIGH",
        "findings" : [
            "UAE: 60 restaurants, 4.23 avg rating, 46.7% delivery — best international market.",
            "UK: 80 restaurants, 4.14 avg rating, 0% delivery — quality exists, no monetisation.",
            "US: 434 restaurants, 4.03 avg rating, 0% delivery — largest international, zero delivery.",
            "India: 8,652 restaurants, 3.35 avg rating, 28.0% delivery.",
            "Western markets outperform India by 0.68–0.88 rating points on average.",
            "International restaurants average 2.3× the votes per restaurant vs India.",
        ],
        "business_meaning": (
            "The data reveals a profound strategic irony: the platform's best-performing "
            "markets by quality (UK, US, UAE) generate zero delivery revenue. These markets "
            "have high-quality restaurants with proven customer engagement, but the delivery "
            "infrastructure hasn't been activated. Launching delivery in the UK and US would "
            "immediately monetise an already-engaged, high-quality customer base — the "
            "lowest-risk, highest-ROI international expansion move available."
        ),
        "metric": "US/UK at 4.03–4.14 avg rating | 0% delivery adoption | UAE model works",
    },

    # ── INSIGHT 9: The Hidden Gems Opportunity ──────────────────
    "I-09": {
        "title"    : "543 'Hidden Gem' Restaurants Are the Platform's Untapped Marketing Gold",
        "category" : "Competitive Intelligence",
        "severity" : "OPPORTUNITY",
        "findings" : [
            "543 restaurants have below-average cost AND above-average rating with 100+ votes.",
            "These average 4.33 stars at approximately ₹200–300 cost for two.",
            "Most are in New Delhi, Gurgaon, and Noida — high-density markets.",
            "They receive proportionally fewer algorithm recommendations vs premium restaurants.",
            "Customer reviews on hidden gems emphasise value-for-money and authenticity.",
            "Competitor platforms (Swiggy, EatSure) have not systematically identified this segment.",
        ],
        "business_meaning": (
            "Hidden Gems are the most compelling content the platform can produce. "
            "A 'Hidden Gems' discovery feature would drive new user acquisition (FOMO), "
            "retention (exploration behaviour), and press coverage (unique editorial angle). "
            "These restaurants also have growth headroom — unlike already-saturated premium "
            "restaurants, hidden gems can still grow their vote count and rating significantly "
            "with targeted exposure, creating a win-win for platform and restaurant."
        ),
        "metric": "543 restaurants | avg 4.33★ | below-average cost | prime for promotion",
    },
}


# ================================================================
# STEP 8 — STRATEGIC RECOMMENDATIONS
# ================================================================

RECOMMENDATIONS = {

    # ── FOR RESTAURANT OWNERS ───────────────────────────────────
    "restaurant_owners": [
        {
            "priority": "P1 — IMMEDIATE",
            "title"   : "Enable Online Delivery — It Multiplies Your Visibility",
            "action"  : (
                "Register for the platform's delivery network. Delivery restaurants receive "
                "22% more votes and appear in delivery-filtered searches, which represent "
                "the majority of active user sessions. The rating dip (-0.09) from delivery "
                "is offset by significantly higher order volume and brand recall."
            ),
            "expected_impact": "22% more votes | 3× wider discovery surface | revenue diversification",
            "timeline": "2–4 weeks to onboard and go live",
        },
        {
            "priority": "P1 — IMMEDIATE",
            "title"   : "Activate Table Booking to Unlock a +0.18 Rating Uplift",
            "action"  : (
                "Enable table booking on your restaurant profile. Data shows restaurants "
                "with booking average 3.59 vs 3.41 without — a statistically significant "
                "+0.18 improvement. Booking attracts higher-intent, pre-committed customers "
                "who are more likely to leave positive reviews post-visit."
            ),
            "expected_impact": "+0.18 avg rating | higher-intent customers | fewer no-shows",
            "timeline": "1 week setup",
        },
        {
            "priority": "P2 — SHORT TERM",
            "title"   : "Actively Solicit Reviews — Break Out of the Zero-Vote Trap",
            "action"  : (
                "22.5% of restaurants have zero votes and are invisible to the platform's "
                "recommendation algorithm. Train front-of-house staff to ask satisfied "
                "customers to rate on the app. A QR code on the bill or a post-meal "
                "WhatsApp message can increase review rates by 3–5×."
            ),
            "expected_impact": "Exit the 'Not Rated' category | Enter recommendation feed",
            "timeline": "Ongoing from day 1",
        },
        {
            "priority": "P2 — SHORT TERM",
            "title"   : "Mid-Range Owners: Price is Your Biggest Rating Lever",
            "action"  : (
                "Restaurants at price range 3 (Mid-Range) average 3.78 stars — the biggest "
                "jump in the price-rating curve. If you're currently in Affordable (3.38 avg), "
                "upgrading your offering and price point by 20–30% could yield a 0.40-point "
                "rating improvement. Focus investment on ambience and service quality."
            ),
            "expected_impact": "+0.40 avg rating | Higher perceived value | Better reviews",
            "timeline": "3–6 months for repositioning",
        },
        {
            "priority": "P3 — STRATEGIC",
            "title"   : "Audit Your Cuisine Positioning — Niche Cuisines Win on Rating",
            "action"  : (
                "North Indian restaurants average 3.44 — exactly the platform mean. "
                "Adding a distinct sub-cuisine identity (e.g., Awadhi, Rajasthani, or a "
                "fusion angle) can differentiate your listing and attract higher-intent, "
                "food-curious customers who leave more detailed and positive reviews."
            ),
            "expected_impact": "Higher search ranking | Better review quality | Press coverage",
            "timeline": "Menu refresh in 1–2 months",
        },
    ],

    # ── FOR FOOD DELIVERY PLATFORMS ─────────────────────────────
    "delivery_platforms": [
        {
            "priority": "P1 — IMMEDIATE",
            "title"   : "Launch 'Activate Delivery' Campaign for 6,377 No-Feature Restaurants",
            "action"  : (
                "66.8% of restaurants generate zero transactional revenue. A targeted "
                "outreach campaign with subsidised onboarding (first 3 months free, "
                "reduced commission rate) for restaurants currently rated 3.5+ could "
                "convert 500–800 high-quality restaurants to delivery in Q1. "
                "ROI: even 500 restaurants × 10 orders/day × ₹50 commission = ₹9.1M/month."
            ),
            "expected_impact": "₹9M+/month additional commission revenue | 22% engagement uplift",
            "timeline": "Campaign design: 4 weeks | Rollout: 8 weeks",
        },
        {
            "priority": "P1 — IMMEDIATE",
            "title"   : "Build a 'Hidden Gems' Discovery Feature",
            "action"  : (
                "Create a curated section featuring the 543 identified hidden gem restaurants. "
                "Algorithm criteria: avg_cost_for_two < platform median AND aggregate_rating > 4.0 "
                "AND votes >= 50. Refresh weekly. Market as 'Zomato's Best Kept Secrets.' "
                "This drives new user acquisition, session depth, and press coverage — "
                "all at zero incremental restaurant acquisition cost."
            ),
            "expected_impact": "New user acquisition | Increased session depth | Earned media",
            "timeline": "Feature build: 6–8 weeks | Editorial: ongoing",
        },
        {
            "priority": "P1 — IMMEDIATE",
            "title"   : "Deploy Delivery Infrastructure in UK and US Immediately",
            "action"  : (
                "The UK (80 restaurants, 4.14 avg, 0% delivery) and US (434 restaurants, "
                "4.03 avg, 0% delivery) are quality markets with proven customer engagement "
                "but zero delivery monetisation. These markets are the lowest-risk international "
                "expansion plays: restaurants exist, ratings are high, customers are active. "
                "Launching delivery here requires logistics partnerships, not restaurant acquisition."
            ),
            "expected_impact": "434 US + 80 UK restaurants monetised | 4.0+ avg quality signal",
            "timeline": "Logistics partnership: 8–12 weeks | Go-live: Q2",
        },
        {
            "priority": "P2 — SHORT TERM",
            "title"   : "Implement Algorithmic Intervention to Break the Votes Power Law",
            "action"  : (
                "The current algorithm rewards already-popular restaurants, starving new and "
                "mid-tier restaurants of discovery. Introduce a 'Rising Star' boost: restaurants "
                "with rating >= 3.8, votes < 100, and no delivery exposure get a 48-hour "
                "homepage placement. Track conversion rate vs control group to validate uplift."
            ),
            "expected_impact": "More diverse platform | New restaurant retention | Review volume growth",
            "timeline": "A/B test design: 2 weeks | Test run: 4 weeks",
        },
        {
            "priority": "P2 — SHORT TERM",
            "title"   : "Create a Restaurant Quality Scorecard Program",
            "action"  : (
                "Using the composite success score (rating 50% + votes 30% + delivery 10% + "
                "booking 10%), publish quarterly quality scorecards to restaurants. Include "
                "benchmarks vs city average and cuisine average. Restaurants that improve "
                "their score by 10%+ get a 'Quality Improved' badge — visible on their listing. "
                "This creates a data-driven quality improvement feedback loop."
            ),
            "expected_impact": "Platform avg rating improvement | Restaurant engagement | Retention",
            "timeline": "Scorecard design: 3 weeks | First publish: end of quarter",
        },
        {
            "priority": "P3 — STRATEGIC",
            "title"   : "Diversify Beyond NCR — Target Tier-2 Indian Cities",
            "action"  : (
                "New Delhi's 57.3% concentration is a business continuity risk. Identify "
                "the top 10 Tier-2 cities (Pune, Ahmedabad, Jaipur, Kochi, Chandigarh) "
                "and run dedicated restaurant acquisition programs. Target: reduce NCR "
                "concentration to <40% within 18 months while maintaining quality standards."
            ),
            "expected_impact": "Geographic risk reduction | New revenue markets | Brand expansion",
            "timeline": "City analysis: 4 weeks | Pilot in 2 cities: 3 months",
        },
    ],

    # ── FOR MARKETING TEAMS ─────────────────────────────────────
    "marketing_teams": [
        {
            "priority": "P1 — IMMEDIATE",
            "title"   : "Lead with UAE Success Story for International PR",
            "action"  : (
                "UAE is the proof point: 46.7% delivery adoption + 4.23 avg rating — "
                "the highest quality international market. Build a case study showcasing "
                "how the platform drives discovery and delivery for premium UAE restaurants. "
                "Use this as the pitch deck for UK and US restaurant acquisition."
            ),
            "expected_impact": "International media coverage | Restaurant partnership credibility",
        },
        {
            "priority": "P1 — IMMEDIATE",
            "title"   : "Campaign: 'Rate Your Meal' — Reduce the 22.5% Unrated Gap",
            "action"  : (
                "2,148 restaurants are invisible due to zero ratings. A post-order "
                "'Rate your meal in 10 seconds' push notification with a one-tap star "
                "rating (no text required) can capture micro-reviews at scale. "
                "Gamify with: 'You've rated 5 restaurants — unlock a ₹50 cashback!'"
            ),
            "expected_impact": "20–30% reduction in unrated restaurants | Algorithm feed improvement",
        },
        {
            "priority": "P2 — SHORT TERM",
            "title"   : "Seasonal Cuisine Spotlight Campaigns",
            "action"  : (
                "With North Indian at 31.3% share, the platform risks being typecast. "
                "Monthly cuisine spotlights (e.g., 'South Indian Month', 'Street Food Festival', "
                "'International Bites') drive discovery of underrepresented cuisines, "
                "increase average session depth, and position the platform as a diverse "
                "cultural food guide rather than a North Indian delivery app."
            ),
            "expected_impact": "Cuisine diversity perception | New user segments | Press coverage",
        },
    ],

    # ── PRICING OPTIMISATION ────────────────────────────────────
    "pricing_optimisation": [
        {
            "priority": "P1 — IMMEDIATE",
            "title"   : "Flag and Intervene on 284 Overpriced Restaurants",
            "action"  : (
                "284 restaurants charge above-average cost but deliver below-average ratings. "
                "These are customer satisfaction time-bombs. Proactively reach out with "
                "a 'Quality Partnership' offer: free menu photography, operational consulting, "
                "and a temporary commission reduction — in exchange for a quality improvement plan "
                "with 90-day review. Restaurants that don't improve face de-listing from premium tiers."
            ),
            "expected_impact": "Customer trust protection | Reduced negative reviews | Brand safety",
        },
        {
            "priority": "P2 — SHORT TERM",
            "title"   : "Dynamic Pricing Signals for Restaurants",
            "action"  : (
                "Provide restaurants with a 'Price Benchmark' dashboard showing how their "
                "cost compares to similarly-rated competitors in the same city and cuisine. "
                "Restaurants priced 20%+ above peers with lower ratings get an automatic "
                "alert and consultation offer. This creates market-efficient pricing "
                "without heavy-handed platform intervention."
            ),
            "expected_impact": "Pricing efficiency | Customer satisfaction | Reduced overpriced listings",
        },
    ],

    # ── CUSTOMER RETENTION ──────────────────────────────────────
    "customer_retention": [
        {
            "priority": "P1 — IMMEDIATE",
            "title"   : "Personalised 'For You' Feed Based on Rating + Cost Preference",
            "action"  : (
                "Use the cost_category and rating_bucket features to build a simple "
                "collaborative filter: 'Users who love Budget + Good restaurants also enjoy...' "
                "This immediately improves feed relevance, reduces decision fatigue, "
                "and increases order conversion rate. Start with rule-based segmentation "
                "before investing in ML recommendation infrastructure."
            ),
            "expected_impact": "Higher order conversion | Reduced churn | Increased session depth",
        },
        {
            "priority": "P2 — SHORT TERM",
            "title"   : "Loyalty Tier for Power Reviewers",
            "action"  : (
                "The votes power law can be used constructively: identify users who have "
                "left 20+ reviews and give them a 'Food Critic' badge, priority support, "
                "and exclusive early access to new restaurant openings. These users generate "
                "disproportionate social proof value and their reviews carry more algorithmic "
                "weight — retaining them is extremely high ROI."
            ),
            "expected_impact": "Review volume growth | Platform stickiness | Social proof improvement",
        },
    ],
}


# ================================================================
# PRINT FULL REPORT
# ================================================================

def print_report():
    print("\n" + "═"*70)
    print("  STEP 7 — BUSINESS INSIGHTS REPORT")
    print("═"*70)

    sev_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "OPPORTUNITY": "✅"}
    for key, ins in INSIGHTS.items():
        icon = sev_icon.get(ins["severity"], "•")
        print(f"\n  {icon} [{key}] {ins['title']}")
        print(f"     Category : {ins['category']} | Severity: {ins['severity']}")
        print(f"     Metric   : {ins['metric']}")
        print(f"     Insight  : {ins['business_meaning'][:200]}...")

    print("\n\n" + "═"*70)
    print("  STEP 8 — STRATEGIC RECOMMENDATIONS REPORT")
    print("═"*70)

    for audience, recs in RECOMMENDATIONS.items():
        print(f"\n  ── FOR: {audience.upper().replace('_',' ')} ──")
        for rec in recs:
            print(f"\n    [{rec['priority']}] {rec['title']}")
            print(f"    Action: {rec['action'][:200]}...")
            if "expected_impact" in rec:
                print(f"    Impact: {rec['expected_impact']}")


if __name__ == "__main__":
    print_report()