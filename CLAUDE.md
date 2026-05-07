# Rafagj — Marketing Digital & Gestión de Pauta

## Descripción del proyecto

Repositorio de herramientas y agentes para gestión de campañas de marketing digital, con foco en **Meta Ads (Facebook & Instagram)**, análisis de rendimiento y optimización de presupuesto.

## Estructura

```
.
├── agents/                      # Agentes autónomos de marketing
│   ├── meta_campaign_manager.py # Gestión completa de campañas Meta
│   ├── performance_reporter.py  # Reportes de rendimiento multi-canal
│   └── budget_optimizer.py      # Optimización de presupuesto y ROAS
├── .claude/skills/              # Skills de Claude Code
│   ├── meta-pauta.md            # Gestión de pauta en Meta
│   ├── analitica-marketing.md   # Análisis de métricas y KPIs
│   └── optimizacion-presupuesto.md  # Optimización de inversión
├── analyze_campaign.py          # Analizador base de campañas (CSV)
└── CLAUDE.md                    # Este archivo
```

## Skills disponibles

Invoca los skills con `/meta-pauta`, `/analitica-marketing` u `/optimizacion-presupuesto`.

## Agentes disponibles

```bash
# Gestionar campañas en Meta Ads
python agents/meta_campaign_manager.py --account <ID> --action list

# Generar reporte de rendimiento
python agents/performance_reporter.py --client "Cupra Wines" --period last-30-days

# Optimizar presupuesto
python agents/budget_optimizer.py --account <ID> --budget 5000 --objective ROAS
```

## KPIs clave

| Métrica | Descripción | Benchmark |
|---------|-------------|-----------|
| ROAS | Retorno sobre inversión publicitaria | > 3x |
| CTR | Click-through rate | > 1.5% Meta, > 3% Search |
| CPC | Coste por clic | Depende de industria |
| CPM | Coste por 1.000 impresiones | < 10 EUR Meta |
| Conv. Rate | Tasa de conversión | > 2% |
| Frecuencia | Veces que un usuario ve el anuncio | < 3 (awareness) |

## Clientes activos

| Cliente | Account ID | Moneda | MCP | Vertical |
|---------|-----------|--------|-----|---------|
| Dra. Maria Eugenia Buonsante | 1238818623235612 | ARS | ✅ | MedSpa / Salud estética |
| Sorace Mendoza | 905876964450782 | — | ❌ | — |
| Javier Rodriguez (Nutrición) | 219433399508952 | — | ✅ | Nutrición |
| Javier Rodriguez JRN 2025 | 1067365748751452 | — | ✅ | Nutrición |
| Tradition & Rebellion | 1255958546224523 | USD | ✅ | Restaurant / Bar |
| Presidente Bar | 803670943793654 | — | ❌ | Bar / Gastronomía |
| Sarapura | 852858213205966 | ARS | ✅ | — |

## Convenciones

- Moneda por defecto: ARS (Argentina) / USD según cliente
- Zona horaria: America/Argentina/Buenos_Aires
- Periodos estándar: `last-7-days`, `last-30-days`, `last-60-days`, `last-90-days`
- Atribución: 7-day click, 1-day view (Meta estándar)

---

## Context Engineering — Workflow de implementación

### Comandos disponibles

| Comando | Qué hace |
|---------|----------|
| `/generate-prp INITIAL.md` | Investiga el codebase y genera un PRP completo para la feature |
| `/execute-prp PRPs/nombre.md` | Implementa la feature siguiendo el blueprint del PRP |

### Flujo recomendado para nuevas features

1. **Describí la feature** en `INITIAL.md` (ya existe como template)
2. **Generá el PRP** con `/generate-prp INITIAL.md` → se guarda en `PRPs/`
3. **Ejecutá el PRP** con `/execute-prp PRPs/nombre.md`

### Estructura de PRPs

```
PRPs/
├── templates/
│   └── prp_base.md          # Template base para nuevos PRPs
└── {feature-name}.md        # PRPs generados
```

### Reglas de código (Context Engineering)

- Nunca crear archivos de más de 500 líneas — refactorizar en módulos si es necesario
- Siempre crear tests unitarios para nuevas features
- Usar `python-dotenv` para variables de entorno
- Type hints en todo el código Python
- Nunca asumir contexto faltante — preguntar si hay dudas
