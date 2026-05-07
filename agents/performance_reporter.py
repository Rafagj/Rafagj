#!/usr/bin/env python3
"""
Performance Reporter — genera reportes ejecutivos de rendimiento de campañas.

Lee datos desde CSV local o desde Meta Ads API y produce:
- Reporte de consola con KPIs globales y por campaña
- CSV con datos detallados
- Resumen ejecutivo en Markdown

Usage:
    python agents/performance_reporter.py --client "Cupra Wines" --period last-30-days
    python agents/performance_reporter.py --csv datos.csv --output reporte.md
    python agents/performance_reporter.py --client "Cupra Wines" --period last-7-days --format md
"""

import argparse
import csv
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def coerce_row(row: dict) -> dict:
    """Cast numeric fields from string to float/int."""
    int_fields = {"impressions", "clicks", "conversions"}
    float_fields = {"ctr_%", "conv_rate_%", "spend_eur", "revenue_eur", "roas", "cpc_eur"}
    out = dict(row)
    for f in int_fields:
        if f in out:
            try:
                out[f] = int(out[f])
            except (ValueError, TypeError):
                out[f] = 0
    for f in float_fields:
        if f in out:
            try:
                out[f] = float(out[f])
            except (ValueError, TypeError):
                out[f] = 0.0
    return out


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate_global(rows: list[dict]) -> dict:
    impressions = sum(r["impressions"] for r in rows)
    clicks = sum(r["clicks"] for r in rows)
    conversions = sum(r["conversions"] for r in rows)
    spend = sum(r["spend_eur"] for r in rows)
    revenue = sum(r["revenue_eur"] for r in rows)

    ctr = clicks / impressions * 100 if impressions else 0.0
    conv_rate = conversions / clicks * 100 if clicks else 0.0
    cpa = spend / conversions if conversions else 0.0
    roas = revenue / spend if spend else 0.0
    cpm = spend / impressions * 1_000 if impressions else 0.0
    cpc = spend / clicks if clicks else 0.0

    return {
        "impressions": impressions,
        "clicks": clicks,
        "conversions": conversions,
        "spend_eur": round(spend, 2),
        "revenue_eur": round(revenue, 2),
        "ctr_%": round(ctr, 2),
        "conv_rate_%": round(conv_rate, 2),
        "cpa_eur": round(cpa, 2),
        "roas": round(roas, 2),
        "cpm_eur": round(cpm, 2),
        "cpc_eur": round(cpc, 2),
    }


def aggregate_by_campaign(rows: list[dict]) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        key = (r.get("campaign", ""), r.get("channel", ""), r.get("format", ""))
        buckets[key].append(r)

    result = []
    for (campaign, channel, fmt), bucket in buckets.items():
        agg = aggregate_global(bucket)
        agg["campaign"] = campaign
        agg["channel"] = channel
        agg["format"] = fmt
        result.append(agg)

    result.sort(key=lambda x: x["roas"], reverse=True)
    return result


def aggregate_by_channel(rows: list[dict]) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        buckets[r.get("channel", "Desconocido")].append(r)

    result = []
    for channel, bucket in buckets.items():
        agg = aggregate_global(bucket)
        agg["channel"] = channel
        result.append(agg)

    result.sort(key=lambda x: x["spend_eur"], reverse=True)
    return result


def daily_trend(rows: list[dict]) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        buckets[r.get("date", "")].append(r)

    result = []
    for day in sorted(buckets):
        agg = aggregate_global(buckets[day])
        agg["date"] = day
        result.append(agg)
    return result


# ---------------------------------------------------------------------------
# Anomaly detection
# ---------------------------------------------------------------------------

def detect_anomalies(trend: list[dict]) -> list[str]:
    alerts: list[str] = []
    if len(trend) < 7:
        return alerts

    window = 7
    for i in range(window, len(trend)):
        today = trend[i]
        past = trend[i - window: i]
        avg_roas = sum(d["roas"] for d in past) / window
        avg_ctr = sum(d["ctr_%"] for d in past) / window

        if avg_roas > 0 and today["roas"] < avg_roas * 0.7:
            alerts.append(
                f"{today['date']}: ROAS cayó a {today['roas']}x "
                f"(media 7d: {avg_roas:.2f}x) — caída del {(1 - today['roas']/avg_roas)*100:.0f}%"
            )
        if avg_ctr > 0 and today["ctr_%"] < avg_ctr * 0.6:
            alerts.append(
                f"{today['date']}: CTR cayó a {today['ctr_%']}% "
                f"(media 7d: {avg_ctr:.2f}%) — posible fatiga creativa"
            )
        if today["spend_eur"] == 0 and past[-1]["spend_eur"] > 0:
            alerts.append(f"{today['date']}: Gasto = 0 EUR — verificar estado de campañas")

    return alerts


