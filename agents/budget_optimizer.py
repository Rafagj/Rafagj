#!/usr/bin/env python3
"""
Budget Optimizer — redistribuye presupuesto entre campañas según ROAS/CPA.

Lee el rendimiento actual de campañas y produce un plan de redistribución
con reglas de escalado seguro, simulación de retorno y opción de aplicación
automática vía Meta Ads API.

Usage:
    python agents/budget_optimizer.py --csv datos.csv --budget 5000
    python agents/budget_optimizer.py --csv datos.csv --budget 5000 --objective ROAS --target 3.5
    python agents/budget_optimizer.py --mock --budget 10000 --apply
"""

import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROAS_SCALE = 4.0       # ROAS > this → scale up
ROAS_MAINTAIN = 3.0    # ROAS between maintain and scale → keep
ROAS_REDUCE = 2.0      # ROAS between reduce and maintain → cut
MAX_SCALE_FACTOR = 1.30  # Max single-day budget increase: 30%
MIN_BUDGET_EUR = 5.0   # Minimum daily budget per campaign


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CampaignMetrics:
    id: str
    name: str
    channel: str
    spend: float
    revenue: float
    conversions: int
    impressions: int
    clicks: int
    current_budget: float = 0.0

    @property
    def roas(self) -> float:
        return self.revenue / self.spend if self.spend > 0 else 0.0

    @property
    def cpa(self) -> float:
        return self.spend / self.conversions if self.conversions > 0 else float("inf")

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions > 0 else 0.0

    @property
    def conv_rate(self) -> float:
        return self.conversions / self.clicks if self.clicks > 0 else 0.0

    @property
    def label(self) -> str:
        if self.roas >= ROAS_SCALE:
            return "ESCALAR"
        if self.roas >= ROAS_MAINTAIN:
            return "MANTENER"
        if self.roas >= ROAS_REDUCE:
            return "REDUCIR"
        return "PAUSAR"


@dataclass
class BudgetPlan:
    campaign: CampaignMetrics
    current_budget: float
    recommended_budget: float
    action: str
    reason: str
    projected_roas: float
    projected_revenue: float

    @property
    def delta(self) -> float:
        return self.recommended_budget - self.current_budget

    @property
    def delta_pct(self) -> float:
        return self.delta / self.current_budget * 100 if self.current_budget > 0 else 0.0


# ---------------------------------------------------------------------------
# Load data from CSV
# ---------------------------------------------------------------------------

def load_csv_metrics(path: Path) -> list[CampaignMetrics]:
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        buckets[r.get("campaign", "")].append(r)

    metrics = []
    for name, bucket in buckets.items():
        spend = sum(float(r.get("spend_eur", 0)) for r in bucket)
        revenue = sum(float(r.get("revenue_eur", 0)) for r in bucket)
        conversions = sum(int(r.get("conversions", 0)) for r in bucket)
        impressions = sum(int(r.get("impressions", 0)) for r in bucket)
        clicks = sum(int(r.get("clicks", 0)) for r in bucket)
        channel = bucket[0].get("channel", "Desconocido")
        days = len(set(r.get("date", "") for r in bucket)) or 1
        avg_daily_spend = spend / days

        metrics.append(CampaignMetrics(
            id=f"camp_{abs(hash(name)) % 100_000:05d}",
            name=name,
            channel=channel,
            spend=round(spend, 2),
            revenue=round(revenue, 2),
            conversions=conversions,
            impressions=impressions,
            clicks=clicks,
            current_budget=round(avg_daily_spend, 2),
        ))

    return sorted(metrics, key=lambda m: m.roas, reverse=True)


def mock_metrics() -> list[CampaignMetrics]:
    return [
        CampaignMetrics("120001", "Brand Awareness - Instagram", "Instagram",
                        spend=1243.80, revenue=5230.00, conversions=87,
                        impressions=85420, clicks=940, current_budget=50.0),
        CampaignMetrics("120002", "Conversion - Google Search", "Google Ads",
                        spend=2180.40, revenue=9102.00, conversions=210,
                        impressions=34120, clicks=1820, current_budget=80.0),
        CampaignMetrics("120003", "Retargeting - Facebook", "Facebook",
                        spend=890.20, revenue=2100.00, conversions=42,
                        impressions=29800, clicks=620, current_budget=35.0),
        CampaignMetrics("120004", "YouTube Pre-Roll", "YouTube",
                        spend=540.00, revenue=870.00, conversions=18,
                        impressions=112000, clicks=310, current_budget=20.0),
        CampaignMetrics("120005", "Email Newsletter - Weekly", "Email",
                        spend=120.00, revenue=980.00, conversions=55,
                        impressions=45000, clicks=9800, current_budget=5.0),
    ]


