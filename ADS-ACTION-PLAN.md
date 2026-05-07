# Ads Action Plan — Dra. Maria Eugenia Buonsante
**Generado:** 7 de mayo de 2026 | **Score actual:** 82/100 | **Score potencial:** 97/100

---

## 🔴 CRÍTICO — Resolver hoy

### C1 — Reconectar WhatsApp Business
**Impacto:** +1 pt Score | Delivery inmediato de campaña bloqueada  
**Tiempo estimado:** 5-10 min  
**Pasos:**
1. Ir a Meta Business Settings → WhatsApp Accounts
2. Verificar que el número esté conectado a la Página de Facebook correcta
3. Si no aparece: Settings → Business Assets → Conectar número de WA
4. Una vez reconectado, los ads 120228140063060106 y 120219029442500106 reanudan automáticamente en 24-48h

**Cuentas afectadas:** Campaña `120219029442460106` — 2 ads bloqueados

---

### C2 — Resolver "Ad Set Not Delivering" (2 ad sets)
**Impacto:** +7 pts Score combinados | Presupuesto activo recuperado  
**Tiempo estimado:** 15-20 min  
**Pasos por ad set:**

**Ad set 120230316935430106 (campaña 120222127373520106):**
- Evaluar si la campaña tiene historial reciente (>60 días sin gasto → archivar directamente)
- Si activa: crear nuevo ad set dentro de la misma campaña con audiencia más amplia (Advantage+)
- Pausar el ad set original

**Ad set 120214027852420106 (campaña 120214027852270106):**
- Misma evaluación: campaña antigua → archivar
- Si vale la pena mantener: duplicar ad set, cambiar a Advantage+ audience, activar

---

## 🟡 ALTO — Resolver esta semana (7 días)

### A1 — Aumentar budget en 3 ad sets limitados
**Impacto:** +3 pts Score | Más conversaciones a CPR existente  
**Tiempo estimado:** 5 min  
**Ad sets afectados:**
- `120211369805250106` (Alopecia Androgenica) — $2.750 ARS/día → subir a $4.500 ARS
- `120217934384670106` (El metasoma) — presupuesto desde campaña → revisar techo
- `120213985290490106` (¿Sentis que tu piel ha...) — $2.500 ARS/día → subir a $4.000 ARS

**Mejor performer a escalar primero:** `120213985290490106` — CPR $1.685 ARS (el más eficiente)

---

### A2 — Fusionar ad sets fragmentados
**Impacto:** +3 pts Score | -17% costo por mensaje  
**Tiempo estimado:** 20 min  
**Ad sets a fusionar:** `120213985290490106` + `120217934384670106`

**Pasos:**
1. Identificar cuál tiene mejor CPR histórico (120213985290490106 con $1.685 vs 120217934384670106 con $4.480)
2. Duplicar el mejor (120213985290490106)
3. Ampliar audiencia para cubrir el alcance del ad set eliminado
4. Pausar `120217934384670106`
5. Monitorear fase de reaprendizaje (3-7 días)

---

### A3 — Agregar formato video al ad set de Interacción
**Impacto:** +1 pt Score | Potencial mejora CTR sobre 1.5%  
**Tiempo estimado:** 10 min (si el video ya existe)  
**Ad set:** `120233853993190106`  
**Pasos:**
1. Duplicar uno de los ads de imagen existentes en el ad set
2. Reemplazar la imagen por un video (mismo copy)
3. Activar el nuevo ad — Meta optimizará entre formatos automáticamente

---

### A4 — Resolver errores de creativa (3 ads)

**A4a — Invalid Creative For Objective** (Ad `120212539858390106`, campaña `120212539858210106`)
- Verificar qué CTA tiene el anuncio vs objetivo de campaña
- Editar el anuncio para alinear CTA con objetivo o mover a campaña correcta

**A4b — IG media not supported** (Ad `120212475940940106`, campaña `120212475940120106`)
- Revisar formato del archivo (relación de aspecto, resolución mínima)
- IG Feed requiere 1:1, 4:5, o 1.91:1 — mínimo 1080×1080px
- Exportar creativa corregida y reemplazar

**A4c — No Valid Formats** (Ad `120210705016060106`, campaña `120210453999660106`)
- Revisar placements activos en el ad set
- Subir versiones de la creativa en múltiples formatos (1:1, 4:5, 9:16) o restringir manualmente los placements compatibles

---

## 🟢 MEDIO — Resolver en 30 días

### M1 — Archivar campañas con lookalike eliminada (3 campañas)
**Impacto:** Limpieza de cuenta | Score indirecto  
**Tiempo estimado:** 5 min total  
**Campañas a archivar:**
- `23849100303310105`
- `23848787262030105`
- `23848324359110105`

Todas pausadas por "Público similar (AR, 1%) - Los que tuvieron interacción con la cuenta" eliminado. Sin actividad reciente → archivar directamente, no recrear.

---

### M2 — Archivar "Archived Organic Media" 
**Impacto:** Limpieza | +1 error menos en cuenta  
**Tiempo estimado:** 2 min  
**Campaña:** `120209143561380106` / Ad `120209143561600106`  
- El post orgánico de Instagram fue archivado → el anuncio no puede entregar
- Archivar la campaña completa o recrear como Dark Post

---

### M3 — Estandarizar naming convention
**Impacto:** Gestión operativa  
**Tiempo estimado:** 15 min  
**Acciones:**
- Renombrar campaña "FW" con nombre descriptivo (¿qué es FW?)
- Renombrar los 3 ad sets llamados "Instagram Post" → incluir contenido/fecha/objetivo

---

## 🔵 BAJO — Backlog

### B1 — Configurar Conversions API (CAPI)
**Impacto:** Mejora calidad de señal, menor CPR a futuro  
- Integrar CAPI via partner (Zapier, Make) o directamente
- Priorizar evento "Contact" / "Lead" para conversiones de WhatsApp

### B2 — Agregar exclusión de clientes actuales
- Crear Custom Audience de personas que ya tuvieron conversación iniciada
- Excluirla de los ad sets activos de mensajes

### B3 — Configurar Messaging Events
**Impacto:** -24% CPP según recomendación Meta  
- Configurar eventos de compra vía WhatsApp
- Activar objetivo "Maximizar compras a través de mensajes"

### B4 — Evaluar Google Search para intención alta
- Keywords: "médico alopecia Buenos Aires", "medspa CABA", "tratamiento piel Buenos Aires"
- Complementar captura de demanda activa vs Meta (demanda latente)
