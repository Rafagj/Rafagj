# Skill: Auditoría de Cuenta Meta Ads

## Descripción

Ejecuta una auditoría completa y estandarizada de cualquier cuenta Meta Ads en una sola pasada. Cubre campañas activas, opportunity score, contexto del anunciante, errores de entrega y señales de anomalía.

## Cuándo usar este skill

Invoca `/auditoria-meta` cuando el usuario pida:
- Auditar o revisar una cuenta de Meta Ads
- Ver el estado general de una cuenta
- Diagnóstico antes de tomar decisiones de presupuesto o audiencia
- Revisión periódica (semanal/mensual) de rendimiento

## Proceso: 5 llamadas en paralelo

Siempre ejecutar estas 5 herramientas simultáneamente para máxima eficiencia:

```
1. ads_get_ad_entities        → campañas últimos 30 días
2. ads_get_opportunity_score  → score y recomendaciones
3. ads_insights_advertiser_context → vertical, funnel, objetivo
4. ads_get_errors             → errores de entrega activos
5. ads_insights_anomaly_signal → anomalías de rendimiento
```

### Campos para ads_get_ad_entities (nivel campaign)
```
["id", "name", "impressions", "clicks", "ctr", "cpm", "cpc",
 "frequency", "reach", "actions:link_click", "objective"]
sort: impressions_descending
date_preset: last_30d
```

## Interpretación de resultados

### Campañas — semáforo de KPIs

| Métrica | Verde ✅ | Amarillo ⚠️ | Rojo 🔴 |
|---------|---------|------------|--------|
| CTR (Link Clicks) | > 2% | 1–2% | < 1% |
| CTR (Engagement) | > 1% | 0.5–1% | < 0.5% |
| Frecuencia | < 2.5 | 2.5–3.5 | > 3.5 |
| CPM Meta (USD) | < 5 | 5–12 | > 12 |
| CPM Meta (ARS) | < 5.000 | 5.000–12.000 | > 12.000 |

### Opportunity Score

| Score | Interpretación |
|-------|---------------|
| 90–100 | Cuenta optimizada, solo ajustes menores |
| 75–89 | Problemas resolubles, acción recomendada |
| < 75 | Cuenta con issues estructurales, priorizar limpieza |

**Ordenar recomendaciones por `opportunity_score_lift` descendente** — trabajar primero las de mayor impacto.

### Errores de entrega — clasificación por urgencia

| Error | Urgencia | Acción |
|-------|---------|--------|
| WhatsApp number required | 🔴 Alta | Reconectar WA en Business Settings |
| Lookalike audience deleted | 🔴 Alta | Recrear audiencia o cambiar a Advantage+ |
| Ad set not delivering | 🟡 Media | Recrear ad set con nueva configuración |
| Invalid creative for objective | 🟡 Media | Reemplazar creativa compatible |
| No valid formats / IG media | 🟡 Media | Revisar specs de formato por placement |
| Organic media archived | 🟢 Baja | Archivar campaña o reemplazar creativa |

### Anomalías

| Anomalía | Umbral crítico | Acción |
|----------|---------------|--------|
| Narrow audience | < 5.000 personas | Ampliar audiencia o activar Advantage+ |
| Narrow audience | 5.000–20.000 | Evaluar expansión, monitorear frecuencia |
| ROAS caída > 30% vs 7d | Inmediato | Revisar creative fatigue y competencia |
| Gasto = 0 con campaña activa | Inmediato | Verificar errores, presupuesto y estado |

## Formato de reporte de auditoría

```markdown
## Auditoría [Cuenta] — [Fecha]

**Vertical:** [industria]  |  **Opportunity Score:** [X]/100

### Campañas activas
[tabla con KPIs y semáforo]

### Errores activos ([N])
[lista por urgencia con acción recomendada]

### Anomalías
[lista con contexto]

### Recomendaciones prioritarias
1. [Acción] — [Lift estimado] — [Urgencia]
2. ...
```

## Cuentas del portfolio

| Cliente | Account ID | Moneda | MCP habilitado |
|---------|-----------|--------|---------------|
| Cupra USD | 2734330683439155 | USD | ✅ |
| Tradition & Rebellion | 1255958546224523 | USD | ✅ |
| Dra. Maria Eugenia Buonsante | 1238818623235612 | ARS | ✅ |
| LP - La PLAYA 2023 | 1425628214343986 | — | ✅ |
| Sarapura | 852858213205966 | — | ✅ |
| Darwin Buen Ayre | 1311426056636753 | — | ✅ |
| Darwin SI - Pesos | 26730211493278328 | — | ✅ |
| Javier Nutrición | 219433399508952 | — | ✅ |
| Javier Rodriguez JRN 2025 | 1067365748751452 | — | ✅ |
| Dra. Barbara Villanustre | 571264391657764 | — | ✅ |
| Dr. Fernando Martin | 368020019406638 | — | ✅ |
| Skintegrity | 842960848330387 | — | ✅ |
| Prueba JRN | 1566431454395784 | — | ✅ |

## Cadencia recomendada

| Frecuencia | Qué revisar |
|------------|-------------|
| Diaria | Errores nuevos, anomalías, gasto 0 |
| Semanal | KPIs completos, frecuencia, CTR |
| Mensual | Opportunity Score, limpieza de errores acumulados |
