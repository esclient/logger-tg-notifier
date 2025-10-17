from __future__ import annotations

import asyncio
import logging
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import ANY, AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from loggertgnotifier.bot.telegram_bot import TelegramBot
from loggertgnotifier.endpoints.log_endpoint import receive_post
from loggertgnotifier.service.message_service import MessageService
from loggertgnotifier.settings import Settings


@pytest.fixture(name="sample_payload")
def fixture_sample_payload() -> dict[str, Any]:
    return {
        "service_name": "test-service",
        "message": "ValueError: could not convert string to float: 'str'",
        "timestamp": "2024-10-17T12:00:00",
        "filename": "test_file.py",
        "fileline": 15,
        "error_level": "ERROR",
        "context": {
            "test_id": "test_001",
            "user_id": 12345,
            "action": "process_payment",
            "environment": "testing",
            "additional_data": {"amount": 100.50, "currency": "USD"},
        },
        "traceback": "Traceback (most recent call last): ... ValueError",
    }


@pytest.fixture(name="service_under_test")
def fixture_service_under_test() -> tuple[MessageService, AsyncMock, Settings]:
    send_document_mock: AsyncMock = AsyncMock()
    bot = cast(
        TelegramBot,
        SimpleNamespace(send_document_with_message=send_document_mock),
    )
    settings = Settings(
        TG_BOT_TOKEN="token",
        TG_CHAT_ID="12345",
        TG_THREAD_ID=678,
        HOST="localhost",
        PORT=7009,
    )
    service = MessageService(bot, settings)
    return service, send_document_mock, settings


def test_process_error_message_sends_document(
    service_under_test: tuple[MessageService, AsyncMock, Settings],
    sample_payload: dict[str, Any],
) -> None:
    service, send_document_mock, settings = service_under_test

    result = asyncio.run(service.process_error_message(sample_payload))

    send_document_mock.assert_awaited_once_with(
        sample_payload["traceback"], ANY
    )
    assert result == {
        "status": "ok",
        "sent_to": {
            "chat_id": settings.CHAT_ID,
            "thread_id": settings.THREAD_ID,
        },
    }


def test_process_error_message_logs_error_when_sending_fails(
    service_under_test: tuple[MessageService, AsyncMock, Settings],
    sample_payload: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
) -> None:
    service, send_document_mock, _settings = service_under_test
    send_document_mock.side_effect = RuntimeError("telegram is down")

    with caplog.at_level(logging.ERROR):
        result = asyncio.run(service.process_error_message(sample_payload))

    assert "Failed to send message to Telegram" in caplog.text
    assert result["status"] == "ok"


def test_receive_post_returns_message_service_result(
    sample_payload: dict[str, Any],
) -> None:
    service_mock = SimpleNamespace(
        process_error_message=AsyncMock(return_value={"status": "ok"})
    )
    app = FastAPI()
    app.add_api_route("/log", receive_post, methods=["POST"])
    app.state.message_service = service_mock

    client = TestClient(app)
    response = client.post("/log", json=sample_payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    service_mock.process_error_message.assert_awaited_once_with(sample_payload)