# ---------------------------------------------------------------------------
# Printers
# ---------------------------------------------------------------------------

SEP = "=" * 70

def print_global(metrics: dict, client: str, period: str) -> None:
    print(f"\n{SEP}")
    print(f"  Reporte de Rendimiento — {client} — {period}")
    print(SEP)
    print(f"  Impresiones  : {metrics['impressions']:>12,}")
    print(f"  Clicks       : {metrics['clicks']:>12,}")
    print(f"  CTR          : {metrics['ctr_%']:>11.2f}%")
    print(f"  Conversiones : {metrics['conversions']:>12,}")
    print(f"  Conv. Rate   : {metrics['conv_rate_%']:>11.2f}%")
    print(f"  Gasto (EUR)  : {metrics['spend_eur']:>12,.2f}")
    print(f"  Revenue (EUR): {metrics['revenue_eur']:>12,.2f}")
    print(f"  ROAS         : {metrics['roas']:>12.2f}x")
    print(f"  CPA (EUR)    : {metrics['cpa_eur']:>12.2f}")
    print(f"  CPM (EUR)    : {metrics['cpm_eur']:>12.2f}")
    print(f"  CPC (EUR)    : {metrics['cpc_eur']:>12.2f}")
    print(SEP + "\n")


def print_by_campaign(campaigns: list[dict]) -> None:
    print("Rendimiento por campaña (ordenado por ROAS):")
    print(f"  {'Canal':<14} {'Formato':<12} {'ROAS':>6} {'CTR':>7} {'Gasto':>10} {'Revenue':>10}  Nombre")
    print("  " + "-" * 88)
    for c in campaigns:
        name = c["campaign"][:30]
        print(
            f"  {c['channel']:<14} {c['format']:<12} {c['roas']:>5.2f}x "
            f"{c['ctr_%']:>6.2f}% {c['spend_eur']:>9.2f}€ {c['revenue_eur']:>9.2f}€  {name}"
        )
    print()


def print_by_channel(channels: list[dict]) -> None:
    print("Rendimiento por canal:")
    print(f"  {'Canal':<16} {'Gasto':>10} {'ROAS':>7} {'CTR':>7} {'Conv.':>7} {'CPA':>9}")
    print("  " + "-" * 65)
    for c in channels:
        print(
            f"  {c['channel']:<16} {c['spend_eur']:>9.2f}€ {c['roas']:>6.2f}x "
            f"{c['ctr_%']:>6.2f}% {c['conversions']:>7,} {c['cpa_eur']:>8.2f}€"
        )
    print()


def print_alerts(alerts: list[str]) -> None:
    if not alerts:
        print("Sin anomalías detectadas.\n")
        return
    print(f"Anomalías detectadas ({len(alerts)}):")
    for a in alerts:
        print(f"  ALERTA  {a}")
    print()


# ---------------------------------------------------------------------------
# Markdown report generator
# ---------------------------------------------------------------------------

