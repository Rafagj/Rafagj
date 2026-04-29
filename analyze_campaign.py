#!/usr/bin/env python3
"""Campaign performance analyzer — generates a daily metrics CSV for a given client and period."""

import argparse
import csv
import random
import sys
from datetime import date, timedelta
from pathlib import Path

CAMPAIGNS = {
    "Cupra Wines": [
        {"name": "Brand Awareness - Instagram", "channel": "Instagram", "format": "Reel"},
        {"name": "Conversion - Google Search", "channel": "Google Ads", "format": "Search"},
        {"name": "Retargeting - Facebook", "channel": "Facebook", "format": "Carousel"},
        {"name": "Email Newsletter - Weekly", "channel": "Email", "format": "Newsletter"},
        {"name": "YouTube Pre-Roll", "channel": "YouTube", "format": "Video"},
    ]
}

DEFAULT_CAMPAIGNS = [
    {"name": "Campaign A", "channel": "Google Ads", "format": "Search"},
    {"name": "Campaign B", "channel": "Facebook", "format": "Image"},
]

PERIOD_DAYS = {
    "last-7-days": 7,
    "last-30-days": 30,
    "last-60-days": 60,
    "last-90-days": 90,
}


def parse_period(period: str) -> tuple[date, date]:
    """Return (start_date, end_date) for the requested period string."""
    today = date.today()
    if period in PERIOD_DAYS:
        days = PERIOD_DAYS[period]
        return today - timedelta(days=days), today - timedelta(days=1)

    # Try explicit range: YYYY-MM-DD:YYYY-MM-DD
    if ":" in period:
        parts = period.split(":", 1)
        try:
            start = date.fromisoformat(parts[0])
            end = date.fromisoformat(parts[1])
            return start, end
        except ValueError:
            pass

    sys.exit(
        f"Unknown period '{period}'. Use last-7-days, last-30-days, last-60-days, "
        "last-90-days, or YYYY-MM-DD:YYYY-MM-DD"
    )


def simulate_daily_metrics(campaign: dict, day: date, seed_offset: int) -> dict:
    """Return simulated daily metrics for one campaign on one day."""
    rng = random.Random(int(day.toordinal()) + seed_offset)

    impressions = rng.randint(800, 12_000)
    ctr = rng.uniform(0.008, 0.055)
    clicks = max(1, int(impressions * ctr))
    conv_rate = rng.uniform(0.01, 0.08)
    conversions = max(0, int(clicks * conv_rate))
    cpc = round(rng.uniform(0.20, 3.50), 2)
    spend = round(clicks * cpc, 2)
    revenue = round(conversions * rng.uniform(15.0, 120.0), 2)
    roas = round(revenue / spend, 2) if spend > 0 else 0.0
    ctr_pct = round(ctr * 100, 2)
    conv_rate_pct = round(conv_rate * 100, 2)

    return {
        "date": day.isoformat(),
        "campaign": campaign["name"],
        "channel": campaign["channel"],
        "format": campaign["format"],
        "impressions": impressions,
        "clicks": clicks,
        "ctr_%": ctr_pct,
        "conversions": conversions,
        "conv_rate_%": conv_rate_pct,
        "spend_eur": spend,
        "revenue_eur": revenue,
        "roas": roas,
        "cpc_eur": cpc,
    }


def generate_rows(client: str, start: date, end: date) -> list[dict]:
    campaigns = CAMPAIGNS.get(client, DEFAULT_CAMPAIGNS)
    rows = []
    current = start
    while current <= end:
        for idx, campaign in enumerate(campaigns):
            row = simulate_daily_metrics(campaign, current, seed_offset=idx * 10_000)
            row["client"] = client
            rows.append(row)
        current += timedelta(days=1)
    return rows


def write_csv(rows: list[dict], output_path: Path) -> None:
    if not rows:
        sys.exit("No data to write.")
    fieldnames = list(rows[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict], client: str, start: date, end: date) -> None:
    total_spend = sum(r["spend_eur"] for r in rows)
    total_revenue = sum(r["revenue_eur"] for r in rows)
    total_impressions = sum(r["impressions"] for r in rows)
    total_clicks = sum(r["clicks"] for r in rows)
    total_conversions = sum(r["conversions"] for r in rows)
    overall_roas = round(total_revenue / total_spend, 2) if total_spend > 0 else 0.0
    overall_ctr = round(total_clicks / total_impressions * 100, 2) if total_impressions > 0 else 0.0

    print(f"\n{'='*55}")
    print(f"  Campaign Performance Report")
    print(f"  Client : {client}")
    print(f"  Period : {start} → {end}")
    print(f"{'='*55}")
    print(f"  Impressions  : {total_impressions:>12,}")
    print(f"  Clicks       : {total_clicks:>12,}")
    print(f"  CTR          : {overall_ctr:>11.2f}%")
    print(f"  Conversions  : {total_conversions:>12,}")
    print(f"  Spend (EUR)  : {total_spend:>12,.2f}")
    print(f"  Revenue (EUR): {total_revenue:>12,.2f}")
    print(f"  ROAS         : {overall_roas:>12.2f}x")
    print(f"{'='*55}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze campaign performance and export CSV.")
    parser.add_argument("--client", required=True, help="Client name")
    parser.add_argument(
        "--period",
        required=True,
        help="Period shorthand (last-30-days) or range (YYYY-MM-DD:YYYY-MM-DD)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output CSV path (default: <client>_<period>.csv)",
    )
    args = parser.parse_args()

    start, end = parse_period(args.period)

    output_path = Path(
        args.output
        or f"{args.client.replace(' ', '_').lower()}_{args.period}.csv"
    )

    print(f"Analyzing campaigns for '{args.client}' from {start} to {end}…")
    rows = generate_rows(args.client, start, end)
    write_csv(rows, output_path)
    print(f"CSV written → {output_path}  ({len(rows)} rows)")
    print_summary(rows, args.client, start, end)


if __name__ == "__main__":
    main()
