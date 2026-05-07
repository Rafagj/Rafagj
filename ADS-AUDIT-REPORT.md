# Ads Audit Report — Dra. Maria Eugenia Buonsante
**Fecha:** 7 de mayo de 2026  
**Período analizado:** últimos 30 días (7 abr – 6 may 2026)  
**Plataforma:** Meta Ads (única activa)  
**Account ID:** 1238818623235612  
**Moneda:** ARS (ref: ~$1.100 ARS = $1 USD)

---

## Executive Summary

### Ads Health Score

```
Meta Score:  56 / 100   ●●●●●●○○○○   Grado D
─────────────────────────────────────────────
Aggregate:   56 / 100   Grado D
Potencial:   97 / 100   (si se resuelven todos los errores activos)
```

**Opportunity Score Meta:** 82/100 → potencial 97/100 (+15 pts disponibles)

### Business Type Detectado
MedSpa / Medicina Estética — Argentina. Foco en mensajes (WhatsApp/DM) como canal principal de conversión. Vertical de alta intención, audiencia femenina 30-55 años CABA.

### Plataformas Activas
| Plataforma | Estado | Cobertura audit |
|-----------|--------|----------------|
| Meta Ads | ✅ Activa | Completa |
| Google Ads | ❌ No detectado | — |
| TikTok / LinkedIn | ❌ No detectado | — |

### Top 5 Problemas Críticos
1. 🔴 **WhatsApp desconectado** — 2 ads sin entrega en campaña de mensajes
2. 🔴 **4 campañas con delivery error** — ad sets bloqueados, revenue en pausa
3. 🟡 **Fragmentación** — 2 ad sets con mismo objetivo/creativa, audiencias separadas (+17% CPM innecesario)
4. 🟡 **3 ad sets budget-limited** — presupuesto insuficiente frena escala (+3 pts Score disponibles)
5. 🟡 **3 campañas antiguas con audiencia eliminada** — generan ruido en la cuenta

### Top 5 Quick Wins (< 15 min)
1. ⚡ Reconectar WhatsApp en Business Settings (+1 pt, delivery inmediato)
2. ⚡ Archivar 3 campañas con lookalike eliminada (+limpia score)
3. ⚡ Agregar formato video al ad set de Interacción (+1 pt mixed formats)
4. ⚡ Aumentar budget en 3 ad sets limitados (+3 pts Score)
5. ⚡ Archivar 2 ad sets "not delivering" (120230316935430106 + 120214027852420106)

---

## Meta Ads — Análisis Detallado

### Meta Health Score: 56/100 (Grado D)

| Categoría | Peso | Score | Puntos |
|-----------|------|-------|--------|
| Pixel / CAPI Health | 30% | 45/100 | 13.5 |
| Creative Quality | 30% | 60/100 | 18.0 |
| Account Structure | 20% | 55/100 | 11.0 |
| Audience | 20% | 65/100 | 13.0 |
| **TOTAL** | | **56/100** | |

---

### Campañas activas (últimos 30 días)

| Campaña | Objetivo | Gasto ARS | Gasto USD | Resultado | CPR ARS | CPR USD | CTR | CPM ARS | Frec |
|---------|---------|-----------|-----------|-----------|---------|---------|-----|---------|------|
| Interacción Marzo 2026 | Engagement | $1.504.968 | ~$1.368 | 937 conv. mensajes | $1.606 | ~$1.46 | 1,31% | $5.439 | 1,88 |
| FW | Link Clicks | $167.822 | ~$153 | 3.894 profile visits | $43 | ~$0.04 | 4,01% | $1.746 | 1,28 |
| El metasoma es la... | Messages | $120.979 | ~$110 | 27 conv. | $4.481 | ~$4.07 | 3,61% | $7.579 | 1,96 |
| Alopecia Androgenica | Messages | $81.381 | ~$74 | 23 conv. | $3.538 | ~$3.22 | 1,86% | $6.300 | 1,65 |
| ¿Sentis que tu piel ha... | Messages | $75.841 | ~$69 | 45 conv. | $1.685 | ~$1.53 | 3,74% | $12.238 | 1,96 |
| **TOTAL** | | **$1.950.993** | **~$1.774** | **1.032** | | | | | |

