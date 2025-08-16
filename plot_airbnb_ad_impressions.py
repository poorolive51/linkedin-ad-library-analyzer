"""
Visualizes Airbnb's LinkedIn ad impressions in Amsterdam vs. the rest of the Netherlands.
Parses saved ad data, calculates daily impressions, and plots them over time with annotations for key policy events.
"""

import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from collections import defaultdict

CURRENT_DATE = datetime.now().date()
DATA_FILE = "airbnb_all_ads.json"

# Load saved ad data
try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: {DATA_FILE} not found.")
    exit()

ads = []

# Process ads and filter for Netherlands impressions
for ad in data:
    stats = ad.get("details", {}).get("adStatistics", {})
    if not stats or "firstImpressionAt" not in stats or "latestImpressionAt" not in stats:
        continue

    dist = stats.get("impressionsDistributionByCountry", [])
    nl_pct = next(
        (c["impressionPercentage"] for c in dist if c["country"] == "urn:li:country:NL"),
        0
    )

    ad_url = ad.get("adUrl", "Unknown URL")
    targeting = ad.get("details", {}).get("adTargeting", [])
    is_amsterdam = any(
        "amsterdam" in seg.lower()
        for t in targeting if t.get("facetName") == "Location"
        for seg in t.get("includedSegments", [])
    )
    location_segments = [
        seg
        for t in targeting if t.get("facetName") == "Location"
        for seg in t.get("includedSegments", [])
    ]

    if nl_pct > 50 and stats.get("totalImpressions"):
        imp_range = stats["totalImpressions"]
        impr_mid = (imp_range["from"] + imp_range["to"]) / 2
        duration_days = ((datetime.fromtimestamp(stats["latestImpressionAt"] / 1000) -
                          datetime.fromtimestamp(stats["firstImpressionAt"] / 1000)).days) + 1
        impr_per_day = impr_mid / duration_days if duration_days > 0 else 0

        ads.append({
            "Ad URL": ad_url,
            "Impr Mid": impr_mid,
            "Start": datetime.fromtimestamp(stats["firstImpressionAt"] / 1000),
            "End": datetime.fromtimestamp(stats["latestImpressionAt"] / 1000),
            "NL %": round(nl_pct, 2),
            "Impr Per Day": impr_per_day,
            "Is Amsterdam": is_amsterdam,
            "Location Segments": location_segments
        })

df = pd.DataFrame(ads)
df["Duration (days)"] = (df["End"] - df["Start"]).dt.days + 1
df = df[df["Duration (days)"] > 0]

# Aggregate daily impressions
daily_amsterdam = defaultdict(float)
daily_other_nl = defaultdict(float)

for _, row in df.iterrows():
    day = row["Start"].date()
    while day <= row["End"].date():
        if row["Is Amsterdam"]:
            daily_amsterdam[day] += row["Impr Per Day"]
        else:
            daily_other_nl[day] += row["Impr Per Day"]
        day += timedelta(days=1)

# Create DataFrames with all dates filled
all_dates = pd.date_range(start=df["Start"].min().date(), end=CURRENT_DATE)
amsterdam_df = pd.DataFrame(daily_amsterdam.items(), columns=["Date", "Total Impressions"]).set_index("Date").reindex(all_dates, fill_value=0).reset_index().rename(columns={"index": "Date"})
other_nl_df = pd.DataFrame(daily_other_nl.items(), columns=["Date", "Total Impressions"]).set_index("Date").reindex(all_dates, fill_value=0).reset_index().rename(columns={"index": "Date"})

# Marker DataFrames for non-zero days
amsterdam_markers = amsterdam_df[amsterdam_df["Total Impressions"] > 0]
other_nl_markers = other_nl_df[other_nl_df["Total Impressions"] > 0]

# Colors
amsterdam_color = "#FF5A5F"
other_nl_color = "rgb(189, 195, 199)"

fig = go.Figure()

# Amsterdam line + markers
fig.add_trace(go.Scatter(x=amsterdam_df["Date"], y=amsterdam_df["Total Impressions"], mode="lines",
                         name="Amsterdam Impressions", line=dict(color=amsterdam_color, width=2, dash="dot"), showlegend=False))
fig.add_trace(go.Scatter(x=amsterdam_markers["Date"], y=amsterdam_markers["Total Impressions"], mode="markers",
                         name="Amsterdam Impressions", marker=dict(color=amsterdam_color, size=8),
                         hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Impressions (Amsterdam):</b> %{y:,.0f}<extra></extra>"))

# Other NL line + markers
fig.add_trace(go.Scatter(x=other_nl_df["Date"], y=other_nl_df["Total Impressions"], mode="lines",
                         name="Other NL Impressions", line=dict(color=other_nl_color, width=2, dash="dot"), showlegend=False))
fig.add_trace(go.Scatter(x=other_nl_markers["Date"], y=other_nl_markers["Total Impressions"], mode="markers",
                         name="Other NL Impressions", marker=dict(color=other_nl_color, size=8),
                         hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Impressions (Other NL):</b> %{y:,.0f}<extra></extra>"))

# Add annotations for key events
fig.add_annotation(
    x=amsterdam_df["Date"].min() + timedelta(days=190), y=5,
    text="March 19: Airbnb policy paper to government",
    showarrow=True, arrowhead=1, ax=0, ay=-200,
    font=dict(size=12), bgcolor="white", bordercolor=amsterdam_color,
    borderwidth=2, borderpad=4, opacity=0.8
)
fig.add_annotation(
    x=amsterdam_df["Date"].min() + timedelta(days=180), y=0.2,
    text="March 11: Amsterdam city govt announces plans to restrict Airbnb rentals",
    showarrow=True, arrowhead=1, ax=0, ay=-100,
    font=dict(size=12), bgcolor="white", bordercolor="#1e8cd0",
    borderwidth=2, borderpad=4, opacity=0.8
)
fig.add_annotation(
    x=amsterdam_df["Date"].min() + timedelta(days=270), y=35000,
    text="May 23: Public consultation period starts...",
    showarrow=False, font=dict(size=12), bgcolor="white", bordercolor="#1e8cd0",
    borderwidth=2, borderpad=4, opacity=0.8
)

# Layout
fig.update_layout(
    title=dict(text="Airbnb Ads in Amsterdam vs. Other NL", x=0.5, xanchor="center"),
    yaxis_title="Daily Impressions",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.show()
