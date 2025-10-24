import io
import json
from typing import Any

from telegram.constants import ParseMode
from telegram.ext import Application

from loggertgnotifier.settings import Settings


class TelegramBot:
    def __init__(self, settings: Settings):
        self.settings = settings
        builder = Application.builder().token(self.settings.TOKEN)

        proxy_url = self.settings.PROXY_URL
        if proxy_url:
            builder = builder.proxy(proxy_url).get_updates_proxy(proxy_url)

        self.application = builder.build()
        self.bot = self.application.bot

    async def send_document_with_message(
        self,
        document: Any,
        message: str,
        parse_mode: str = ParseMode.MARKDOWN_V2,
    ) -> None:
        json_bytes = json.dumps(document, indent=4).encode("utf-8")
        raw_error = io.BytesIO(json_bytes)
        raw_error.name = "raw_error.txt"

        await self.bot.send_document(
            chat_id=self.settings.CHAT_ID,
            message_thread_id=self.settings.THREAD_ID,
            document=raw_error,
            caption=message,
            parse_mode=parse_mode,
        )