**Mejor performer:** "¿Sentis que tu piel ha..." — 45 conversaciones al menor CPR relativo ($1.685 ARS) con buen CTR (3.74%)  
**Peor performer:** "El metasoma es la..." — 27 conversaciones a $4.481 ARS/conv, CPM alto para budget de $4.000/día

---

### Categoría 1: Pixel / CAPI Health (45/100) 🔴

| Check | Estado | Detalle |
|-------|--------|---------|
| M01 — Pixel activo | ✅ PASS | Eventos de mensajes registrándose correctamente |
| M02 — Conversions API | ⚠️ WARN | Sin evidencia de CAPI configurado |
| M03 — Eventos duplicados | ✅ PASS | Sin señales de deduplicación |
| M04 — WhatsApp conectado | ❌ FAIL | 2 ads bloqueados: "WhatsApp number required" en campaña 120219029442460106 |
| M05 — Delivery errors activos | ❌ FAIL | 4 campañas con delivery error total |
| M06 — EMQ Score | ⚠️ WARN | No disponible vía API — verificar en Events Manager |

**Problema principal:** WhatsApp desconectado bloquea toda la campaña 120219029442460106. Impacto inmediato en revenue.

---

### Categoría 2: Creative Quality (60/100) 🟡

| Check | Estado | Detalle |
|-------|--------|---------|
| M10 — CTR > benchmark 1.5% (MedSpa) | ⚠️ WARN | Interacción Marzo: 1.31% ❌ / FW: 4.01% ✅ / Mensajes: 1.86-3.74% ✅ |
| M11 — Frecuencia < 2.5 | ✅ PASS | Máxima: 1.96 — ninguna en zona de fatiga |
| M12 — Mix de formatos (imagen + video) | ⚠️ WARN | Ad set Interacción usa solo un formato (recomendación activa) |
| M13 — Creatividades activas por ad set | ⚠️ WARN | Campañas de Messages con posts orgánicos boosteados |
| M14 — Errores de formato IG | ❌ FAIL | 3 ads con errores: IG media not supported, No Valid Formats, Archived Organic Media |

**CTR benchmark MedSpa:** > 1.5%. La campaña principal de Interacción (1.31%) está por debajo — revisar copy y formato.  
**CPM "¿Sentis que tu piel ha...":** $12.238 ARS/CPM supera el benchmark ($8.800 ARS equiv. a $8 USD) → audiencia muy estrecha o competencia alta.

---

### Categoría 3: Account Structure (55/100) 🟡

| Check | Estado | Detalle |
|-------|--------|---------|
| M20 — Naming convention | ❌ FAIL | Campaña "FW" sin nombre descriptivo. Ad sets llamados "Instagram Post" (x3) |
| M21 — Fragmentación | ❌ FAIL | Ad sets 120213985290490106 + 120217934384670106 fragmentados (mismo obj/creativa) |
| M22 — Campañas zombie | ❌ FAIL | 3 campañas antiguas con audiencia eliminada, sin archivarse |
| M23 — Campañas "not delivering" | ❌ FAIL | 2 ad sets con "not delivering" activos sin resolver |
| M24 — Máx 3-5 ad sets por campaña | ✅ PASS | Estructura simple |
| M25 — Máx 2-3 ads por ad set | ✅ PASS | Dentro de rango |

**Fragmentation cost:** Fusionar los 2 ad sets fragmentados reduciría CPM un 17% según recomendación de Meta.

---

### Categoría 4: Audience (65/100) 🟡

