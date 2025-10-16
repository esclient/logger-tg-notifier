import json
import io
from settings import Settings
from telegram.ext import Application
from telegram.constants import ParseMode


class TelegramBot:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.application = Application.builder().token(self.settings.TOKEN).build()
        self.bot = self.application.bot
        
    async def send_document_with_message(self, document: any, message: str, parse_mode: str = ParseMode.MARKDOWN_V2):
        json_bytes = json.dumps(document, indent=4).encode('utf-8')
        raw_error = io.BytesIO(json_bytes)
        raw_error.name = "raw_error.txt"
        
        await self.bot.send_document(
            chat_id=self.settings.CHAT_ID,
            message_thread_id=self.settings.THREAD_ID,
            document=raw_error, 
            caption=message,
            parse_mode=parse_mode
        )
