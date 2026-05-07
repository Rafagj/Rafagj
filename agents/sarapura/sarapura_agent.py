"""Agente Sarapura — servidor FastAPI que procesa eventos de Instagram y WhatsApp.

Recibe webhooks reenviados por Make.com y orquesta las respuestas con Claude.

Endpoints:
  POST /ig/dm          — Mensaje directo de Instagram
  POST /ig/comment     — Comentario en publicación
  POST /ig/mention     — Mención en story
  POST /wa/approval    — Respuesta del admin (SI/NO) para repostear story
  GET  /health         — Health check

Variables de entorno requeridas (.env):
  ANTHROPIC_API_KEY
  SARAPURA_IG_ACCESS_TOKEN
  SARAPURA_IG_PAGE_ID
  SARAPURA_WA_PHONE_NUMBER_ID
  SARAPURA_WA_ACCESS_TOKEN
  SARAPURA_ADMIN_PHONE
  MAKE_WEBHOOK_SECRET    — token secreto para validar llamadas de Make.com
"""

import json
import logging
import os
from typing import Optional

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel

from sarapura_instagram import InstagramClient
from sarapura_prompts import (
    APPROVAL_MESSAGE,
    COMMENT_PROMPT,
    DM_PROMPT,
    STORY_SENTIMENT_PROMPT,
    SYSTEM_PROMPT,
)
from sarapura_whatsapp import WhatsAppClient

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sarapura_agent")

app = FastAPI(title="Sarapura Social Agent", version="1.0.0")

claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
ig = InstagramClient()
wa = WhatsAppClient()

MAKE_SECRET = os.getenv("MAKE_WEBHOOK_SECRET", "")

# Cola en memoria para stories pendientes de aprobación {mention_id: media_id}
pending_approvals: dict[str, str] = {}


# ─── Models ──────────────────────────────────────────────────────────────────

class DMEvent(BaseModel):
    sender_id: str
    sender_name: str
    message_text: str
    conversation_id: Optional[str] = None


class CommentEvent(BaseModel):
    commenter_name: str
    comment_id: str
    comment_text: str
    media_id: str


class MentionEvent(BaseModel):
    mention_id: str
    username: str
    story_text: Optional[str] = ""
    media_url: Optional[str] = None


class ApprovalEvent(BaseModel):
    from_phone: str
    message_text: str


# ─── Auth ─────────────────────────────────────────────────────────────────────

def verify_secret(x_make_secret: str = Header(default="")):
    if MAKE_SECRET and x_make_secret != MAKE_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")


# ─── Claude helpers ───────────────────────────────────────────────────────────

def claude_reply(user_prompt: str) -> str:
    """Llama a Claude y devuelve el texto de respuesta."""
    message = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text.strip()


def analyze_story_sentiment(story_text: str) -> dict:
    """Analiza el sentimiento de una story y decide si sugerir reposteo."""
    prompt = STORY_SENTIMENT_PROMPT.format(story_text=story_text or "(sin texto — solo imagen)")
    message = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        system="Sos un analizador de sentimientos. Respondé siempre con JSON válido.",
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()
    # Extraer JSON aunque venga con texto extra
    start = raw.find("{")
    end = raw.rfind("}") + 1
    return json.loads(raw[start:end])


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "agent": "sarapura"}


@app.post("/ig/dm")
async def handle_dm(event: DMEvent, x_make_secret: str = Header(default="")):
    verify_secret(x_make_secret)
    logger.info(f"DM de {event.sender_name}: {event.message_text}")

    history = ""
    if event.conversation_id:
        try:
            msgs = ig.get_conversation_history(event.conversation_id)
            history = "\n".join(f"{m['sender']}: {m['text']}" for m in msgs[-4:])
        except Exception:
            pass

    prompt = DM_PROMPT.format(
        sender_name=event.sender_name,
        message_text=event.message_text,
        history=history or "(sin historial previo)",
    )
    reply = claude_reply(prompt)
    ig.reply_to_dm(event.sender_id, reply)
    logger.info(f"DM respondido a {event.sender_name}: {reply}")
    return {"status": "replied", "reply": reply}


@app.post("/ig/comment")
async def handle_comment(event: CommentEvent, x_make_secret: str = Header(default="")):
    verify_secret(x_make_secret)
    logger.info(f"Comentario de {event.commenter_name}: {event.comment_text}")

    caption = ""
    try:
        caption = ig.get_post_caption(event.media_id)
    except Exception:
        pass

    prompt = COMMENT_PROMPT.format(
        post_caption=caption or "(sin descripción)",
        commenter_name=event.commenter_name,
        comment_text=event.comment_text,
    )
    reply = claude_reply(prompt)
    ig.reply_to_comment(event.comment_id, reply)
    logger.info(f"Comentario respondido: {reply}")
    return {"status": "replied", "reply": reply}


@app.post("/ig/mention")
async def handle_story_mention(event: MentionEvent, x_make_secret: str = Header(default="")):
    verify_secret(x_make_secret)
    logger.info(f"Mención en story de @{event.username}")

    analysis = analyze_story_sentiment(event.story_text)
    logger.info(f"Análisis: {analysis}")

    if not analysis.get("repostear", False):
        logger.info(f"Story de @{event.username} descartada (sentimiento: {analysis.get('sentiment')})")
        return {"status": "discarded", "reason": analysis.get("sentiment")}

    # Guardar en cola de aprobación
    pending_approvals[event.mention_id] = event.mention_id

    approval_text = APPROVAL_MESSAGE.format(
        username=event.username,
        summary=analysis.get("resumen", "Historia mencionando a Sarapura"),
        sentiment=analysis.get("sentiment", "positivo"),
        score=analysis.get("score", 0.8),
    )

    wa.send_approval_request(
        to=os.getenv("SARAPURA_ADMIN_PHONE"),
        approval_text=approval_text,
        story_image_url=event.media_url,
    )
    logger.info(f"Aprobación enviada al admin para story de @{event.username}")
    return {"status": "pending_approval", "mention_id": event.mention_id}


@app.post("/wa/approval")
async def handle_approval(event: ApprovalEvent, x_make_secret: str = Header(default="")):
    verify_secret(x_make_secret)
    approved = wa.parse_approval_reply(event.message_text)

    if not pending_approvals:
        return {"status": "no_pending"}

    # Tomar la aprobación más reciente pendiente
    mention_id, media_id = next(iter(pending_approvals.items()))

    if approved:
        try:
            ig.repost_story_mention(media_id)
            del pending_approvals[mention_id]
            wa.notify_admin("✅ Historia reposteada correctamente.")
            logger.info(f"Story {mention_id} reposteada")
            return {"status": "reposted", "mention_id": mention_id}
        except Exception as e:
            wa.notify_admin(f"❌ Error al repostear: {str(e)}")
            logger.error(f"Error reposteando: {e}")
            return {"status": "error", "detail": str(e)}
    else:
        del pending_approvals[mention_id]
        logger.info(f"Story {mention_id} rechazada por el admin")
        return {"status": "rejected", "mention_id": mention_id}
