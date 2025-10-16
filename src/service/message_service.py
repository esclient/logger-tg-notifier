from bot.telegram_bot import TelegramBot
from settings import Settings
from helpers.parse_context import parse_context
from helpers.escape_markdown_v2 import escape_md_v2


class MessageService:
    def __init__(self, bot: TelegramBot, settings: Settings):
        self.bot = bot
        self.settings = settings

    async def process_error_message(self, data: dict) -> dict:
        service_name = data.get("service_name", "Не указано")
        message = data.get("message", "Не указано")
        timestamp = data.get("timestamp", "Не указано")
        filename = data.get("filename", "Не указано")
        fileline = data.get("fileline", "Не указано")
        error_level = data.get("error_level", "Не указано")
        context = parse_context(data.get("context", { }))
        traceback = data.get("traceback", { })

        full_message = (
                f"\\[\\] Ошибка в сервисе: {escape_md_v2(service_name)}\n"
                f"\\[\\] Текст ошибки: {escape_md_v2(message)}\n"
                f"\\[\\] Дата и время: {escape_md_v2(timestamp)}\n"
                f"\\[\\] Файл: {escape_md_v2(filename)} \\| Строка: {fileline}\n"
                f"\\[\\] Уровень: {escape_md_v2(error_level)}\n"
                f"\\[\\] Контекст:\n{context}"
                )

        try:
            await self.bot.send_document_with_message(traceback, full_message)
        except Exception as e:
            print(f"Ошибка при отправке в Telegram: {e}")

        return {
            "status": "ok",
            "sent_to": { "chat_id": self.settings.CHAT_ID, "thread_id": self.settings.THREAD_ID }
        }