def generate_markdown(
    client: str,
    period: str,
    global_metrics: dict,
    by_campaign: list[dict],
    by_channel: list[dict],
    alerts: list[str],
    output_path: Path,
) -> None:
    top3 = by_campaign[:3]
    bottom3 = by_campaign[-3:][::-1]

    lines = [
        f"# Reporte de Rendimiento — {client}",
        f"**Período:** {period}  |  **Generado:** {date.today().isoformat()}",
        "",
        "---",
        "",
        "## Resumen ejecutivo",
        "",
        f"El período analizó **{global_metrics['impressions']:,} impresiones** con un gasto de "
        f"**{global_metrics['spend_eur']:,.2f} EUR** y un ROAS global de **{global_metrics['roas']}x**. "
        f"Se generaron **{global_metrics['conversions']:,} conversiones** a un CPA de "
        f"**{global_metrics['cpa_eur']:.2f} EUR**.",
        "",
        "## KPIs globales",
        "",
        "| Métrica | Valor |",
        "|---------|-------|",
        f"| Impresiones | {global_metrics['impressions']:,} |",
        f"| Clicks | {global_metrics['clicks']:,} |",
        f"| CTR | {global_metrics['ctr_%']}% |",
        f"| Conversiones | {global_metrics['conversions']:,} |",
        f"| Conv. Rate | {global_metrics['conv_rate_%']}% |",
        f"| Gasto | {global_metrics['spend_eur']:,.2f} EUR |",
        f"| Revenue | {global_metrics['revenue_eur']:,.2f} EUR |",
        f"| ROAS | {global_metrics['roas']}x |",
        f"| CPA | {global_metrics['cpa_eur']:.2f} EUR |",
        f"| CPM | {global_metrics['cpm_eur']:.2f} EUR |",
        "",
        "## Top 3 campañas por ROAS",
        "",
        "| Campaña | Canal | ROAS | CTR | Gasto |",
        "|---------|-------|------|-----|-------|",
    ]
    for c in top3:
        lines.append(
            f"| {c['campaign']} | {c['channel']} | {c['roas']}x | {c['ctr_%']}% | {c['spend_eur']:.2f}€ |"
        )

    lines += [
        "",
        "## Bottom 3 campañas por ROAS",
        "",
        "| Campaña | Canal | ROAS | CTR | Gasto |",
        "|---------|-------|------|-----|-------|",
    ]
    for c in bottom3:
        lines.append(
            f"| {c['campaign']} | {c['channel']} | {c['roas']}x | {c['ctr_%']}% | {c['spend_eur']:.2f}€ |"
        )

    lines += [
        "",
        "## Rendimiento por canal",
        "",
        "| Canal | Gasto | ROAS | CTR | Conv. |",
        "|-------|-------|------|-----|-------|",
    ]
    for ch in by_channel:
        lines.append(
            f"| {ch['channel']} | {ch['spend_eur']:.2f}€ | {ch['roas']}x | {ch['ctr_%']}% | {ch['conversions']:,} |"
        )

    lines += ["", "## Anomalías y alertas", ""]
    if alerts:
        for a in alerts:
            lines.append(f"- **ALERTA** {a}")
    else:
        lines.append("Sin anomalías detectadas en el período.")

    lines += [
        "",
        "## Próximas acciones",
        "",
        "- [ ] Revisar campañas con ROAS < 2x y evaluar pausa",
        "- [ ] Rotar creatividades en campañas con frecuencia > 3",
        "- [ ] Escalar presupuesto en top campañas (+20%)",
        "- [ ] Test A/B de nuevo copy en campaña de mayor gasto",
        "",
        "---",
        f"*Generado automáticamente por performance_reporter.py — {date.today().isoformat()}*",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Reporte Markdown guardado en: {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Performance Reporter — Marketing Digital")
    parser.add_argument("--client", default="Cliente", help="Nombre del cliente")
    parser.add_argument(
        "--period",
        default="last-30-days",
        help="Período (last-7-days, last-30-days, last-60-days, last-90-days)",
    )
    parser.add_argument("--csv", help="Ruta a CSV de datos (si no se especifica, usa analyze_campaign.py)")
    parser.add_argument("--output", help="Ruta de salida para el reporte Markdown")
    parser.add_argument(
        "--format",
        choices=["console", "md", "both"],
        default="both",
        help="Formato de salida",
    )
    return parser


def resolve_csv(args: argparse.Namespace) -> Path:
    if args.csv:
        p = Path(args.csv)
        if not p.exists():
            sys.exit(f"Error: no se encuentra {args.csv}")
        return p

    slug = f"{args.client.replace(' ', '_').lower()}_{args.period}"
    candidates = [
        Path(f"{slug}.csv"),
        Path(f"../{slug}.csv"),
    ]
    for c in candidates:
        if c.exists():
            return c

    print(f"[INFO] CSV no encontrado — generando datos de prueba con analyze_campaign.py")
    import subprocess
    result = subprocess.run(
        [sys.executable, "analyze_campaign.py", "--client", args.client, "--period", args.period],
        capture_output=True, text=True
    )
    p = Path(f"{slug}.csv")
    if p.exists():
        return p
    sys.exit(f"Error: no se pudo generar CSV para {args.client}/{args.period}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    csv_path = resolve_csv(args)
    print(f"Cargando datos desde: {csv_path}")
    raw_rows = load_csv(csv_path)
    rows = [coerce_row(r) for r in raw_rows]

    if not rows:
        sys.exit("Error: el CSV está vacío.")

    global_metrics = aggregate_global(rows)
    by_campaign = aggregate_by_campaign(rows)
    by_channel = aggregate_by_channel(rows)
    trend = daily_trend(rows)
    alerts = detect_anomalies(trend)

    if args.format in ("console", "both"):
        print_global(global_metrics, args.client, args.period)
        print_by_channel(by_channel)
        print_by_campaign(by_campaign)
        print_alerts(alerts)

    if args.format in ("md", "both"):
        slug = f"{args.client.replace(' ', '_').lower()}_{args.period}"
        output_path = Path(args.output or f"{slug}_reporte.md")
        generate_markdown(
            client=args.client,
            period=args.period,
            global_metrics=global_metrics,
            by_campaign=by_campaign,
            by_channel=by_channel,
            alerts=alerts,
            output_path=output_path,
        )


if __name__ == "__main__":
    main()
