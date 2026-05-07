# Skill: Analítica de Marketing Digital

## Descripción

Analiza métricas de rendimiento de campañas digitales multi-canal (Meta, Google, YouTube, Email), genera insights accionables y detecta anomalías. Usa datos de CSV exportados o conexiones directas a plataformas.

## Cuándo usar este skill

Invoca `/analitica-marketing` cuando el usuario pida:
- Análisis de rendimiento de campañas por período
- Comparación entre canales o campañas
- Detección de tendencias y anomalías
- Generación de reportes ejecutivos
- Benchmarking contra industria

## Fuentes de datos

1. **CSV local**: Usar `analyze_campaign.py` o archivos en el repositorio
2. **Meta Ads**: Vía herramientas MCP `ads_insights_*`
3. **Datos históricos**: Archivos `*_last-*.csv` en el repositorio

## Proceso de análisis

### 1. Recopilar datos

```bash
# Generar datos para un cliente y período
python analyze_campaign.py --client "Cupra Wines" --period last-30-days

# Leer CSV existente
# Usar herramienta Read sobre archivos .csv del repositorio
```

### 2. Métricas a calcular siempre

| Métrica | Fórmula | Objetivo |
|---------|---------|---------|
| CTR | Clicks / Impresiones × 100 | > 1.5% |
| CPC | Gasto / Clicks | Minimizar |
| CPM | (Gasto / Impresiones) × 1.000 | < 10 EUR |
| Conv. Rate | Conversiones / Clicks × 100 | > 2% |
| CPA | Gasto / Conversiones | Según objetivo |
| ROAS | Ingresos / Gasto | > 3x |
| ROI | (Ingresos - Gasto) / Gasto × 100 | > 200% |

### 3. Análisis por dimensiones

Siempre segmentar por:
- **Canal**: Meta, Google, YouTube, Email
- **Formato**: Reel, Carousel, Search, Video, Newsletter
- **Período**: Día, semana, mes (detectar estacionalidad)
- **Campaña**: Rendimiento individual

### 4. Detección de anomalías

Buscar:
- Variaciones > 30% en CTR semana sobre semana
- Caídas de ROAS > 20% en 3 días consecutivos
- CPM > 2× la media histórica
- Conversiones = 0 durante > 2 días con gasto activo

### 5. Formato de reporte ejecutivo

```markdown
## Reporte de Rendimiento — [Cliente] — [Período]

### Resumen ejecutivo
[2-3 frases con los hallazgos principales]

### KPIs globales
| Métrica | Valor | vs Período Anterior | vs Objetivo |
|---------|-------|--------------------|-----------  |

### Top campañas
[Tabla con las 3 mejores y 3 peores por ROAS]

### Hallazgos clave
1. [Insight con dato concreto y acción recomendada]
2. ...

### Próximas acciones
- [ ] Acción 1 — Responsable — Fecha
- [ ] Acción 2 — Responsable — Fecha
```

## Benchmarks de industria (referencia)

| Canal | CTR | Conv. Rate | ROAS | CPM |
|-------|-----|-----------|------|-----|
| Meta (ecomm) | 0.9-1.5% | 1-3% | 2-4x | 7-12 EUR |
| Google Search | 3-6% | 3-8% | 3-6x | — |
| YouTube | 0.5-1% | 0.5-2% | 1.5-3x | 5-8 EUR |
| Email | 18-25% OR | 2-5% CTR | — | — |

## Herramientas de apoyo

- `ads_insights_industry_benchmark`: benchmarks actualizados por industria
- `ads_insights_performance_trend`: tendencias históricas de la cuenta
- `ads_insights_anomaly_signal`: alertas automáticas de anomalías
- `analyze_campaign.py`: generador y analizador de datos CSV
