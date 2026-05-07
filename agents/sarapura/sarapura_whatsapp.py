"""Cliente WhatsApp Cloud API — envío de mensajes y notificaciones de aprobación."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

WA_URL = "https://graph.facebook.com/v21.0"
WA_PHONE_NUMBER_ID = os.getenv("SARAPURA_WA_PHONE_NUMBER_ID")
WA_ACCESS_TOKEN = os.getenv("SARAPURA_WA_ACCESS_TOKEN")
ADMIN_PHONE = os.getenv("SARAPURA_ADMIN_PHONE")  # Número de Rafa para aprobaciones (ej: 549XXXXXXXXXX)


class WhatsAppClient:
    def __init__(
        self,
        phone_number_id: str = WA_PHONE_NUMBER_ID,
        access_token: str = WA_ACCESS_TOKEN,
    ):
        self.phone_number_id = phone_number_id
        self.token = access_token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def send_text(self, to: str, text: str) -> dict:
        """Envía un mensaje de texto simple."""
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text},
        }
        resp = self.session.post(
            f"{WA_URL}/{self.phone_number_id}/messages", json=payload
        )
        resp.raise_for_status()
        return resp.json()

    def send_approval_request(self, to: str, approval_text: str, story_image_url: str = None) -> dict:
        """Envía al admin una solicitud de aprobación para repostear una historia.

        Incluye la imagen de la story si está disponible, seguida del texto de aprobación.
        """
        if story_image_url:
            image_payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "image",
                "image": {"link": story_image_url, "caption": approval_text},
            }
            resp = self.session.post(
                f"{WA_URL}/{self.phone_number_id}/messages", json=image_payload
            )
            resp.raise_for_status()
            return resp.json()

        return self.send_text(to, approval_text)

    def notify_admin(self, message: str) -> dict:
        """Atajo para enviar una notificación al número administrador configurado."""
        return self.send_text(ADMIN_PHONE, message)

    def parse_approval_reply(self, message_text: str) -> bool:
        """Parsea la respuesta del admin: SI = True, NO = False."""
        return message_text.strip().upper() in ("SI", "SÍ", "S", "YES", "Y", "1")
