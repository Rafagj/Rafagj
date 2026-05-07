#!/usr/bin/env python3
"""
Meta Ads Campaign Manager — CLI agent for managing Meta Ads campaigns.

Supports listing, creating, pausing, activating, and auditing campaigns,
ad sets, and ads via the Meta Marketing API.

Usage:
    python agents/meta_campaign_manager.py --account <ACCOUNT_ID> --action list
    python agents/meta_campaign_manager.py --account <ACCOUNT_ID> --action audit
    python agents/meta_campaign_manager.py --account <ACCOUNT_ID> --action create --config campaign.json
    python agents/meta_campaign_manager.py --account <ACCOUNT_ID> --action pause --entity-id <ID>
    python agents/meta_campaign_manager.py --account <ACCOUNT_ID> --action activate --entity-id <ID>
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any

try:
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.ad import Ad
    HAS_SDK = True
except ImportError:
    HAS_SDK = False


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CampaignConfig:
    name: str
    objective: str
    daily_budget: float
    status: str = "PAUSED"
    special_ad_categories: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "CampaignConfig":
        return cls(
            name=data["name"],
            objective=data["objective"],
            daily_budget=float(data["daily_budget"]),
            status=data.get("status", "PAUSED"),
            special_ad_categories=data.get("special_ad_categories", []),
        )


@dataclass
class AdSetConfig:
    name: str
    campaign_id: str
    daily_budget: float
    optimization_goal: str
    billing_event: str
    bid_amount: float | None
    targeting: dict
    start_time: str | None = None
    end_time: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "AdSetConfig":
        return cls(
            name=data["name"],
            campaign_id=data["campaign_id"],
            daily_budget=float(data["daily_budget"]),
            optimization_goal=data["optimization_goal"],
            billing_event=data["billing_event"],
            bid_amount=data.get("bid_amount"),
            targeting=data.get("targeting", {}),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
        )


# ---------------------------------------------------------------------------
# Meta API client wrapper
# ---------------------------------------------------------------------------

class MetaAdsClient:
    """Thin wrapper around the Meta Business SDK."""

    CAMPAIGN_FIELDS = [
        "id", "name", "status", "objective",
        "daily_budget", "lifetime_budget", "start_time", "stop_time",
    ]

    ADSET_FIELDS = [
        "id", "name", "status", "campaign_id",
        "daily_budget", "optimization_goal", "bid_amount", "targeting",
    ]

    AD_FIELDS = [
        "id", "name", "status", "adset_id", "campaign_id", "effective_status",
    ]

    INSIGHT_FIELDS = [
        "impressions",
        "clicks",
        "ctr",
        "spend",
        "actions",
        "action_values",
        "cost_per_action_type",
        "cpc",
        "cpm",
        "frequency",
        "reach",
    ]

    def __init__(self, access_token: str, account_id: str, app_id: str = "", app_secret: str = ""):
        if not HAS_SDK:
            raise RuntimeError(
                "facebook-business SDK not installed. Run: pip install facebook-business"
            )
        FacebookAdsApi.init(app_id, app_secret, access_token)
        self.account = AdAccount(f"act_{account_id.lstrip('act_')}")

    # --- Campaigns -----------------------------------------------------------

    def list_campaigns(self, status_filter: list[str] | None = None) -> list[dict]:
        params: dict = {}
        if status_filter:
            params["effective_status"] = status_filter
        campaigns = self.account.get_campaigns(fields=self.CAMPAIGN_FIELDS, params=params)
        return [c.export_all_data() for c in campaigns]

    def create_campaign(self, config: CampaignConfig) -> dict:
        params = {
            "name": config.name,
            "objective": config.objective,
            "daily_budget": int(config.daily_budget * 100),  # cents
            "status": config.status,
            "special_ad_categories": config.special_ad_categories,
        }
        campaign = self.account.create_campaign(fields=[], params=params)
        return campaign.export_all_data()

    def set_campaign_status(self, campaign_id: str, status: str) -> dict:
        campaign = Campaign(campaign_id)
        campaign["status"] = status
        campaign.remote_update()
        return {"id": campaign_id, "status": status}

    # --- Ad Sets -------------------------------------------------------------

    def list_adsets(self, campaign_id: str | None = None) -> list[dict]:
        if campaign_id:
            campaign = Campaign(campaign_id)
            adsets = campaign.get_ad_sets(fields=self.ADSET_FIELDS)
        else:
            adsets = self.account.get_ad_sets(fields=self.ADSET_FIELDS)
        return [a.export_all_data() for a in adsets]

    def create_adset(self, config: AdSetConfig) -> dict:
        params = {
            "name": config.name,
            "campaign_id": config.campaign_id,
            "daily_budget": int(config.daily_budget * 100),
            "optimization_goal": config.optimization_goal,
            "billing_event": config.billing_event,
            "targeting": config.targeting,
            "status": "PAUSED",
        }
        if config.bid_amount is not None:
            params["bid_amount"] = int(config.bid_amount * 100)
        if config.start_time:
            params["start_time"] = config.start_time
        if config.end_time:
            params["end_time"] = config.end_time
        adset = self.account.create_ad_set(fields=[], params=params)
        return adset.export_all_data()

    # --- Insights ------------------------------------------------------------

    def get_insights(self, date_preset: str = "last_30d", level: str = "campaign") -> list[dict]:
        params = {
            "date_preset": date_preset,
            "level": level,
            "fields": self.INSIGHT_FIELDS,
        }
        insights = self.account.get_insights(params=params)
        return [i.export_all_data() for i in insights]

    # --- Audit ---------------------------------------------------------------

    def audit(self) -> dict:
        campaigns = self.list_campaigns(status_filter=["ACTIVE", "PAUSED"])
        insights = self.get_insights(date_preset="last_30d", level="campaign")
        insights_by_id = {i.get("campaign_id", ""): i for i in insights}

        issues: list[str] = []
        for c in campaigns:
            cid = c.get("id", "")
            ins = insights_by_id.get(cid, {})
            ctr = float(ins.get("ctr", 0))
            spend = float(ins.get("spend", 0))
            freq = float(ins.get("frequency", 0))

            if c.get("status") == "ACTIVE" and spend == 0:
                issues.append(f"[{c['name']}] Activa pero sin gasto en 30 días")
            if ctr < 0.008 and spend > 0:
                issues.append(f"[{c['name']}] CTR muy bajo ({ctr*100:.2f}%) — revisar creatividades")
            if freq > 3.5:
                issues.append(f"[{c['name']}] Frecuencia alta ({freq:.1f}) — rotar creatividades")

        return {
            "total_campaigns": len(campaigns),
            "active": sum(1 for c in campaigns if c.get("status") == "ACTIVE"),
            "paused": sum(1 for c in campaigns if c.get("status") == "PAUSED"),
            "issues": issues,
            "campaigns": campaigns,
        }


# ---------------------------------------------------------------------------
# Mock client for testing without credentials
# ---------------------------------------------------------------------------

class MockMetaAdsClient:
    """Returns realistic fake data for development/testing."""

    _CAMPAIGNS = [
        {"id": "120001", "name": "CupraWines_BRAND_IG_Reel_2026Q2", "status": "ACTIVE",
         "objective": "BRAND_AWARENESS", "daily_budget": "5000"},
        {"id": "120002", "name": "CupraWines_CONV_Retargeting_Carousel_2026Q2", "status": "ACTIVE",
         "objective": "CONVERSIONS", "daily_budget": "8000"},
        {"id": "120003", "name": "CupraWines_TRAFFIC_TOF_Video_2026Q2", "status": "PAUSED",
         "objective": "LINK_CLICKS", "daily_budget": "3000"},
    ]

    _INSIGHTS = [
        {"campaign_id": "120001", "campaign_name": "CupraWines_BRAND_IG_Reel_2026Q2",
         "impressions": "85420", "clicks": "940", "ctr": "0.011", "spend": "1243.80",
         "reach": "42100", "frequency": "2.03", "cpm": "14.56", "cpc": "1.32"},
        {"campaign_id": "120002", "campaign_name": "CupraWines_CONV_Retargeting_Carousel_2026Q2",
         "impressions": "34120", "clicks": "1820", "ctr": "0.053", "spend": "2180.40",
         "reach": "18900", "frequency": "1.81", "cpm": "63.90", "cpc": "1.20"},
        {"campaign_id": "120003", "campaign_name": "CupraWines_TRAFFIC_TOF_Video_2026Q2",
         "impressions": "0", "clicks": "0", "ctr": "0", "spend": "0",
         "reach": "0", "frequency": "0", "cpm": "0", "cpc": "0"},
    ]

    def list_campaigns(self, status_filter=None):
        if not status_filter:
            return self._CAMPAIGNS
        return [c for c in self._CAMPAIGNS if c["status"] in status_filter]

    def create_campaign(self, config: CampaignConfig) -> dict:
        return {"id": "120099", "name": config.name, "status": config.status,
                "objective": config.objective}

    def set_campaign_status(self, campaign_id: str, status: str) -> dict:
        return {"id": campaign_id, "status": status}

    def list_adsets(self, campaign_id=None) -> list[dict]:
        return [
            {"id": "210001", "name": "Mujeres 25-45 España", "status": "ACTIVE",
             "campaign_id": "120002", "daily_budget": "4000"},
            {"id": "210002", "name": "Lookalike 1% compradores", "status": "ACTIVE",
             "campaign_id": "120002", "daily_budget": "4000"},
        ]

    def create_adset(self, config: AdSetConfig) -> dict:
        return {"id": "210099", "name": config.name, "campaign_id": config.campaign_id}

    def get_insights(self, date_preset="last_30d", level="campaign") -> list[dict]:
        return self._INSIGHTS

    def audit(self) -> dict:
        campaigns = self.list_campaigns(status_filter=["ACTIVE", "PAUSED"])
        issues = [
            "[CupraWines_TRAFFIC_TOF_Video_2026Q2] Activa pero sin gasto en 30 días"
        ]
        return {
            "total_campaigns": len(campaigns),
            "active": 2,
            "paused": 1,
            "issues": issues,
            "campaigns": campaigns,
        }


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

def print_campaigns(campaigns: list[dict]) -> None:
    print(f"\n{'ID':<10} {'Estado':<10} {'Objetivo':<22} {'Presupuesto/día':>16}  Nombre")
    print("-" * 90)
    for c in campaigns:
        budget_eur = int(c.get("daily_budget", 0)) / 100 if HAS_SDK else int(c.get("daily_budget", 0)) / 100
        budget_str = f"{budget_eur:.2f} EUR" if budget_eur else "—"
        print(f"{c['id']:<10} {c.get('status','?'):<10} {c.get('objective','?'):<22} "
              f"{budget_str:>16}  {c['name']}")
    print()


def print_insights(insights: list[dict]) -> None:
    print(f"\n{'Campaña':<45} {'Impresiones':>12} {'CTR':>7} {'CPC':>8} {'Gasto':>10}")
    print("-" * 90)
    for i in insights:
        name = i.get("campaign_name", i.get("campaign_id", "?"))[:44]
        impressions = int(i.get("impressions", 0))
        ctr = float(i.get("ctr", 0)) * 100
        cpc = float(i.get("cpc", 0))
        spend = float(i.get("spend", 0))
        print(f"{name:<45} {impressions:>12,} {ctr:>6.2f}% {cpc:>7.2f}€ {spend:>9.2f}€")
    print()


def print_audit(audit: dict) -> None:
    print(f"\n{'='*60}")
    print("  Auditoría de Cuenta Meta Ads")
    print(f"{'='*60}")
    print(f"  Campañas totales : {audit['total_campaigns']}")
    print(f"  Activas          : {audit['active']}")
    print(f"  Pausadas         : {audit['paused']}")
    print(f"\n  Problemas detectados ({len(audit['issues'])}):")
    if audit["issues"]:
        for issue in audit["issues"]:
            print(f"  ⚠  {issue}")
    else:
        print("  Sin problemas detectados.")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Meta Ads Campaign Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--account", required=True, help="Meta Ads account ID (sin 'act_')")
    parser.add_argument(
        "--action",
        required=True,
        choices=["list", "audit", "insights", "create", "pause", "activate", "list-adsets"],
        help="Acción a ejecutar",
    )
    parser.add_argument("--token", default="", help="Meta access token (o variable META_ACCESS_TOKEN)")
    parser.add_argument("--entity-id", help="ID de campaña/ad set/anuncio para pause/activate")
    parser.add_argument("--config", help="JSON de configuración para create")
    parser.add_argument("--campaign-id", help="ID de campaña para list-adsets")
    parser.add_argument("--period", default="last_30d",
                        help="Período para insights (last_7d, last_30d, last_90d)")
    parser.add_argument("--mock", action="store_true",
                        help="Usar datos de prueba sin conectar a Meta API")
    return parser


def get_client(args: argparse.Namespace):
    if args.mock or not args.token:
        print("[INFO] Modo mock activado — usando datos de prueba\n")
        return MockMetaAdsClient()
    import os
    token = args.token or os.environ.get("META_ACCESS_TOKEN", "")
    if not token:
        sys.exit("Error: proporciona --token o define META_ACCESS_TOKEN")
    return MetaAdsClient(access_token=token, account_id=args.account)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    client = get_client(args)

    if args.action == "list":
        campaigns = client.list_campaigns(status_filter=["ACTIVE", "PAUSED", "ARCHIVED"])
        print(f"Campañas en cuenta {args.account}:")
        print_campaigns(campaigns)

    elif args.action == "audit":
        result = client.audit()
        print_audit(result)

    elif args.action == "insights":
        insights = client.get_insights(date_preset=args.period, level="campaign")
        print(f"Insights ({args.period}) — cuenta {args.account}:")
        print_insights(insights)

    elif args.action == "create":
        if not args.config:
            sys.exit("Error: --config <fichero.json> requerido para crear campaña")
        config_path = Path(args.config)
        if not config_path.exists():
            sys.exit(f"Error: no se encuentra {args.config}")
        data = json.loads(config_path.read_text())
        config = CampaignConfig.from_dict(data)
        result = client.create_campaign(config)
        print(f"Campaña creada: {result}")

    elif args.action == "pause":
        if not args.entity_id:
            sys.exit("Error: --entity-id requerido")
        result = client.set_campaign_status(args.entity_id, "PAUSED")
        print(f"Campaña {args.entity_id} pausada.")

    elif args.action == "activate":
        if not args.entity_id:
            sys.exit("Error: --entity-id requerido")
        result = client.set_campaign_status(args.entity_id, "ACTIVE")
        print(f"Campaña {args.entity_id} activada.")

    elif args.action == "list-adsets":
        adsets = client.list_adsets(campaign_id=args.campaign_id)
        print(f"Ad sets{f' (campaña {args.campaign_id})' if args.campaign_id else ''}:")
        for a in adsets:
            budget_eur = int(a.get("daily_budget", 0)) / 100
            print(f"  {a['id']}  [{a.get('status','?')}]  {budget_eur:.2f}€/día  {a['name']}")
        print()


if __name__ == "__main__":
    main()