# ---------------------------------------------------------------------------
# Optimization engine
# ---------------------------------------------------------------------------

def compute_budget_plans(
    campaigns: list[CampaignMetrics],
    total_budget: float,
    objective: str = "ROAS",
    cpa_target: float | None = None,
    roas_target: float = 3.0,
) -> list[BudgetPlan]:
    plans: list[BudgetPlan] = []

    active = [c for c in campaigns if c.label != "PAUSAR"]
    paused = [c for c in campaigns if c.label == "PAUSAR"]

    # Weighted allocation: ROAS-proportional for active campaigns
    total_weight = sum(max(c.roas, 0.1) for c in active) or 1.0
    base_allocations = {
        c.id: (max(c.roas, 0.1) / total_weight) * total_budget
        for c in active
    }

    for c in active:
        raw = base_allocations[c.id]
        # Apply max scale factor (no more than 30% increase in one step)
        if c.current_budget > 0:
            capped = min(raw, c.current_budget * MAX_SCALE_FACTOR)
            recommended = max(capped, MIN_BUDGET_EUR)
        else:
            recommended = max(raw, MIN_BUDGET_EUR)

        recommended = round(recommended, 2)
        action = c.label
        reason = _reason(c, objective, cpa_target, roas_target)
        projected_roas = c.roas  # assumes same efficiency at scale (conservative)
        projected_revenue = recommended * c.roas * 30  # 30-day projection

        plans.append(BudgetPlan(
            campaign=c,
            current_budget=c.current_budget,
            recommended_budget=recommended,
            action=action,
            reason=reason,
            projected_roas=round(projected_roas, 2),
            projected_revenue=round(projected_revenue, 2),
        ))

    for c in paused:
        plans.append(BudgetPlan(
            campaign=c,
            current_budget=c.current_budget,
            recommended_budget=0.0,
            action="PAUSAR",
            reason=f"ROAS {c.roas:.2f}x por debajo del mínimo ({ROAS_REDUCE}x)",
            projected_roas=0.0,
            projected_revenue=0.0,
        ))

    return plans


def _reason(c: CampaignMetrics, objective: str, cpa_target: float | None, roas_target: float) -> str:
    if c.roas >= ROAS_SCALE:
        return f"ROAS {c.roas:.2f}x — campaña ganadora, escalar con precaución"
    if c.roas >= ROAS_MAINTAIN:
        return f"ROAS {c.roas:.2f}x — rendimiento saludable, mantener"
    if c.roas >= ROAS_REDUCE:
        return f"ROAS {c.roas:.2f}x — por debajo del objetivo, reducir e investigar"
    return f"ROAS {c.roas:.2f}x — ineficiente, pausar y revisar"


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------

def simulate_return(plans: list[BudgetPlan], days: int = 30) -> dict:
    total_new_spend = sum(p.recommended_budget * days for p in plans)
    total_proj_revenue = sum(p.projected_revenue for p in plans)
    total_proj_roas = total_proj_revenue / total_new_spend if total_new_spend else 0.0

    current_spend_monthly = sum(p.current_budget * days for p in plans)
    current_campaigns = [p for p in plans if p.current_budget > 0]
    current_roas = (
        sum(p.campaign.roas * p.current_budget for p in current_campaigns)
        / sum(p.current_budget for p in current_campaigns)
        if current_campaigns else 0.0
    )
    current_revenue = current_spend_monthly * current_roas

    return {
        "days": days,
        "current_spend_eur": round(current_spend_monthly, 2),
        "current_revenue_eur": round(current_revenue, 2),
        "current_roas": round(current_roas, 2),
        "projected_spend_eur": round(total_new_spend, 2),
        "projected_revenue_eur": round(total_proj_revenue, 2),
        "projected_roas": round(total_proj_roas, 2),
        "revenue_uplift_eur": round(total_proj_revenue - current_revenue, 2),
        "revenue_uplift_pct": round((total_proj_revenue / current_revenue - 1) * 100, 2)
        if current_revenue > 0 else 0.0,
    }


# ---------------------------------------------------------------------------
# Printers
# ---------------------------------------------------------------------------

SEP = "=" * 72

def print_plans(plans: list[BudgetPlan]) -> None:
    print(f"\n{'Acción':<10} {'Actual/día':>11} {'Nuevo/día':>11} {'Delta':>9} {'ROAS':>7}  Campaña")
    print("-" * 85)
    for p in plans:
        delta_str = f"{p.delta:+.2f}€" if p.recommended_budget > 0 else "PAUSAR"
        print(
            f"  {p.action:<9} {p.current_budget:>9.2f}€ {p.recommended_budget:>9.2f}€ "
            f"{delta_str:>9} {p.campaign.roas:>6.2f}x  {p.campaign.name}"
        )
    print()


