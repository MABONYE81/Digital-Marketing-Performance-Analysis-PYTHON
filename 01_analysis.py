"""
Greenside Villas — Digital Marketing & Booking Analysis
Portfolio Section 3: Python (pandas EDA + matplotlib/seaborn visualization)

Reads the four weekly-tracked channels (Facebook, Instagram, Website, Airbnb),
builds a unified weekly dataframe, and produces:
  - Monthly trend charts (reach, traffic, revenue)
  - Booking funnel visualization
  - Correlation heatmap across channels
  - Facebook reach 4-week rolling average
Outputs all charts as PNG files in ./charts/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 130
plt.rcParams["font.size"] = 10

NAVY = "#1F4E78"
TEAL = "#2E9E8E"
CORAL = "#E4572E"
GOLD = "#D9A441"

# ---------------------------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------------------------
fb = pd.read_csv("facebook_weekly.csv", parse_dates=["week_date"])
ig = pd.read_csv("instagram_weekly.csv", parse_dates=["week_date"])
web = pd.read_csv("website_weekly.csv", parse_dates=["week_date"])
ab = pd.read_csv("airbnb_weekly.csv", parse_dates=["week_date"])

# ---------------------------------------------------------------------------
# 2. BUILD UNIFIED WEEKLY DATAFRAME
# ---------------------------------------------------------------------------
df = fb[["week_date", "reach", "engagements"]].rename(
    columns={"reach": "fb_reach", "engagements": "fb_engagements"})
df = df.merge(ig[["week_date", "reach", "engagements"]].rename(
    columns={"reach": "ig_reach", "engagements": "ig_engagements"}), on="week_date", how="left")
df = df.merge(web[["week_date", "visitors", "conversions"]].rename(
    columns={"visitors": "site_visitors", "conversions": "site_conversions"}), on="week_date", how="left")
df = df.merge(ab[["week_date", "views", "inquiries", "bookings", "revenue"]].rename(
    columns={"views": "airbnb_views", "inquiries": "airbnb_inquiries",
             "bookings": "airbnb_bookings", "revenue": "airbnb_revenue"}), on="week_date", how="left")

df = df.sort_values("week_date").reset_index(drop=True)
df["month"] = df["week_date"].dt.to_period("M")

# ---------------------------------------------------------------------------
# 3. MONTHLY ROLLUP
# ---------------------------------------------------------------------------
monthly = df.groupby("month").agg(
    fb_reach=("fb_reach", "sum"),
    ig_reach=("ig_reach", "sum"),
    site_visitors=("site_visitors", "sum"),
    airbnb_views=("airbnb_views", "sum"),
    airbnb_inquiries=("airbnb_inquiries", "sum"),
    airbnb_bookings=("airbnb_bookings", "sum"),
    airbnb_revenue=("airbnb_revenue", "sum"),
).reset_index()
monthly["month_str"] = monthly["month"].astype(str)
monthly = monthly[monthly["fb_reach"].notna() & (monthly["month_str"] < "2026-07")]  # drop incomplete/future month

print("Monthly summary:")
print(monthly[["month_str", "fb_reach", "ig_reach", "site_visitors", "airbnb_bookings", "airbnb_revenue"]]
      .to_string(index=False))

# ---------------------------------------------------------------------------
# 4. FUNNEL METRICS (whole period)
# ---------------------------------------------------------------------------
total_views = monthly["airbnb_views"].sum()
total_inquiries = monthly["airbnb_inquiries"].sum()
total_bookings = monthly["airbnb_bookings"].sum()
total_revenue = monthly["airbnb_revenue"].sum()

view_to_inquiry = total_inquiries / total_views * 100
inquiry_to_booking = total_bookings / total_inquiries * 100

print(f"\nFunnel (18 months): {total_views} views -> {total_inquiries} inquiries "
      f"({view_to_inquiry:.2f}%) -> {total_bookings} bookings ({inquiry_to_booking:.2f}%)")
print(f"Total revenue: ${total_revenue:,.0f}")

# ---------------------------------------------------------------------------
# 5. CHART 1 — Monthly Reach Trend (FB vs IG)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly["month_str"], monthly["fb_reach"], marker="o", color=NAVY, label="Facebook Reach")
ax.plot(monthly["month_str"], monthly["ig_reach"], marker="o", color=TEAL, label="Instagram Reach")
ax.set_title("Monthly Social Reach: Facebook vs Instagram (Jan 2025–Jun 2026)", fontweight="bold")
ax.set_ylabel("Reach")
ax.set_xlabel("Month")
plt.xticks(rotation=60, ha="right")
ax.legend()
plt.tight_layout()
plt.savefig("charts/01_reach_trend.png")
plt.close()

# ---------------------------------------------------------------------------
# 6. CHART 2 — Website Traffic Growth
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly["month_str"], monthly["site_visitors"], marker="o", color=GOLD, linewidth=2)
ax.fill_between(range(len(monthly)), monthly["site_visitors"], color=GOLD, alpha=0.15)
ax.set_title("Monthly Website Visitors — Steady Growth Trend", fontweight="bold")
ax.set_ylabel("Visitors")
ax.set_xlabel("Month")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig("charts/02_website_growth.png")
plt.close()

# ---------------------------------------------------------------------------
# 7. CHART 3 — Booking Funnel (Views -> Inquiries -> Bookings)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
stages = ["Listing\nViews", "Inquiries", "Bookings"]
values = [total_views, total_inquiries, total_bookings]
colors = [NAVY, TEAL, CORAL]
bars = ax.bar(stages, values, color=colors, width=0.5)
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
             f"{int(v):,}", ha="center", fontweight="bold")
ax.set_yscale("log")
ax.set_title(f"Airbnb Booking Funnel — 18 Months\nView\u2192Inquiry: {view_to_inquiry:.1f}%   |   Inquiry\u2192Booking: {inquiry_to_booking:.1f}%",
             fontweight="bold")
ax.set_ylabel("Count (log scale)")
plt.tight_layout()
plt.savefig("charts/03_booking_funnel.png")
plt.close()

# ---------------------------------------------------------------------------
# 8. CHART 4 — Monthly Revenue Bar Chart
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
bar_colors = [CORAL if v == monthly["airbnb_revenue"].max() else NAVY for v in monthly["airbnb_revenue"]]
ax.bar(monthly["month_str"], monthly["airbnb_revenue"], color=bar_colors)
ax.set_title("Monthly Airbnb Revenue (highlight = best month)", fontweight="bold")
ax.set_ylabel("Revenue ($)")
ax.set_xlabel("Month")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig("charts/04_revenue_by_month.png")
plt.close()

# ---------------------------------------------------------------------------
# 9. CHART 5 — Correlation Heatmap
# ---------------------------------------------------------------------------
corr_cols = ["fb_reach", "ig_reach", "site_visitors", "airbnb_views",
             "airbnb_inquiries", "airbnb_bookings", "airbnb_revenue"]
corr = df[corr_cols].corr()
fig, ax = plt.subplots(figsize=(7.5, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax,
            cbar_kws={"label": "Pearson correlation"})
ax.set_title("Weekly Cross-Channel Correlation Matrix", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/05_correlation_heatmap.png")
plt.close()

# ---------------------------------------------------------------------------
# 10. CHART 6 — Facebook Reach: Raw vs 4-Week Rolling Average
# ---------------------------------------------------------------------------
df["fb_reach_roll4"] = df["fb_reach"].rolling(4, min_periods=1).mean()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["week_date"], df["fb_reach"], color="#BBBBBB", linewidth=1, label="Weekly reach (raw)")
ax.plot(df["week_date"], df["fb_reach_roll4"], color=NAVY, linewidth=2, label="4-week rolling average")
ax.set_title("Facebook Reach — Weekly vs 4-Week Rolling Average", fontweight="bold")
ax.set_ylabel("Reach")
ax.set_xlabel("Week")
ax.legend()
plt.tight_layout()
plt.savefig("charts/06_fb_reach_rolling_avg.png")
plt.close()

print("\nAll charts saved to ./charts/")

# ---------------------------------------------------------------------------
# 11. Correlation with bookings — printed for the report
# ---------------------------------------------------------------------------
print("\nCorrelation of each channel with airbnb_bookings (weekly):")
print(corr["airbnb_bookings"].sort_values(ascending=False).to_string())
