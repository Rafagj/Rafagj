# Skill: Resolución de Errores Meta Ads

## Descripción

Playbook completo para diagnosticar y resolver los errores más comunes que bloquean la entrega de campañas en Meta Ads. Cada error incluye causa raíz, pasos de resolución y acción de API cuando aplica.

## Cuándo usar este skill

Invoca `/errores-meta` cuando el usuario pida:
- Resolver un error específico de Meta Ads
- Limpiar errores acumulados en una cuenta
- Entender por qué un ad set o anuncio no está entregando
- Mejorar el Opportunity Score resolviendo delivery errors

## Catálogo de errores

---

### 1. WhatsApp number required

**Mensaje:** *"Reconnect your WhatsApp number to your Facebook Page or Instagram account to run this ad."*

**Causa:** El número de WhatsApp Business fue desconectado de la Página de Facebook o de la cuenta de Instagram asociada a la cuenta publicitaria.

**Resolución:**
```
1. Ir a Meta Business Settings → WhatsApp Accounts
2. Verificar que el número de WA está conectado a la Página correcta
3. Si no está: Settings → Business Assets → Conectar número de WA
4. Una vez reconectado, los anuncios reanudan entrega automáticamente (24-48h)
5. Si persiste: revisar si el número de WA tiene restricciones propias (cuenta no verificada)
```

**Impacto:** Todos los anuncios con destino WhatsApp quedan bloqueados. Crítico para campañas de mensajes.

---

### 2. Lookalike audience deleted

**Mensaje:** *"Your ad set was paused because the audience X was deleted and removed from this ad set."*

**Causa:** Alguien eliminó la Custom Audience o el Lookalike desde Meta Audiences, o la audiencia fue desactivada automáticamente por inactividad.

**Resolución según prioridad de la campaña:**

```
Campaña ANTIGUA (> 60 días sin gasto significativo):
→ Archivar la campaña completa. No recrear.

Campaña ACTIVA con buen historial:
1. Meta Audiences → Crear nueva Custom Audience equivalente
   (misma fuente: IG interactions, website visitors, etc.)
2. Crear Lookalike desde esa nueva fuente
3. ads_update_entity → actualizar targeting del ad set con nueva audience ID
4. ads_activate_entity → reactivar ad set
5. Esperar fase de aprendizaje (3-7 días)

Sin fuente disponible:
→ Cambiar a Advantage+ Audience (targeting_as_signal: 1)
   con geo del mercado objetivo
```

---

### 3. This ad set is not delivering

**Mensaje:** *"Try creating a new ad set with different settings to begin delivering to your audience."*

**Causa:** El ad set tiene una configuración que Meta ya no puede optimizar — puede ser por cambios en políticas, targeting demasiado restrictivo, o incompatibilidad de objetivo.

**Resolución:**
```
1. No intentar editar el ad set existente — Meta lo indica claramente
2. Crear un nuevo ad set (ads_create_ad_set) dentro de la misma campaña con:
   - Misma configuración base pero audiencia más amplia
   - Considerar Advantage+ Audience si el problema es targeting
   - Revisar si el optimization_goal es compatible con el objetivo de la campaña
3. Pausar el ad set original
4. Duplicar los ads del ad set original al nuevo
```

---

### 4. Invalid Creative For Objective

**Mensaje:** *"The ad's creative is incompatible with the objective of the campaign the ad belongs to."*

**Causa:** La creativa (formato, CTA o URL de destino) no es compatible con el objetivo de la campaña. Ej: un anuncio con CTA "Enviar mensaje" en una campaña de Link Clicks.

**Compatibilidad creativa por objetivo:**

| Objetivo | CTAs válidos | Destino |
|----------|-------------|---------|
| LINK_CLICKS | Learn More, Shop Now, Sign Up | URL externa |
| OUTCOME_ENGAGEMENT | Like, Comment, Share | Post de IG/FB |
| MESSAGES | Send Message | WhatsApp / Messenger / DM |
| OUTCOME_LEADS | Sign Up, Get Quote | Lead Form |
| OUTCOME_SALES | Shop Now, Buy Now | Web con Pixel |

