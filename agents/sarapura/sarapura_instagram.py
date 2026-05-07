"""Cliente para Instagram Graph API — mensajes, comentarios y stories."""

import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

GRAPH_URL = "https://graph.facebook.com/v21.0"
IG_ACCESS_TOKEN = os.getenv("SARAPURA_IG_ACCESS_TOKEN")
IG_PAGE_ID = os.getenv("SARAPURA_IG_PAGE_ID")


class InstagramClient:
    def __init__(self, access_token: str = IG_ACCESS_TOKEN, page_id: str = IG_PAGE_ID):
        self.token = access_token
        self.page_id = page_id
        self.session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        params = params or {}
        params["access_token"] = self.token
        resp = self.session.get(f"{GRAPH_URL}/{endpoint}", params=params)
        resp.raise_for_status()
        return resp.json()

    def _post(self, endpoint: str, data: dict = None) -> dict:
        data = data or {}
        data["access_token"] = self.token
        resp = self.session.post(f"{GRAPH_URL}/{endpoint}", data=data)
        resp.raise_for_status()
        return resp.json()

    def reply_to_dm(self, recipient_id: str, message_text: str) -> dict:
        """Envía un mensaje directo a un usuario de Instagram."""
        return self._post(f"{self.page_id}/messages", {
            "recipient": f'{{"id":"{recipient_id}"}}',
            "message": f'{{"text":"{message_text}"}}',
            "messaging_type": "RESPONSE",
        })

    def reply_to_comment(self, comment_id: str, reply_text: str) -> dict:
        """Responde a un comentario en una publicación."""
        return self._post(f"{comment_id}/replies", {"message": reply_text})

    def get_conversation_history(self, conversation_id: str, limit: int = 5) -> list[dict]:
        """Obtiene los últimos mensajes de una conversación de DM."""
        data = self._get(f"{conversation_id}", {
            "fields": "messages{message,from,created_time}",
            "limit": limit,
        })
        messages = data.get("messages", {}).get("data", [])
        return [
            {"sender": m["from"]["name"], "text": m["message"], "time": m["created_time"]}
            for m in reversed(messages)
        ]

    def get_post_caption(self, media_id: str) -> str:
        """Obtiene el caption de una publicación para dar contexto al agente."""
        data = self._get(media_id, {"fields": "caption"})
        return data.get("caption", "")

    def repost_story_mention(self, media_id: str) -> dict:
        """Repostea una historia donde Sarapura fue mencionado."""
        return self._post(f"{self.page_id}/media", {
            "media_type": "STORIES",
            "source_media_id": media_id,
        })

    def get_mention_media(self, mention_id: str) -> dict:
        """Obtiene datos de una mención en story (texto, imagen, usuario)."""
        return self._get(f"{self.page_id}", {
            "fields": f"mentioned_media.fields(caption,media_url,username,timestamp)",
            "media_id": mention_id,
        })
