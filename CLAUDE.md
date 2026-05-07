# Rafagj — Marketing Digital & Gestión de Pauta

## Descripción del proyecto

Repositorio de herramientas y agentes para gestión de campañas de marketing digital, con foco en **Meta Ads (Facebook & Instagram)**, análisis de rendimiento y optimización de presupuesto.

## Estructura

```
.
├── agents/                      # Agentes autónomos de marketing
│   ├── meta_campaign_manager.py # Gestión completa de campañas Meta
│   ├── performance_reporter.py  # Reportes de rendimiento multi-canal
│   └── budget_optimizer.py      # Optimización de presupuesto y ROAS
├── .claude/skills/              # Skills de Claude Code
│   ├── meta-pauta.md            # Gestión de pauta en Meta
│   ├── analitica-marketing.md   # Análisis de métricas y KPIs
│   └── optimizacion-presupuesto.md  # Optimización de inversión
├── analyze_campaign.py          # Analizador base de campañas (CSV)
└── CLAUDE.md                    # Este archivo
```

## Skills disponibles

Invoca los skills con `/meta-pauta`, `/analitica-marketing` u `/optimizacion-presupuesto`.

## Agentes disponibles

```bash
# Gestionar campañas en Meta Ads
python agents/meta_campaign_manager.py --account <ID> --action list

# Generar reporte de rendimiento
python agents/performance_reporter.py --client "Cupra Wines" --period last-30-days

# Optimizar presupuesto
python agents/budget_optimizer.py --account <ID> --budget 5000 --objective ROAS
```

## KPIs clave

| Métrica | Descripción | Benchmark |
|---------|-------------|-----------|
| ROAS | Retorno sobre inversión publicitaria | > 3x |
| CTR | Click-through rate | > 1.5% Meta, > 3% Search |
| CPC | Coste por clic | Depende de industria |
| CPM | Coste por 1.000 impresiones | < 10 EUR Meta |
| Conv. Rate | Tasa de conversión | > 2% |
| Frecuencia | Veces que un usuario ve el anuncio | < 3 (awareness) |

## Clientes activos

- **Cupra Wines** — Campañas en Instagram, Facebook, Google, YouTube, Email

## Convenciones

- Moneda por defecto: EUR
- Zona horaria: Europe/Madrid
- Periodos estándar: `last-7-days`, `last-30-days`, `last-60-days`, `last-90-days`
- Atribución: 7-day click, 1-day view (Meta estándar)