**Resolución:**
```
1. Identificar qué CTA o destino es incompatible
2. Editar el anuncio (ads_update_entity) para alinear CTA con objetivo
   O crear un nuevo anuncio compatible
3. Si el problema es estructural (objetivo equivocado):
   → Considerar mover el anuncio a una campaña con objetivo correcto
```

---

### 5. Instagram media not supported

**Mensaje:** *"The ad media is not supported for IG. Please review the preview for IG placements."*

**Causa:** El formato del archivo (imagen o video) no cumple las especificaciones de Instagram para el placement específico (Feed, Stories, Reels).

**Especificaciones correctas por placement:**

| Placement | Relación de aspecto | Resolución mínima | Duración video |
|-----------|--------------------|--------------------|---------------|
| IG Feed | 1:1, 4:5, 1.91:1 | 1080×1080px | Hasta 60s |
| IG Stories | 9:16 | 1080×1920px | Hasta 15s |
| IG Reels | 9:16 | 1080×1920px | Hasta 90s |
| FB Feed | 1:1, 4:5 | 1080×1080px | Hasta 240min |

**Resolución:**
```
1. Identificar qué placement está fallando (revisar preview en Ads Manager)
2. Exportar la creativa en el formato correcto para ese placement
3. Reemplazar el asset en el anuncio
4. Alternativa: excluir el placement problemático del ad set si no es prioritario
```

---

### 6. No Valid Formats

**Mensaje:** *"Your ad's creative is incompatible with the selected placements."*

**Causa:** Ninguno de los placements seleccionados acepta el formato de la creativa actual. Suele ocurrir con placements automáticos (Advantage+ placements) cuando la creativa es muy específica.

**Resolución:**
```
1. Revisar qué placements están activos en el ad set
2. Opción A: Usar Advantage+ placements y subir versiones de la creativa
   en múltiples formatos (1:1, 4:5, 9:16) — Meta selecciona automáticamente
3. Opción B: Seleccionar manualmente solo los placements compatibles
   con el formato de creativa disponible
4. Opción C: Crear un nuevo asset en el formato correcto
```

---

### 7. Instagram Ads Archived Organic Media

**Mensaje:** *"Ads from organic IG media but the organic media were archived."*

**Causa:** El anuncio fue creado a partir de un post orgánico de Instagram que luego fue archivado o eliminado desde la cuenta de IG.

**Resolución:**
```
Opción A — Restaurar el post orgánico:
1. Ir a Instagram → Perfil → Archivados
2. Restaurar el post
3. El anuncio retoma entrega automáticamente

Opción B — Recrear el anuncio:
1. Crear un nuevo anuncio con la misma creativa subida directamente
   (no como post boost, sino como Dark Post)
2. Archivar la campaña original

Recomendación: siempre crear anuncios como Dark Posts, no desde posts orgánicos,
para evitar este problema.
```

---

## Priorización de limpieza

Al auditar una cuenta con múltiples errores, resolver en este orden:

```
1. 🔴 WhatsApp desconectado → bloquea revenue inmediato
2. 🔴 Lookalike audiences eliminadas (campañas activas) → perdiendo escala
3. 🟡 Ad set not delivering (campañas con presupuesto activo) → gasto bloqueado
4. 🟡 Invalid creative / No valid formats → anuncios sin entrega
5. 🟢 Organic media archived (campañas antiguas) → archivar directamente
6. 🟢 Lookalike eliminada (campañas > 60 días) → archivar directamente
```

## Template de reporte de errores

```markdown
## Errores activos — [Cuenta] — [Fecha]

| # | Tipo | Campaña/Ad | Urgencia | Acción |
|---|------|-----------|---------|--------|
| 1 | WhatsApp desconectado | [nombre] | 🔴 Alta | Reconectar en Business Settings |
| 2 | Lookalike eliminada | [nombre] | 🔴 Alta | Recrear audiencia |
| ... | | | | |

**Impacto en Opportunity Score:** +X puntos al resolver todos
```
