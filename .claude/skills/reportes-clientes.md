# Skill: Reportes Multi-Cliente Meta Ads

## Descripción

Workflow para generar reportes estandarizados de rendimiento para múltiples cuentas en una sola sesión. Produce resúmenes ejecutivos por cliente y una vista consolidada del portfolio.

## Cuándo usar este skill

Invoca `/reportes-clientes` cuando el usuario pida:
- Reporte semanal o mensual de todas las cuentas
- Comparar rendimiento entre clientes
- Generar un resumen ejecutivo para presentar
- Vista consolidada del portfolio de cuentas

## Proceso de reporte multi-cuenta

### 1. Definir alcance

```
Período estándar: last_30d (mensual) o last_7d (semanal)
Cuentas a reportar: solo las con is_ads_mcp_enabled: true
```

### 2. Ejecutar en paralelo (máximo 5 cuentas simultáneas)

Para cada cuenta, lanzar en paralelo:
```
ads_get_ad_entities (level: account, date_preset: last_30d)
  campos: impressions, clicks, ctr, cpm, cpc, frequency,
          reach, amount_spent, results, cost_per_result
ads_get_opportunity_score
```

Agrupar en lotes de 5 si el portfolio supera esa cantidad.

### 3. Métricas a extraer por cuenta

| Métrica | Campo API | Descripción |
|---------|-----------|-------------|
| Gasto total | amount_spent | Inversión del período |
| Impresiones | impressions | Alcance bruto |
| Clicks | clicks | Interacciones totales |
| CTR global | ctr | Eficiencia de la creativa |
| CPM | cpm | Costo por mil impresiones |
| CPC | cpc | Costo por click |
| Resultados | results | Objetivo principal (varía por cuenta) |
| CPR | cost_per_result | Costo por resultado |
| Frecuencia | frequency | Saturación de audiencia |
| Opportunity Score | — | Salud general de la cuenta |

### 4. Semáforo de salud por cuenta

```
🟢 Saludable:   Score ≥ 90, sin errores críticos, CTR > benchmark
🟡 Atención:    Score 75-89, errores menores, algún KPI fuera de rango
🔴 Crítico:     Score < 75, errores bloqueantes, múltiples KPIs rojos
```

## Portfolio actual — clientes activos

| Cliente | Account ID | Moneda | MCP | Vertical |
|---------|-----------|--------|-----|---------|
| Dra. Maria Eugenia Buonsante | 1238818623235612 | ARS | ✅ | MedSpa / Salud estética |
| Sorace Mendoza | 905876964450782 | — | ❌ | — |
| Javier Rodriguez (Nutrición) | 219433399508952 | ARS | ✅ | Nutrición |
| Javier Rodriguez JRN 2025 | 1067365748751452 | ARS | ✅ | Nutrición |
| Tradition & Rebellion | 1255958546224523 | USD | ✅ | Restaurant / Bar |
| Presidente Bar | 803670943793654 | — | ❌ | Bar / Gastronomía |
| Sarapura | 852858213205966 | ARS | ✅ | — |

## Formato de reporte ejecutivo

### Vista portfolio (resumen)

```markdown
# Reporte de Portfolio — [Período]
Generado: [fecha]  |  Cuentas activas: [N]

## Resumen consolidado

| Cliente | Gasto | CTR | CPM | Score | Estado |
|---------|-------|-----|-----|-------|--------|
| Cupra USD | $X | X% | $X | XX/100 | 🟢 |
| T&R | $X | X% | $X | XX/100 | 🟢 |
| Buonsante | $X | X% | $X | XX/100 | 🟡 |
| ... | | | | | |

## Cuentas que requieren atención
[Lista de cuentas con estado 🟡 o 🔴 con el problema principal]

## Acciones pendientes
- [ ] [Cliente] — [Acción] — [Prioridad]
```

### Vista cliente (detalle)

```markdown
## [Cliente] — [Período]

**Gasto:** $X  |  **Impresiones:** X  |  **CTR:** X%  |  **Score:** X/100

### Campaña destacada
[Nombre] → CTR X%, CPM $X — [comentario de 1 línea]

### Campaña a revisar
[Nombre] → [problema concreto]

### Próxima acción
[1 acción específica con fecha sugerida]
```

## Benchmarks por vertical (referencia)

| Vertical | CTR | CPM (USD) | Frecuencia máx |
|---------|-----|-----------|----------------|
| Wine & Spirits | > 2% | < 3 | 3 |
| Restaurant / Bar | > 2.5% | < 2.5 | 3 |
| MedSpa / Salud | > 1.5% | < 8 | 2.5 |
| Retail / Ecomm | > 1.5% | < 10 | 3 |
| Servicios prof. | > 1% | < 6 | 2 |

## Notas sobre monedas

- Cuentas en **USD**: comparar CPM directamente con benchmarks USD
- Cuentas en **ARS**: dividir por el tipo de cambio del período para normalizar
  - Referencia: $1 USD ≈ $1.000–1.200 ARS (verificar al momento del reporte)
- Al comparar entre cuentas ARS y USD, siempre normalizar a USD

## Cadencia de reportes

| Tipo | Frecuencia | Audiencia | Formato |
|------|-----------|-----------|---------|
| Flash | Diario | Interno | Score + alertas |
| Semanal | Lunes | Cliente | Resumen ejecutivo |
| Mensual | Día 5 del mes | Cliente + dirección | Reporte completo |
| Trimestral | — | Dirección | Estrategia + benchmarking |
