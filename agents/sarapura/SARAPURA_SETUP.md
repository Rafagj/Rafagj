# Setup — Agente Sarapura

## Arquitectura

```
Instagram / WhatsApp
        ↓  (webhooks)
    Make.com
        ↓  (HTTP POST)
  FastAPI Server         ←→   Claude API (respuestas)
  (sarapura_agent.py)   ←→   Instagram Graph API (publicar)
                        ←→   WhatsApp Cloud API (notif. admin)
```

---

## Paso 1 — Crear Meta App y configurar permisos

1. Ir a [developers.facebook.com](https://developers.facebook.com) → **My Apps → Create App**
2. Tipo: **Business**
3. Agregar productos:
   - **Instagram Graph API**
   - **WhatsApp Business Platform**
4. En **Instagram → API Setup**: conectar la cuenta de Instagram de Sarapura
5. Solicitar permisos (requieren revisión de Meta):
   - `instagram_manage_messages` — DMs
   - `instagram_manage_comments` — comentarios
   - `instagram_mentions` — menciones en stories
   - `pages_messaging` — mensajes de página
6. Generar un **Page Access Token** de larga duración (60 días → intercambiar por never-expiring con la API)

> **Anota:**
> - `SARAPURA_IG_PAGE_ID` — ID de la Página de Facebook vinculada a Instagram
> - `SARAPURA_IG_ACCESS_TOKEN` — Page Access Token

---

## Paso 2 — Configurar WhatsApp Cloud API

1. En la Meta App → **WhatsApp → Getting Started**
2. Agregar número de teléfono de Sarapura (requiere verificación por llamada/SMS)
3. Configurar el número en el sandbox primero para pruebas
4. Anotar:
   - `SARAPURA_WA_PHONE_NUMBER_ID` — ID del número en la plataforma
   - `SARAPURA_WA_ACCESS_TOKEN` — Token de acceso (mismo que IG o separado)
5. `SARAPURA_ADMIN_PHONE` — Tu número personal para recibir aprobaciones (formato: `549XXXXXXXXXX`)

---

## Paso 3 — Desplegar el servidor Python

### Opción recomendada: Railway

```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Desde la carpeta del agente
cd agents/sarapura
railway init
railway up
```

### Variables de entorno en Railway

```
ANTHROPIC_API_KEY=sk-ant-...
SARAPURA_IG_ACCESS_TOKEN=EAA...
SARAPURA_IG_PAGE_ID=123456789
SARAPURA_WA_PHONE_NUMBER_ID=123456789
SARAPURA_WA_ACCESS_TOKEN=EAA...
SARAPURA_ADMIN_PHONE=549XXXXXXXXXX
MAKE_WEBHOOK_SECRET=elige-un-token-secreto-largo
```

### Alternativa: Render

1. Crear cuenta en [render.com](https://render.com)
2. New Web Service → conectar este repositorio
3. Root Directory: `agents/sarapura`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn sarapura_agent:app --host 0.0.0.0 --port $PORT`

### Para desarrollo local (ngrok)

```bash
pip install -r requirements.txt
uvicorn sarapura_agent:app --reload --port 8000

# En otra terminal:
ngrok http 8000
# Copiar la URL pública (ej: https://abc123.ngrok.io)
```

---

## Paso 4 — Configurar Make.com

1. Ir a [make.com](https://make.com) → **Scenarios → Import Blueprint**
2. Subir `make_blueprint.json`
3. Reemplazar las variables en el blueprint:
   - `AGENT_URL` → URL pública del servidor (Railway/Render/ngrok)
   - `MAKE_SECRET` → mismo valor que `MAKE_WEBHOOK_SECRET` en el .env
   - `SARAPURA_IG_PAGE_ID` → ID de la Página
   - `SARAPURA_WA_PHONE_NUMBER_ID` → ID del número WA
   - `SARAPURA_ADMIN_PHONE` → Tu número
4. Conectar las apps de Instagram Business y WhatsApp Business en Make.com con las credenciales de la Meta App
5. Activar los 4 escenarios

---

## Paso 5 — Archivo .env local

Crear `agents/sarapura/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
SARAPURA_IG_ACCESS_TOKEN=
SARAPURA_IG_PAGE_ID=
SARAPURA_WA_PHONE_NUMBER_ID=
SARAPURA_WA_ACCESS_TOKEN=
SARAPURA_ADMIN_PHONE=
MAKE_WEBHOOK_SECRET=
```

---

## Paso 6 — Instalar dependencias

```bash
cd agents/sarapura
pip install -r requirements.txt
```

---

## Verificar que funciona

```bash
# Health check
curl https://TU-SERVIDOR.railway.app/health

# Test DM manual
curl -X POST https://TU-SERVIDOR.railway.app/ig/dm \
  -H "Content-Type: application/json" \
  -H "X-Make-Secret: TU_SECRET" \
  -d '{
    "sender_id": "123",
    "sender_name": "Test User",
    "message_text": "Hola, quiero información sobre sus servicios"
  }'
```

---

## Flujo del agente

### DM de Instagram
```
Usuario envía DM → Make.com lo detecta → POST /ig/dm
→ Claude genera respuesta con personalidad Sarapura
→ Instagram Graph API publica la respuesta en el DM
```

### Comentario en publicación
```
Usuario comenta → Make.com lo detecta → POST /ig/comment
→ Claude lee el caption del post + el comentario
→ Claude genera respuesta contextual
→ Instagram Graph API publica la respuesta al comentario
```

### Mención en story
```
Usuario menciona @sarapura en story → Make.com detecta → POST /ig/mention
→ Claude analiza sentimiento (positivo/neutro/negativo)
→ Si positivo: WhatsApp al admin con imagen + texto de aprobación
→ Admin responde SI → agente repostea la story
→ Admin responde NO → agente descarta silenciosamente
```

---

## Personalidad del agente

Editá `sarapura_prompts.py` para ajustar:
- **SYSTEM_PROMPT** — tono, estilo, restricciones generales
- **DM_PROMPT** — cómo responder mensajes directos
- **COMMENT_PROMPT** — cómo responder comentarios
- **STORY_SENTIMENT_PROMPT** — criterios de análisis de stories

---

## Notas importantes

- Los permisos `instagram_manage_messages` e `instagram_mentions` requieren **revisión de Meta** (proceso de app review, ~1-2 semanas)
- Durante el desarrollo se puede usar el **modo sandbox** con cuentas de prueba
- El agente NO responde comentarios de spam o con palabras en lista negra (configurar en `sarapura_prompts.py`)
- Las aprobaciones de story están en **memoria RAM** — si el servidor reinicia se pierden. Para producción, migrar a Redis o una DB simple
