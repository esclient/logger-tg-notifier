import uvicorn
from fastapi import APIRouter, FastAPI

from loggertgnotifier.bot.telegram_bot import TelegramBot
from loggertgnotifier.endpoints.health_endpoint import health_check
from loggertgnotifier.endpoints.log_endpoint import receive_post
from loggertgnotifier.service.message_service import MessageService
from loggertgnotifier.settings import Settings

settings: Settings = Settings()


def create_app() -> FastAPI:
    app = FastAPI(title="logger-tg-notifier")
    telegram_bot = TelegramBot(settings)
    message_service = MessageService(telegram_bot, settings)
    router = APIRouter()

    router.add_api_route("/health", health_check, methods=["GET"])
    router.add_api_route("/log", receive_post, methods=["POST"])

    app.include_router(router)
    app.state.message_service = message_service

    return app


app: FastAPI = create_app()


def main() -> None:
    uvicorn.run(
        "loggertgnotifier.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
