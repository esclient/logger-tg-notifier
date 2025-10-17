from typing import Any, cast

from fastapi import Depends, HTTPException, Request

from loggertgnotifier.service.message_service import MessageService


def get_message_service(request: Request) -> MessageService:
    return cast(MessageService, request.app.state.message_service)


async def receive_post(
    request: Request,
    service: MessageService = Depends(get_message_service),
) -> dict[str, Any]:
    try:
        data = await request.json()
        result = await service.process_error_message(data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {e!s}",
        ) from e