| Check | Estado | Detalle |
|-------|--------|---------|
| M30 — Audiencias válidas | ❌ FAIL | 3 lookalikes eliminadas (Público similar AR 1% interacción) |
| M31 — Budget suficiente | ⚠️ WARN | 3 ad sets budget-limited (+3 pts disponibles en Score) |
| M32 — Frecuencia audiencia | ✅ PASS | Todas < 2.5 |
| M33 — Exclusiones | ⚠️ WARN | Sin evidencia de exclusión de clientes actuales |
| M34 — Advantage+ | ⚠️ WARN | Optimization goal "REPLIES" correcto pero sin A+ Audience habilitado |

---

### Errores Activos — Catálogo Completo

| # | Tipo | Entidad | Urgencia | Campaña ID |
|---|------|---------|---------|-----------|
| 1 | WhatsApp number required | Ads 120228140063060106 + 120219029442500106 | 🔴 Crítico | 120219029442460106 |
| 2 | Delivery error (not delivering) | Adset 120230316935430106 | 🔴 Alto | 120222127373520106 |
| 3 | Delivery error (not delivering) | Adset 120214027852420106 | 🔴 Alto | 120214027852270106 |
| 4 | Invalid Creative For Objective | Ad 120212539858390106 | 🟡 Medio | 120212539858210106 |
| 5 | IG media not supported | Ad 120212475940940106 | 🟡 Medio | 120212475940120106 |
| 6 | No Valid Formats | Ad 120210705016060106 | 🟡 Medio | 120210453999660106 |
| 7 | Archived Organic Media | Ad 120209143561600106 | 🟢 Bajo | 120209143561380106 |
| 8 | Lookalike eliminada | Adset 23849100303330105 | 🟢 Bajo | 23849100303310105 |
| 9 | Lookalike eliminada | Adset 23848787262080105 | 🟢 Bajo | 23848787262030105 |
| 10 | Lookalike eliminada | Adset 23848324359200105 | 🟢 Bajo | 23848324359110105 |

---

### Opportunity Score — Desglose de Puntos

| Recomendación | Lift | Puntos |
|--------------|------|--------|
| Delivery error campaña 120214451623540106 | Delivery habilitado | +4 pts |
| Budget limited (3 ad sets) | Más resultados | +3 pts |
| Fragmentation (merge 2 ad sets) | -17% costo/mensaje | +3 pts |
| Delivery error campaña 120214027852270106 | Delivery habilitado | +3 pts |
| WhatsApp delivery error | Delivery habilitado | +1 pt |
| Delivery error campaña 120212249579180106 | Delivery habilitado | +1 pt |
| Messaging events setup | -24% CPP | +1 pt |
| Click-to-message preset | -7% CPconv | +1 pt |
| Mixed formats ad set Interacción | Más conversiones | +1 pt |
| **TOTAL DISPONIBLE** | | **+18 pts** |
| **Score actual → Score potencial** | | **82 → 97** |

---

## Análisis Cross-Platform

**Tracking:** Solo Meta Pixel activo. Sin CAPI confirmado. Sin Google Analytics / GTM detectado.  
**Budget allocation:** 100% Meta — sin diversificación de plataformas.  
**Creative consistency:** N/A (plataforma única).  
**Attribution:** Sin overlap (plataforma única, atribución 7-day click 1-day view estándar).

---

## Recomendaciones Estratégicas

### Priorización de plataformas
Dado el vertical MedSpa con foco en mensajes WhatsApp, Meta es la plataforma correcta como primaria. A considerar en Q3 2026: Google Search para captación de intención alta ("médico alopecia CABA").

### Oportunidades de escala
- **"¿Sentis que tu piel ha..."** — mejor CPR ($1.685 ARS). Candidata a escalar budget +30%.
- **"Interacción Marzo 2026"** — mayor volumen (937 conv.). Agregar video para bajar CPM y subir CTR sobre benchmark.

### Kill list
- **Campañas 23849100303310105, 23848787262030105, 23848324359110105** — 3 campañas con lookalike eliminada → ARCHIVAR
- **Ad sets 120230316935430106 + 120214027852420106** — "not delivering" → ARCHIVAR o recrear
