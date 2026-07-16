# 03_Python — README

## Where's the dashboard?
It's not one interactive dashboard — it's **6 separate chart images**,
already generated and sitting right here in `04_charts/`. Python isn't a BI
tool like Power BI/Tableau; a Python script typically produces static image
files. You already have them — you don't need to run anything to see them.

## Fastest way to see the results: just open the images
Go to the `04_charts/` folder and open these like any photo (double-click,
they'll open in Windows Photos / macOS Preview / any image viewer):

1. `01_reach_trend.png` — Facebook vs Instagram reach by month
2. `02_website_growth.png` — website visitor growth trend
3. `03_booking_funnel.png` — the views → inquiries → bookings funnel
4. `04_revenue_by_month.png` — monthly Airbnb revenue
5. `05_correlation_heatmap.png` — which metrics actually relate to bookings
6. `06_fb_reach_rolling_avg.png` — smoothed Facebook reach trend

That's the "dashboard" for this section — six charts, viewed as regular
image files.

## If you want to re-run the script yourself (optional)
You don't have to — the charts above are already the output. But if you
want to regenerate them yourself, or modify the analysis:

1. Install **Python**: https://python.org (check "Add to PATH" during setup on Windows)
2. Install **VS Code**: https://code.visualstudio.com, then install its
   "Python" extension (Extensions icon on the left sidebar → search
   "Python" → Install, by Microsoft).
3. Open this `03_Python` folder in VS Code: File → Open Folder.
4. Open a terminal inside VS Code: Terminal menu → New Terminal.
5. In that terminal, type:
   ```bash
   pip install pandas matplotlib seaborn numpy
   ```
   and press Enter. Wait for it to finish.
6. Then type:
   ```bash
   python 01_analysis.py
   ```
   and press Enter.
7. You'll see text output appear in the terminal (tables of numbers), and
   new/updated chart images will be saved into a `charts/` folder next to
   the script.

### Why double-clicking the .py file doesn't work
On Windows, double-clicking a `.py` file opens a black console window that
runs the script and then **closes itself immediately** — faster than you
can read anything. This isn't a bug, it's just not how Python scripts are
meant to be launched. Always run them from inside VS Code's terminal (step 4-6
above), not by double-clicking.

## Files in this folder
1. `01_analysis.py` — the full script (pandas + matplotlib + seaborn)
2. `02_Python_Analytics_Report.docx` — write-up with all 6 charts embedded and explained
3. `03_source_data/` — the 4 CSV files the script reads
4. `04_charts/` — the 6 chart images (already generated — open these directly)
5. `05_Python_Insights_Summary.md` — one-page takeaways
