import asyncio
import traceback
from datetime import datetime
from typing import Any, cast

import aiohttp


async def send_test_error() -> dict[str, Any] | None:
    try:
        _ = float("str")
    except Exception as exc:
        error = exc
        tb = traceback.format_exc()
    else:
        return None

    error_data: dict[str, Any] = {
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
        async with (
            aiohttp.ClientSession() as session,
            session.post(url, json=error_data) as response,
        ):
            result = cast(dict[str, Any], await response.json())
            print(f"Server response: {result}")
            return result
    except Exception as exc:
        print(f"Failed to send error: {exc}")
        return None


async def main() -> None:
    print("Waiting 5 seconds before sending the test error...")

    await asyncio.sleep(5)

    print("Sending test error...")
    result = await send_test_error()

    if result and result.get("status") == "ok":
        print("Test error processed successfully! Telegram notification sent.")
    else:
        print("Test error request failed.")


if __name__ == "__main__":
    asyncio.run(main())
