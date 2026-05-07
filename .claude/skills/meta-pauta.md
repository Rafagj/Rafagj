# Skill: Gestión de Pauta en Meta Ads

## Descripción

Gestiona campañas publicitarias en Facebook e Instagram a través de Meta Ads Manager. Cubre creación, edición, activación/pausa, monitoreo de rendimiento y auditoría de cuentas.

## Cuándo usar este skill

Invoca `/meta-pauta` cuando el usuario pida:
- Crear, pausar o activar campañas/ad sets/anuncios en Meta
- Consultar rendimiento de campañas activas
- Revisar errores o rechazos de anuncios
- Obtener el opportunity score o benchmarks de subasta
- Gestionar catálogos de productos (DPA/retargeting dinámico)
- Consultar páginas de Facebook asociadas a una cuenta

## Herramientas disponibles

Las siguientes herramientas MCP de Meta Ads están disponibles:

| Herramienta | Uso |
|-------------|-----|
| `ads_get_ad_accounts` | Listar cuentas publicitarias |
| `ads_get_ad_entities` | Obtener campañas, ad sets o anuncios |
| `ads_create_campaign` | Crear una nueva campaña |
| `ads_create_ad_set` | Crear un ad set dentro de una campaña |
| `ads_create_ad` | Crear un anuncio dentro de un ad set |
| `ads_update_entity` | Editar nombre, estado, presupuesto, etc. |
| `ads_activate_entity` | Activar o pausar una entidad |
| `ads_get_errors` | Ver rechazos y errores de política |
| `ads_get_opportunity_score` | Score de optimización de la cuenta |
| `ads_insights_performance_trend` | Tendencia de métricas en el tiempo |
| `ads_insights_industry_benchmark` | Benchmarks por industria |
| `ads_insights_auction_ranking_benchmarks` | Posición relativa en subasta |
| `ads_insights_anomaly_signal` | Detectar anomalías en rendimiento |
| `ads_insights_advertiser_context` | Contexto general del anunciante |
| `ads_get_pages_for_business` | Páginas de Facebook del negocio |
| `ads_catalog_*` | Gestión de catálogos y feeds de productos |

## Proceso estándar

### 1. Auditoría de cuenta

```
1. ads_get_ad_accounts → identificar cuenta activa
2. ads_get_opportunity_score → ver score y recomendaciones
3. ads_insights_advertiser_context → contexto general
4. ads_get_errors → revisar rechazos pendientes
```

### 2. Crear campaña nueva

```
1. ads_get_ad_accounts → obtener account_id
2. ads_get_pages_for_business → obtener page_id
3. ads_create_campaign → definir objetivo, nombre, presupuesto diario/total
4. ads_create_ad_set → audiencia, ubicaciones, presupuesto, puja
5. ads_create_ad → creatividad, copy, CTA, URL destino
6. ads_activate_entity → activar campaña
```

### 3. Revisar rendimiento

```
1. ads_get_ad_entities → listar campañas activas
2. ads_insights_performance_trend → métricas por período
3. ads_insights_anomaly_signal → detectar caídas o picos
4. ads_insights_auction_ranking_benchmarks → competitividad
```

### 4. Optimizar campaña existente

```
1. ads_get_ad_entities → estado actual
2. ads_insights_performance_trend → identificar bajo rendimiento
3. ads_update_entity → ajustar presupuesto, puja o targeting
4. ads_activate_entity → pausar ad sets/anuncios ineficientes
```

## Objetivos de campaña Meta

| Objetivo | Código | Cuándo usarlo |
|----------|--------|---------------|
| Reconocimiento | `BRAND_AWARENESS` | Top of funnel, alcance máximo |
| Alcance | `REACH` | Maximizar personas únicas |
| Tráfico | `LINK_CLICKS` | Llevar tráfico al sitio |
| Interacción | `ENGAGEMENT` | Likes, comentarios, shares |
| Leads | `LEAD_GENERATION` | Formularios nativos de Meta |
| Conversiones | `CONVERSIONS` | Compras, registros (requiere Pixel) |
| Ventas catálogo | `PRODUCT_CATALOG_SALES` | DPA/retargeting dinámico |

## Convenciones de nomenclatura

```
[Cliente]_[Objetivo]_[Audiencia]_[Formato]_[Fecha]
Ej: CupraWines_CONV_Retargeting_Carousel_2026Q2
```

## Alertas y umbrales

- Frecuencia > 3: revisar rotación de creatividades
- CTR < 0.8%: revisar copy y creatividad
- ROAS < 2x: revisar audiencia y oferta
- CPA > objetivo × 1.5: pausar y revisar
- CPM > 15 EUR: excesiva competencia, ajustar audiencia
