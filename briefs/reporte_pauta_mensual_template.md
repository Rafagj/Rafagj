# Reporte mensual de pauta — template

**Para:** Martín · Sofi · Sequi
**De:** Rafa (analista de pauta)
**Periodicidad:** primer lunes hábil del mes siguiente.
**Regla de oro:** una sola página. Si necesita más, abrir reunión.

---

## Cómo usar este template

- Reemplazar el ejemplo numérico (mes de junio 2026) por los datos reales.
- Mantener exactamente las 5 secciones — la familiaridad acelera la lectura.
- No agregar gráficos en el documento. Los gráficos viven en el dashboard de Looker (link al final).
- Si una métrica está en rojo, agregar una línea de explicación. Si está verde, no.

---

## Ejemplo lleno — Junio 2026

# Reporte de pauta · Junio 2026

**Gasto total:** USD 2.487 · **vs plan:** USD 2.500 · **delta:** –0.5%
**Reservas atribuidas:** 73 · **Costo por reserva:** USD 34.1
**Ticket promedio del mes (data interna):** USD 78 · **ROAS estimado:** 2.29×

---

### 1. Performance vs objetivo

| Métrica | Objetivo junio | Real | Estado |
|---|---:|---:|:---:|
| CPM Meta (Set A locales) | <USD 3.50 | USD 2.91 | 🟢 |
| CPM Meta (Set B turistas) | <USD 4.00 | USD 5.20 | 🔴 |
| ThruPlay rate medio | >15% | 19.4% | 🟢 |
| CPC engagement | <USD 0.25 | USD 0.18 | 🟢 |
| Costo por visita al perfil | <USD 0.60 | USD 0.41 | 🟢 |
| Costo por reserva | <USD 40 | USD 34.10 | 🟢 |
| Frecuencia semanal Set A | <2.5 | 2.1 | 🟢 |
| Frecuencia semanal Set B | <2.5 | 3.4 | 🔴 |

**🔴 Set B turistas — CPM y frecuencia altos.** La audiencia "Visitors AR + interest Buenos Aires nightlife" está muy chica (≈18K personas) y se quema rápido. Recomendación: ampliar a "Travelers Latin America" en julio.

---

### 2. Top 3 creatividades

| Pieza | Pilar | Gasto | Hook rate | ThruPlay | Cost / profile visit |
|---|---|---:|---:|---:|---:|
| Negroni del Sur (Cap 01, 15s) | Diálogos | USD 845 | 58% | 22% | USD 0.31 |
| Sunset session (Atmósfera) | Atmósfera | USD 612 | 61% | 19% | USD 0.38 |
| Behind the bar (Autores) | Autores | USD 410 | 49% | 17% | USD 0.46 |

**Hallazgo:** las piezas con humano visible (manos del bartender, jefe de barra) superan en 12 puntos al promedio de Hook Rate. Replicar el patrón en Cap 02-04.

---

### 3. Aprendizajes del mes

1. **A/B challenger Negroni del Sur ganó la versión CON texto en pantalla.** Delta de +14% en ThruPlay. Implementar la estructura "LA REGLA / LA REBELIÓN" en todos los reels de Diálogos siguientes.
2. **El reel de Atmósfera de 9 segundos performó mejor que el de 15.** En audiencia fría conviene cortar antes. Mantener 15s solo para retargeting.
3. **YouTube Search en inglés trajo 11 reservas con CPL de USD 22.** Mejor que Meta para captar turistas. Reasignar USD 200 de Meta Set B → Google Search EN en julio.
4. **Lookalike 1% de engagers (creado el día 18) ya supera a intereses fríos en costo por visita.** Pasar 30% del presupuesto Set A a LAL desde semana 2 de julio.

---

### 4. Recomendación para julio

| Acción | Impacto esperado | Costo / decisión |
|---|---|---|
| Subir presupuesto total a USD 3.000 | escalado controlado +20% | aprobación de Martín |
| Reasignar USD 200 Meta Set B → Google Search EN | mejor CPL turistas | mía |
| Activar LAL 1% engagers al 30% del Set A | menor costo de profile visit | mía |
| Producir Cap 02 (Empanada × Kombu) con misma estructura visual | replicar ganador | depende de Sequi |
| Pausar pieza "Behind the bar v1" (fatiga creativa, CTR –32%) | liberar presupuesto | mía |
| Test A/B nuevo: copy "Reservá" vs "Conocé" | aprender CTA óptimo | mía |

---

### 5. Calendario julio (alto nivel)

- **Sem 1:** rebalanceo de audiencias + lanzamiento de Cap 02.
- **Sem 2:** activación LAL + boosting de UGC top del mes.
- **Sem 3:** A/B de CTAs.
- **Sem 4:** prepausa de campañas con fatiga + brief para piezas de agosto.

---

**Dashboard en vivo:** [Looker Studio · TyR Paid](#)
**Comentarios o preguntas:** quedo para el viernes 11:00.

---
---

## Apéndice — definiciones operativas

Para que el equipo lea los números con la misma vara:

| Término | Definición operativa |
|---|---|
| **Reserva atribuida** | Evento `reserva_confirmada` en GA4 + Meta Pixel con last-click 7 días o view 1 día. |
| **Hook rate** | % de impresiones que pasan los 3s de video. |
| **ThruPlay rate** | % de personas que completaron ≥15s del video (o el total si es <15s). |
| **Costo por visita al perfil** | Gasto / (profile visits desde ads). Excluye visitas orgánicas. |
| **Frecuencia** | Impresiones / alcance único en la ventana de la campaña. |
| **Fatiga creativa** | Caída de CTR ≥20% en los últimos 7 días vs los 7 anteriores. |
| **ROAS estimado** | (Reservas × ticket promedio) / gasto. Estimado porque el ticket no se cobra online. |

---

## Apéndice — versión semanal (1/4 de página, por viernes)

Lo que va a Martín cada viernes (formato whatsapp / slack):

```
🍸 TyR · Paid · Sem 23 (3-9 jun)

GASTO: USD 587  ·  ALCANCE: 41.2K
RESERVAS ATRIBUIDAS: 18  ·  CPR: USD 32.6

TOP 1: Negroni del Sur 15s · ER 4.1% · 22 saves
TOP 2: Sunset session · ER 3.8% · 11 saves
BOTTOM: Behind the bar v1 · CTR cayó -28% → pauso

RECOMENDACIÓN
- Mantener Cap 01 escalando 10%
- Pasar 30% Set B a Google Search EN

Siguiente reporte completo: lun 1 julio.
```

---

*Template de reporte de pauta · versión 1 · Q2 2026.*
