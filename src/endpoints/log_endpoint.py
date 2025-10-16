from fastapi import Depends, HTTPException, Request

from service.message_service import MessageService


def get_message_service(request: Request) -> MessageService:
    return request.app.state.message_service


async def receive_post(
    request: Request,
    service: MessageService = Depends(get_message_service),
):
    try:
        data = await request.json()
        result = await service.process_error_message(data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка обработки запроса: {str(e)}"
        )
