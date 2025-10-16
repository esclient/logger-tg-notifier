from fastapi import FastAPI, APIRouter
from bot.telegram_bot import TelegramBot
from service.message_service import MessageService
from settings import Settings
from endpoints.health_endpoint import health_check
from endpoints.log_endpoint import receive_post
import uvicorn


settings = Settings()

def create_app() -> FastAPI:
    app = FastAPI(title="tg-bot-error-notifier")
    telegram_bot = TelegramBot(settings)
    message_service = MessageService(telegram_bot, settings)
    router = APIRouter()

    router.add_api_route("/health", health_check, methods=["GET"])
    router.add_api_route("/log", receive_post, methods=["POST"])

    app.include_router(router)
    app.state.message_service = message_service

    return app

app = create_app()

def main():
    uvicorn.run("server:app", host=settings.HOST, port=settings.PORT, reload=True)

if __name__ == "__main__":
    main()