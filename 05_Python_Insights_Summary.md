# Python Section — Key Insights (One-Pager)
**Greenside Villas | Pandas EDA + Correlation Analysis, Jan 2025–Jun 2026**

## The 3 things that matter

1. **Reach and bookings are statistically unrelated.** Correlation between weekly Facebook reach and bookings: **-0.06**. Instagram reach: **-0.04**. Website visitors: **+0.06**. All effectively zero. This isn't a visual impression anymore — it's a number, and it confirms what Excel and SQL both hinted at.

2. **The only things correlated with bookings are already downstream of a booking.** Revenue (+0.85) and inquiries (+0.67) move with bookings — unsurprising, since they're part of the same event chain. Nothing upstream (views, reach, traffic) shows a meaningful relationship.

3. **The rolling average confirms the Facebook collapse is real, not noise.** Smoothing weekly Facebook reach over a 4-week window still shows a hard drop after February 2025 that never recovers — this rules out "it's just weekly volatility" as an explanation.

## What this changes
Three independent methods (Excel visual trends, SQL funnel math, Python correlation) now agree: **traffic and reach are not the constraint on revenue here — the view-to-inquiry conversion step is.** That's a strong, well-triangulated finding for a portfolio piece, because it wasn't assumed — it was tested three different ways and held up each time.

*Companion files: `analysis.py`, 4 CSVs, `charts/` (6 PNGs), `Python_Analytics_Report.docx`.*