def print_simulation(sim: dict) -> None:
    print(f"{SEP}")
    print("  Simulación de retorno a 30 días")
    print(SEP)
    print(f"  {'':25} {'Actual':>14} {'Proyectado':>14}")
    print(f"  {'Gasto mensual':25} {sim['current_spend_eur']:>13,.2f}€ {sim['projected_spend_eur']:>13,.2f}€")
    print(f"  {'Revenue mensual':25} {sim['current_revenue_eur']:>13,.2f}€ {sim['projected_revenue_eur']:>13,.2f}€")
    print(f"  {'ROAS':25} {sim['current_roas']:>13.2f}x {sim['projected_roas']:>13.2f}x")
    uplift = sim["revenue_uplift_eur"]
    sign = "+" if uplift >= 0 else ""
    print(f"\n  Incremento de revenue estimado: {sign}{uplift:,.2f}€ ({sign}{sim['revenue_uplift_pct']:.1f}%)")
    print(SEP + "\n")


def print_warnings(plans: list[BudgetPlan]) -> None:
    warnings = [p for p in plans if abs(p.delta_pct) > 20 and p.recommended_budget > 0]
    if not warnings:
        return
    print("Advertencias de escalado:")
    for p in warnings:
        print(f"  AVISO  {p.campaign.name}: cambio del {p.delta_pct:+.1f}% — aplicar gradualmente")
    print()


def export_plan_csv(plans: list[BudgetPlan], output: Path) -> None:
    rows = []
    for p in plans:
        rows.append({
            "campaign_id": p.campaign.id,
            "campaign": p.campaign.name,
            "channel": p.campaign.channel,
            "action": p.action,
            "current_budget_eur": p.current_budget,
            "recommended_budget_eur": p.recommended_budget,
            "delta_eur": round(p.delta, 2),
            "delta_pct": round(p.delta_pct, 1),
            "current_roas": round(p.campaign.roas, 2),
            "reason": p.reason,
        })
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Plan exportado a: {output}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Budget Optimizer — Marketing Digital")
    parser.add_argument("--csv", help="CSV de rendimiento de campañas")
    parser.add_argument("--budget", type=float, required=True,
                        help="Presupuesto diario total disponible (EUR)")
    parser.add_argument("--objective", choices=["ROAS", "CPA"], default="ROAS",
                        help="Objetivo de optimización")
    parser.add_argument("--target", type=float, help="Valor objetivo (ROAS o CPA en EUR)")
    parser.add_argument("--days", type=int, default=30,
                        help="Días para la simulación de retorno")
    parser.add_argument("--export", help="Exportar plan a CSV")
    parser.add_argument("--mock", action="store_true",
                        help="Usar datos de prueba sin CSV")
    parser.add_argument("--apply", action="store_true",
                        help="Aplicar cambios vía Meta Ads API (requiere credenciales)")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.mock:
        print("[INFO] Modo mock activado — usando datos de prueba\n")
        campaigns = mock_metrics()
    elif args.csv:
        csv_path = Path(args.csv)
        if not csv_path.exists():
            sys.exit(f"Error: no se encuentra {args.csv}")
        print(f"Cargando métricas desde: {csv_path}\n")
        campaigns = load_csv_metrics(csv_path)
    else:
        sys.exit("Error: proporciona --csv <archivo> o usa --mock")

    if not campaigns:
        sys.exit("Error: no se encontraron campañas.")

    roas_target = args.target if args.objective == "ROAS" and args.target else 3.0
    cpa_target = args.target if args.objective == "CPA" else None

    plans = compute_budget_plans(
        campaigns,
        total_budget=args.budget,
        objective=args.objective,
        cpa_target=cpa_target,
        roas_target=roas_target,
    )

    print(f"{SEP}")
    print(f"  Plan de Optimización de Presupuesto")
    print(f"  Presupuesto diario total: {args.budget:.2f} EUR  |  Objetivo: {args.objective}")
    print(SEP)

    print_plans(plans)
    print_warnings(plans)

    sim = simulate_return(plans, days=args.days)
    print_simulation(sim)

    if args.export:
        export_plan_csv(plans, Path(args.export))

    if args.apply:
        print("[APLICAR] Conectando a Meta Ads API para aplicar cambios...")
        print("[AVISO] Implementa la conexión real en meta_campaign_manager.py")
        for p in plans:
            if p.action == "PAUSAR":
                print(f"  PAUSAR  → {p.campaign.name} (ID: {p.campaign.id})")
            elif p.recommended_budget != p.current_budget:
                print(f"  UPDATE  → {p.campaign.name}: {p.current_budget:.2f}€ → {p.recommended_budget:.2f}€/día")
        print("\n[INFO] En producción, llamar ads_update_entity / ads_activate_entity para cada cambio.")


if __name__ == "__main__":
    main()
