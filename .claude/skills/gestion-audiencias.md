# Skill: Gestión de Audiencias Meta Ads

## Descripción

Estrategia completa de audiencias para Meta Ads: cuándo usar cada tipo, cómo manejar audiencias eliminadas o estrechas, configuración de Advantage+ Audience y retargeting.

## Cuándo usar este skill

Invoca `/gestion-audiencias` cuando el usuario pida:
- Decidir entre Lookalike, Interés o Advantage+ para un ad set
- Resolver el error "audiencia eliminada" o "audiencia estrecha"
- Configurar retargeting o audiencias de exclusión
- Escalar una campaña que está limitada por audiencia

## Árbol de decisión: ¿qué audiencia usar?

```
¿Cuántas conversiones/interacciones tiene la cuenta?
│
├── < 50 eventos/mes → Usar INTERESES AMPLIOS + geo
│   └── Objetivo: acumular datos para lookalike
│
├── 50–500 eventos/mes → LOOKALIKE 1–3% del mercado principal
│   └── Fuente: Custom Audience de compradores, leads o visitantes web
│
└── > 500 eventos/mes → ADVANTAGE+ AUDIENCE
    └── Dar señal con mejor audiencia custom, dejar optimizar a Meta
```

## Tipos de audiencia y cuándo usarlos

### Lookalike Audiences

| Porcentaje | Tamaño aprox. (AR) | Cuándo usar |
|-----------|-------------------|-------------|
| 1% | ~300K | Mayor similitud, menor escala. Ideal para cuentas nuevas |
| 2–3% | ~600K–1M | Balance entre similitud y escala. Más recomendado |
| 5% | ~1.5M | Para escalar cuando 1–3% se agota |
| 10% | ~3M | Top of funnel amplio, awareness |

**Regla crítica:** Nunca usar Lookalike 1% con filtros adicionales de edad/interés — la audiencia resultante cae a < 5.000 personas y bloquea la optimización.

**Fuentes de Lookalike en orden de calidad:**
1. Compradores / leads con alta intención
2. Visitantes que llegaron a página de confirmación
3. Usuarios que interactuaron con el perfil de IG (últimos 90 días)
4. Fans de la página de Facebook

### Advantage+ Audience (A+A)

Activar con `targeting_as_signal: 1` en el ad set.

**Cuándo es la mejor opción:**
- Audiencias Lookalike que cayeron a < 10.000 personas
- Cuentas con > 500 conversiones/mes (algoritmo tiene datos suficientes)
- Campañas "always on" que necesitan escalar sin gestión manual
- Cuando se quiere expandir audiencia manteniendo geo restricción

**Cómo configurar:**
```
targeting_as_signal: 1
targeting: {geo_locations: {countries: ["AR"]}}  ← señal, no filtro duro
```

**Nota:** Con A+A, la geo se convierte en señal preferencial. Si necesitás geo estricto, validar que Meta respeta la restricción revisando los reportes por región tras 3-7 días.

### Custom Audiences — segmentos clave para salud/gastronomía/retail

| Segmento | Ventana | Uso |
|---------|---------|-----|
| Visitantes web | 30 días | Retargeting caliente |
| Visitantes web | 90 días | Retargeting frío |
| Interacción IG (video 50%) | 30 días | Remarketing video |
| Interacción perfil IG | 60 días | Remarketing engagement |
| Compradores / leads | Lifetime | Fuente de Lookalike |
| Exclusión: clientes actuales | — | Evitar gastar en clientes ya convertidos |

## Protocolo: Audiencia eliminada

Cuando aparece el error *"Your ad set was paused because the audience X was deleted"*:

```
1. Identificar qué audiencia fue eliminada (nombre en el mensaje de error)
2. Evaluar si recrearla vale la pena:
   - Campaña antigua (> 60 días sin actividad) → ARCHIVAR campaña
   - Campaña activa importante → RECREAR audiencia y reactivar
3. Si se recrea:
   a. Ir a Meta Audiences → crear nueva Custom/Lookalike equivalente
   b. Asignar al ad set con ads_update_entity (targeting field)
   c. Reactivar con ads_activate_entity
4. Si la fuente original ya no existe → usar Advantage+ Audience como alternativa
```

## Protocolo: Audiencia estrecha (< 20.000 personas)

```
Diagnóstico según tamaño:
│
├── < 1.000 personas → Acción inmediata
│   ├── Opción A: Activar Advantage+ (targeting_as_signal: 1)
│   ├── Opción B: Subir Lookalike de 1% a 3–5%
│   └── Opción C: Eliminar filtros de edad/interés restrictivos
│
├── 1.000–5.000 personas → Acción recomendada
│   ├── Monitorear frecuencia diariamente
│   └── Expandir si frecuencia supera 3x en < 7 días
│
└── 5.000–20.000 personas → Monitorear
    └── Evaluar expansión si CTR cae > 30% sostenido 3 días
```

## Exclusiones recomendadas siempre

```json
{
  "exclusions": [
    "Compradores últimos 30 días (evitar sobre-impactar)",
    "Empleados / equipo (si aplica)",
    "Audiencias de competidores propios (si se tienen segmentos separados)"
  ]
}
```

## Señales de fatiga de audiencia

| Señal | Umbral | Acción |
|-------|--------|--------|
| Frecuencia > 3.5 | En < 14 días | Rotar creatividad o expandir audiencia |
| CTR cayó > 40% vs semana anterior | — | Fatiga creativa o de audiencia |
| CPM subió > 50% vs semana anterior | — | Audiencia agotada, ampliar o cambiar |
| Reach se estancó con presupuesto estable | — | Audiencia saturada |
