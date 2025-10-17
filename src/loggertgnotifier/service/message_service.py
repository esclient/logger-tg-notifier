import logging
from typing import Any

from loggertgnotifier.bot.telegram_bot import TelegramBot
from loggertgnotifier.helpers.escape_markdown_v2 import escape_md_v2
from loggertgnotifier.helpers.parse_context import parse_context
from loggertgnotifier.settings import Settings

logger = logging.getLogger(__name__)


class MessageService:
    def __init__(self, bot: TelegramBot, settings: Settings):
        self.bot = bot
        self.settings = settings

    async def process_error_message(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        placeholder = "Unknown"
        service_name = data.get("service_name", placeholder)
        message = data.get("message", placeholder)
        timestamp = data.get("timestamp", placeholder)
        filename = data.get("filename", placeholder)
        fileline = data.get("fileline", placeholder)
        error_level = data.get("error_level", placeholder)
        context = parse_context(data.get("context", {}))
        traceback = data.get("traceback", {})

        full_message = (
            f"\\[\\] Service: {escape_md_v2(service_name)}\n"
            f"\\[\\] Message: {escape_md_v2(message)}\n"
            f"\\[\\] Timestamp: {escape_md_v2(timestamp)}\n"
            f"\\[\\] File: {escape_md_v2(filename)} \\| Line: {fileline}\n"
            f"\\[\\] Level: {escape_md_v2(error_level)}\n"
            f"\\[\\] Context:\n{context}"
        )

        try:
            await self.bot.send_document_with_message(traceback, full_message)
        except Exception:
            logger.exception("Failed to send message to Telegram")

        return {
            "status": "ok",
            "sent_to": {
                "chat_id": self.settings.CHAT_ID,
                "thread_id": self.settings.THREAD_ID,
            },
        }
