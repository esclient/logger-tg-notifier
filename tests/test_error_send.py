import asyncio
import traceback
from datetime import datetime

import aiohttp


async def send_test_error():
    try:
        some_var = float("str")
    except Exception as e:
        error = e
        tb = traceback.format_exc()

    error_data = {
        "service_name": "test-service",
        "message": str(error),
        "timestamp": datetime.now().isoformat(),
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
        "traceback": tb,
    }

    url = "http://localhost:7009/log"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=error_data) as response:
                result = await response.json()
                print(f"Ответ от сервера: {result}")
                return result
    except Exception as e:
        print(f"Ошибка при отправке: {e}")
        return None


async def main():
    print("Тест запущен. Ожидание 5 секунд перед отправкой ошибки...")

    await asyncio.sleep(5)

    print("Отправляю тестовую ошибку...")
    result = await send_test_error()

    if result and result.get("status") == "ok":
        print("Тест завершен успешно! Ошибка отправлена в Telegram.")
    else:
        print("Тест завершен с ошибкой.")


if __name__ == "__main__":
    asyncio.run(main())
