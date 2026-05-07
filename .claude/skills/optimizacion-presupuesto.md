# Skill: Optimización de Presupuesto Publicitario

## Descripción

Redistribuye presupuesto entre campañas, canales y ad sets para maximizar ROAS o minimizar CPA. Aplica reglas de escalado, pausado automático y estrategias de puja según rendimiento.

## Cuándo usar este skill

Invoca `/optimizacion-presupuesto` cuando el usuario pida:
- Redistribuir presupuesto entre campañas según rendimiento
- Escalar campañas ganadoras
- Pausar campañas con bajo ROAS/CPA elevado
- Definir estrategia de puja (cost cap, bid cap, lowest cost)
- Simular escenarios de inversión y retorno esperado

## Principios de optimización

### Regla 80/20 de presupuesto

```
80% → Campañas probadas con ROAS > objetivo
20% → Testeo: nuevas audiencias, formatos, creatividades
```

### Umbrales de decisión

| ROAS | CPA vs objetivo | Acción |
|------|----------------|--------|
| > 4x | < 70% | Escalar +20-30% presupuesto |
| 3-4x | 70-100% | Mantener, optimizar creatividad |
| 2-3x | 100-150% | Pausar ad sets peores, reducir -10% |
| < 2x | > 150% | Pausar campaña, revisar estrategia |

### Reglas de escalado seguro

1. **Nunca escalar > 30% en un solo día** (evitar salir de la fase de aprendizaje)
2. **Esperar 3-7 días** antes de evaluar tras un cambio de presupuesto
3. **Duplicar ad sets ganadores** en lugar de escalar el original si > +50%
4. **Presupuesto mínimo por ad set**: 5× CPA objetivo / día

## Proceso de optimización

### 1. Diagnóstico inicial

```
1. ads_get_ad_entities → estado y presupuesto de todas las campañas
2. ads_insights_performance_trend → ROAS/CPA últimos 7 y 30 días
3. ads_get_opportunity_score → recomendaciones automáticas de Meta
4. Clasificar campañas en: Escalar / Mantener / Reducir / Pausar
```

### 2. Plan de redistribución

```
Presupuesto total: X EUR
├── Campañas top ROAS (≥ 3x): 60% → Y EUR
├── Campañas en aprendizaje: 20% → Z EUR  
├── Tests A/B activos: 10% → W EUR
└── Reserva/nuevas iniciativas: 10% → V EUR
```

### 3. Aplicar cambios

```
Por cada campaña a modificar:
1. ads_update_entity → nuevo daily_budget o lifetime_budget
2. ads_activate_entity → pausar entidades bajo rendimiento
3. Registrar cambios con fecha y justificación
```

### 4. Seguimiento post-cambio

```
- Día 1-3: No evaluar resultados (fase de reaprendizaje)
- Día 4-7: Primera evaluación parcial
- Día 7+: Evaluación completa y siguiente ajuste si necesario
```

## Estrategias de puja

| Estrategia | Cuándo usar | Riesgo |
|------------|-------------|--------|
| Lowest Cost | Maximizar volumen, sin objetivo CPA fijo | Alto CPM en escala |
| Cost Cap | CPA objetivo definido, volumen suficiente | Entrega limitada |
| Bid Cap | Control total del CPC/CPM máximo | Difícil escalar |
| ROAS Target | e-commerce con pixel maduro (>50 conv/sem) | Requiere datos |
| Value Optimization | Maximizar valor de conversión | Requiere valores distintos |

## Simulador de escenarios

Para estimar retorno antes de cambiar presupuesto:

```
ROAS actual: R
Presupuesto actual: B EUR/día
Gasto actual: G EUR (período)
Ingresos actuales: I EUR

Nuevo presupuesto: B_new EUR/día
→ Gasto estimado: G × (B_new / B)
→ Ingresos estimados: Gasto_estimado × R
→ Beneficio neto estimado: Ingresos_estimados - Gasto_estimado
→ ROI estimado: (Beneficio / Gasto_estimado) × 100
```

## Calendario de revisiones

| Frecuencia | Qué revisar |
|------------|-------------|
| Diaria | Anomalías, rechazos, presupuesto agotado |
| Semanal | ROAS/CPA por campaña, rotación de creatividades |
| Mensual | Redistribución presupuestaria, nuevos tests |
| Trimestral | Estrategia, objetivos, benchmarking competencia |

## Herramientas de apoyo

- `budget_optimizer.py`: simulación y aplicación automática de reglas
- `ads_update_entity`: actualizar presupuestos vía API
- `ads_get_opportunity_score`: recomendaciones de Meta
- `ads_insights_auction_ranking_benchmarks`: competitividad en subasta
